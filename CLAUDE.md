@AGENTS.md

# Claude Code Entry Point

Claude Code reads `CLAUDE.md` at session start. The shared project instructions are imported from `AGENTS.md` above.

## Additional Claude Code Notes

- Also read `docs/00_project_concept.md`, `docs/02_quickstart.md`, `docs/03_prompt_templates.md`, and `aidlc-docs/` before starting workflow tasks.
- Use `uv` for Python and dependency management.
- Repository skills live under `.agents/skills/`. In Claude Code, these are available as slash commands under `.claude/commands/`.
- If the purpose is unclear, ask whether the task is `competition-starter`, `competition-winning`, `technical-research`, `implementation-only`, or `knowledge-reuse`.
- Do not start implementation until the minimum Inception docs and Construction design docs are filled in.
- For new code, align architecture with `aidlc-docs/construction/implementation-questionnaire.md` and `architecture.md`.
- Prefer Hydra, loguru, MLflow, and a Kaggle MCP / Gateway boundary for new implementations.
- When asking humans to review experiment results or choose the next hypothesis, regenerate the HTML report and point them to `outputs/reports/improvement-report.html` and MLflow UI instead of using Markdown as the main review surface.

## Slash Commands (Claude Code)

The following project-specific slash commands are available:

| Command | Use case |
| --- | --- |
| `/kaggle-starter <competition-slug>` | Kaggle コンペ参加開始: データ・評価指標・baseline 方針を整理する |
| `/kaggle-winning-research <competition-slug>` | Discussion / Notebook から勝ち筋・失敗例・実装候補を抽出する |
| `/technical-research <theme>` | 業務 PoC / 技術調査: 候補手法・実装候補・PoC スコープを整理する |
| `/improvement-review` | 継続改善: HTML report 再生成・次の仮説選定を人間に案内する |

MCP サーバー (`kaggle`, `arxiv`, `huggingface`) は `.mcp.json` で設定済みです。`.claude/settings.local.json` で有効化されています。
