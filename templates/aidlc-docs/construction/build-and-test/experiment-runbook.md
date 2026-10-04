# Experiment Runbook

## Before

- [ ] 依頼範囲、予算、仮説、stop condition を確認
- [ ] Data / split / config / hardware を確認
- [ ] Run ごとの出力先と tracking URI を確認
- [ ] 実行時間を見積り、小規模実行を完了

## Run / Stop / Resume

- Command / config override: TBD
- 時間・メモリ・費用の監視方法: TBD
- Stop command / checkpoint / failed artifact の保存: TBD
- 再開 command と上書きの扱い: TBD

## After

- [ ] Exit status / duration / run ID / resolved config を記録
- [ ] Metrics / OOF / model / 出力 / manifest を保存
- [ ] 失敗・未実施も experiment-log に記録
- [ ] 結果に合わせ experiment-plan / tracking / lessons を更新
- [ ] HTML report を生成
