#!/usr/bin/env python3
"""Check template structure and local references without requiring record equality."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "aidlc-state.md",
    "audit.md",
    "inception/problem-overview.md",
    "inception/source-register.md",
    "inception/data-contract.md",
    "inception/evaluation-contract.md",
    "inception/kaggle-starter.md",
    "inception/winning-research.md",
    "inception/technical-research.md",
    "construction/implementation-questionnaire.md",
    "construction/architecture.md",
    "construction/experiment-plan.md",
    "construction/code-generation-plan.md",
    "operations/experiment-log.md",
    "operations/poc-decision.md",
]


def check(root: Path) -> list[str]:
    errors: list[str] = []
    template = root / "templates/aidlc-docs"
    for path in REQUIRED:
        if not (template / path).is_file():
            errors.append(f"Missing seed: {path}")
    audit = template / "audit.md"
    if audit.exists() and re.search(r"^### \d{4}-\d{2}-\d{2}", audit.read_text(), re.MULTILINE):
        errors.append("Seed audit contains project-specific historical entries.")
    for path in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not frontmatter:
            errors.append(f"Missing skill frontmatter: {path.relative_to(root)}")
            continue
        values = dict(
            re.findall(r"^(name|description):\s*(.+)$", frontmatter.group(1), re.MULTILINE)
        )
        if values.get("name") != path.parent.name or not values.get("description"):
            errors.append(f"Invalid skill name/description: {path.relative_to(root)}")

    try:
        codex = tomllib.loads((root / ".codex/config.toml").read_text())
        claude = json.loads((root / ".mcp.json").read_text())
        kiro = json.loads((root / ".kiro/settings/mcp.json").read_text())
        json.loads((root / ".claude/settings.json").read_text())
        json.loads((root / ".kiro/agents/research-agent.json").read_text())
        args = codex["mcp_servers"]["kaggle"]["args"]
        if (
            args != claude["mcpServers"]["kaggle"]["args"]
            or args != kiro["mcpServers"]["kaggle"]["args"]
        ):
            errors.append("Bundled Kaggle server commands differ across clients.")
        if not (root / args[-1]).is_file():
            errors.append("Configured MCP server script is missing.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid client configuration: {exc}")

    for path, target in (
        (".kiro/skills", ".agents/skills"),
        (".kiro/steering/agents.md", "AGENTS.md"),
    ):
        if (root / path).resolve() != (root / target).resolve():
            errors.append(f"Unexpected or broken shared reference: {path}")

    parser = MarkdownIt("commonmark", {"html": False}).enable("table")
    documents = [root / path for path in ("README.md", "AGENTS.md", "CLAUDE.md", "COPILOT.md")]
    for directory in ("docs", "templates/aidlc-docs", "aidlc-docs", ".agents/skills", "tools"):
        documents.extend((root / directory).rglob("*.md"))
    for source in documents:
        if not source.is_file():
            errors.append(f"Missing document: {source.relative_to(root)}")
            continue
        for token in parser.parse(source.read_text(encoding="utf-8")):
            for child in token.children or []:
                if child.type != "link_open":
                    continue
                href = child.attrGet("href") or ""
                parts = urlsplit(href)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                target = source.parent / unquote(parts.path)
                if not target.exists() and source.is_relative_to(template):
                    generated_source = root / "aidlc-docs" / source.relative_to(template)
                    target = generated_source.parent / unquote(parts.path)
                if not target.exists():
                    errors.append(f"Broken link in {source.relative_to(root)}: {href}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check(args.root.resolve())
    for error in errors:
        print(error)
    print(f"Template validation: {len(errors)} errors. Project records may differ from seeds.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
