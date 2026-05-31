# Quickstart

このテンプレートを使って、Kaggle コンペまたは業務 PoC / 技術調査を始めるための最短手順です。

## 1. 初期化

リポジトリのルートで実行します。

このプロジェクトは `uv` で Python と依存関係を管理します。Python は最新安定版の 3.14 系を前提にします。

```bash
uv sync
```

AI-DLC docs を初期化します。

```bash
uv run scripts/init_aidlc_docs.sh
```

既存の `aidlc-docs/` ファイルは上書きされません。

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

どの coding agent でも、起動後に以下を貼ります。

```text
このリポジトリでは、Kaggle / 技術調査を AI-DLC 風に進めます。

まず docs/00_project_concept.md、docs/02_quickstart.md、AGENTS.md、aidlc-docs/ を読み、現在のワークフロー構成を理解してください。

今回の目的が未確定であれば、以下を確認してください。

- 用途: competition-starter / competition-winning / technical-research / implementation-only / knowledge-reuse
- 対象: Kaggle competition slug または技術調査テーマ
- 実行環境: local / Kaggle Notebook / Colab / EC2 / Vast.ai など
- 成果物: 調査ドキュメント / baseline notebook / Python package / submission file / PoC script / report
- 制約: 外部データ、Internet access、実行時間、メモリ、チーム開発か個人開発か

実装は、Inception の最小ドキュメントが揃うまで開始しないでください。
外部情報を取得した場合は、日時、URL、実行コマンド、判断を aidlc-docs/audit.md に記録してください。
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
aidlc-docs/construction/experiment-plan.md を作成または更新してください。

実装は、これらの骨子が揃ってから開始してください。
```

Kaggle CLI が使える場合、データ取得は以下で行えます。

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
aidlc-docs/construction/code-generation-plan.md を作成または更新してください。

実装は、PoC の最小スコープと validation 方針が決まってから開始してください。
```

## 7. 完了条件

実装に入る前に、最低限以下が揃っている状態を目指します。

- 何を解くかが `problem-overview.md` に書かれている。
- 評価指標または成功条件が明確になっている。
- 使うデータ、制約、リスクが整理されている。
- 最初に作る baseline または PoC の範囲が決まっている。
- 実行コマンド、validation 方法、成果物の置き場所が決まっている。

