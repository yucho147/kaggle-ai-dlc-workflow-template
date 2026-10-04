# Reusable Patterns

| Pattern | Implementation | Preconditions / limits |
| --- | --- | --- |
| Seed を破壊しない missing-only 初期化 | scripts/init_aidlc_docs.py | reset は先に backup。保存先の保全は案件で決める |
| CLI 境界と完全 snapshot | src/workflow_tools/kaggle.py | subprocess を shell なしで実行、response を制限、cache は正本ではない |
| Fold 内の numeric / categorical preprocessing | src/baseline/model.py | CSV classification。利用可能時点・除外特徴は案件で確定 |
| 同一 split の dummy 比較と OOF | src/baseline/evaluate.py | stratified / kfold。group / time は追加実装 |
| ID で提出整列 | src/baseline/data.py | sample / test の一意 ID と1予測列 |
| Local manifest と MLflow | src/baseline/tracking.py / train.py | root 基準 URI、config / environment / data / split / run ID を保全 |
| Markdown 正本から report 生成 | scripts/render_improvement_report.py | raw HTML を無効化。HTML は直接編集しない |

外部 Notebook の移植はない。新しい候補実装を再利用するときは license、revision、依存、データと評価の前提を確認する。
