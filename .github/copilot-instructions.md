# GitHub Copilot CLI Instructions

このリポジトリは、Kaggle コンペ、勝ち筋調査、業務 PoC / 技術調査を AI-DLC 風に進めるための workflow template です。

## Core Workflow

- 作業前に `docs/00_project_concept.md`, `docs/02_quickstart.md`, `docs/03_prompt_templates.md`, `aidlc-docs/` を読む。
- Python と依存関係管理には `uv` を使う。
- setup は `uv sync` で行う。
- 必要に応じて `uv run scripts/init_aidlc_docs.sh` で AI-DLC docs を初期化する。
- Inception の最小 docs と Construction の設計 docs が揃うまで実装を始めない。
- 新規コードでは、Hydra / loguru / MLflow を標準にする。
- Kaggle の Competition / Discussion / Notebook / Dataset 取得は MCP / Gateway 境界を優先し、CLI は adapter fallback とする。
- 外部情報源、実行 command、仮定、判断を `aidlc-docs/audit.md` に記録する。
- 実験 command と結果を `aidlc-docs/operations/experiment-log.md` に記録する。
- 継続的な改善サイクルでは、人間の閲覧面は MLflow UI と `outputs/reports/improvement-report.html`、agent の正本は `aidlc-docs/` の Markdown とする。
- 実験結果レビュー、次の仮説選定、採用/不採用判断などを人間に促すときは、`uv run python scripts/render_improvement_report.py` で HTML report を再生成し、Markdown ではなく HTML report と MLflow UI を案内する。

## Skills

Repository skills は `.agents/skills/` 配下にある。

- `.agents/skills/kaggle-starter/SKILL.md`
- `.agents/skills/kaggle-winning-research/SKILL.md`
- `.agents/skills/technical-research/SKILL.md`

workflow に応じた skill instructions を読んでから docs / code を変更する。

## Kaggle

- Kaggle 情報取得は MCP / Gateway 経由を優先する。
- CLI が必要な場合は `uv run kaggle ...` を adapter fallback として使う。
- data download 前に Kaggle API authentication と competition rules を確認する。
- downloaded data は `data/raw/` 配下に置き、data files は commit しない。
