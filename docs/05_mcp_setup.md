# MCP サーバーセットアップ

このテンプレートは3つの MCP サーバーをデフォルトで設定しています。

| サーバー | 用途 |
| --- | --- |
| `kaggle` | Competition / Discussion / Notebook / Dataset 取得 |
| `arxiv` | 論文検索・取得 |
| `huggingface` | モデル・Dataset・Spaces 検索 |

---

## Codex

Codex はリポジトリルートの `.codex/config.toml` を project-scoped configuration として読み込みます。Codex CLI と IDE extension で同じ設定が共有されます。

ローカルの stdio server には、リポジトリルートを `cwd` として指定し、`uv` の cache / tool directory を `.cache/` 配下に固定しています。これにより、sandbox 内から書き込みできない `~/.cache/uv` や `~/.local/share/uv/tools` を参照して起動に失敗することを防ぎます。初回 dependency 解決を考慮し、startup timeout は 60 秒に設定しています。

```bash
cd /path/to/kaggle-ai-dlc-workflow-template
codex
```

初回はプロジェクトを trust してください。起動後、以下で MCP server と repository skill を確認できます。

```text
/mcp
/skills
```

Skills の正本は `.agents/skills/` です。Codex はこのディレクトリを自動検出するため、`.codex/skills/` へのコピーやリンクは不要です。

コマンドラインから MCP 設定だけを確認する場合:

```bash
codex mcp list
```

---

## Claude Code

プロジェクトルートの `.mcp.json` が自動で読み込まれます。追加設定は不要です。

HuggingFace のプライベートモデルやプライベート Dataset を使う場合は `.env` に追加してください。

```bash
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
```

---

## GitHub Copilot CLI

Copilot CLI はプロジェクトレベルの設定ファイルに対応していないため、ユーザーレベルの設定ファイルに追記してください。

```bash
~/.copilot/mcp-config.json
```

以下の内容を `mcpServers` に追記します。`<project-root>` はこのリポジトリの絶対パスに置き換えてください。

```json
{
  "mcpServers": {
    "kaggle": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--group", "mcp", "python", "<project-root>/tools/kaggle-mcp/server.py"],
      "cwd": "<project-root>",
      "env": {
        "UV_CACHE_DIR": "<project-root>/.cache/uv"
      },
      "tools": ["*"]
    },
    "arxiv": {
      "type": "stdio",
      "command": "uvx",
      "args": ["arxiv-mcp-server"],
      "cwd": "<project-root>",
      "env": {
        "UV_CACHE_DIR": "<project-root>/.cache/uv",
        "UV_TOOL_DIR": "<project-root>/.cache/uv-tools"
      },
      "tools": ["*"]
    },
    "huggingface": {
      "type": "http",
      "url": "https://huggingface.co/mcp",
      "tools": ["*"]
    }
  }
}
```

設定後、Copilot CLI セッション内で確認できます。

```
/mcp show
```

---

## 各サーバーの主なツール

### kaggle

`tools/kaggle-mcp/server.py` に実装されています。

- `kaggle_competitions_list` — コンペ一覧
- `kaggle_competition_overview` — コンペ概要
- `kaggle_competition_files` — データファイル一覧
- `kaggle_competition_download` — データダウンロード
- `kaggle_discussions_list` — Discussion 一覧
- `kaggle_discussion_get` — Discussion 詳細
- `kaggle_notebooks_search` — Notebook 検索
- `kaggle_notebook_pull` — Notebook 取得
- `kaggle_datasets_list` — Dataset 一覧
- `kaggle_dataset_download` — Dataset ダウンロード
- `kaggle_submissions_list` — 提出履歴

Kaggle 認証が必要な操作は [docs/04_kaggle_auth_setup.md](04_kaggle_auth_setup.md) を参照してください。

### arxiv

- `search_papers` — キーワード・カテゴリ・日付で論文検索
- `download_paper` — arXiv ID を指定して論文をダウンロード
- `read_paper` — ダウンロード済み論文をテキストで読む
- `list_papers` — ローカルにキャッシュされた論文一覧

### huggingface

HuggingFace 公式リモートサーバー（`https://huggingface.co/mcp`）です。インストール不要。

- モデル・Dataset の検索とメタデータ取得
- Spaces（Gradio アプリ）の実行
- Inference API 経由のモデル推論

---

## 前提

- `uv` がインストール済みであること（Kaggle / arxiv）
- Kaggle 認証設定済みであること（Kaggle の一部 tool）
- Codex で project-scoped configuration を使う場合は、プロジェクトを trust していること

## Troubleshooting

`MCP startup failed` とともに `Operation not permitted` が表示される場合は、エラーの参照先を確認してください。

- `~/.cache/uv`: `UV_CACHE_DIR` が書き込み可能な場所を指していない。
- `~/.local/share/uv/tools`: `uvx` 用の `UV_TOOL_DIR` が書き込み可能な場所を指していない。
- `tools/kaggle-mcp/server.py` が見つからない: MCP process の `cwd` がリポジトリルートではない。
- 10 秒前後で終了する: 初回 dependency 解決に対して startup timeout が短い。
