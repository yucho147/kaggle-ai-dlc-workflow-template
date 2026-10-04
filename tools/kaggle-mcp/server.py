"""MCP tools for Kaggle retrieval; CLI execution lives in workflow_tools.kaggle."""

from __future__ import annotations

from pathlib import Path
import zipfile
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from workflow_tools.kaggle import (
    destination_path,
    download_competition,
    extract_archive,
    finalize,
    run_kaggle,
    validate_ref,
    validate_slug,
)

mcp = FastMCP(
    "kaggle-mcp",
    instructions=(
        "Use kaggle_cli_version before retrieval. Tools return CLI text with ok/error, "
        "timestamps and snapshot_path; check failures and truncation. Overview is only "
        "discovery metadata and URLs, not page content or rules. Record short source summaries "
        "and revisions in aidlc-docs. Downloads write local files under the project data roots. "
        "Do not execute pulled notebooks without checking licenses and assumptions."
    ),
)
READ = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True)
DOWNLOAD = ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True)


def _page(page: int | None) -> list[str]:
    if page is not None and page < 1:
        raise ValueError("page must be at least 1.")
    return ["-p", str(page)] if page is not None else []


def _page_size(size: int) -> list[str]:
    if not 1 <= size <= 200:
        raise ValueError("page_size must be between 1 and 200.")
    return ["--page-size", str(size)]


def _run(tool: str, args: list[str], **metadata: Any) -> dict[str, Any]:
    return finalize(run_kaggle(tool, args, metadata=metadata))


def _url(competition: str) -> str:
    return f"https://www.kaggle.com/competitions/{validate_slug(competition)}"


@mcp.tool(annotations=READ)
def kaggle_cli_version() -> dict[str, Any]:
    """Return CLI version and help. This does not prove authenticated API access."""
    version = _run("kaggle_cli_version", ["--version"])
    help_result = _run("kaggle_cli_help", ["--help"])
    return {
        "schema_version": 1,
        "ok": version["ok"] and help_result["ok"],
        "version": version,
        "help": help_result,
    }


@mcp.tool(annotations=READ)
def kaggle_competitions_list(
    search: str | None = None,
    page: int | None = None,
    sort_by: str | None = None,
) -> dict[str, Any]:
    """Discover competitions. Inspect pagination and exact refs before selecting one."""
    args = ["competitions", "list", *_page(page)]
    if search:
        args += ["-s", search]
    if sort_by:
        args += ["--sort-by", sort_by]
    return _run("kaggle_competitions_list", args, query=search, page=page)


@mcp.tool(annotations=READ)
def kaggle_competition_overview(competition: str) -> dict[str, Any]:
    """Return discovery metadata and page URLs, not overview/evaluation/rules bodies."""
    url = _url(competition)
    return _run(
        "kaggle_competition_overview",
        ["competitions", "list", "-s", competition],
        competition=competition,
        metadata_only=True,
        kaggle_url=url,
        evaluation_url=f"{url}/overview/evaluation",
        rules_url=f"{url}/rules",
        discussion_url=f"{url}/discussion",
    )


@mcp.tool(annotations=READ)
def kaggle_competition_files(
    competition: str,
    page_size: int = 100,
    page_token: str | None = None,
) -> dict[str, Any]:
    """List a bounded page of competition files, sizes and any continuation token."""
    url = _url(competition)
    args = ["competitions", "files", competition, *_page_size(page_size)]
    if page_token:
        args += ["--page-token", page_token]
    return _run(
        "kaggle_competition_files",
        args,
        competition=competition,
        page_size=page_size,
        page_token=page_token,
        kaggle_url=f"{url}/data",
    )


@mcp.tool(annotations=DOWNLOAD)
def kaggle_competition_download(
    competition: str,
    output_dir: str | None = None,
    unzip: bool = True,
) -> dict[str, Any]:
    """Download to data/raw; extraction validates paths and refuses existing files."""
    return download_competition(competition, output_dir=output_dir, unzip=unzip)


@mcp.tool(annotations=READ)
def kaggle_discussions_list(
    competition: str,
    sort: Literal["hot", "top", "new", "recent", "active", "relevance"] = "top",
    page: int | None = None,
) -> dict[str, Any]:
    """List one page of topics. top is the supported alternative to invalid votes sort."""
    url = _url(competition)
    if sort not in {"hot", "top", "new", "recent", "active", "relevance"}:
        raise ValueError("Unsupported discussion sort; inspect topics list --help.")
    args = ["competitions", "topics", "list", competition, "-s", sort, *_page(page)]
    return _run(
        "kaggle_discussions_list",
        args,
        competition=competition,
        sort=sort,
        page=page,
        kaggle_url=f"{url}/discussion",
    )


@mcp.tool(annotations=READ)
def kaggle_discussion_get(
    competition: str,
    topic: str,
    page_size: int = 100,
    page_token: str | None = None,
) -> dict[str, Any]:
    """Read a topic and a bounded page of comments. Check continuation tokens."""
    url = _url(competition)
    parts = topic.split("/")
    if len(parts) == 2:
        if parts[0] != competition:
            raise ValueError("Topic ref must match competition.")
        topic = parts[1]
    if not topic.isascii() or not topic.isdigit():
        raise ValueError("topic must be a numeric ID or competition/ID.")
    args = ["competitions", "topics", "show", competition, topic, *_page_size(page_size)]
    if page_token:
        args += ["--page-token", page_token]
    return _run(
        "kaggle_discussion_get",
        args,
        competition=competition,
        topic_ref=f"{competition}/{topic}",
        page_size=page_size,
        page_token=page_token,
        kaggle_url=f"{url}/discussion/{topic}",
    )


@mcp.tool(annotations=READ)
def kaggle_notebooks_search(
    query: str,
    competition: str | None = None,
    page: int | None = None,
    page_size: int = 20,
) -> dict[str, Any]:
    """Search notebooks with an optional competition filter."""
    args = ["kernels", "list", "--search", query, *_page(page), *_page_size(page_size)]
    if competition:
        args += ["--competition", validate_slug(competition)]
    return _run(
        "kaggle_notebooks_search",
        args,
        query=query,
        competition=competition,
        page=page,
        page_size=page_size,
        kaggle_url="https://www.kaggle.com/code",
    )


@mcp.tool(annotations=DOWNLOAD)
def kaggle_notebook_pull(notebook_ref: str, output_dir: str | None = None) -> dict[str, Any]:
    """Pull source and metadata into notebooks_external; does not execute source."""
    ref = validate_ref(notebook_ref)
    destination = destination_path(output_dir, "notebooks_external", ref.replace("/", "_"))
    payload = run_kaggle(
        "kaggle_notebook_pull",
        ["kernels", "pull", ref, "-p", str(destination), "--metadata"],
        timeout=300,
        metadata={
            "notebook_ref": ref,
            "output_dir": str(destination),
            "kaggle_url": f"https://www.kaggle.com/code/{ref}",
        },
    )
    payload["files"] = sorted(str(path) for path in destination.iterdir())
    return finalize(payload)


@mcp.tool(annotations=READ)
def kaggle_datasets_list(search: str, page: int | None = None) -> dict[str, Any]:
    """Search one page of datasets. Inspect dataset versions and licenses separately."""
    return _run(
        "kaggle_datasets_list",
        ["datasets", "list", "-s", search, *_page(page)],
        query=search,
        page=page,
        kaggle_url="https://www.kaggle.com/datasets",
    )


@mcp.tool(annotations=DOWNLOAD)
def kaggle_dataset_download(
    dataset_ref: str,
    output_dir: str | None = None,
    unzip: bool = True,
) -> dict[str, Any]:
    """Download to data/external; preserve archives and validate extraction locally."""
    ref = validate_ref(dataset_ref)
    destination = destination_path(output_dir, "data/external", ref.replace("/", "_"))
    payload = run_kaggle(
        "kaggle_dataset_download",
        ["datasets", "download", ref, "-p", str(destination)],
        timeout=900,
        metadata={
            "dataset_ref": ref,
            "output_dir": str(destination),
            "kaggle_url": f"https://www.kaggle.com/datasets/{ref}",
        },
    )
    if payload["ok"] and unzip:
        archives = list(destination.glob("*.zip"))
        if len(archives) != 1:
            payload.update(
                ok=False,
                error={"kind": "extraction", "message": "Expected exactly one dataset archive."},
            )
        else:
            try:
                payload["extracted"] = extract_archive(Path(archives[0]), destination)
            except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as exc:
                payload.update(ok=False, error={"kind": "extraction", "message": str(exc)})
    payload["files"] = sorted(str(path) for path in destination.iterdir())
    return finalize(payload)


@mcp.tool(annotations=READ)
def kaggle_submissions_list(competition: str) -> dict[str, Any]:
    """Read submission history; never create a submission."""
    url = _url(competition)
    return _run(
        "kaggle_submissions_list",
        ["competitions", "submissions", competition],
        competition=competition,
        kaggle_url=f"{url}/submissions",
    )


if __name__ == "__main__":
    mcp.run()
