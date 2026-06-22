---
description: Kaggle コンペ参加開始時に概要・データ・評価指標・baseline 方針を aidlc-docs/ に整理する
allowed-tools: Bash, Read, Write, Edit, mcp__kaggle__kaggle_competition_overview, mcp__kaggle__kaggle_competition_files, mcp__kaggle__kaggle_competition_download, mcp__kaggle__kaggle_discussions_list, mcp__kaggle__kaggle_notebooks_search
---

Kaggle competition starter を実施してください。

対象コンペ: $ARGUMENTS

## 手順

1. `docs/00_project_concept.md`、`AGENTS.md`、`aidlc-docs/` を読んでください。
2. Kaggle 情報取得は MCP 優先で行ってください。MCP がない場合のみ CLI adapter fallback を使い、実行前に `uv run kaggle --version` を確認してください。
   - MCP: `kaggle_competition_overview` でコンペ概要を取得する。
   - MCP: `kaggle_competition_files` でデータファイル一覧を取得する。
   - MCP fallback: `uv run scripts/download_kaggle_competition.sh <competition>` でデータを取得する。
3. `train` / `test` / `sample_submission` の構造、評価指標、target、id column、submission columns を特定してください。
4. 欠損・型・サイズ・分布・リーク可能性を確認してください。
5. 以下のドキュメントを作成または更新してください。
   - `aidlc-docs/inception/problem-overview.md`
   - `aidlc-docs/inception/kaggle-starter.md`
   - `aidlc-docs/construction/implementation-questionnaire.md` (コード構成・Hydra/loguru/MLflow・MCP/adapter 方針を含む)
   - `aidlc-docs/construction/architecture.md`
   - `aidlc-docs/construction/kaggle-data-access.md`
   - `aidlc-docs/construction/experiment-plan.md`
6. 取得元、実行コマンド、日時、判断を `aidlc-docs/audit.md` に記録してください。

実装は、上記ドキュメントの骨子が揃ってから開始してください。
