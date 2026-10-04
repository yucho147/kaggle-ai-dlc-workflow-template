# MCP Setup

MCP は任意です。付属設定の既定 server は **kaggle** です。論文・モデル検索は必要な案件で追加します。
ロックされていない `uvx` package を毎回起動時に取得する構成は標準から外しています。

## Local Kaggle Server

```bash
uv sync --locked --group mcp
uv run --locked --group mcp python tools/kaggle-mcp/server.py
```

Repository root から起動します。stdio は MCP protocol 専用で、実行結果は JSON response と snapshot に保存します。
認証は [Kaggle setup](04_kaggle_auth_setup.md)、tool の input / output は [server README](../tools/kaggle-mcp/README.md) を参照してください。

## Client Settings

| Client | 付属ファイル | 確認 |
| --- | --- | --- |
| Codex | .codex/config.toml | /mcp または codex mcp list |
| Claude Code | .mcp.json | /mcp と project server の trust |
| Kiro CLI | .kiro/settings/mcp.json | client の MCP 表示と log |
| Copilot CLI | .mcp.json（対応版・trusted folder） | /mcp list / /mcp show kaggle |

Codex の project settings は trusted project に適用されます。
[OpenAI MCP docs](https://developers.openai.com/codex/mcp) の cwd / timeout / tool allowlist を確認してください。
相対 cwd は client の起動位置に依存するため、repository root で起動し、必要なら絶対パスへ変更します。

Client ごとの MCP 設定 schema を混用しません。汎用 `tools: ["*"]` や shell の一括許可をテンプレート側で追加しません。

現在の [Copilot CLI 公式手順](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers) は project の `.mcp.json` / `.github/mcp.json` を読み込むと説明しています。付属 `.mcp.json` は stdio 型を明示します。旧版では対応状況を help で確認してください。

## Optional Sources

- Hugging Face: [公式 MCP 説明](https://huggingface.co/docs/hub/en/agents-mcp) の endpoint・認証・現在の tools を確認して追加。
- arXiv: 採用する server の repository、license、package version、保存先を確認して導入。第三者 server を arXiv 公式 API と混同しない。
- 公式 Web / 論文 / GitHub は MCP なしでも調査可能。

利用する server の版・起動 command・取得 source を audit に記録します。
付属 Kaggle server は論文検索やモデル inference を行いません。

## Environment / Timeout

- `UV_CACHE_DIR=.cache/uv` を付属 stdio config で指定。
- Server は repository root と保存先を固定し、起動 cwd に依存して別 project へ書き込まない。
- Read command は120秒、download は900秒の上限。Client 側 timeout も整合させる。
- 初回依存の導入は手動で先に実行し、起動時の解決負荷を減らす。
- 秘密 token は client の認証・環境変数管理から渡す。`.env` の自動読込は仮定しない。

## Connection Evidence

次を区別して記録します。

1. 設定ファイルの構造検査。
2. MCP initialize / tools list。
3. CLI version / help。
4. 対象の認証付き API と本文取得。
5. Download したデータの version / schema。

低い段階の成功を全体の接続成功と記載しません。取得失敗や切り詰めは source register に残します。
