---
name: technical-research
description: Use when conducting general technical research for a business PoC, research theme, or non-Kaggle technical investigation, and you need to organize the problem setting, existing methods, papers, official docs, GitHub implementations, Kaggle references, Hugging Face resources, applicability risks, PoC scope, and baseline implementation plan.
metadata:
  short-description: Plan technical research and PoC
---

# technical-research

Kaggle 以外も含めた技術調査を行い、業務 PoC / 研究テーマを baseline 実装に入れる状態へ整理する skill です。

## 入力

- 技術テーマ
- 任意: 業務データの前提、利用可能な情報源、実行環境、制約

## 手順

1. `docs/00_project_concept.md` と `AGENTS.md` を読む。
2. `aidlc-docs/` がなければ `uv run scripts/init_aidlc_docs.sh` を実行する。
3. 問題設定、成功条件、制約を明確化する。
4. 既存手法、代表論文、公式 Docs を調査する。
5. Kaggle MCP を使い、技術テーマに近い Competition / Dataset / Notebook / Discussion を検索する。
   - `kaggle_competitions_list` で関連 competition を探す。
   - 有望な competition は `kaggle_discussions_list` / `kaggle_discussion_get` で手法、CV、失敗例、リーク、LB shakeup を確認する。
   - `kaggle_notebooks_search` で再利用できる実装候補を探す。
   - `kaggle_datasets_list` で関連 dataset を探す。
6. Kaggle 由来の知見を、論文・公式 Docs・GitHub・Hugging Face と比較し、PoC に使う最良候補を整理する。
7. GitHub 実装、Hugging Face model / dataset、Papers with Code を確認する。
8. 業務データへの転用可能性、リスク、PoC の最小スコープを整理する。
9. 実装前に `aidlc-docs/construction/implementation-questionnaire.md` を埋め、アーキテクチャを対話で決める。
   - layered / clean-ish / onion / notebook wrapper / domain-specific engine
   - Hydra / loguru / MLflow を標準採用するか
   - external service / dataset access を adapter または MCP 境界に分離するか
10. 実装候補と baseline 方針を作る。

## 出力

- `aidlc-docs/inception/technical-research.md`
- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/inception/risk-assessment.md`
- `aidlc-docs/construction/implementation-questionnaire.md`
- `aidlc-docs/construction/architecture.md`
- `aidlc-docs/construction/code-generation-plan.md`

## 完了条件

- 技術テーマが整理されている。
- 候補手法が比較されている。
- Kaggle Competition / Discussion / Notebook / Dataset 由来の再利用可能な知見が整理されている。
- 実装候補が特定されている。
- PoC の最小スコープが定義されている。
- baseline 実装計画がある。
