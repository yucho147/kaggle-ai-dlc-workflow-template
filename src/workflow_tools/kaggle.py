"""Kaggle CLI boundary: bounded responses, complete snapshots and safe downloads."""

from __future__ import annotations

import os
import re
import shlex
import shutil
import stat
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
REF_PART = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
MAX_RESPONSE_CHARS = 16_000


def validate_slug(value: str) -> str:
    if not SLUG.fullmatch(value):
        raise ValueError("Expected a competition slug, without URL, flags or path components.")
    return value


def validate_ref(value: str) -> str:
    parts = value.split("/")
    if len(parts) != 2 or any(
        not REF_PART.fullmatch(part) or part in {".", ".."} for part in parts
    ):
        raise ValueError("Expected an owner/resource reference.")
    return value


def destination_path(value: str | None, kind: str, name: str) -> Path:
    base = (ROOT / kind).resolve()
    if not base.is_relative_to(ROOT.resolve()):
        raise ValueError("Download root resolves outside the project.")
    destination = Path(value).expanduser() if value else base / name
    if not destination.is_absolute():
        destination = ROOT / destination
    destination = destination.resolve()
    if not destination.is_relative_to(base):
        raise ValueError(f"Destination must be inside {kind}/.")
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def _text(value: str | bytes | None) -> str:
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")


def _redact(value: str) -> str:
    for key in ("KAGGLE_API_TOKEN", "KAGGLE_KEY", "HF_TOKEN"):
        secret = os.environ.get(key)
        if secret and len(secret) >= 4:
            value = value.replace(secret, "[REDACTED]")
    return value


def run_kaggle(
    tool: str,
    args: list[str],
    *,
    timeout: int = 120,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    override = os.environ.get("KAGGLE_MCP_KAGGLE_CMD")
    command = shlex.split(override) if override else [shutil.which("kaggle") or "kaggle"]
    command += args
    payload: dict[str, Any] = {
        "schema_version": 1,
        "tool": tool,
        "source": "kaggle-cli",
        "command": [_redact(part) for part in command],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "returncode": None,
        "ok": False,
        "error": None,
        "stdout": "",
        "stderr": "",
        **(metadata or {}),
    }
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        payload.update(
            returncode=completed.returncode,
            ok=completed.returncode == 0,
            stdout=_redact(completed.stdout),
            stderr=_redact(completed.stderr),
        )
        if not payload["ok"]:
            payload["error"] = {
                "kind": "cli",
                "message": "Kaggle CLI returned a nonzero exit code.",
            }
    except subprocess.TimeoutExpired as exc:
        payload.update(
            stdout=_redact(_text(exc.stdout)),
            stderr=_redact(_text(exc.stderr)),
            error={"kind": "timeout", "message": f"Exceeded {timeout} seconds."},
        )
    except OSError as exc:
        payload["error"] = {"kind": "process", "message": _redact(str(exc))}
    payload["finished_at"] = datetime.now(timezone.utc).isoformat()
    return payload


def finalize(payload: dict[str, Any]) -> dict[str, Any]:
    import json

    cache = Path(os.environ.get("KAGGLE_MCP_CACHE_DIR", str(ROOT / ".cache/kaggle-mcp")))
    if not cache.is_absolute():
        cache = ROOT / cache
    cache = cache.expanduser().resolve()
    directory = cache / payload["tool"]
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    snapshot = directory / f"{stamp}-{uuid4().hex}.json"
    payload = {
        **payload,
        "snapshot_path": str(snapshot),
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with snapshot.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    response = dict(payload)
    truncated = False
    for key in ("stdout", "stderr"):
        value = payload.get(key, "")
        if len(value) > MAX_RESPONSE_CHARS:
            truncated = True
            response[key] = value[:MAX_RESPONSE_CHARS] + "\n[truncated; inspect snapshot]"
    for key in ("files", "extracted"):
        if key in response:
            response[f"{key}_count"] = len(response[key])
            if len(response[key]) > 200:
                truncated = True
                response[key] = response[key][:200]
    response["truncated"] = truncated
    return response


def extract_archive(archive: Path, destination: Path) -> list[str]:
    """Validate all members before extracting; never replace existing data."""
    destination = destination.resolve()
    limit = int(os.environ.get("KAGGLE_MCP_MAX_EXTRACT_BYTES", str(5 * 1024**3)))
    if limit <= 0:
        raise ValueError("KAGGLE_MCP_MAX_EXTRACT_BYTES must be positive.")
    extracted: list[str] = []
    with zipfile.ZipFile(archive) as handle:
        entries = handle.infolist()
        total = sum(item.file_size for item in entries)
        if total > limit or total > shutil.disk_usage(destination).free:
            raise ValueError("Archive exceeds extraction budget or free disk space.")
        paths: set[Path] = set()
        for item in entries:
            relative = PurePosixPath(item.filename)
            path = (destination / item.filename).resolve()
            mode = item.external_attr >> 16
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or "\\" in item.filename
                or ":" in item.filename
                or stat.S_ISLNK(mode)
                or not path.is_relative_to(destination)
            ):
                raise ValueError(f"Unsafe archive member: {item.filename}")
            if path in paths:
                raise ValueError(f"Duplicate archive member: {item.filename}")
            paths.add(path)
            if path.exists() and not (item.is_dir() and path.is_dir()):
                raise FileExistsError(f"Refusing to overwrite existing data: {path}")
        for item in entries:
            path = destination / item.filename
            if item.is_dir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with handle.open(item) as source, path.open("xb") as target:
                    shutil.copyfileobj(source, target)
                extracted.append(str(path))
    return extracted


def download_competition(
    competition: str,
    *,
    output_dir: str | None = None,
    unzip: bool = True,
) -> dict[str, Any]:
    competition = validate_slug(competition)
    destination = destination_path(output_dir, "data/raw", competition)
    payload = run_kaggle(
        "kaggle_competition_download",
        ["competitions", "download", competition, "-p", str(destination)],
        timeout=900,
        metadata={"competition": competition, "output_dir": str(destination)},
    )
    if payload["ok"] and unzip:
        archive = destination / f"{competition}.zip"
        if archive.is_file():
            try:
                payload["extracted"] = extract_archive(archive, destination)
            except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
                payload.update(ok=False, error={"kind": "extraction", "message": str(exc)})
        else:
            payload["extracted"] = []
            payload["extraction_note"] = "No combined zip found; inspect downloaded files."
    payload["files"] = sorted(str(path) for path in destination.iterdir())
    return finalize(payload)
