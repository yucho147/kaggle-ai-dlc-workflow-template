#!/usr/bin/env python3
"""Download competition files using the same CLI boundary as the MCP server."""

from __future__ import annotations

import argparse
import sys

from workflow_tools.kaggle import download_competition, finalize, run_kaggle, validate_slug


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("competition")
    parser.add_argument("--no-unzip", action="store_true")
    args = parser.parse_args()
    try:
        validate_slug(args.competition)
        for name, command in (
            ("kaggle_cli_version", ["--version"]),
            ("kaggle_cli_help", ["--help"]),
            ("kaggle_competition_files", ["competitions", "files", args.competition]),
        ):
            result = finalize(run_kaggle(name, command))
            print(result["stdout"])
            if not result["ok"]:
                print(result["stderr"] or str(result["error"]), file=sys.stderr)
                return 1
        result = download_competition(args.competition, unzip=not args.no_unzip)
        print(result["stdout"])
        print(f"Snapshot: {result['snapshot_path']}")
        if not result["ok"]:
            print(result["stderr"] or str(result["error"]), file=sys.stderr)
            return 1
        print(f"Data directory: {result['output_dir']}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
