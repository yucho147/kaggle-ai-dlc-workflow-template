# GitHub Copilot CLI Entry Point

このリポジトリは、Kaggle / 技術調査を AI-DLC 風に進めるための workflow template です。

GitHub Copilot CLI で作業を始める場合は、まず以下を読ませてください。

1. `AGENTS.md`
2. `docs/00_project_concept.md`
3. `docs/02_quickstart.md`
4. `docs/03_prompt_templates.md`
5. `docs/01_agent_execution_guide.md`
6. `aidlc-docs/`

## Interactive Start

```bash
copilot
```

起動後、以下を貼ります。

```text
このリポジトリでは、Kaggle / 技術調査を AI-DLC 風に進めます。

AGENTS.md、docs/00_project_concept.md、docs/02_quickstart.md、docs/03_prompt_templates.md、aidlc-docs/ を読み、現在のワークフロー構成を理解してください。

今回の目的が未確定であれば、competition-starter / competition-winning / technical-research / implementation-only / knowledge-reuse のどれかを確認してください。

実装は、Inception の最小ドキュメントと Construction の設計ドキュメントが揃うまで開始しないでください。
新規コードでは、Hydra / loguru / MLflow と Kaggle MCP / Gateway 境界を標準にしてください。
実装前に implementation-questionnaire.md と architecture.md を更新してください。
外部情報を取得した場合は aidlc-docs/audit.md に記録してください。
```

## Non-Interactive Start

```bash
copilot -p "AGENTS.md、docs/00_project_concept.md、docs/02_quickstart.md、docs/03_prompt_templates.md、aidlc-docs/ を読み、この workflow template の現在状態と次に確認すべきことを整理してください。"
```
