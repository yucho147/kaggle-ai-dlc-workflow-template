# Build Instructions

```bash
uv sync --locked --group research --group mcp
uv run --no-sync python scripts/check_template.py
```

Python 3.13、project-local uv cache を使用。Notebook / columnar は必要な案件だけ optional groups を追加する。
標準の editable project に baseline と workflow_tools を含む。
今回の lock install は成功。別 OS / clean wheel installation は今回の確認範囲外。
