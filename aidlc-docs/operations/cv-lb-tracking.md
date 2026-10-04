# CV / LB Tracking

今回の smoke は synthetic 環境確認。Leaderboard と業務評価は該当しない。

| Run | Data / split | Metric | CV mean / std | Public / Private LB | Interpretation |
| --- | --- | --- | --- | --- | --- |
| 2306cd91e5424639b9a4ba8358e39215 | synthetic 1,000 rows / seed42 / stratified5 | accuracy、maximize | RF 0.8900 / 0.02627、dummy 0.5000 / 0.0000 | N/A | 評価・比較・保存の配線確認。コンペ性能の主張ではない |

Data / split fingerprint と fold 別 score は experiment-log と run manifest を参照する。
別の data・split・metric の結果とは直接比較しない。
