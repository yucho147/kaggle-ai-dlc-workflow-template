# Audit Log

外部取得、重要な判断、仮定、承認範囲、失敗と再試行を追記する。秘密情報や全文転載を含めない。
取得物の主張と証拠は `inception/source-register.md`、実行結果は `operations/experiment-log.md` に記録する。

## Entry Format

### YYYY-MM-DD HH:MM TZ — 要件 / 判断 / 外部取得

- Actor:
- Action:
- Source ID / URL / revision:
- Tool / command（秘密値を除く）:
- Result / failure / snapshot:
- Decision / rationale:
- Assumption / expiry or revisit trigger:
- Authorization / scope（必要な場合）:

## Entries

初期状態。プロジェクトを開始したら最初の依頼と作業範囲を記入する。
