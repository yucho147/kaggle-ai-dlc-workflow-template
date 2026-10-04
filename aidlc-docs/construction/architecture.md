# Architecture

## 今回の改訂

template-maintenance / 2026-10-04。実装前の方針は audit に記録済み。

| Boundary | Implementation | Contract |
| --- | --- | --- |
| Seed / records | templates/aidlc-docs と aidlc-docs | 内容の完全一致を要求しない |
| Initialization | scripts/init_aidlc_docs.py + shell | 欠落補充、check、backup 付き reset |
| Kaggle CLI | src/workflow_tools/kaggle.py | positional 構文、bounded response、snapshot、timeout |
| MCP tools | tools/kaggle-mcp/server.py | input / output / annotations、未取得本文を区別 |
| Baseline | src/baseline の5 modules | explicit data mode、fold 内 fit、OOF、ID 整列 |
| Tracking | local run directory + MLflow | config、data / split fingerprint、git / versions、failed evidence |
| Report | markdown-it-py + local CSS | raw HTML を無効化、tables / links、standalone HTML |
| Validation | scripts/check_template.py + tests / CI | derived docs の編集と実行契約を検証 |

## Standard / Exceptions

- 実験は Hydra / loguru / MLflow。保守用 CLI は stdlib argparse。
- Notebook / plotting / columnar を optional dependency groups に分離。
- Default MCP は Kaggle。論文・モデル source は案件に応じて追加する。
- Shared commands は skill を読み、独立した重複ルールを持たない。
- 大きな gateway framework や全案件共通の layered architecture を作らない。

## Limits

付属 baseline は小規模 CSV 分類、stratified / kfold、1予測列の例。
Group / time / simulation / LLM の評価は案件契約を決めて実装する。
External API 成功、全 client の trust・認証・UI 動作はローカル検証とは別の確認事項。
