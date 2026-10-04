# Agent Execution Guide

新規案件の作成・依存導入は [Quickstart](02_quickstart.md) を参照してください。
入口指示は `AGENTS.md`、手順は `.agents/skills/` に集約しています。

## Clients

| Client | 起動例 | この repository の入口 |
| --- | --- | --- |
| Codex | codex | AGENTS.md、.agents/skills/、.codex/config.toml |
| Claude Code | claude | CLAUDE.md、.claude/commands/、.mcp.json |
| GitHub Copilot CLI | copilot | .github/copilot-instructions.md、AGENTS.md、.mcp.json |
| Kiro CLI | kiro-cli chat | .kiro/steering/agents.md、.kiro/agents/research-agent.json |

MCP の trust・OAuth・有効化は client の仕様とユーザー設定に従います。
ファイルがあることと、実際に読み込まれたこと・認証付き API が成功したことは別に確認します。
この改訂で GUI / 各 client の対話起動は実機検証していません。

## Codex

Repository skills の配置と trusted project の MCP configuration は
[OpenAI の skills](https://developers.openai.com/codex/skills) と [MCP](https://developers.openai.com/codex/mcp) の公式資料で確認します。

Project root から起動し、`/skills`、`/mcp` で現在読み込まれた一覧を確認します。
用途を明示する場合は `$kaggle-starter` 等を指定できます。付属 skill は4つです。
Project config は sandbox / approval を広げません。必要な設定を確認してから project を trust します。

## Claude Code

`CLAUDE.md` から共通指示を import し、commands は正本 skill を参照します。

| Command | 用途 |
| --- | --- |
| /kaggle-starter <slug> | 参加準備 |
| /kaggle-winning-research <slug> | 解法調査 |
| /technical-research <theme> | PoC / 技術調査 |
| /improvement-review | 結果と次仮説のレビュー |

Project MCP の有効化は [Claude MCP 公式資料](https://code.claude.com/docs/en/mcp) に従います。
`.env` が自動で全 server に渡るとは限りません。秘密値は client の認証・環境変数管理を使います。
共有設定で汎用 shell / uv command を一括許可しません。

## GitHub Copilot CLI / Kiro

[Copilot CLI 公式資料](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)、
[Kiro CLI 公式資料](https://kiro.dev/docs/cli/) を参照し、利用中の版の help と設定表示を確認します。
Copilot には必要なら AGENTS と該当 skill を読むよう指示してください。
Kiro の `research-agent` は入口文書と skill の参照を提供します。
現在の [Kiro custom agent reference](https://kiro.dev/docs/custom-agents/configuration-reference/)（CLI 3.0）では `file://` / `skill://` resources と `includeMcpJson` が案内されています。付属 agent は workspace MCP を取り込みます。旧版は公式の移行手順を確認してください。

## Start / Resume

[プロンプト集](03_prompt_templates.md) の開始例を使うか、目的を直接伝えてください。

- 到達点、環境、予算、未決事項を state に残す。
- 既存の source / contract / run と次の作業を引き継ぐ。
- API が利用できない場合は公式 Web / 手動 snapshot を代替にし、未取得範囲を記録する。
- Agent や client を変えても、判断と実験の正本は `aidlc-docs/` と run artifacts に維持する。

Install command や client の細かな設定は公式の最新手順を参照し、調査日時と利用版を audit に残します。

## 用語の引継ぎ

開始・再開時は問題設定文書の「用語と名称」を読む。専門用語は初出で説明し、独自の呼び名を増やさない。
報告前に、何を変え、何と比べ、何が分かったかを具体的に書けているか確認する。
[用語と説明のガイド](07_terminology.md) に定義の記録方法と例を示す。
