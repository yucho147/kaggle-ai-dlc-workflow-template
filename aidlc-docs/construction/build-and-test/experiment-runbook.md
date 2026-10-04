# Experiment Runbook

```bash
uv run --locked --group research --group mcp python -m baseline.train
uv run python scripts/render_improvement_report.py
uv run --group research mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1
```

Artifacts: outputs/runs/<local_run_id>/。Tracking: root 基準の sqlite:///mlruns.db と MLflow artifact store。
今回の成功 run と metric、再試行・未実施項目は operations/experiment-log.md を参照する。
失敗時も local manifest / config / run.log を保全し、別 run directory で再試行する。
