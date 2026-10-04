# Unit Test Instructions

## Scope

意味のある契約を検証する。実装をそのまま写すテストや score の固定値だけを確認するテストを避ける。

- データ欠落、ID 不整合、NaN / inf、未知 schema: TBD
- Fold 内 fit、split overlap、予測方式: TBD
- 外部境界の失敗・timeout・保存先: TBD
- 初期化の記録保全・report の安全な rendering: TBD

## Template Checks

```bash
uv run --locked ruff check .
uv run --locked --group research --group mcp pytest
uv run --locked python scripts/check_template.py
```

## Project Commands / Results

- Command: TBD
- Result / limitations: TBD
