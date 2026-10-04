---
name: improvement-review
description: Prepare a Kaggle or PoC experiment review by comparing compatible runs, updating evidence and prioritized next hypotheses, then regenerating the HTML report and pointing to MLflow when available.
metadata:
  short-description: Prepare experiment review
---

# Improvement Review

Read AGENTS.md, current state, experiment plan/log, evaluation contract, tracking and lessons.
For a PoC also read poc-decision.md.

## Prepare Before Presenting

1. Confirm each run's data/split/metric, MLflow or local run ID and actual artifacts. Separate failed, unperformed and completed work.
2. Compare compatible runs, baseline deltas, fold/seed variability, slices, runtime/cost and inference constraints. State what remains unverified.
3. Update the experiment facts, interpretations, risks and candidate hypotheses. Give each next candidate evidence, priority, a minimum check, cost and a rejection/stop criterion.
4. Record only actual adoption decisions; human review is not complete merely because the report was generated.
5. Regenerate with uv run python scripts/render_improvement_report.py after all source edits.
6. Present outputs/reports/improvement-report.html as the primary reading surface and MLflow UI when available, using the same backend URI. If tracking is unavailable, identify local artifacts and the limitation.

Completion means the report is current and the requested decisions are concrete and reviewable. Do not launch new expensive experiments or external submissions just to prepare a review.
