# Evaluation Contract

## Metric

| Metric | 定義 / implementation | Direction | 予測方式 | 集約 / 単位 |
| --- | --- | --- | --- | --- |
| primary | TBD | maximize / minimize | label / probability 等 | fold / pooled / weighted |
| secondary | TBD | TBD | TBD | TBD |

- Kaggle 公式 metric と local implementation の対応: TBD
- sklearn negative scorer 等の符号と表示値: TBD
- Positive label / multiclass order / threshold の決め方: TBD

## Protocol

- 評価の単位 / 対象母集団: TBD
- Split: holdout / stratified / group / time / custom
- Group / time key、gap・purge、label 到着時点: TBD
- Train / validation / test の件数と overlap check: TBD
- Split の保存先 / fingerprint / seed: TBD
- Preprocessing・feature selection・early stopping・calibration の fit 範囲: TBD
- OOF prediction の行対応・fold ID の保存: TBD
- 最終 holdout の固定方法 / アクセスを許すタイミング: TBD

## Comparison / Uncertainty

- 比較 baseline / 同一条件: TBD
- 最小の改善幅 / fold・seed のばらつき / paired comparison: TBD
- Slice（rare group / 時間 / domain 等）の評価: TBD
- Public LB の使用回数・限界: TBD
- 異なる metric / split / dataset の score を直接比較しないための識別子: TBD

## Business / PoC

- 誤検知・見逃し等の業務コスト、現行手法との差: TBD
- Quality / latency / memory / cost の許容値: TBD
- Go / iterate / no-go の閾値と判断者: TBD
- LLM judge を使う場合: judge revision / prompt / human calibration / contamination checks
- Simulation の場合: opponent set / episode seeds / pairings / confidence

## Ready Criteria

- [ ] 予測と target の対応・score 計算を例で確認
- [ ] Split の根拠と leakage 境界を記録
- [ ] 評価データと比較条件を固定
- [ ] 採否の基準と限界を記録
