# Kaggle MCP Server

Kaggle Competition / Discussion / Notebook / Dataset / Submission 取得を MCP tool として抽象化するための最小 server です。

## 目的

- agent が毎回 Kaggle CLI command を組み立てないようにする。
- Discussion / Notebook / Dataset の取得元、command、snapshot を共通形式で残す。
- training code / feature code が Kaggle CLI に直接依存しないようにする。
- Technical Research でも Kaggle の類似コンペ、Discussion、Notebook、Dataset を最良手法探索の情報源として使う。

## 起動

Kaggle 認証が必要な tool を使う前に、[docs/04_kaggle_auth_setup.md](../../docs/04_kaggle_auth_setup.md) に従って Kaggle CLI の認証を設定してください。

```bash
uv run --group mcp python tools/kaggle-mcp/server.py
```

server 内部では既定で `uv run kaggle ...` を実行します。別の Kaggle command を使う場合は、MCP client 側の環境変数で指定します。

```bash
KAGGLE_MCP_KAGGLE_CMD="kaggle" uv run --group mcp python tools/kaggle-mcp/server.py
```

snapshot 保存先の既定値は `.cache/kaggle-mcp/` です。変更する場合:

```bash
KAGGLE_MCP_CACHE_DIR=".cache/kaggle-mcp" uv run --group mcp python tools/kaggle-mcp/server.py
```

## Tools

| Tool | 用途 |
| --- | --- |
| `kaggle_cli_version` | Kaggle CLI version / help の確認 |
| `kaggle_competitions_list` | 類似 competition の検索 |
| `kaggle_competition_overview` | competition の軽量 metadata と URL 取得 |
| `kaggle_competition_files` | competition file 一覧 |
| `kaggle_competition_download` | competition data download |
| `kaggle_discussions_list` | discussion topic 一覧 |
| `kaggle_discussion_get` | discussion 本文・コメント取得 |
| `kaggle_notebooks_search` | Kaggle notebook 検索 |
| `kaggle_notebook_pull` | Kaggle notebook source 取得 |
| `kaggle_datasets_list` | Kaggle dataset 検索 |
| `kaggle_dataset_download` | Kaggle dataset download |
| `kaggle_submissions_list` | submission history 取得 |

## MCP Client 設定例

```json
{
  "mcpServers": {
    "kaggle": {
      "command": "uv",
      "args": [
        "run",
        "--group",
        "mcp",
        "python",
        "tools/kaggle-mcp/server.py"
      ],
      "cwd": "/path/to/kaggle-ai-dlc-workflow-template"
    }
  }
}
```

## Audit 方針

各 tool は以下を返します。

- `tool`
- `source`
- `command`
- `started_at`
- `finished_at`
- `returncode`
- `stdout`
- `stderr`
- `snapshot_path`

agent は `stdout` を要約し、参照した `snapshot_path` と判断を `aidlc-docs/audit.md` に記録してください。
