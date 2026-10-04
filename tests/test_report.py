from html.parser import HTMLParser
from pathlib import Path

from scripts.render_improvement_report import build_html, render_markdown


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.hrefs = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append(tag)
        if "href" in values:
            self.hrefs.append(values["href"])
        if "id" in values:
            self.ids.append(values["id"])


def test_markdown_renders_tables_escaped_pipes_and_nested_lists():
    result = render_markdown(
        "| Name | Value |\n| --- | --- |\n| a \\| b | **bold** |\n\n- parent\n  - child\n"
    )
    assert "<table>" in result and "<strong>bold</strong>" in result
    assert "a | b" in result and 'data-label="Name"' in result
    assert result.count("<ul>") == 2


def test_untrusted_html_and_unsafe_links_are_not_active():
    result = render_markdown(
        "<script>alert(1)</script>\n\n[x](javascript:alert(1))\n\n"
        "[y](data:text/html,bad)\n\n[z](//remote.example)"
    )
    parsed = Links()
    parsed.feed(result)
    assert "script" not in parsed.tags
    assert not any(href.startswith(("javascript:", "data:", "//")) for href in parsed.hrefs)


def test_closed_and_unclosed_code_fences_are_preserved():
    assert "&lt;tag&gt;" in render_markdown("```html\n<tag>\n```")
    assert "unfinished" in render_markdown("```\nunfinished")


def test_local_links_resolve_from_source_and_report_output(tmp_path):
    source = tmp_path / "aidlc-docs/operations/lessons-learned.md"
    source.parent.mkdir(parents=True)
    output = tmp_path / "outputs/reports/report.html"
    result = render_markdown(
        "[state](../aidlc-state.md) [artifact](../../outputs/runs/a/model.joblib)",
        source=source,
        output=output,
        root=tmp_path,
    )
    assert 'href="#project-state"' in result
    assert 'href="../runs/a/model.joblib"' in result


def test_report_is_standalone_and_navigation_targets_are_unique(tmp_path):
    output = tmp_path / "report.html"
    result = build_html(tmp_path, output)
    parser = Links()
    parser.feed(result)
    assert len(parser.ids) == len(set(parser.ids))
    assert all(href[1:] in parser.ids for href in parser.hrefs if href.startswith("#"))
    assert "未生成の文書" in result
    assert "<style>" in result and "script" not in parser.tags


def test_title_is_escaped(tmp_path):
    result = build_html(tmp_path, Path("report.html"), title="<script>bad</script>")
    parser = Links()
    parser.feed(result)
    assert "script" not in parser.tags
    assert "&lt;script&gt;bad&lt;/script&gt;" in result
