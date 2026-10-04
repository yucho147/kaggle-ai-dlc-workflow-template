# Kaggle 認証と接続確認

付属 MCP と download wrapper は Kaggle CLI を使います。
認証方式と最新の互換性は [Kaggle CLI の公式 README](https://github.com/Kaggle/kaggle-cli) を参照してください。

## CLI の確認

```bash
uv run kaggle --version
uv run kaggle --help
uv run kaggle auth --help
```

利用中の CLI の help を優先します。版の違いで command・sort・paging・format が変わります。
コンペのデータ取得に必要な規約受諾は Kaggle Web でユーザーが行います。

## 認証方法

公式 CLI は OAuth、`KAGGLE_API_TOKEN`、`~/.kaggle/access_token`、legacy `~/.kaggle/kaggle.json` を案内しています。

Local OAuth の例:

```bash
uv run kaggle auth login
```

CI / MCP では client や CI の secret 管理から環境変数を渡す方法もあります。
既存の credentials が有効なら、そのまま使用します。Legacy file があることだけで認証失敗とは判断しません。
File を使う場合は本人のみ読める権限にし、token の内容を tool output・audit・Git に出しません。

## Read-only 接続確認

```bash
uv run kaggle competitions files titanic
```

MCP では `kaggle_cli_version` と `kaggle_competition_files` の `ok`、error、取得時刻を確認します。
匿名で取得できた結果は認証確認と同義ではありません。公開・private・規約受諾・resource ごとの権限差を確認します。

## Failure Handling

- Authentication error: 認証方式、client に渡した環境変数、token 有効性を確認。
- Forbidden / rules: 対象 resource の権限・規約受諾状態を確認。
- Unknown flag: 同じ環境の subcommand help を確認。
- Timeout / rate limit: 失敗を記録し、取得範囲を縮小。無制限に再試行しない。
- Client 起動失敗: cwd、依存導入、cache の書込権限を確認。

`auth print-access-token` は秘密値を表示する command なので、共有ログを取る診断に使用しません。
