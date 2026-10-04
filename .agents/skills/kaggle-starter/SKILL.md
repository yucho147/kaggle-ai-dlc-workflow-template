---
name: kaggle-starter
description: Prepare a Kaggle competition by verifying rules, data, evaluation and submission contracts, and a first baseline plan. Use for participation setup; stop at research when implementation is not requested.
metadata:
  short-description: Prepare Kaggle participation
---

# Kaggle Starter

Read AGENTS.md, docs/00_project_concept.md and the current AI-DLC state.
Infer the requested arrival point and existing decisions before asking questions.

## Workflow

1. Confirm the exact competition slug and phase. Read official overview, evaluation and rules bodies. The overview MCP tool provides discovery metadata and URLs only.
2. Use available MCP / CLI / Web paths. With the bundled MCP, call kaggle_cli_version first. For CLI fallback, inspect version, help and uncertain subcommand flags.
3. Inspect file sizes and choose a bounded sample or necessary files before downloading. Record missing access, rule acceptance, and incomplete pagination.
4. Describe observation unit, target, IDs, groups, time and information available at prediction time in data-contract.md. Verify sample submission or code evaluation API.
5. Define metric, prediction type, aggregation, split rationale and fold fit boundaries in evaluation-contract.md. Include group/time/duplicate leakage relevant to this competition.
6. Record short source summaries, revisions and confidence in source-register.md; record retrieval commands and assumptions in audit.md.
7. Select a simple comparison baseline and first experiment with cost and stop conditions. Update kaggle-starter.md and experiment-plan.md.
8. If implementation is requested, complete the relevant questionnaire, architecture and generation plan before code. Existing accepted decisions do not require new approval.

## Completion

Research is complete when the competition, constraints, contracts, unknowns and first experiment are reviewable. A blocked download can be documented without inventing schema or results.
Regenerate the HTML report. Update state with the next concrete action.
