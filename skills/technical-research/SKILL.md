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
2. `aidlc-docs/` がなければ `scripts/init_aidlc_docs.sh` を実行する。
3. 問題設定、成功条件、制約を明確化する。
4. 既存手法、代表論文、公式 Docs を調査する。
5. Kaggle Dataset / Notebook / Discussion を必要に応じて調査する。
6. GitHub 実装、Hugging Face model / dataset、Papers with Code を確認する。
7. 業務データへの転用可能性、リスク、PoC の最小スコープを整理する。
8. 実装候補と baseline 方針を作る。

## 出力

- `aidlc-docs/inception/technical-research.md`
- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/inception/risk-assessment.md`
- `aidlc-docs/construction/architecture.md`
- `aidlc-docs/construction/code-generation-plan.md`

## 完了条件

- 技術テーマが整理されている。
- 候補手法が比較されている。
- 実装候補が特定されている。
- PoC の最小スコープが定義されている。
- baseline 実装計画がある。

