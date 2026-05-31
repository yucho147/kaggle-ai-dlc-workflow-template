# Code Generation Plan

この計画は `implementation-questionnaire.md` と `architecture.md` を埋めた後に作る。目的は一回限りの巨大な baseline script ではなく、拡張しやすく、検証しやすいコードを生成することである。

## Scope

TBD

## 設計入力

| 入力 | 参照先 | 状態 |
| --- | --- | --- |
| 問題設定 | `aidlc-docs/inception/problem-overview.md` | TBD |
| 実装前質問票 | `aidlc-docs/construction/implementation-questionnaire.md` | TBD |
| アーキテクチャ | `aidlc-docs/construction/architecture.md` | TBD |
| 実験計画 | `aidlc-docs/construction/experiment-plan.md` | TBD |
| Kaggle data access | `aidlc-docs/construction/kaggle-data-access.md` | TBD |

## 標準実装方針

- 新規構成では Hydra で設定と command override を管理する。
- 実行ログは loguru を使う。
- 実験管理は MLflow を使う。Kaggle 提出に必要な artifact は `outputs/<experiment_id>/` にも保存する。
- entrypoint は薄く保ち、再利用ロジックは `src/<package_name>/` 配下に置く。
- Notebook は共有コードの利用者にする。core logic の唯一の置き場にしない。
- Kaggle へのアクセスは gateway / adapter 境界を通す。training module や feature module に Kaggle CLI 呼び出しを埋め込まない。
- model、feature set、validation strategy、metric、data access adapter が複数になりうる場合は registry / factory を優先する。

## Files To Create / Modify

| File | Purpose |
| --- | --- |
| `configs/config.yaml` | Hydra root config and defaults |
| `configs/data/*.yaml` | Data source and schema settings |
| `configs/model/*.yaml` | Model family and hyperparameters |
| `configs/features/*.yaml` | Feature set selection |
| `configs/validation/*.yaml` | CV/split/metric settings |
| `configs/tracking/*.yaml` | MLflow/loguru/output settings |
| `src/<package_name>/app/train.py` | Training use case entrypoint |
| `src/<package_name>/app/predict.py` | Inference/submission entrypoint if needed |
| `src/<package_name>/adapters/kaggle.py` | Kaggle gateway implementations |
| `src/<package_name>/data/` | Loading, schema checks, split inputs |
| `src/<package_name>/features/` | Feature builders and registries |
| `src/<package_name>/models/` | Model factories/wrappers |
| `src/<package_name>/validation/` | Splitter and scoring logic |
| `src/<package_name>/tracking/` | MLflow and logging setup |
| `src/<package_name>/submission/` | Submission format checks |
| `tools/kaggle-mcp/` | Kaggle MCP server for competition/discussion/notebook/dataset retrieval |
| `tests/` | Unit tests for non-trivial reusable logic |

## Implementation Steps

1. package 構成と Hydra config skeleton を作る。
2. data loading と schema check を実装する。
3. deterministic feature builder と feature registry を実装する。
4. model factory / registry を実装する。
5. validation strategy と metric logging を実装する。
6. MLflow / loguru setup を実装する。
7. 利用可能な MCP / CLI に応じて Kaggle gateway adapter または stub を実装する。
8. train / predict / submit entrypoint を薄い orchestration として実装する。
9. smoke test と leakage check を追加する。
10. baseline を実行し、結果を `aidlc-docs/operations/experiment-log.md` に記録する。

## Interface

| Interface | 責務 | 初期実装 |
| --- | --- | --- |
| `KaggleGateway` | competition metadata、discussion、files、submission 履歴の取得 | MCP adapter 優先。CLI adapter は fallback |
| `DataLoader` | raw / interim data の読み込みと schema validation | TBD |
| `FeatureBuilder` | deterministic feature または fold-safe transform の構築 | TBD |
| `ModelFactory` | config から estimator / model を構築 | TBD |
| `Validator` | CV score と必要に応じた OOF prediction の生成 | TBD |
| `ExperimentTracker` | params、metrics、artifacts の記録 | MLflow |

## Commands

```bash
uv run --group research python -m <package_name>.app.train experiment=exp001
uv run --group research python -m <package_name>.app.predict experiment=exp001
uv run --group research mlflow ui
```

## Tests / Validation

- Config が正しく compose できる。
- Data schema validation が target / id column の欠落を検知できる。
- Feature builder が deterministic で、明示許可なしに full data で fit しない。
- CV split strategy が問題の制約に合っている。
- MLflow run に params、metrics、config、artifacts、submission が記録されている。
- Kaggle submission file が sample submission の columns と row count に一致している。

## Done Criteria

- Hydra config から baseline が end-to-end で動く。
- 実験が MLflow と local `outputs/` の両方に記録されている。
- submission または PoC output が生成されている。
- 実装判断、標準方針の採用、仮定が `aidlc-docs/audit.md` に記録されている。
