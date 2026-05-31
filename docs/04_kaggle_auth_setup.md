# Kaggle 認証セットアップ

このテンプレートでは、Kaggle Competition / Discussion / Notebook / Dataset の取得に Kaggle CLI を使います。MCP server も内部では Kaggle CLI を呼ぶため、認証が必要な操作では Kaggle CLI の認証設定が必要です。

公式 Kaggle CLI documentation では、認証方法として以下が案内されています。

- OAuth: `kaggle auth login`
- 環境変数: `KAGGLE_API_TOKEN`
- API token file: `~/.kaggle/access_token`
- Legacy API credentials file: `~/.kaggle/kaggle.json`

推奨は OAuth または `KAGGLE_API_TOKEN` / `~/.kaggle/access_token` です。`kaggle.json` は legacy 扱いなので、新しい CLI で認証に失敗する場合は OAuth または access token 方式に切り替えてください。

## 1. OAuth でログインする

ローカル環境でブラウザを開ける場合:

```bash
uv run kaggle auth login
```

ブラウザを自動起動したくない場合:

```bash
uv run kaggle auth login --no-launch-browser
```

既存 login を更新する場合:

```bash
uv run kaggle auth login --force
```

## 2. API token を環境変数で渡す

Kaggle の API settings で token を生成し、shell の環境変数に設定します。

```bash
export KAGGLE_API_TOKEN="xxxxxxxxxxxxxx"
```

この方法は CI / MCP client / 一時的な検証に向いています。token は repository に commit しないでください。

## 3. API token file を使う

Kaggle の API settings で token を生成し、以下に保存します。

```bash
mkdir -p ~/.kaggle
chmod 700 ~/.kaggle
printf '%s' 'xxxxxxxxxxxxxx' > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```

## 4. Legacy `kaggle.json` を使う

Kaggle の API settings で legacy API key を生成し、`~/.kaggle/kaggle.json` に置きます。

```bash
mkdir -p ~/.kaggle
chmod 700 ~/.kaggle
mv /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

ただし、Kaggle CLI 2.2.0 では OAuth / access token 方式が主経路です。`kaggle.json` が存在していても API 呼び出しで `Authentication required` が出る場合は、OAuth または access token 方式に切り替えてください。

## 5. 認証状態の確認

まず CLI version と help を確認します。

```bash
uv run kaggle --version
uv run kaggle --help
uv run kaggle auth --help
```

設定状態を確認します。

```bash
uv run kaggle config view
```

実際に API 呼び出しが通るか確認します。

```bash
uv run kaggle competitions files -c titanic
uv run kaggle kernels list --search "titanic survival" --competition titanic
```

MCP 経由で確認する場合は、`kaggle_cli_version` と `kaggle_competition_files` を呼びます。

## 6. MCP server で使う場合

MCP server は既定で以下を内部実行します。

```bash
uv run kaggle ...
```

通常は Kaggle CLI 側の認証設定がそのまま使われます。別の command を使いたい場合は `KAGGLE_MCP_KAGGLE_CMD` を指定します。

```bash
KAGGLE_MCP_KAGGLE_CMD="kaggle" uv run --group mcp python tools/kaggle-mcp/server.py
```

snapshot 保存先を変える場合:

```bash
KAGGLE_MCP_CACHE_DIR=".cache/kaggle-mcp" uv run --group mcp python tools/kaggle-mcp/server.py
```

## 7. トラブルシューティング

### `Authentication required to call the Kaggle API.`

以下を順に確認します。

1. `uv run kaggle config view` で認証方式が表示されるか。
2. OAuth の場合は `uv run kaggle auth login --force` で再ログインする。
3. token 方式の場合は `KAGGLE_API_TOKEN` または `~/.kaggle/access_token` が正しいか。
4. legacy `kaggle.json` のみの場合は、OAuth または access token 方式へ切り替える。
5. private competition や rules acceptance が必要な competition では、Kaggle Web 上で rules を accept する。

### Discussion は取得できるが files / notebooks が失敗する

Kaggle CLI の command によって匿名アクセス可否が異なります。Discussion list / show が通っても、competition files、notebook search、dataset download は認証が必要な場合があります。
