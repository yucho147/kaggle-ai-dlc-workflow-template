# Evaluation Contract

## Template Acceptance

1. 初期化で既存記録を保全し、記入済みの派生案件が構造検査を通る。
2. 取得境界は actual CLI parser に整合し、失敗・timeout・未取得・切り詰めを明示する。
3. Baseline の前処理・OOF・データ欠落・提出 ID・artifact 対応を検証する。
4. Skills / settings / links / HTML の整合を確認し、再実行方法と限界を残す。

回帰検証・lint・構造検査・local smoke を使う。速度や synthetic score の向上は採用条件ではない。

## Synthetic Baseline Protocol

| Field | Definition |
| --- | --- |
| Metric / direction | sklearn accuracy、maximize |
| Prediction | class label。Scorer と submission mode は設定上区別する |
| Aggregation | unweighted fold mean、population std（ddof=0） |
| Split | stratified 5-fold、shuffle=true、seed=42、各 train 800 / validation 200 rows |
| Candidate | random forest、50 trees、n_jobs=1、random_state=42 |
| Comparator | DummyClassifier most_frequent、同一 fold |
| Fit boundary | imputation / encoding / model は fold 内。最後に全 train で fit して保存 |
| Evidence | 1行につき1つの OOF、fold ID、data / split SHA256、resolved config、manifest、MLflow run |
| Submission / leaderboard | 該当しない |

Split fingerprint: `d415982608d84a14922ce9a6ab49dff9d07de76b19fd580409a6cb1f3c4afd34`。
Binary probability、正例 label、negative scorer 等に変更する場合は、metric の定義・class order・表示値を案件側で固定する。

## Limits

- Holdout・Public LB・実データ・業務 slice・費用対効果の評価は実施していない。
- 単一 seed の synthetic 結果は分類例の配線確認であり、汎化や勝ち筋の根拠ではない。
- macOS / Python 3.13.5 で確認。GitHub-hosted Linux CI と各 client の trust / auth は未検証。
