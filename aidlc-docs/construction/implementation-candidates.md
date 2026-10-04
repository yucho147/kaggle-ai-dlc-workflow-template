# Implementation Candidates

| Candidate | Decision | Reason / evidence |
| --- | --- | --- |
| 既存 Hydra / loguru / MLflow | retained | config、local logs、tracking を一緒に保存 |
| markdown-it-py | adopted | maintained parser を dependency として利用。tables / nested list / links 回帰検証 |
| workflow_tools.kaggle | adopted | MCP と CLI wrapper の構文・timeout・snapshot・展開を共有 |
| 追加の多層 gateway framework | rejected | 現時点の差し替え要求には不要。学習は固定した local data を読む |
| Notebook / columnar の全同梱 | rejected | research / notebooks / columnar groups へ分離 |
| arXiv / Hugging Face server の既定自動起動 | rejected | 案件との関連・版・利用条件を確認して追加 |

外部 Notebook や winning solution code の port は行っていない。
Dependency の配布条件に従い、本文参照とコード移植を区別する手順を skills / seed に明記した。
