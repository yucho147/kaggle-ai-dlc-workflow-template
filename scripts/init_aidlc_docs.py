#!/usr/bin/env python3
"""Seed project records without overwriting them; explicit resets create backups."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def initialize(
    template: Path,
    target: Path,
    *,
    check: bool = False,
    force: bool = False,
    new_project: bool = False,
) -> tuple[int, Path | None]:
    template = template.resolve()
    target = target.absolute()
    if target.is_symlink():
        raise ValueError("The target directory must not be a symlink.")
    target = target.resolve()
    if (
        target == target.parent
        or template.is_relative_to(target)
        or target.is_relative_to(template)
    ):
        raise ValueError("Target must not contain, or be inside, the template directory.")
    if (target / ".git").exists() or (target / "pyproject.toml").exists():
        raise ValueError("Target looks like a repository root, not an AI-DLC docs directory.")
    sources = sorted(template.rglob("*.md"))
    if not sources:
        raise ValueError(f"No Markdown templates found: {template}")
    if any(path.is_symlink() for path in sources):
        raise ValueError("Template files must not be symlinks.")
    if target.exists() and not target.is_dir():
        raise ValueError("Target must be a directory.")

    missing = [
        path.relative_to(template)
        for path in sources
        if not (target / path.relative_to(template)).is_file()
    ]
    if check:
        for path in missing:
            print(f"Missing: {path}")
        print(f"Checked {len(sources)} required files; {len(missing)} missing.")
        return (1 if missing else 0), None

    backup = None
    if target.exists() and (force or new_project):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = (
            target.parent / "outputs" / "doc-backups" / f"{target.name}-{stamp}-{uuid4().hex[:8]}"
        )
        if backup.is_relative_to(target):
            raise ValueError("Backup directory must be outside target.")
        backup.parent.mkdir(parents=True, exist_ok=True)
        if new_project:
            target.rename(backup)
        else:
            shutil.copytree(target, backup, symlinks=True)
        print(f"Backup: {backup}")

    target.mkdir(parents=True, exist_ok=True)
    written = 0
    for source in sources:
        destination = target / source.relative_to(template)
        if destination.exists() and not force:
            continue
        if destination.is_symlink() or not destination.resolve().is_relative_to(target):
            raise ValueError(f"Unsafe destination: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f".{destination.name}.{uuid4().hex}.tmp")
        temporary.write_bytes(source.read_bytes())
        temporary.replace(destination)
        written += 1
    print(f"Initialized {target}: {written} files written, existing records preserved.")
    return 0, backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="Check required file presence.")
    modes.add_argument("--force", action="store_true", help="Back up and overwrite seed files.")
    modes.add_argument("--new-project", action="store_true", help="Archive docs and start fresh.")
    parser.add_argument(
        "--target", default="aidlc-docs", help="Destination, relative to repo root."
    )
    args = parser.parse_args()
    target = Path(args.target).expanduser()
    if not target.is_absolute():
        target = ROOT / target
    try:
        code, _ = initialize(
            ROOT / "templates/aidlc-docs",
            target,
            check=args.check,
            force=args.force,
            new_project=args.new_project,
        )
        return code
    except (OSError, ValueError) as exc:
        print(f"Initialization failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
