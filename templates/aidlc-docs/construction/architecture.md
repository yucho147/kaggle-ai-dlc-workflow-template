# Architecture

## Decision

- 対象・最初の変更: TBD
- 構成と採用理由: TBD
- 既存コードから変更する境界: TBD

小規模 baseline はこの構成から始め、変更理由が増えたら分割する。

```text
configs/                 # Hydra config
src/<package_name>/
  data.py                # schema / loading
  model.py               # preprocessing pipeline / model
  evaluate.py            # split / metric / predictions
  tracking.py            # reproducibility / tracker
  train.py               # thin orchestration
tests/                   # contracts with meaningful failure cases
outputs/runs/<run_id>/    # immutable run artifacts
```

CV / NLP / forecasting / simulation 等では domain に応じて dataset / trainer / environment を追加する。
全案件に layered / onion / registry / gateway を要求しない。

## Interfaces / Data Flow

| Boundary | Input | Output | Failure behavior |
| --- | --- | --- | --- |
| Data | version / schema | features / target / ID | 不整合で停止 |
| Evaluation | split / model / scorer | OOF / metrics / split evidence | leakage・非有限値を検出 |
| Tracking | config / manifest / artifacts | run ID / local paths | offline 方針を明示 |
| Output | predictions / IDs | submission / PoC output | 契約違反で停止 |

- データ取得は学習と別工程。学習は固定済み local data から再実行可能にする。
- Fit が必要な処理は fold 内に置く。推論時に target が必要な特徴は使わない。
- Notebook は共有 package を呼び出す。
- 依存性の抽象化は実際に交換する境界に設ける。

## Configuration / Reproducibility

- Config / command / entrypoint: TBD
- Dataset / split / source revisions: TBD
- Seeds / library versions / git commit + dirty state: TBD
- Run ID、local artifact、MLflow URI の対応: TBD
- Remote / offline / Kaggle への package と config の持ち込み方: TBD

## Extension / Limits

- 次に model / split / feature を変える場所: TBD
- 今回対応しない task・data shape: TBD
- 移行・破壊的変更 / 復旧方法: TBD
