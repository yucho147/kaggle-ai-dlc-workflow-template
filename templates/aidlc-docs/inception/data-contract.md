# Data Contract

## Version / Availability

- Dataset ID / version / fingerprint: TBD
- Source / local path / source IDs: TBD
- 利用権限・license・持ち出し可否: TBD
- Unit of observation: TBD
- 学習・評価・予測時に利用できる情報: TBD
- Target が確定する時点 / 観測 cutoff: TBD

## Schema

| Field | dtype / unit | 意味 | Null / range | ID / target / group / time / feature |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

- ID の一意性、重複と join cardinality: TBD
- Timestamp の timezone / interval / as-of semantics: TBD
- Train/test の schema 差、未知 category、欠損の扱い: TBD
- Sample size / 全量サイズ / 読込時の resource 見積り: TBD

## Leakage Boundary

- 同一 entity / group / duplicate の split 跨ぎ: TBD
- 未来情報・target 派生・後付け集計・label delay: TBD
- Fold 内で fit する処理: imputation / scaling / encoding / feature selection 等
- Join・外部データの利用可能時点: TBD
- 評価データを使った調整の範囲: TBD

## Output Contract

- 列名・順序・行数・dtype: TBD
- ID 対応 / 行順を検証する方法: TBD
- Label / probability / rank / code 等の予測方式: TBD
- 許容範囲、NaN / inf、正例 label: TBD
- Sample submission / API schema / 業務利用者: TBD

## Checks / Changes

- 小規模チェックと全量チェックの実行コマンド: TBD
- 不一致時の挙動: エラー停止。黙って別データ・別形式に置き換えない。
- 契約変更日時 / 理由 / 影響を受ける実験: TBD
