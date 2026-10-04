# PoC Decision

## Applicability

Status: not-applicable。今回、業務 PoC の採否判断は行っていない。
改訂した seed は、現行手法との品質・latency・費用比較、go / iterate / no-go の閾値、判断者、引継ぎを記録するためのもの。

## Template Handoff

- 改訂コード・config・lockfile・空の seed・4 skills・CI を同じ repository に保存。
- 検証と限界は experiment-log、変更理由と移行手順は technical-research と共通 docs に記録。
- 新規案件: `uv sync --locked` → `uv run scripts/init_aidlc_docs.sh --new-project`。
- 既存案件: 記録を保全し、引数なしで欠落補充。data / evaluation contract を記入してから実装変更。
- Backup、data、run、MLflow DB / artifact store、生成 HTML は local artifacts。必要なものは案件の保存方針で別途保全する。
- 各 client の trust / auth、対象の規約・実データ評価は次の案件で確認する。
