# Quickstart

このテンプレートを使って、Kaggle コンペまたは業務 PoC / 技術調査を始めるための最短手順です。

## 1. 初期化

**このリポジトリは GitHub Template Repository です。「Use this template」で派生リポジトリを作ってから作業してください。**

派生リポジトリで依存関係を同期します。

```bash
uv sync
```

`aidlc-docs/` はすでにプレースホルダーが入った状態で含まれています。`init_aidlc_docs.sh` の実行は不要です。

> テンプレートと `aidlc-docs/` の同期状態を確認したい場合:
> ```bash
> uv run scripts/init_aidlc_docs.sh --check
> ```
> テンプレートの状態にリセットしたい場合:
> ```bash
> uv run scripts/init_aidlc_docs.sh --force
> ```

## 2. 用途を選ぶ

最初に、今回の目的を 1 つ選びます。

| 用途 | 使う場面 | 主な出力 |
| --- | --- | --- |
| `competition-starter` | Kaggle コンペ参加を始める | `kaggle-starter.md`, `problem-overview.md`, `experiment-plan.md` |
| `competition-winning` | Discussion / Notebook から勝ち筋を調べる | `winning-research.md`, `strategy.md`, `implementation-candidates.md` |
| `technical-research` | 業務 PoC / 研究テーマを調査する | `technical-research.md`, `architecture.md`, `code-generation-plan.md` |
| `implementation-only` | 既に方針があり実装だけ進める | `code-generation-plan.md`, build-and-test docs |
| `knowledge-reuse` | 過去知見を再利用可能に整理する | `lessons-learned.md`, `reusable-patterns.md` |

迷った場合は、以下を選びます。

- 新しい Kaggle コンペ: `competition-starter`
- 既に終わったコンペや上位解法調査: `competition-winning`
- 業務アイデア、研究テーマ、PoC 構想: `technical-research`

## 3. Coding Agent を起動する

### Codex

```bash
codex
```

初回はプロジェクトを trust します。起動後に `/skills` と `/mcp` を実行し、3つの repository skill と `kaggle` / `arxiv` / `huggingface` MCP server が表示されることを確認してください。

### GitHub Copilot CLI

```bash
copilot
```

### Claude Code

```bash
claude
```

詳しいセットアップは [docs/01_agent_execution_guide.md](01_agent_execution_guide.md) を参照してください。

## 4. 最初に貼るプロンプト

どの coding agent でも、起動後は [docs/03_prompt_templates.md](03_prompt_templates.md) の「共通開始プロンプト」を貼ります。用途別の詳細プロンプトも同じファイルにまとめています。

```text
このリポジトリでは、Kaggle / 技術調査を AI-DLC 風に進めます。

まず docs/00_project_concept.md、docs/02_quickstart.md、docs/03_prompt_templates.md、AGENTS.md、aidlc-docs/ を読み、現在のワークフロー構成を理解してください。

今回の目的が未確定であれば、以下を確認してください。

- 用途: competition-starter / competition-winning / technical-research / implementation-only / knowledge-reuse
- 対象: Kaggle competition slug または技術調査テーマ
- 実行環境: local / Kaggle Notebook / Colab / cloud VM / CI など
- 実行スタイル: script-first / notebook-first / hybrid
- 成果物: 調査ドキュメント / baseline notebook / Python package / submission file / PoC script / report
- 制約: 外部データ、Internet access、実行時間、メモリ、チーム開発か個人開発か

実装は、Inception の最小ドキュメントと Construction の設計ドキュメントが揃うまで開始しないでください。
外部情報を取得した場合は、日時、URL または tool / command、判断を aidlc-docs/audit.md に記録してください。
```

## 5. Kaggle コンペを始める場合

```text
Kaggle competition starter を実施してください。

対象コンペ:
<competition-slug>

docs/00_project_concept.md、AGENTS.md、.agents/skills/kaggle-starter/SKILL.md、aidlc-docs/ を読み、
コンペ概要、評価指標、データ構造、提出形式、初期 EDA / baseline 方針を整理してください。

まず aidlc-docs/inception/problem-overview.md、
aidlc-docs/inception/kaggle-starter.md、
aidlc-docs/construction/implementation-questionnaire.md、
aidlc-docs/construction/architecture.md、
aidlc-docs/construction/kaggle-data-access.md、
aidlc-docs/construction/experiment-plan.md を作成または更新してください。

実装は、これらの骨子が揃ってから開始してください。
```

Kaggle 情報取得は MCP または KaggleGateway 経由を優先します。最小 MCP server は `tools/kaggle-mcp/` にあります。

```bash
uv run --group mcp python tools/kaggle-mcp/server.py
```

MCP が使えない場合は CLI adapter fallback とし、Kaggle CLI を使う前に `uv run kaggle --version` と `uv run kaggle --help` を確認します。
Kaggle 認証の初期設定は [docs/04_kaggle_auth_setup.md](04_kaggle_auth_setup.md) を参照してください。

```bash
uv run scripts/download_kaggle_competition.sh <competition-slug>
```

## 6. 業務 PoC / 技術調査を始める場合

```text
General technical research を実施してください。

技術テーマ:
<technical-theme>

docs/00_project_concept.md、AGENTS.md、.agents/skills/technical-research/SKILL.md、aidlc-docs/ を読み、
問題設定、既存手法、実装候補、適用リスク、PoC の最小スコープを整理してください。

まず aidlc-docs/inception/problem-overview.md、
aidlc-docs/inception/technical-research.md、
aidlc-docs/inception/risk-assessment.md、
aidlc-docs/construction/implementation-questionnaire.md、
aidlc-docs/construction/architecture.md、
aidlc-docs/construction/code-generation-plan.md を作成または更新してください。

実装は、PoC の最小スコープと validation 方針が決まってから開始してください。
```

## 7. 完了条件

実装に入る前に、最低限以下が揃っている状態を目指します。

- 何を解くかが `problem-overview.md` に書かれている。
- 評価指標または成功条件が明確になっている。
- 使うデータ、制約、リスクが整理されている。
- 最初に作る baseline または PoC の範囲が決まっている。
- コード構成、Notebook 方針、Hydra / loguru / MLflow、Kaggle MCP / adapter 方針が `implementation-questionnaire.md` に書かれている。
- 疎結合な module 分割と data access 境界が `architecture.md` に書かれている。
- 実行コマンド、validation 方法、成果物の置き場所が決まっている。
