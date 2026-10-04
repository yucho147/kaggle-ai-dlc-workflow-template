# 実装前質問票

既存の依頼・文書から回答できる項目を先に記入する。目的・評価・利用権限を変える未決事項をまとめて質問する。
軽微な設計は合理的な標準を採用し `../audit.md` に理由を残す。

| 項目 | 回答 / 標準 | 未決事項 / blocker |
| --- | --- | --- |
| 今回の成果物と最初の仮説 | TBD | TBD |
| Domain / タスク / 入出力 | TBD | TBD |
| 既存コード / 再利用する部分 | TBD | TBD |
| 環境 / Python / CPU・GPU / 制限 | TBD | TBD |
| Script / Notebook / hybrid | script を標準。Notebook は EDA・orchestration | TBD |
| Package と最小 module 構成 | src/<package_name>/ | TBD |
| 名称と説明 | 一般用語・具体的な名前を優先。案件固有の名称は problem-overview.md に定義し、コード識別子との対応を記録 | TBD |
| 設定 / logging / tracker | Hydra / loguru / MLflow を標準 | TBD |
| Offline・制限環境の tracking | local config / metrics / manifest を保存し後で取り込む | TBD |
| Data / evaluation contract | inception の契約文書を参照 | TBD |
| 外部取得の経路 | 関連する場合 MCP / adapter / 手動 snapshot | TBD |
| 計算時間 / 費用上限 / stop condition | TBD | TBD |
| Artifact / 提出・業務出力 | TBD | TBD |
| 必要な検証 / 再実行 command | TBD | TBD |

## Decisions

- 選んだ構成と理由: TBD
- 標準から変える箇所と理由: TBD
- 共有ロジックを置く場所 / Notebook 方針: TBD
- 実装前に解決が必要な事項: TBD
- 仮定で進める事項 / 再検討条件: TBD

調査・文書作成だけの場合はコード構成の詳細を確定する必要はない。
