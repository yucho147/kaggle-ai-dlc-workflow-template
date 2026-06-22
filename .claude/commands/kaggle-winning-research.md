---
description: Kaggle Discussion / Notebook / Writeup から CV 戦略・特徴量・モデル・失敗例・実装候補を抽出する
allowed-tools: Bash, Read, Write, Edit, mcp__kaggle__kaggle_discussions_list, mcp__kaggle__kaggle_discussion_get, mcp__kaggle__kaggle_notebooks_search, mcp__kaggle__kaggle_notebook_pull
---

Kaggle winning research を実施してください。

対象コンペ: $ARGUMENTS

## 手順

1. `docs/00_project_concept.md`、`AGENTS.md`、`aidlc-docs/` を読んでください。
2. Discussion topics を MCP 優先で取得してください。
   - MCP: `kaggle_discussions_list(competition=<slug>, sort="hot")` で重要トピックを取得する。
   - MCP: `kaggle_discussions_list(competition=<slug>, sort="votes")` でも補完する。
   - MCP: `kaggle_discussion_get` で重要トピックの本文とコメントツリーを読む。
3. Notebook / GitHub 実装を検索してください。
   - MCP: `kaggle_notebooks_search(query=<theme>, competition=<slug>)` で実装候補を取得する。
4. 知見を以下に分類して `aidlc-docs/inception/winning-research.md` に要約してください。
   - CV / Feature Engineering / Model / Loss・Metric / Ensemble / External Data
   - Data Leakage / LB shakeup / Inference / Runtime・Memory / Failed approaches / Reusable ideas
5. Notebook や GitHub 実装を移植候補にする場合は、ライセンス・依存ライブラリ・前提データ構造・移植 module を確認してください。
6. 以下を作成または更新してください。
   - `aidlc-docs/inception/risk-assessment.md`
   - `aidlc-docs/inception/strategy.md`
   - `aidlc-docs/construction/implementation-candidates.md`
   - `aidlc-docs/construction/implementation-questionnaire.md`
   - `aidlc-docs/construction/architecture.md`
   - `aidlc-docs/construction/experiment-plan.md`
7. 取得元、実行コマンド、日時、判断を `aidlc-docs/audit.md` に記録してください。
