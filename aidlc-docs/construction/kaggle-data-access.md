# Kaggle Data Access

## Maintenance Verification

- CLI: 2.2.0 を確認後、2.2.4 / kagglesdk 0.1.37 に更新し、help と official parser で構文を確認。
- 経路: src/workflow_tools/kaggle.py を MCP server と download wrapper から共有する。
- 2026-10-04 11:56 JST: actual stdio MCP initialize / tools list / kaggle_cli_version が成功。12 tools、version と help の ok=true。
- 認証付き API・データ取得・Notebook pull・submission は実行していない。
- Snapshot: .cache/kaggle-mcp/kaggle_cli_version/20261004T025652476786Z-9261a17207e64ec98bc465d88ad7f3fd.json、対応 help snapshot。cache は Git 管理対象外。

## Retrieval Contract

ok / error / truncated / snapshot を確認する。Overview は metadata / URLs のみ。
各コマンドの paging、本文・コメント範囲、CLI 版を source register / audit に記録する。
Download は所定の data roots、archive 展開は既存 file 上書き拒否と resource budget を使う。
外部 Notebook は source / metadata だけ取得し、license・依存・前提を確認するまで実行しない。

CLI コマンド、入力、response、失敗と展開の限界は tools/kaggle-mcp/README.md に記載する。
