# Kaggle MCP Server

Kaggle 情報取得の CLI 境界です。`src/workflow_tools/kaggle.py` の subprocess・snapshot・download 処理を MCP tools と shell wrapper が共有します。
学習コードに MCP client を導入する必要はありません。

## Start

```bash
uv sync --locked --group mcp
uv run --locked --group mcp python tools/kaggle-mcp/server.py
```

Client 設定は [MCP setup](../../docs/05_mcp_setup.md)、認証は [Kaggle setup](../../docs/04_kaggle_auth_setup.md) を参照してください。
まず `kaggle_cli_version` を呼び、実機の version / help を記録します。

## Tools

| Tool | 出力 / 注意 |
| --- | --- |
| kaggle_cli_version | version / help。認証付き API 成功の証拠ではない |
| kaggle_competitions_list | 一覧と検索。slug の完全一致を別途確認 |
| kaggle_competition_overview | 一覧 metadata と URL。概要・規約・評価本文は取得しない |
| kaggle_competition_files | bounded page、file size、continuation token |
| kaggle_competition_download | data/raw/ 内へ取得・必要なら安全に展開 |
| kaggle_discussions_list | top / hot / recent 等、1 page |
| kaggle_discussion_get | 本文と bounded comments。page token を確認 |
| kaggle_notebooks_search | query + competition filter、page size |
| kaggle_notebook_pull | notebooks_external/ に source + metadata。実行しない |
| kaggle_datasets_list | 一覧。版・license は別途確認 |
| kaggle_dataset_download | data/external/ に取得・展開 |
| kaggle_submissions_list | 既存提出履歴の読取 |

自動提出、規約受諾、Notebook push、server-side 実験は含みません。

## Response Contract

`schema_version=1`。通常の response は次を含みます。

- `ok`、`returncode`、`error.kind / message`
- `tool`、`source`、`command`、`started_at / finished_at`
- `stdout / stderr`（CLI text。resource ごとの JSON schema ではない）
- `snapshot_path`、`truncated`、resource ref と source URL

Version tool は `version` と `help` にそれぞれ response を返します。
CLI の非ゼロ終了、command 起動失敗、timeout、展開失敗を区別します。
不正な input / 保存先は tool error です。Snapshot 書込失敗も tool error として扱います。
Response は stdout / stderr 各16,000文字で切り詰め、snapshot に全内容を保存します。
Timestamp + UUID で snapshot の衝突を防ぎます。Metadata と error も snapshot に含まれます。

`ok=true` は command 成功であり、全文・全件取得の保証ではありません。
Page / token、切り詰め、空結果、検索対象を確認してから要約します。

## Environment / Downloads

- `KAGGLE_MCP_KAGGLE_CMD`: command override。既定は現在の PATH の kaggle executable。
- `KAGGLE_MCP_CACHE_DIR`: snapshot 保存先。既定は repository の .cache/kaggle-mcp/。
- `KAGGLE_MCP_MAX_EXTRACT_BYTES`: 展開総サイズ上限。既定5 GiB。予算を確認して変更する。

Competition は data/raw/、Dataset は data/external/、Notebook は notebooks_external/ 内だけに保存できます。
参照は slug または owner/resource。URL、path traversal、option の混入を拒否します。
Archive は path / symlink / 重複 / サイズを確認してから展開し、既存データを上書きしません。
再取得は別の directory を指定するか、archive を保持して差分を確認します。既存ファイル衝突は失敗として返します。
展開途中の I/O 失敗では一部ファイルが残る場合があり、error と directory を確認して復旧します。

Snapshot は cache なので、参照 ID・取得日・revision・短い要約を
`aidlc-docs/inception/source-register.md` に残し、tool / command を audit に記録します。
認証の秘密値を引数に渡したり、取得内容に含めたりしません。
