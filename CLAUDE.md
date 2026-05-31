@AGENTS.md

# Claude Code Entry Point

Claude Code reads `CLAUDE.md` at session start. The shared project instructions are imported from `AGENTS.md` above.

## Additional Claude Code Notes

- Also read `docs/00_project_concept.md`, `docs/02_quickstart.md`, `docs/03_prompt_templates.md`, and `aidlc-docs/` before starting workflow tasks.
- Use `uv` for Python and dependency management.
- Repository skills live under `.agents/skills/`.
- If the purpose is unclear, ask whether the task is `competition-starter`, `competition-winning`, `technical-research`, `implementation-only`, or `knowledge-reuse`.
- Do not start implementation until the minimum Inception docs and Construction design docs are filled in.
- For new code, align architecture with `aidlc-docs/construction/implementation-questionnaire.md` and `architecture.md`.
- Prefer Hydra, loguru, MLflow, and a Kaggle MCP / Gateway boundary for new implementations.
- When asking humans to review experiment results or choose the next hypothesis, regenerate the HTML report and point them to `outputs/reports/improvement-report.html` and MLflow UI instead of using Markdown as the main review surface.
