---
name: kaggle-winning-research
description: Use when researching a Kaggle competition discussions, notebooks, writeups, and reusable implementations to extract winning strategies, CV design, features, models, ensembles, external data, leakage risks, LB shakeup risks, failed approaches, and prioritized experiment ideas.
metadata:
  short-description: Research Kaggle winning strategies
---

# kaggle-winning-research

Kaggle Discussion / Notebook / Writeup から勝ち筋、注意点、実装候補を抽出するための skill です。

## 入力

- Kaggle competition slug
- 任意: 調査対象トピック数、Notebook 数、重視観点

## 手順

1. `docs/00_project_concept.md` と `AGENTS.md` を読む。
2. `aidlc-docs/` がなければ `scripts/init_aidlc_docs.sh` を実行する。
3. Discussion topics を `recent` / `hot` / `votes` / `comments` の観点で取得する。
4. 重要トピックの本文とコメントツリーを読む。
5. Notebook / Writeup / GitHub 実装を検索する。
6. 知見を以下に分類する。
   - CV
   - Feature Engineering
   - Model
   - Loss / Metric
   - Ensemble
   - External Data
   - Data Leakage
   - LB shakeup
   - Inference
   - Runtime / Memory
   - Failed approaches
   - Reusable ideas
7. 最初に試す実験候補を優先順位付きで整理する。

## 出力

- `aidlc-docs/inception/winning-research.md`
- `aidlc-docs/inception/risk-assessment.md`
- `aidlc-docs/inception/strategy.md`
- `aidlc-docs/construction/implementation-candidates.md`
- `aidlc-docs/construction/experiment-plan.md`

## 完了条件

- 重要 Discussion が整理されている。
- 有力 Notebook / Writeup が整理されている。
- 勝ち筋の候補がある。
- リスクと禁止事項が整理されている。
- 最初の実験計画がある。

