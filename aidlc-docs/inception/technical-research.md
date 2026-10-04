# Technical Research

## Template Maintenance — 2026-10-04

全 tracked files と公式一次資料をレビューし、次の問題を修正した。


| 既存の問題 | 改訂 | 利用者への影響 |
| --- | --- | --- |
| 案件 docs と seed の完全一致 CI | 構造・設定・リンク・実行契約の検査へ変更 | 案件記録を書いても CI が失敗しない |
| --force が記録を無保護で上書き | backup、missing-only、fresh project を分離 | 再開と新規案件を使い分けられる |
| 初期 audit に過去保守履歴を複製 | seed audit を空にし、保守記録は現在の docs に保存 | --new-project で案件固有の記録を開始できる |
| PoC でも Kaggle 調査を一律必須 | 関連する情報源・必要な工程だけ選択 | 調査だけの依頼や非 ML PoC にも使える |
| 外部主張の根拠・確度が曖昧 | source-register と coverage / failures | 報告、実測、推論を区別できる |
| CV・情報利用時点・出力の定義不足 | data / evaluation contract を追加 | group・時間・ID・予測方式を実装前に確定 |
| 業務評価と終了判断が不足 | PoC thresholds、poc-decision、引継ぎ | 品質・latency・費用を含め採否を判断 |
| 実機 CLI にない -c、--unzip、votes sort | positional args、top、safe local extraction | CLI の版・help に沿って取得 |
| MCP の timeout / failure / snapshot の不足 | 共通 CLI 境界、structured errors、一意 snapshot、bounded response | 失敗・未取得・切り詰めを見落としにくい |
| 指定データ欠落で synthetic へ切替 | explicit synthetic / csv、欠落エラー | smoke score を実データ結果と混同しない |
| 前処理・OOF・比較・提出整列が不足 | fold 内 Pipeline、dummy 比較、OOF、ID alignment、prediction mode | 評価と提出の対応を確認できる |
| 再現情報と artifact が分散 | run directory、config、manifest、data / split hash、versions、MLflow ID | 失敗も含めて再実行・追跡できる |
| Model 依存が自動 export 任せ / root に Hydra log | model requirements と model URI を明示、local / MLflow manifest を照合、loguru に集約 | モデルと実行記録を対応させて保全できる |
| 手書き Markdown rendering の制約 | markdown-it-py、raw HTML 無効、tables / safe links | 調査と PoC docs も HTML で閲覧 |
| 重複した agent instructions / commands | AGENTS と4 skills を正本にし commands は参照 | 更新箇所と判断の一貫性を保てる |
| 汎用 shell 許可、無固定の optional server | 共有許可を絞り、default MCP を Kaggle に整理 | 接続と追加依存を案件ごとに選べる |
| Notebook / columnar を research に全同梱 | optional groups に分離 | baseline に必要な環境を小さく保てる |
| 古い CI action と内容一致だけの検査 | 現行 action のタグを確認して SHA 固定、契約の回帰検証を追加 | 実装と派生運用の両方を検査 |

## Evidence / Scope

Source register の reported / observed / inferred を区別する。
AWS の adaptive workflow 原則を参考にする独自テンプレートであり、現行公式 runtime の完全移植ではない。
Kaggle main の仕様と installed 2.2.4 help が異なる部分は、実機の版・help を記録して修正した。

Model runtime dependencies の明示、bool feature の補完、Hydra logging の整理、CI action の SHA 固定も実施した。
検証結果は Experiment Log、残る限界は Risks を参照する。

## Migration

新規案件: `uv sync --locked` → `uv run scripts/init_aidlc_docs.sh --new-project`。
既存案件: records / tracker / artifacts を保全し、引数なしで欠落雛形を補い、data / evaluation contract と CSV / ID / prediction の設定を移す。
`--force` は backup 付きの seed 上書き。進行中案件の通常更新には使わない。

各 client の対話起動・認証付き API・実コンペ / 業務性能は今回未検証。
