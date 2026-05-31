#!/usr/bin/env python3
"""Render a human-facing HTML report from AI-DLC markdown docs.

The generated HTML is a review surface. The source of truth remains the small
Markdown files under aidlc-docs/.
"""

from __future__ import annotations

import argparse
import html
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_SECTIONS = [
    ("Improvement Loop", "aidlc-docs/operations/improvement-loop.md"),
    ("Experiment Plan", "aidlc-docs/construction/experiment-plan.md"),
    ("Experiment Log", "aidlc-docs/operations/experiment-log.md"),
    ("CV / LB Tracking", "aidlc-docs/operations/cv-lb-tracking.md"),
    ("Lessons Learned", "aidlc-docs/operations/lessons-learned.md"),
    ("Reusable Patterns", "aidlc-docs/operations/reusable-patterns.md"),
]

SECTION_DESCRIPTIONS = {
    "Improvement Loop": "Roles, review flow, and the source-of-truth boundary.",
    "Experiment Plan": "Human hypotheses, priorities, expected impact, and stop conditions.",
    "Experiment Log": "Commands, configs, MLflow runs, artifacts, and factual outcomes.",
    "CV / LB Tracking": "Score comparison, trust judgment, and the next action.",
    "Lessons Learned": "What worked, what failed, and reusable conclusions.",
    "Reusable Patterns": "Patterns worth carrying into future projects.",
}

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
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def repo_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT_DIR))
    except ValueError:
        return str(path)


def inline_markdown(text: str) -> str:
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    parts: list[str] = []
    last = 0
    for match in link_pattern.finditer(text):
        parts.append(_inline_code(text[last : match.start()]))
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        parts.append(f'<a href="{href}">{label}</a>')
        last = match.end()
    parts.append(_inline_code(text[last:]))
    return "".join(parts)


def _inline_code(text: str) -> str:
    pieces = text.split("`")
    rendered: list[str] = []
    for index, piece in enumerate(pieces):
        escaped = html.escape(piece)
        if index % 2 == 1:
            rendered.append(f"<code>{escaped}</code>")
        else:
            rendered.append(escaped)
    return "".join(rendered)


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table_cell(cell: str) -> str:
    stripped = cell.strip()
    normalized = stripped.lower()
    if normalized in STATUS_VALUES:
        return f'<span class="pill status-{html.escape(normalized)}">{inline_markdown(stripped)}</span>'
    if re.fullmatch(r"P[0-9]+", stripped, flags=re.IGNORECASE):
        return f'<span class="pill priority">{inline_markdown(stripped)}</span>'
    if normalized == "tbd":
        return '<span class="muted-pill">TBD</span>'
    return inline_markdown(stripped)


def render_table(lines: list[str], start: int) -> tuple[str, int]:
    header = split_table_row(lines[start])
    rows: list[list[str]] = []
    index = start + 2
    while index < len(lines):
        line = lines[index]
        if not (line.strip().startswith("|") and line.strip().endswith("|")):
            break
        rows.append(split_table_row(line))
        index += 1

    cells = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    body_rows = []
    for row in rows:
        body_cells = "".join(
            f'<td data-label="{html.escape(header[index] if index < len(header) else "")}">'
            f"{render_table_cell(cell)}</td>"
            for index, cell in enumerate(row)
        )
        body_rows.append(f"<tr>{body_cells}</tr>")

    table = f"<table><thead><tr>{cells}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"
    return table, index


def close_list(stack: list[str], output: list[str]) -> None:
    while stack:
        output.append(f"</{stack.pop()}>")


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    list_stack: list[str] = []
    in_code = False
    code_lines: list[str] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_list(list_stack, output)
            if in_code:
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not stripped:
            flush_paragraph()
            close_list(list_stack, output)
            index += 1
            continue

        if index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            flush_paragraph()
            close_list(list_stack, output)
            table, index = render_table(lines, index)
            output.append(table)
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list(list_stack, output)
            level = min(len(heading.group(1)) + 1, 4)
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            index += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_list(list_stack, output)
            quote = stripped.lstrip(">").strip()
            output.append(f"<blockquote>{inline_markdown(quote)}</blockquote>")
            index += 1
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if unordered or ordered:
            flush_paragraph()
            tag = "ul" if unordered else "ol"
            if not list_stack or list_stack[-1] != tag:
                close_list(list_stack, output)
                output.append(f"<{tag}>")
                list_stack.append(tag)
            item = unordered.group(1) if unordered else ordered.group(1)
            output.append(f"<li>{inline_markdown(item)}</li>")
            index += 1
            continue

        close_list(list_stack, output)
        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    close_list(list_stack, output)
    return "\n".join(output)


def render_section(title: str, source: Path) -> str:
    section_id = slugify(title)
    if not source.exists():
        body = f"<p>Source file not found: <code>{html.escape(repo_path(source))}</code></p>"
    else:
        markdown = source.read_text(encoding="utf-8")
        lines = markdown.splitlines()
        if lines and lines[0].startswith("# "):
            markdown = "\n".join(lines[1:]).lstrip()
        body = render_markdown(markdown)
    source_label = html.escape(repo_path(source))
    description = html.escape(SECTION_DESCRIPTIONS.get(title, ""))
    return (
        f'<section class="doc-section" id="{section_id}">'
        f'<div class="section-heading">'
        f"<div><h2>{html.escape(title)}</h2>"
        f'<p class="section-description">{description}</p></div>'
        f'<p class="source">Source <code>{source_label}</code></p>'
        f"</div>{body}</section>"
    )


def build_html(title: str, output: Path, css: str) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    nav = "\n".join(
        f'<a href="#{slugify(section_title)}"><span>{index:02d}</span>{html.escape(section_title)}</a>'
        for index, (section_title, _) in enumerate(DEFAULT_SECTIONS, start=1)
    )
    sections = "\n".join(
        render_section(section_title, ROOT_DIR / section_path)
        for section_title, section_path in DEFAULT_SECTIONS
    )
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
{css}
  </style>
</head>
<body>
  <div class="app-shell">
    <aside class="side-nav">
      <div class="brand">
        <span class="brand-mark">AI</span>
        <div>
          <strong>AI-DLC</strong>
          <small>Improvement Review</small>
        </div>
      </div>
      <nav>{nav}</nav>
      <div class="side-note">
        <strong>Review surface</strong>
        <p>Use this report with MLflow UI. Edit Markdown sources, not generated HTML.</p>
      </div>
    </aside>

    <div class="page">
      <header class="hero">
        <div>
          <p class="eyebrow">Human Review Dashboard</p>
          <h1>{html.escape(title)}</h1>
          <p class="subtitle">Generated at {html.escape(generated_at)}. Built for hypothesis review, experiment comparison, and next-action decisions.</p>
        </div>
        <div class="hero-actions">
          <a class="button primary" href="#experiment-plan">Review Plan</a>
          <a class="button" href="#cv-lb-tracking">Check Scores</a>
        </div>
      </header>

      <section class="guide" aria-label="Review workflow summary">
        <div class="guide-card accent-blue">
          <span class="card-label">Human View</span>
          <h2>MLflow + HTML</h2>
          <p>Review metrics, artifacts, hypotheses, and decisions in browser-friendly surfaces.</p>
        </div>
        <div class="guide-card accent-green">
          <span class="card-label">Agent Source</span>
          <h2>Markdown stays canonical</h2>
          <p>Agents update <code>aidlc-docs/</code>. This page is regenerated from those files.</p>
        </div>
        <div class="guide-card accent-amber">
          <span class="card-label">Loop State</span>
          <h2>Idea to decision</h2>
          <p>Move from hypothesis to spec, implementation, execution, review, and decision.</p>
        </div>
      </section>

      <main>{sections}</main>
      <p class="footer">Generated by <code>scripts/render_improvement_report.py</code></p>
    </div>
  </div>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="outputs/reports/improvement-report.html",
        help="HTML output path.",
    )
    parser.add_argument("--title", default="AI-DLC Improvement Report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = (ROOT_DIR / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    css_source = ROOT_DIR / "docs" / "assets" / "improvement-report.css"
    output.write_text(
        build_html(args.title, output, css_source.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    print(f"Rendered {repo_path(output)}")


if __name__ == "__main__":
    main()
