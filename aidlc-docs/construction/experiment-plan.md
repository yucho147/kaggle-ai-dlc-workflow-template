# Experiment Plan

## Objective

TBD

## Baseline

- Model:
- Features:
- Validation:
- Metric:

## Experiments

| ID | Status | Priority | Hypothesis | Change | Expected Impact | Evidence | Stop Condition | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exp001 | idea | P1 | TBD | TBD | TBD | TBD | TBD | TBD |

Status values:

- `idea`: human idea, not selected yet.
- `selected`: human selected this idea for the next loop.
- `specced`: implementation scope is written in `code-generation-plan.md`.
- `implemented`: code/config changes are ready.
- `executed`: run completed and `experiment-log.md` is updated.
- `reviewed`: human reviewed MLflow UI and HTML report.
- `adopted` / `rejected` / `iterate`: final decision for the loop.

## Validation

- Split:
- Leakage checks:
- Seed:
- Reproducibility:

## Commands

```bash
TBD
```

## Human Review Surface

- MLflow UI: compare runs, params, metrics, artifacts.
- HTML report: `outputs/reports/improvement-report.html`.
- Generate HTML with `uv run python scripts/render_improvement_report.py`.

## Done Criteria

- Baseline runs end-to-end.
- Metric is recorded.
- Submission or PoC output can be generated.
