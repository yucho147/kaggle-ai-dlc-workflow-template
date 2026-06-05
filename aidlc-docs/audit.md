# Audit Log

外部情報の取得、重要な判断、仮定、ユーザーとの合意事項を記録する。

## Log

### YYYY-MM-DD HH:MM

- Actor:
- Action:
- Command / Source:
- Result:
- Decision:
- Assumption:

### 2026-06-05 15:40 JST

- Actor: Codex
- Action: Codex 向け repository skills / project-scoped MCP configuration の公式仕様を確認した。
- Command / Source: OpenAI Developer Docs MCP (`https://developers.openai.com/codex/skills`, `https://developers.openai.com/codex/mcp`, `https://developers.openai.com/codex/config-basic`)
- Result: Repository skills は `.agents/skills/`、project-scoped MCP configuration は trusted project の `.codex/config.toml` が公式対応配置であることを確認した。
- Decision: Skills は既存 `.agents/skills/` を共通の正本とし、Codex 用には `.codex/config.toml` だけを追加する。
- Assumption: Codex はリポジトリルートから起動し、プロジェクトを trust して利用する。

### 2026-06-05 16:20 JST

- Actor: Codex
- Action: MCP server の起動失敗を再現し、Codex の project-scoped MCP 設定を精査した。
- Command / Source: `codex mcp list`; `uv run --group mcp ...`; `uvx arxiv-mcp-server`; OpenAI Developer Docs MCP (`https://developers.openai.com/codex/config-reference#configtoml`)
- Result: sandbox 内では既定の `~/.cache/uv` と `~/.local/share/uv/tools` が書き込み不可だった。また Kaggle / arXiv server の初期化は検証環境で約 17 秒かかり、Codex の既定 startup timeout 10 秒を超えた。書き込み可能な project-local directory を指定後、両 server で MCP initialize と tools/list が成功した。
- Decision: `.codex/config.toml` に `cwd`、`UV_CACHE_DIR`、`UV_TOOL_DIR`、startup/tool timeout を設定し、`.mcp.json` にも同じ directory 方針を反映する。
- Assumption: MCP client はリポジトリルートから project configuration を読み込む。

### 2026-06-05 16:40 JST

- Actor: User / Codex
- Action: Codex 対応の動作確認結果をドキュメントへ反映した。
- Command / Source: User confirmation; `git diff`; `UV_CACHE_DIR=.cache/uv uv run scripts/init_aidlc_docs.sh --check`
- Result: Codex で repository skills と3つの MCP server が正常に利用できることを確認した。README、Quickstart、Agent Execution Guide に Codex 対応と確認手順を明記した。
- Decision: OpenAI Codex を本テンプレートの対応 Coding Agent として明示する。
- Assumption: 動作確認日は 2026-06-05、プロジェクトを trust した Codex 環境を対象とする。
