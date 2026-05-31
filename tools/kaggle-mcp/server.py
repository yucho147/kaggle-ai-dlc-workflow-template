"""MCP server for Kaggle research workflows.

The server intentionally wraps Kaggle CLI commands instead of importing Kaggle
internals. This keeps authentication, CLI versioning, and future adapter swaps
outside training/research orchestration code.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kaggle-mcp")


DEFAULT_TIMEOUT_SECONDS = 120


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _cache_root() -> Path:
    configured = os.environ.get("KAGGLE_MCP_CACHE_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return (_repo_root() / ".cache" / "kaggle-mcp").resolve()


def _kaggle_cmd() -> list[str]:
    return shlex.split(os.environ.get("KAGGLE_MCP_KAGGLE_CMD", "uv run kaggle"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_name(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in value)
    return safe.strip("_") or "snapshot"


def _write_snapshot(tool_name: str, payload: dict[str, Any]) -> str:
    cache_dir = _cache_root() / tool_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = cache_dir / f"{stamp}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _run_kaggle(
    tool_name: str,
    args: list[str],
    *,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    command = [*_kaggle_cmd(), *args]
    started_at = _now_iso()
    completed = subprocess.run(
        command,
        cwd=_repo_root(),
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    payload: dict[str, Any] = {
        "tool": tool_name,
        "source": "kaggle-cli",
        "command": command,
        "started_at": started_at,
        "finished_at": _now_iso(),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "ok": completed.returncode == 0,
    }
    payload["snapshot_path"] = _write_snapshot(tool_name, payload)
    return payload


def _competition_url(slug: str) -> str:
    return f"https://www.kaggle.com/competitions/{slug}"


def _topic_ref(competition: str, topic: str) -> str:
    if "/" in topic:
        return topic
    return f"{competition}/{topic}"


@mcp.tool()
def kaggle_cli_version() -> dict[str, Any]:
    """Return Kaggle CLI version and help summary for audit/setup checks."""
    version = _run_kaggle("kaggle_cli_version", ["--version"])
    help_result = _run_kaggle("kaggle_cli_help", ["--help"])
    return {
        "version": version,
        "help": help_result,
    }


@mcp.tool()
def kaggle_competitions_list(
    search: str | None = None,
    page: int | None = None,
    sort_by: str | None = None,
) -> dict[str, Any]:
    """List Kaggle competitions, optionally filtered by a search query."""
    args = ["competitions", "list"]
    if search:
        args.extend(["-s", search])
    if page is not None:
        args.extend(["-p", str(page)])
    if sort_by:
        args.extend(["--sort-by", sort_by])
    return _run_kaggle("kaggle_competitions_list", args)


@mcp.tool()
def kaggle_competition_overview(competition: str) -> dict[str, Any]:
    """Return lightweight competition metadata discoverable from CLI."""
    result = _run_kaggle("kaggle_competition_overview", ["competitions", "list", "-s", competition])
    result["competition"] = competition
    result["kaggle_url"] = _competition_url(competition)
    result["evaluation_url"] = f"{_competition_url(competition)}/overview/evaluation"
    result["rules_url"] = f"{_competition_url(competition)}/rules"
    result["discussion_url"] = f"{_competition_url(competition)}/discussion"
    return result


@mcp.tool()
def kaggle_competition_files(competition: str) -> dict[str, Any]:
    """List files for a Kaggle competition."""
    result = _run_kaggle(
        "kaggle_competition_files",
        ["competitions", "files", "-c", competition],
    )
    result["competition"] = competition
    result["kaggle_url"] = f"{_competition_url(competition)}/data"
    return result


@mcp.tool()
def kaggle_competition_download(
    competition: str,
    output_dir: str | None = None,
    unzip: bool = True,
) -> dict[str, Any]:
    """Download competition data under data/raw/<competition> by default."""
    destination = Path(output_dir) if output_dir else Path("data") / "raw" / competition
    destination = (_repo_root() / destination).resolve() if not destination.is_absolute() else destination
    destination.mkdir(parents=True, exist_ok=True)

    args = ["competitions", "download", "-c", competition, "-p", str(destination)]
    if unzip:
        args.append("--unzip")
    result = _run_kaggle("kaggle_competition_download", args, timeout_seconds=900)
    result["competition"] = competition
    result["output_dir"] = str(destination)
    result["files"] = sorted(str(path) for path in destination.glob("*"))
    return result


@mcp.tool()
def kaggle_discussions_list(
    competition: str,
    sort: str = "hot",
    page: int | None = None,
) -> dict[str, Any]:
    """List discussion topics for a competition."""
    args = ["competitions", "topics", "list", competition, "-s", sort]
    if page is not None:
        args.extend(["-p", str(page)])
    result = _run_kaggle("kaggle_discussions_list", args)
    result["competition"] = competition
    result["sort"] = sort
    result["kaggle_url"] = f"{_competition_url(competition)}/discussion"
    return result


@mcp.tool()
def kaggle_discussion_get(competition: str, topic: str) -> dict[str, Any]:
    """Show a discussion topic body and comments."""
    ref = _topic_ref(competition, topic)
    result = _run_kaggle("kaggle_discussion_get", ["competitions", "topics", "show", ref])
    result["competition"] = competition
    result["topic_ref"] = ref
    result["kaggle_url"] = f"{_competition_url(competition)}/discussion/{_safe_name(ref).split('_')[-1]}"
    return result


@mcp.tool()
def kaggle_notebooks_search(
    query: str,
    competition: str | None = None,
    page: int | None = None,
) -> dict[str, Any]:
    """Search Kaggle notebooks/kernels for a query and optional competition."""
    args = ["kernels", "list", "--search", query]
    if competition:
        args.extend(["--competition", competition])
    if page is not None:
        args.extend(["-p", str(page)])
    result = _run_kaggle("kaggle_notebooks_search", args)
    result["query"] = query
    result["competition"] = competition
    result["kaggle_url"] = "https://www.kaggle.com/code"
    return result


@mcp.tool()
def kaggle_notebook_pull(notebook_ref: str, output_dir: str | None = None) -> dict[str, Any]:
    """Pull a Kaggle notebook/kernel source."""
    destination = Path(output_dir) if output_dir else Path("notebooks_external") / _safe_name(notebook_ref)
    destination = (_repo_root() / destination).resolve() if not destination.is_absolute() else destination
    destination.mkdir(parents=True, exist_ok=True)
    result = _run_kaggle(
        "kaggle_notebook_pull",
        ["kernels", "pull", notebook_ref, "-p", str(destination)],
        timeout_seconds=300,
    )
    result["notebook_ref"] = notebook_ref
    result["output_dir"] = str(destination)
    result["files"] = sorted(str(path) for path in destination.glob("*"))
    return result


@mcp.tool()
def kaggle_datasets_list(search: str, page: int | None = None) -> dict[str, Any]:
    """Search Kaggle datasets for technical research."""
    args = ["datasets", "list", "-s", search]
    if page is not None:
        args.extend(["-p", str(page)])
    result = _run_kaggle("kaggle_datasets_list", args)
    result["query"] = search
    result["kaggle_url"] = "https://www.kaggle.com/datasets"
    return result


@mcp.tool()
def kaggle_dataset_download(
    dataset_ref: str,
    output_dir: str | None = None,
    unzip: bool = True,
) -> dict[str, Any]:
    """Download a Kaggle dataset under data/external/<dataset_ref> by default."""
    destination = Path(output_dir) if output_dir else Path("data") / "external" / _safe_name(dataset_ref)
    destination = (_repo_root() / destination).resolve() if not destination.is_absolute() else destination
    destination.mkdir(parents=True, exist_ok=True)
    args = ["datasets", "download", "-d", dataset_ref, "-p", str(destination)]
    if unzip:
        args.append("--unzip")
    result = _run_kaggle("kaggle_dataset_download", args, timeout_seconds=900)
    result["dataset_ref"] = dataset_ref
    result["output_dir"] = str(destination)
    result["files"] = sorted(str(path) for path in destination.glob("*"))
    return result


@mcp.tool()
def kaggle_submissions_list(competition: str) -> dict[str, Any]:
    """List submissions for a Kaggle competition."""
    result = _run_kaggle(
        "kaggle_submissions_list",
        ["competitions", "submissions", "-c", competition],
    )
    result["competition"] = competition
    result["kaggle_url"] = f"{_competition_url(competition)}/submissions"
    return result


if __name__ == "__main__":
    mcp.run()
