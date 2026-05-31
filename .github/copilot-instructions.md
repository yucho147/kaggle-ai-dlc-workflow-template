# GitHub Copilot CLI Instructions

This repository is an AI-DLC style workflow template for Kaggle competitions, winning-solution research, and business PoC / technical research.

## Core Workflow

- Read `docs/00_project_concept.md`, `docs/02_quickstart.md`, and `aidlc-docs/` before starting work.
- Use `uv` for Python and dependency management.
- Run setup with `uv sync`.
- Initialize AI-DLC docs with `uv run scripts/init_aidlc_docs.sh` when needed.
- Do not start implementation until the minimum Inception docs are filled in.
- Record external sources, commands, assumptions, and decisions in `aidlc-docs/audit.md`.
- Record experiment commands and results in `aidlc-docs/operations/experiment-log.md`.

## Skills

Repository skills live under `.agents/skills/`.

- `.agents/skills/kaggle-starter/SKILL.md`
- `.agents/skills/kaggle-winning-research/SKILL.md`
- `.agents/skills/technical-research/SKILL.md`

Use the relevant skill instructions before changing docs or code for that workflow.

## Kaggle

- Run Kaggle CLI through uv: `uv run kaggle ...`.
- Before downloading data, confirm Kaggle API authentication and competition rules.
- Keep downloaded data under `data/raw/` and do not commit data files.
