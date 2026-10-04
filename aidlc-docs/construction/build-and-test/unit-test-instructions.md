# Unit / Regression Instructions

```bash
uv run --no-sync ruff check .
uv run --no-sync pytest -q
```

66 tests: initialization、CSV / submission / fold / OOF、CLI parser / errors / snapshot / extraction、report、derived project、MCP protocol、synthetic end-to-end。
Local fixtures を使い、認証付き API を呼ばない。結果は operations/experiment-log.md に記録済み。
