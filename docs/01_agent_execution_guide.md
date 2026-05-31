# Agent Execution Guide

このテンプレートを Codex、GitHub Copilot CLI、Claude Code で実行するための手順です。

各ツールに共通して、最初にこのリポジトリのルートへ移動してから実行します。

```bash
cd /path/to/kaggle_mcp
```

初回は AI-DLC docs を生成します。

```bash
scripts/init_aidlc_docs.sh
```

## 共通の開始プロンプト

どの coding agent でも、最初は以下のプロンプトを渡します。

```text
このリポジトリでは、Kaggle / 技術調査を AI-DLC 風に進めます。

まず docs/00_project_concept.md、AGENTS.md、aidlc-docs/ を読み、現在のワークフロー構成を理解してください。

今回の目的が未確定であれば、以下を確認してください。

- 用途: competition-starter / competition-winning / technical-research / implementation-only / knowledge-reuse
- 対象: Kaggle competition slug または技術調査テーマ
- 実行環境: local / Kaggle Notebook / Colab / EC2 / Vast.ai など
- 成果物: 調査ドキュメント / baseline notebook / Python package / submission file / PoC script / report
- 制約: 外部データ、Internet access、実行時間、メモリ、チーム開発か個人開発か

実装は、Inception の最小ドキュメントが揃うまで開始しないでください。
```

## Codex CLI

### インストール

公式 docs では、macOS / Linux の standalone installer が案内されています。

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### 対話実行

```bash
cd /path/to/kaggle_mcp
codex
```

起動後、共通の開始プロンプトを貼り付けます。

### このテンプレートでの使い方

Kaggle Starter を始める場合:

```text
Kaggle competition starter を実施してください。

対象コンペ:
<competition-slug>

まず docs/00_project_concept.md、AGENTS.md、skills/kaggle-starter/SKILL.md、aidlc-docs/ を読んでください。
Kaggle CLI の利用可否を確認し、必要な情報を aidlc-docs/ に整理してください。
実装は、problem-overview.md と kaggle-starter.md と experiment-plan.md の骨子が揃ってから開始してください。
```

Technical Research を始める場合:

```text
General technical research を実施してください。

技術テーマ:
<technical-theme>

docs/00_project_concept.md、AGENTS.md、skills/technical-research/SKILL.md、aidlc-docs/ を読み、
problem-overview.md、technical-research.md、risk-assessment.md、code-generation-plan.md を整理してください。
```

## GitHub Copilot CLI

### インストール

公式 docs では、Node.js 22 以降での npm インストール、または Homebrew が案内されています。

```bash
npm install -g @github/copilot
```

macOS / Linux で Homebrew を使う場合:

```bash
brew install copilot-cli
```

### 認証

```bash
copilot
```

対話セッション内で:

```text
/login
```

またはコマンドとして:

```bash
copilot login
```

### 対話実行

```bash
cd /path/to/kaggle_mcp
copilot
```

起動後、共通の開始プロンプトを貼り付けます。

### 非対話実行

単発で依頼する場合は `-p` を使います。

```bash
copilot -p "docs/00_project_concept.md、AGENTS.md、aidlc-docs/ を読み、このテンプレートの現在状態を要約してください。"
```

Kaggle Starter の初動を依頼する場合:

```bash
copilot -p "Kaggle competition starter を開始します。対象コンペは <competition-slug> です。docs/00_project_concept.md、AGENTS.md、skills/kaggle-starter/SKILL.md、aidlc-docs/ を読み、実装前に必要な確認事項を整理してください。"
```

## Claude Code

### インストール

公式 docs では、macOS / Linux / WSL で以下の native install が案内されています。

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Homebrew を使う場合:

```bash
brew install --cask claude-code
```

### 対話実行

```bash
cd /path/to/kaggle_mcp
claude
```

初回はブラウザ認証が求められます。起動後、共通の開始プロンプトを貼り付けます。

### このテンプレートでの使い方

Claude Code はプロジェクトファイルを読ませながら進めやすいので、最初に以下を依頼します。

```text
docs/00_project_concept.md、AGENTS.md、aidlc-docs/ を読んで、この workflow template の使い方を把握してください。
その後、今回の目的が competition-starter / competition-winning / technical-research のどれかを確認してください。
未確定事項があれば質問し、実装前に aidlc-docs/audit.md に仮定と判断を記録してください。
```

## 推奨運用

### 1. テンプレート改善

このリポジトリ自体を改善する場合は、まず以下を依頼します。

```text
このリポジトリは Kaggle / 技術調査向けの workflow template です。
docs/00_project_concept.md と AGENTS.md を読み、テンプレートとして不足している docs、scripts、skills をレビューしてください。
変更する場合は、既存の構想と整合する最小差分にしてください。
```

### 2. 新しい Kaggle コンペ

```text
Kaggle competition starter を実施してください。

対象コンペ:
<competition-slug>

目的:
コンペ概要、評価指標、データ構造、提出形式、初期 EDA / baseline 方針を aidlc-docs/ に整理し、
baseline 実装に入れる状態にすること。
```

### 3. 業務 PoC / 技術調査

```text
General technical research を実施してください。

技術テーマ:
<technical-theme>

目的:
既存手法、実装候補、適用リスク、PoC の最小スコープを整理し、
baseline 実装計画を aidlc-docs/ に落とすこと。
```

## 注意点

- coding agent に実装を依頼する前に、必ず `aidlc-docs/inception/` の最小ドキュメントを埋める。
- 外部情報を調査した場合は、日時、URL、実行コマンド、判断を `aidlc-docs/audit.md` に残す。
- Kaggle の rules、外部データ可否、Internet access 可否は、実装前に確認する。
- Notebook や GitHub 実装を流用する場合は、ライセンスと前提データ構造を確認する。

## 参考公式ドキュメント

- OpenAI Codex CLI: https://developers.openai.com/codex/cli
- GitHub Copilot CLI quickstart: https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started
- GitHub Copilot CLI command reference: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
- Claude Code quickstart: https://code.claude.com/docs/en/quickstart

