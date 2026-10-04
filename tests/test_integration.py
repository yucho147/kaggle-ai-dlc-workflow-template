import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import mlflow
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from scripts.check_template import check
from scripts.init_aidlc_docs import initialize

ROOT = Path(__file__).resolve().parents[1]


def test_derived_project_can_edit_records_and_pass_validation(tmp_path):
    for source in ROOT.iterdir():
        if source.name in {
            "README.md",
            "AGENTS.md",
            "CLAUDE.md",
            "COPILOT.md",
            ".mcp.json",
            ".agents",
            ".codex",
            ".claude",
            ".kiro",
            "docs",
            "templates",
            "tools",
        }:
            if source.is_dir():
                shutil.copytree(
                    source,
                    tmp_path / source.name,
                    symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__"),
                )
            else:
                shutil.copy2(source, tmp_path / source.name)
    target = tmp_path / "aidlc-docs"
    initialize(tmp_path / "templates/aidlc-docs", target)
    (target / "audit.md").write_text("# Audit\n\nMy actual project decisions.")
    (target / "inception/problem-overview.md").write_text("# Problem\n\nMy real use case.")
    assert initialize(tmp_path / "templates/aidlc-docs", target, check=True)[0] == 0
    assert check(tmp_path) == []


def test_mcp_initializes_lists_tools_and_calls_version(tmp_path):
    fake_cli = tmp_path / "fake_cli.py"
    fake_cli.write_text("import sys\nprint('fixture CLI: ' + ' '.join(sys.argv[1:]))\n")
    env = {
        **os.environ,
        "KAGGLE_MCP_CACHE_DIR": str(tmp_path / "cache"),
        "KAGGLE_MCP_KAGGLE_CMD": f'{sys.executable} "{fake_cli}"',
    }

    async def session():
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[str(ROOT / "tools/kaggle-mcp/server.py")],
            cwd=str(ROOT),
            env=env,
        )
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as client:
                initialized = await client.initialize()
                assert initialized.serverInfo.name == "kaggle-mcp"
                listing = await client.list_tools()
                tools = {tool.name: tool for tool in listing.tools}
                assert len(tools) == 12
                assert tools["kaggle_competition_files"].annotations.readOnlyHint
                assert not tools["kaggle_competition_download"].annotations.readOnlyHint
                result = await client.call_tool("kaggle_cli_version", {})
                assert not result.isError
                payload = json.loads(result.content[0].text)
                assert payload["ok"]
                assert Path(payload["version"]["snapshot_path"]).is_file()

    asyncio.run(session())


def test_synthetic_baseline_runs_and_records_reproducible_artifacts(tmp_path):
    output = tmp_path / "runs"
    tracking = tmp_path / "tracking.db"
    command = [
        sys.executable,
        "-m",
        "baseline.train",
        "data.synthetic_samples=80",
        "validation.n_splits=3",
        "model.params.n_estimators=3",
        f"output.dir={output}",
        f"mlflow.tracking_uri=sqlite:///{tracking}",
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    directories = list(output.iterdir())
    assert len(directories) == 1
    run = directories[0]
    manifest = json.loads((run / "manifest.json").read_text())
    metrics = json.loads((run / "metrics.json").read_text())
    oof = pd.read_csv(run / "oof.csv")
    assert manifest["status"] == "succeeded"
    assert manifest["mlflow_run_id"] and manifest["data"]["mode"] == "synthetic"
    assert len(manifest["data"]["sha256"]) == 64 and len(manifest["split_sha256"]) == 64
    assert manifest["duration_seconds"] > 0
    assert len(metrics["fold_scores"]) == 3 and "dummy_mean" in metrics
    assert len(oof) == 80 and oof["row_id"].is_unique and oof["prediction"].notna().all()
    assert sorted(oof["fold_id"].unique()) == [0, 1, 2]
    assert (run / "config.yaml").is_file() and (run / "model.joblib").is_file()
    assert not (run / "submission.csv").exists()
    assert not (ROOT / "train.log").exists()
    original_uri = mlflow.get_tracking_uri()
    try:
        # models:/ resolution uses MLflow's active tracking URI.
        mlflow.set_tracking_uri(manifest["mlflow_uri"])
        model_path = Path(
            mlflow.artifacts.download_artifacts(
                artifact_uri=manifest["mlflow_model_uri"],
                dst_path=str(tmp_path / "downloaded-model"),
            )
        )
    finally:
        mlflow.set_tracking_uri(original_uri)
    requirements = (model_path / "requirements.txt").read_text()
    assert "scikit-learn==" in requirements and "pandas==" in requirements
    artifact_manifest = Path(
        mlflow.artifacts.download_artifacts(
            run_id=manifest["mlflow_run_id"],
            artifact_path="local_run/manifest.json",
            tracking_uri=manifest["mlflow_uri"],
            dst_path=str(tmp_path / "downloaded-run"),
        )
    )
    assert json.loads(artifact_manifest.read_text()) == manifest
