# Validation Instructions

付属 baseline の評価契約は inception/evaluation-contract.md に記録。

- 同一 fold の dummy と candidate を比較する。
- 前処理は train fold に fit し、OOF に validation の行対応と fold ID を保存する。
- CSV 欠落、列・ID・target、提出 probability と sample alignment を検査する。
- Local manifest / config / fingerprints / model と MLflow artifact を確認する。
- 合成データ結果を実データ性能と扱わない。Group / time / 業務 slice 等は案件側で設計する。
