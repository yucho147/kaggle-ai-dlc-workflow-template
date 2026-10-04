import argparse
import importlib.util
import json
import stat
import subprocess
import types
import zipfile
from pathlib import Path

import pytest

from workflow_tools import kaggle

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def server(monkeypatch, tmp_path):
    spec = importlib.util.spec_from_file_location(
        "test_kaggle_mcp", ROOT / "tools/kaggle-mcp/server.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(kaggle, "ROOT", tmp_path)
    monkeypatch.setenv("KAGGLE_MCP_CACHE_DIR", str(tmp_path / "cache"))
    return module


@pytest.mark.parametrize(
    "name,kwargs",
    [
        ("kaggle_competitions_list", {"search": "titanic", "page": 2, "sort_by": "latestDeadline"}),
        ("kaggle_competition_overview", {"competition": "titanic"}),
        ("kaggle_competition_files", {"competition": "titanic", "page_token": "next"}),
        ("kaggle_competition_download", {"competition": "titanic", "unzip": False}),
        ("kaggle_discussions_list", {"competition": "titanic", "sort": "top", "page": 2}),
        ("kaggle_discussion_get", {"competition": "titanic", "topic": "titanic/123"}),
        (
            "kaggle_notebooks_search",
            {"query": "baseline", "competition": "titanic", "page_size": 25},
        ),
        ("kaggle_notebook_pull", {"notebook_ref": "owner/notebook"}),
        ("kaggle_datasets_list", {"search": "weather", "page": 2}),
        ("kaggle_dataset_download", {"dataset_ref": "owner/dataset", "unzip": False}),
        ("kaggle_submissions_list", {"competition": "titanic"}),
    ],
)
def test_tool_commands_are_accepted_by_installed_kaggle_parser(server, monkeypatch, name, kwargs):
    from kaggle import cli

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    cli.parse_competitions(subparsers)
    cli.parse_datasets(subparsers)
    cli.parse_kernels(subparsers)

    def fake_run(command, **options):
        parsed = parser.parse_args(command[1:])
        assert callable(parsed.func)
        assert options["check"] is False
        return subprocess.CompletedProcess(command, 0, stdout="retrieved", stderr="")

    monkeypatch.setattr(
        kaggle,
        "subprocess",
        types.SimpleNamespace(run=fake_run, TimeoutExpired=subprocess.TimeoutExpired),
    )
    result = getattr(server, name)(**kwargs)
    assert result["ok"]
    snapshot = json.loads(Path(result["snapshot_path"]).read_text())
    assert snapshot["ok"]
    if "kaggle_url" in result:
        assert snapshot["kaggle_url"] == result["kaggle_url"]


@pytest.mark.parametrize("slug", ["../escape", "--help", "a/b", "a b", "https://kaggle.com/a"])
def test_invalid_slug_is_rejected(slug):
    with pytest.raises(ValueError):
        kaggle.validate_slug(slug)


def test_download_destination_cannot_escape_project_root(monkeypatch, tmp_path):
    monkeypatch.setattr(kaggle, "ROOT", tmp_path / "project")
    with pytest.raises(ValueError):
        kaggle.destination_path(str(tmp_path / "outside"), "data/raw", "titanic")
    assert not (tmp_path / "outside").exists()


@pytest.mark.parametrize("mode", ["nonzero", "timeout", "missing-command"])
def test_failures_are_structured_and_snapshotted(monkeypatch, tmp_path, mode):
    monkeypatch.setattr(kaggle, "ROOT", tmp_path)
    monkeypatch.setenv("KAGGLE_MCP_CACHE_DIR", str(tmp_path / "cache"))

    def fake_run(command, **options):
        if mode == "timeout":
            raise subprocess.TimeoutExpired(command, 1, output=b"partial output")
        if mode == "missing-command":
            raise FileNotFoundError("not installed")
        return subprocess.CompletedProcess(command, 3, stdout="", stderr="API denied")

    monkeypatch.setattr(
        kaggle,
        "subprocess",
        types.SimpleNamespace(run=fake_run, TimeoutExpired=subprocess.TimeoutExpired),
    )
    result = kaggle.finalize(kaggle.run_kaggle("test", ["competitions", "list"]))
    assert not result["ok"]
    assert (
        result["error"]["kind"]
        == {"nonzero": "cli", "timeout": "timeout", "missing-command": "process"}[mode]
    )
    assert Path(result["snapshot_path"]).is_file()
    if mode == "timeout":
        assert result["stdout"] == "partial output"


def test_snapshot_preserves_full_result_and_bounded_response(monkeypatch, tmp_path):
    monkeypatch.setenv("KAGGLE_MCP_CACHE_DIR", str(tmp_path))
    payload = {
        "tool": "test",
        "stdout": "x" * 20_000,
        "stderr": "",
        "files": [str(i) for i in range(500)],
        "ok": True,
    }
    first = kaggle.finalize(payload)
    second = kaggle.finalize(payload)
    assert first["snapshot_path"] != second["snapshot_path"]
    assert first["truncated"] and first["files_count"] == 500
    assert len(first["files"]) == 200
    raw = json.loads(Path(first["snapshot_path"]).read_text())
    assert len(raw["stdout"]) == 20_000 and len(raw["files"]) == 500


def test_known_token_is_redacted_before_snapshot(monkeypatch, tmp_path):
    monkeypatch.setenv("KAGGLE_API_TOKEN", "example-private-token")
    monkeypatch.setenv("KAGGLE_MCP_CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(
        kaggle,
        "subprocess",
        types.SimpleNamespace(
            run=lambda command, **kw: subprocess.CompletedProcess(
                command, 1, stdout="", stderr="example-private-token"
            ),
            TimeoutExpired=subprocess.TimeoutExpired,
        ),
    )
    result = kaggle.finalize(kaggle.run_kaggle("test", ["competitions", "list"]))
    assert "example-private-token" not in Path(result["snapshot_path"]).read_text()


@pytest.mark.parametrize("member", ["../escape.csv", "/absolute.csv", "a\\b.csv", "C:/file.csv"])
def test_archive_validates_all_members_before_writing(tmp_path, member):
    archive = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("good.csv", "data")
        handle.writestr(member, "bad")
    destination = tmp_path / "data"
    destination.mkdir()
    with pytest.raises(ValueError):
        kaggle.extract_archive(archive, destination)
    assert not list(destination.iterdir())


def test_archive_rejects_symlinks_and_preserves_existing_files(tmp_path):
    destination = tmp_path / "data"
    destination.mkdir()
    archive = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        info = zipfile.ZipInfo("link")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        handle.writestr(info, "../target")
    with pytest.raises(ValueError):
        kaggle.extract_archive(archive, destination)
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("existing.csv", "new data")
    (destination / "existing.csv").write_text("important old data")
    with pytest.raises(FileExistsError):
        kaggle.extract_archive(archive, destination)
    assert (destination / "existing.csv").read_text() == "important old data"


def test_archive_honors_extraction_budget_and_extracts_valid_data(monkeypatch, tmp_path):
    archive = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("nested/file.csv", "data")
    destination = tmp_path / "data"
    destination.mkdir()
    monkeypatch.setenv("KAGGLE_MCP_MAX_EXTRACT_BYTES", "1")
    with pytest.raises(ValueError):
        kaggle.extract_archive(archive, destination)
    monkeypatch.setenv("KAGGLE_MCP_MAX_EXTRACT_BYTES", "1000")
    kaggle.extract_archive(archive, destination)
    assert (destination / "nested/file.csv").read_text() == "data"


def test_invalid_dataset_archive_is_a_structured_failure(server, monkeypatch, tmp_path):
    def fake_run(command, **options):
        destination = Path(command[command.index("-p") + 1])
        (destination / "broken.zip").write_text("not a zip")
        return subprocess.CompletedProcess(command, 0, stdout="downloaded", stderr="")

    monkeypatch.setattr(
        kaggle,
        "subprocess",
        types.SimpleNamespace(run=fake_run, TimeoutExpired=subprocess.TimeoutExpired),
    )
    result = server.kaggle_dataset_download("owner/dataset")
    assert not result["ok"] and result["error"]["kind"] == "extraction"


def test_discussion_rejects_cross_competition_ref_and_invalid_sort(server):
    with pytest.raises(ValueError):
        server.kaggle_discussion_get("titanic", "other/123")
    with pytest.raises(ValueError):
        server.kaggle_discussions_list("titanic", sort="votes")
