# Architecture

## Overview

TBD

このドキュメントは実装開始前に埋める。目的は、coding agent が単一の巨大な `train.py` に処理を集約せず、変更理由ごとに分離された疎結合な構成で baseline を作れる状態にすること。

## 決定サマリー

| 項目 | 決定 | 理由 | 未決定事項 |
| --- | --- | --- | --- |
| コンペ種別 | TBD: tabular / CV / NLP / recsys / simulation / code competition / other | TBD | TBD |
| 実行スタイル | TBD: script-first / notebook-first / hybrid | TBD | TBD |
| アーキテクチャ | TBD: layered / clean-ish / onion / simple pipeline / notebook wrapper | TBD | TBD |
| 設定管理 | 標準: 新規コードは Hydra | 既存コード都合がある場合だけ例外 | TBD |
| Logging | 標準: loguru | 実験コードでは `print` を避ける | TBD |
| 実験管理 | 標準: 新規実験は MLflow 必須 | Kaggle 提出用 artifact は local にも保存する | TBD |
| Kaggle data access | 標準: Kaggle MCP / Gateway 境界。CLI adapter は fallback | business logic から直接 CLI を呼ばない | TBD |
| Notebook 方針 | Notebook は共有 `src` を呼び出してよい。core logic を Notebook だけに置かない | 再現性と再利用性 | TBD |

## Directory Structure

```text
.
├── configs/
│   ├── config.yaml
│   ├── data/
│   ├── model/
│   ├── validation/
│   ├── features/
│   └── tracking/
├── notebooks/                # 必要に応じて作成する EDA / baseline Notebook
├── src/
│   └── <package_name>/
│       ├── app/              # use cases: train, predict, validate, submit
│       ├── domain/           # metric contracts, schemas, competition concepts
│       ├── adapters/         # kaggle, mlflow, filesystem, notebook bridges
│       ├── data/             # loading, splits, dataset objects
│       ├── features/         # feature builders/transforms
│       ├── models/           # model factories/wrappers
│       ├── validation/       # CV/splitters/scoring
│       ├── tracking/         # MLflow/logging helpers
│       └── utils/
├── scripts/                  # thin shell wrappers only
├── outputs/                  # local artifacts, submissions, reports
└── mlruns/ or remote MLflow tracking URI
```

コンペ種別に応じて構成を調整する。

| 種別 | 推奨 module |
| --- | --- |
| Tabular | `data`, `features`, `models`, `validation`, `tracking`, `submission` |
| Computer Vision | `datasets`, `transforms`, `models`, `losses`, `trainer`, `validation`, `inference` |
| NLP / LLM | `datasets`, `tokenization`, `models`, `collators`, `trainer`, `metrics`, `inference` |
| Code competition / simulation | `domain`, `environment`, `agents`, `evaluation`, `submission`, `analysis` |
| Notebook-first | Notebook は orchestration / EDA として使い、共有コードは `src/<package_name>/` に置く |

## Modules

| Module | 責務 |
| --- | --- |
| `app` | train / predict / validate / submit use case を orchestration する。interface と adapter に依存する。 |
| `domain` | target、id、metric、schema、submission contract など安定した概念を定義する。可能な限り pandas / sklearn 固有の orchestration を置かない。 |
| `adapters.kaggle` | MCP または CLI adapter 経由で competition metadata、discussion、notebook、dataset を取得する。 |
| `data` | raw data の読み込み、schema validation、split / dataset 構築を行う。 |
| `features` | deterministic feature transform と feature set registry を持つ。学習を伴う preprocessing は training pipeline の内側に置く。 |
| `models` | model factory / registry。model 追加で training use case を編集しなくて済む構成にする。 |
| `validation` | split strategy、metric calculation、leakage check、CV result serialization を担当する。 |
| `tracking` | MLflow logging、loguru setup、artifact paths、run metadata を担当する。 |
| `submission` | submission file construction と format check を担当する。 |

## Data Flow

```text
Hydra config
  -> app/train.py
  -> adapters/data source
  -> data/schema + split
  -> features/feature set
  -> validation/splitter
  -> models/factory
  -> tracking/mlflow + outputs
  -> submission/format check
```

ルール:

- deterministic feature creation は CV 前に実行してよい。
- learned imputation、scaling、encoding、augmentation statistics、target encoding、tokenizer fitting、model fitting は各 fold の内側で行う。
- `train` は orchestration に徹する。model-specific branching、feature definitions、data download logic、submission formatting details を詰め込まない。

## Configuration

新規コードの標準:

- Hydra entrypoint: `python -m <package_name>.app.train`
- Config groups: `data`, `model`, `features`, `validation`, `tracking`, `runtime`
- CLI override examples:

```bash
uv run --group research python -m <package_name>.app.train \
  experiment=exp001 model=random_forest validation=stratified_kfold
```

argparse は、既存 argparse code を拡張していて移行コストが見合わない場合だけ使う。

## Reproducibility

- Hydra config snapshot を保存する。
- 関連する seed をすべて固定する。
- package versions と git commit を取得できる場合は記録する。
- metrics、parameters、config、model artifacts、predictions、submission files を MLflow に記録する。
- Kaggle 提出しやすいよう、artifact は `outputs/<experiment_id>/` にも保存する。
- command、result、notes を `aidlc-docs/operations/experiment-log.md` に記録する。

## 密結合チェックリスト

- `train.py` を編集せず、file / config 追加で model を追加できるか。
- feature code や model code に触れず validation strategy を変えられるか。
- training logic を変えず、Kaggle access を CLI から MCP に差し替えられるか。
- Notebook と script が同じ feature / model / training function を再利用できるか。
- MLflow / loguru の初期化が boundary で一度だけ行われているか。
- code generation 前に domain decision が文書化されているか。
