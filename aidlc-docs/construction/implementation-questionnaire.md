# 実装前質問票

このドキュメントは、実装前に coding agent と人間が任意性の高い設計判断を擦り合わせるための質問票である。未回答のまま実装すると密結合になりやすい項目を優先して埋める。

## 必須確認事項

| 質問 | 回答 | 実装前に決めるか |
| --- | --- | --- |
| 何の用途か: Kaggle 提出 / 調査 baseline / 業務 PoC / 再利用ライブラリ | TBD | はい |
| コンペ種別または技術領域は何か: tabular / CV / NLP / recsys / simulation / code competition / other | TBD | はい |
| 実行環境は何か: local / Kaggle Notebook / Colab / cloud VM / CI | TBD | はい |
| Notebook-first / script-first / hybrid のどれで進めるか | TBD | はい |
| Notebook を使う場合も、共通ロジックを `src` から読む運用でよいか | TBD | はい |
| 既存コードを拡張するか、新規構成を作るか | TBD | はい |
| 新規構成の場合、Hydra を使うか | 標準: はい | はい |
| loguru を標準 logger として使うか | 標準: はい | はい |
| MLflow を必須の実験 tracker として使うか | 標準: はい | はい |
| Kaggle 情報取得は MCP / CLI adapter / manual のどれを使うか | 標準: MCP または gateway interface。CLI adapter は fallback | はい |
| validation は何を信頼するか: holdout / KFold / StratifiedKFold / GroupKFold / TimeSeriesSplit / custom CV | TBD | はい |
| submission format と id / target columns は何か | TBD | はい |
| 外部データ、Internet、pretrained model の利用可否 | TBD | はい |

## アーキテクチャ選択

| 選択肢 | 選ぶ場面 | 補足 |
| --- | --- | --- |
| シンプルな layered pipeline | 小規模 tabular baseline、素早い試行 | それでも config / data / features / models / validation / tracking は分離する。 |
| Clean architecture 風 | 複数モデル・複数特徴量・複数 tracker を扱う中規模案件 | data access、tracking、model factory に interface を置く。 |
| Onion architecture | 長く使う PoC や domain ルールが重い案件 | domain ルールを framework や I/O から独立させる。 |
| Notebook wrapper | Notebook 管理を重視する場合 | Notebook は共有 `src` を呼び出す。core logic を Notebook だけに閉じ込めない。 |
| コンペ特化 engine | CV / NLP / simulation / code competition | `datasets`、`trainer`、`environment`、`agents` などの domain module を使う。 |

選択: TBD

理由: TBD

## 標準方針

ユーザーが明示的に別方針を指定せず、既存コードの制約もない場合は以下を標準とする。

- 設定管理: config group を使った Hydra。
- Logging: loguru。
- 実験管理: MLflow。Kaggle 提出に必要な artifact は `outputs/<experiment_id>/` にも保存する。
- Package layout: 非自明な実験では flat な `src/train.py` ではなく `src/<package_name>/...`。
- Notebook: EDA と reporting を主用途にし、共有関数・クラスは `src` から import する。
- Data access: `KaggleGateway` interface を置く。MCP adapter を優先し、CLI adapter を fallback にする。
- Training entrypoint: data loading、feature building、model creation、validation、tracking、submission formatting に委譲する薄い orchestration layer にする。

## audit に記録する判断

- 明示確認なしで標準方針を採用した項目。
- Hydra / loguru / MLflow から外れる理由。
- MCP / gateway abstraction ではなく Kaggle CLI を直接使う理由。
- Notebook だけに logic を置く理由。
- validation の妥協や既知の leakage risk。
