# AI-DLC State

## Project

- Name: Kaggle / Technical Research AI-DLC Workflow Template
- Workflow: template-maintenance
- Owner: User
- Started: 2026-10-04
- Phase: operations
- Status: complete
- Updated: 2026-10-04 JST

## Current Objective

ユーザーの依頼に基づき、文書・雛形・スキル・実装・CI を詳細レビューして改訂する。
派生案件で記録が継続でき、データ・評価・実験・判断の根拠がつながるテンプレートにする。

## Scope / Decisions

- 新たなコンペやクラウド実験は開始しない。今回の対象はテンプレート保守。
- 既存 Python 3.13 と Hydra / loguru / MLflow を維持する。
- 調査・文書と実装の完了条件を区別し、ゲートを記録する。
- seed は空の雛形、aidlc-docs は案件記録。新規派生案件で --new-project を使う。
- 新しい汎用 framework を作らず、初期化・CLI 取得・評価・出力の契約を改善する。

## Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| G0 問題設定 | complete | 詳細レビューと改訂をユーザーが依頼 |
| G1 実装準備 | complete | problem-overview / architecture / questionnaire / plan |
| G2 結果確認 | complete | 66 tests、lint、構造・skills、actual CLI / MCP、baseline |
| G3 終了 / 引継ぎ | complete | 改訂理由・移行方法・限界を記録し、HTML を desktop で閲覧確認 |

## Next Actions

今回の改訂は完了。次の案件では次の順序で開始する。

1. 新規派生案件は --new-project で保守記録を backup し、空の雛形へ切り替える。
2. 対象・到達点・予算から必要な workflow と data / evaluation contract を確定する。
3. 既存案件へ取り込む場合は、記録を保全して欠落補充と差分移植を行う。

認証付き API、各 client の対話起動、Linux hosted CI、実コンペ / 業務性能は今回未検証。

## 追加改訂: 用語と説明

ユーザーの用語に関する依頼を受け、共通指示・説明ガイド・文書雛形・報告前の確認手順を追加した。
問題設定文書に用語と旧名の対応を記録し、再開時の参照先を固定した。
コード構成、実験 ID、HTML の生成方式は変更しない。上記の検証結果は先行するテンプレート改訂の結果。
