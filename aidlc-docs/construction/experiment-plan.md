# Experiment Plan

## Maintenance Verification

今回の仮説はテンプレート運用と実装契約の改善。Synthetic score の競争ではない。

| ID | Scope | Conditions | Acceptance | Status |
| --- | --- | --- | --- | --- |
| check001 | regression | local fixtures / installed CLI parser | 記録保全、失敗表現、前処理・ID・HTML 契約が通る | reviewed |
| check002 | local MCP | stdio、実機 Kaggle 2.2.4、version / help のみ | initialize、12 tools、version / help ok | reviewed |
| smoke001 | 標準 baseline | 1,000 synthetic rows、seed42、5-fold、50 trees、CPU | 正常終了、dummy / OOF / manifest / model を保存 | reviewed |
| check003 | 構造・skills | JSON / TOML、links / symlinks、空の seed audit | 構造0 errors、skills 4件 valid、lint 成功 | reviewed |
| check004 | human report | 正本から HTML 再生成、Chrome / localhost | 改訂表・本文・セクション移動を desktop で確認 | reviewed |

## Budget / Commands

CPU の小規模実行。GPU、クラウド、コンペ全量データ、提出は使わない。

```bash
uv sync --locked --group research --group mcp
uv run --no-sync ruff check .
uv run --no-sync python scripts/check_template.py
uv run --no-sync pytest -q
uv run --locked --group research --group mcp python -m baseline.train
uv run python scripts/render_improvement_report.py
```

実際の command には `UV_CACHE_DIR=.cache/uv` を付けた。
結果は [Experiment Log](../operations/experiment-log.md) に記録する。
