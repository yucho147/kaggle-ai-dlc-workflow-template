---
name: kaggle-starter
description: Use when starting a Kaggle competition and you need to organize the competition overview, evaluation metric, data files, target/id/submission format, initial EDA direction, baseline plan, and AI-DLC documents before implementation.
metadata:
  short-description: Start a Kaggle competition
---

# kaggle-starter

Kaggle competition の参加開始時に、データ、評価指標、提出形式、初期 EDA / baseline 方針を整理するための skill です。

## 入力

- Kaggle competition slug
- 任意: 実行環境、GPU 有無、Notebook first / script first の希望、MCP 利用可否

## 手順

1. `docs/00_project_concept.md` と `AGENTS.md` を読む。
2. `aidlc-docs/` がなければ `uv run scripts/init_aidlc_docs.sh` を実行する。
3. Kaggle 情報を MCP 優先で取得する。MCP が使えない場合は CLI adapter fallback を使う。
   - MCP: `kaggle_competition_overview` でコンペ概要を取得する。
   - MCP: `kaggle_competition_files` でデータファイル一覧を取得する。
   - MCP fallback / CLI: `uv run kaggle --version` で CLI の利用可否を確認してから `uv run kaggle competitions files -c <competition>` を使う。
4. データを `data/raw/<competition>/` に取得する。
   - MCP: `kaggle_competition_download` でダウンロードを試みる。
   - MCP fallback / CLI: `uv run scripts/download_kaggle_competition.sh <competition>`
5. `train` / `test` / `sample_submission` の構造を確認する。
6. 評価指標、target、id column、submission columns を特定する。
7. 欠損、型、サイズ、分布、リーク可能性を確認する。
8. 最初の baseline 方針と validation 方針を作る。
9. 実装前に `aidlc-docs/construction/implementation-questionnaire.md` を埋める。
    - コード構成: layered / clean-ish / onion / notebook wrapper / competition-specific engine
    - 実行方針: script-first / notebook-first / hybrid
    - 設定管理: 新規コードは Hydra を標準
    - logging: loguru を標準
    - 実験管理: MLflow を標準
    - Kaggle access: MCP / Gateway 境界を標準、CLI は adapter fallback
10. `aidlc-docs/construction/architecture.md` と `code-generation-plan.md` に疎結合な構成案を作る。
11. 判断、仮定、外部情報源を `aidlc-docs/audit.md` に記録する。

## 出力

- `aidlc-docs/inception/kaggle-starter.md`
- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/construction/implementation-questionnaire.md`
- `aidlc-docs/construction/architecture.md`
- `aidlc-docs/construction/kaggle-data-access.md`
- `aidlc-docs/construction/experiment-plan.md`
- 必要に応じて `notebooks/00_eda.ipynb` / `notebooks/01_baseline.ipynb` の作成計画

## 完了条件

- コンペ概要が整理されている。
- 評価指標が説明されている。
- データファイルと主要カラムが把握されている。
- `sample_submission` と同形式の提出ファイルを作る方針がある。
- 最初に作る baseline と validation 方法が決まっている。
- 実装前質問票でコード構成、Hydra / loguru / MLflow、Kaggle MCP / adapter 方針が確認されている。
