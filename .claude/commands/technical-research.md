---
description: 業務 PoC / 研究テーマの技術調査を行い、問題設定・候補手法・実装候補・PoC スコープを整理する
allowed-tools: Bash, Read, Write, Edit, WebSearch, WebFetch, mcp__kaggle__kaggle_competitions_list, mcp__kaggle__kaggle_discussions_list, mcp__kaggle__kaggle_discussion_get, mcp__kaggle__kaggle_notebooks_search, mcp__kaggle__kaggle_datasets_list, mcp__arxiv__search_papers, mcp__arxiv__get_abstract, mcp__huggingface__hub_repo_search, mcp__huggingface__paper_search
---

General technical research を実施してください。

技術テーマ: $ARGUMENTS

## 手順

1. `docs/00_project_concept.md`、`AGENTS.md`、`aidlc-docs/` を読んでください。
2. 問題設定、成功条件、制約、利用データ、評価方法を `aidlc-docs/inception/problem-overview.md` に整理してください。
3. Kaggle MCP を使い、技術テーマに近い Competition / Dataset / Notebook / Discussion を検索してください。
   - `kaggle_competitions_list` で関連 competition を探す。
   - 有望な competition は `kaggle_discussions_list` / `kaggle_discussion_get` で手法・CV・失敗例・リーク・LB shakeup を確認する。
   - `kaggle_notebooks_search` で再利用できる実装候補を探す。
   - `kaggle_datasets_list` で関連 dataset を探す。
4. arXiv / Hugging Face / 公式 Docs / GitHub で代表論文と実装を調査してください。
5. Kaggle 由来の知見を論文・公式 Docs・GitHub・Hugging Face と比較し、最良候補と採用しない候補を整理してください。
6. 業務データへの転用可能性・リスク・PoC の最小スコープを整理してください。
7. 以下を作成または更新してください。
   - `aidlc-docs/inception/technical-research.md`
   - `aidlc-docs/inception/risk-assessment.md`
   - `aidlc-docs/construction/implementation-questionnaire.md` (Hydra/loguru/MLflow・adapter 境界を含む)
   - `aidlc-docs/construction/architecture.md`
   - `aidlc-docs/construction/code-generation-plan.md`
8. 取得元、MCP tool、実行コマンド、日時、判断を `aidlc-docs/audit.md` に記録してください。
