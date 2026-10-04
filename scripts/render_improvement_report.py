#!/usr/bin/env python3
"""Generate a standalone HTML review surface from canonical AI-DLC records."""

from __future__ import annotations

import argparse
import html
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from markdown_it import MarkdownIt

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SECTIONS = [
    ("Project State", "aidlc-docs/aidlc-state.md"),
    ("Problem Overview", "aidlc-docs/inception/problem-overview.md"),
    ("Sources", "aidlc-docs/inception/source-register.md"),
    ("Data Contract", "aidlc-docs/inception/data-contract.md"),
    ("Evaluation Contract", "aidlc-docs/inception/evaluation-contract.md"),
    ("Kaggle Starter", "aidlc-docs/inception/kaggle-starter.md"),
    ("Winning Research", "aidlc-docs/inception/winning-research.md"),
    ("Technical Research", "aidlc-docs/inception/technical-research.md"),
    ("Strategy", "aidlc-docs/inception/strategy.md"),
    ("Risks", "aidlc-docs/inception/risk-assessment.md"),
    ("Architecture", "aidlc-docs/construction/architecture.md"),
    ("Implementation Candidates", "aidlc-docs/construction/implementation-candidates.md"),
    ("Experiment Plan", "aidlc-docs/construction/experiment-plan.md"),
    ("Code Generation Plan", "aidlc-docs/construction/code-generation-plan.md"),
    ("Experiment Log", "aidlc-docs/operations/experiment-log.md"),
    ("CV / LB Tracking", "aidlc-docs/operations/cv-lb-tracking.md"),
    ("PoC Decision", "aidlc-docs/operations/poc-decision.md"),
    ("Lessons Learned", "aidlc-docs/operations/lessons-learned.md"),
    ("Reusable Patterns", "aidlc-docs/operations/reusable-patterns.md"),
    ("Improvement Loop", "aidlc-docs/operations/improvement-loop.md"),
]
STATUS_VALUES = {
    "idea",
    "selected",
    "specced",
    "implemented",
    "executed",
    "reviewed",
    "adopted",
    "rejected",
    "iterate",
    "failed",
    "pending",
    "active",
    "complete",
    "succeeded",
    "not-applicable",
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-") or "section"


def render_markdown(
    markdown: str, *, source: Path | None = None, output: Path | None = None, root: Path = ROOT_DIR
) -> str:
    parser = MarkdownIt("commonmark", {"html": False}).enable("table").enable("strikethrough")
    tokens = parser.parse(markdown)
    section_targets = {(root / path).resolve(): slugify(title) for title, path in DEFAULT_SECTIONS}
    headers: list[str] = []
    column = 0
    in_header = False
    in_cell = False
    for token in tokens:
        if token.type == "thead_open":
            in_header = True
        elif token.type == "thead_close":
            in_header = False
        elif token.type == "tr_open":
            column = 0
        elif token.type == "td_open":
            token.attrSet("data-label", headers[column] if column < len(headers) else "")
            column += 1
            in_cell = True
        elif token.type == "td_close":
            in_cell = False
        elif token.type == "table_open":
            headers = []
        elif token.type in {"heading_open", "heading_close"}:
            token.tag = f"h{min(int(token.tag[1:]) + 1, 6)}"
        if token.type != "inline":
            continue
        if in_header:
            headers.append(token.content)
        if in_cell and (
            token.content.lower() in STATUS_VALUES
            or re.fullmatch(r"P[0-9]+", token.content, re.IGNORECASE)
        ):
            value = token.content.lower()
            css_class = (
                "priority" if value.startswith("p") and value[1:].isdigit() else f"status-{value}"
            )
            from markdown_it.token import Token

            badge = Token("html_inline", "", 0)
            badge.content = f'<span class="pill {css_class}">{html.escape(token.content)}</span>'
            token.children = [badge]
        for child in token.children or []:
            if child.type != "link_open":
                continue
            href = child.attrGet("href") or ""
            parts = urlsplit(href)
            if parts.scheme and parts.scheme not in {"https", "http", "mailto"}:
                child.attrs.pop("href", None)
            elif href.startswith("//"):
                child.attrs.pop("href", None)
            elif source and output and parts.path and not parts.scheme:
                target = (source.parent / unquote(parts.path)).resolve()
                if not target.is_relative_to(root.resolve()):
                    child.attrs.pop("href", None)
                elif target in section_targets:
                    child.attrSet("href", f"#{section_targets[target]}")
                else:
                    relative = quote(os.path.relpath(target, output.parent), safe="/")
                    child.attrSet(
                        "href", relative + (f"#{parts.fragment}" if parts.fragment else "")
                    )
    return parser.renderer.render(tokens, parser.options, {})


def render_section(title: str, path: str, root: Path, output: Path) -> str:
    source = root / path
    if not source.is_file():
        body = (
            '<p class="missing-source">未生成の文書です。初期化で欠落ファイルを補ってください。</p>'
        )
    else:
        lines = source.read_text(encoding="utf-8").splitlines()
        if lines and lines[0].startswith("# "):
            lines = lines[1:]
        body = render_markdown("\n".join(lines), source=source, output=output, root=root)
    return (
        f'<section class="doc-section" id="{slugify(title)}">'
        f'<div class="section-heading"><h2>{html.escape(title)}</h2>'
        f'<p class="source">Source <code>{html.escape(path)}</code></p></div>'
        f"{body}</section>"
    )


def build_html(root: Path, output: Path, title: str = "AI-DLC 調査・実験レビュー") -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    css_path = root / "docs/assets/improvement-report.css"
    if not css_path.is_file():
        css_path = ROOT_DIR / "docs/assets/improvement-report.css"
    css = css_path.read_text(encoding="utf-8")
    nav = "".join(
        f'<a href="#{slugify(name)}"><span>{index:02d}</span>{html.escape(name)}</a>'
        for index, (name, _) in enumerate(DEFAULT_SECTIONS, 1)
    )
    sections = "".join(render_section(name, path, root, output) for name, path in DEFAULT_SECTIONS)
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{css}</style>
</head>
<body>
<a class="skip-link" href="#main">本文へ</a>
<div class="app-shell">
<aside class="side-nav">
<div class="brand"><span class="brand-mark">AI</span>
<div><strong>AI-DLC</strong><small>Research &amp; Experiment Review</small></div></div>
<nav aria-label="文書一覧">{nav}</nav>
</aside>
<div class="page">
<header class="hero">
<div><p class="eyebrow">Research · Evidence · Decision</p>
<h1>{html.escape(title)}</h1>
<p class="subtitle">生成日時 {timestamp}。
出典、評価条件、結果、次の判断をまとめた閲覧用レポートです。</p></div>
<div class="hero-actions"><a class="button primary" href="#project-state">次の作業</a>
<a class="button" href="#experiment-log">実行結果</a></div>
</header>
<section class="guide" aria-label="レビューの観点">
<div class="guide-card accent-blue"><span class="card-label">Evidence</span>
<h2>条件と出典を確認</h2><p>何を確認済みか、未取得か、仮説かを見分けます。</p></div>
<div class="guide-card accent-green"><span class="card-label">Evaluation</span>
<h2>同じ条件で比較</h2><p>データ・split・metric・run ID を確認し、MLflow で詳細を比較します。</p></div>
<div class="guide-card accent-amber"><span class="card-label">Decision</span>
<h2>採否と次の仮説</h2><p>改善幅、ばらつき、費用、限界から次の作業を選びます。</p></div>
</section>
<main id="main">{sections}</main>
<p class="footer">正本は aidlc-docs/。生成 HTML の変更は再生成で失われます。</p>
</div>
</div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT_DIR)
    parser.add_argument("--output", default="outputs/reports/improvement-report.html")
    parser.add_argument("--title", default="AI-DLC 調査・実験レビュー")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    output = (root / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(root, output, args.title), encoding="utf-8")
    print(f"Rendered {output}")


if __name__ == "__main__":
    main()
