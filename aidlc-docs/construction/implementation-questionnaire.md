# 実装前質問票

2026-10-04: ユーザーのテンプレート改訂依頼から以下を確定。重大な未決事項なし。

| 項目 | 回答 | Reason |
| --- | --- | --- |
| 用途 | template-maintenance | 個別コンペの参加ではなく詳細レビューと改訂 |
| 環境 | macOS / uv / Python 3.13 | 既存環境を維持 |
| Style | package + scripts、Notebook は同梱しない | 再実行可能な例と保守ツール |
| Configuration | 実験 Hydra、保守 CLI argparse | 設定の用途が異なる |
| Logging / tracking | loguru / MLflow + local manifest | 成功・失敗・再現情報を保全 |
| Data access | MCP と wrapper の shared CLI boundary | 学習を取得・network から分離 |
| Code structure | 既存 baseline + dependency-light workflow_tools | 過剰な共通 framework を避ける |
| Seed / active docs | 別の正本。初期化は backup 付き | 派生案件の編集を許容 |
| Tests | records preservation、CLI errors、submission ID、fold fit、HTML | レビューで判明した実害を確認 |
| External actions | 公式資料・CLI help・依存更新まで | 提出、規約受諾、クラウド実行は対象外 |

## Assumptions

Python 3.13 を維持し、GPU 案件には環境別の対応版確認を促す。
調査上限は案件規模で決め、固定件数で全用途を縛らない。
今回の保守記録は aidlc-docs に残し、Use template の新規案件は --new-project で切り替える。
