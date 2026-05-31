# 日本語プロンプト集

このファイルは、coding agent に貼り付けて使う日本語プロンプト集です。新しい Kaggle / 技術調査案件では、まず共通開始プロンプトを使い、その後に用途別プロンプトへ進みます。

## 1. 共通開始プロンプト

```text
このリポジトリでは、Kaggle / 技術調査を AI-DLC 風に進めます。

まず docs/00_project_concept.md、docs/02_quickstart.md、docs/03_prompt_templates.md、AGENTS.md、aidlc-docs/ を読み、現在のワークフロー構成を理解してください。

今回の目的が未確定であれば、実装に入る前に以下を確認してください。

- 用途: competition-starter / competition-winning / technical-research / implementation-only / knowledge-reuse
- 対象: Kaggle competition slug または技術調査テーマ
- 実行環境: local / Kaggle Notebook / Colab / cloud VM / CI など
- 実行スタイル: script-first / notebook-first / hybrid
- 成果物: 調査ドキュメント / baseline notebook / Python package / submission file / PoC script / report
- 制約: 外部データ、Internet access、実行時間、メモリ、チーム開発か個人開発か

実装は、Inception の最小ドキュメントと Construction の設計ドキュメントが揃うまで開始しないでください。
外部情報を取得した場合は、日時、URL または tool / command、判断を aidlc-docs/audit.md に記録してください。
```

## 2. Kaggle Starter

```text
Kaggle competition starter を実施してください。

対象コンペ:
<competition-slug>

目的:
コンペ概要、評価指標、データ構造、提出形式、初期 EDA / baseline 方針を aidlc-docs/ に整理し、baseline 実装に入れる状態にすること。

手順:
1. docs/00_project_concept.md、AGENTS.md、.agents/skills/kaggle-starter/SKILL.md、aidlc-docs/ を読んでください。
2. Kaggle 情報取得は MCP または KaggleGateway 経由を優先してください。MCP がない場合のみ CLI adapter fallback としてください。
3. Kaggle CLI を使う場合は、実行前に uv run kaggle --version と uv run kaggle --help を確認し、aidlc-docs/audit.md に記録してください。
4. aidlc-docs/inception/problem-overview.md と aidlc-docs/inception/kaggle-starter.md を更新してください。
5. 実装前に aidlc-docs/construction/implementation-questionnaire.md を埋め、コード構成、Notebook 方針、Hydra / loguru / MLflow、Kaggle MCP / adapter 方針を確認してください。
6. aidlc-docs/construction/architecture.md、kaggle-data-access.md、experiment-plan.md を更新してください。

実装は、上記ドキュメントの骨子が揃ってから開始してください。
```

## 3. Kaggle Winning Research

```text
Kaggle winning research を実施してください。

対象コンペ:
<competition-slug>

目的:
Discussion / Notebook / Writeup / GitHub 実装から、CV 戦略、特徴量、モデル、ensemble、外部データ、leakage risk、LB shakeup risk、失敗例、再利用できる実装案を抽出すること。

手順:
1. docs/00_project_concept.md、AGENTS.md、.agents/skills/kaggle-winning-research/SKILL.md、aidlc-docs/ を読んでください。
2. Discussion / Notebook の取得は MCP または KaggleGateway 経由を優先し、取得元と日時を aidlc-docs/audit.md に記録してください。
3. 重要 Discussion / Notebook / GitHub 実装は、本文を丸写しせず、要点を aidlc-docs/inception/winning-research.md に要約してください。
4. Notebook や GitHub 実装を移植候補にする場合は、ライセンス、依存ライブラリ、前提データ構造、移植する module を確認してください。
5. aidlc-docs/inception/risk-assessment.md、strategy.md、aidlc-docs/construction/implementation-candidates.md を更新してください。
6. 実装へ進む場合は aidlc-docs/construction/implementation-questionnaire.md と architecture.md を更新し、疎結合な構成に落としてください。
```

## 4. Technical Research

```text
General technical research を実施してください。

技術テーマ:
<technical-theme>

目的:
既存手法、公式 docs、論文、GitHub 実装、Kaggle Competition / Discussion / Notebook / Dataset、Hugging Face などの関連知見を整理し、業務 PoC または baseline 実装に入れる状態にすること。

手順:
1. docs/00_project_concept.md、AGENTS.md、.agents/skills/technical-research/SKILL.md、aidlc-docs/ を読んでください。
2. 問題設定、成功条件、制約、利用データ、評価方法を aidlc-docs/inception/problem-overview.md に整理してください。
3. Kaggle MCP を使い、技術テーマに近い Competition / Dataset / Notebook / Discussion を検索してください。
   - kaggle_competitions_list で関連 competition を探す。
   - 有望な competition は kaggle_discussions_list / kaggle_discussion_get で手法、CV、失敗例、リーク、LB shakeup を確認する。
   - kaggle_notebooks_search で再利用できる実装候補を探す。
   - kaggle_datasets_list で関連 dataset を探す。
4. Kaggle 由来の知見を、論文・公式 docs・GitHub・Hugging Face と比較し、最良候補と採用しない候補を整理してください。
5. 調査した情報源、MCP tool、実行コマンド、取得日時、判断を aidlc-docs/audit.md に記録してください。
6. 実装前に aidlc-docs/construction/implementation-questionnaire.md を埋め、アーキテクチャ、Notebook 方針、Hydra / loguru / MLflow、external service / data access の adapter 境界を確認してください。
7. aidlc-docs/construction/architecture.md と code-generation-plan.md を更新してください。
```

## 5. 実装前設計の擦り合わせ

```text
まだ実装せず、実装前設計だけを擦り合わせてください。

対象:
<competition-slug または technical-theme>

以下の観点を aidlc-docs/construction/implementation-questionnaire.md に質問形式で整理し、回答できるものは仮定を置いて埋めてください。判断に迷うものは実装前に質問してください。

- コンペ種別または技術領域: tabular / CV / NLP / recsys / simulation / code competition / other
- 実行スタイル: script-first / notebook-first / hybrid
- アーキテクチャ: layered / clean-ish / onion / notebook wrapper / competition-specific engine
- ディレクトリ構成: `src/<package_name>/` 配下の module 分割
- 設定管理: 新規コードでは Hydra を使う
- logging: loguru を使う
- 実験管理: MLflow を必須にする
- Notebook 方針: Notebook は `src` の共通ロジックを呼び出す
- Kaggle access: MCP / KaggleGateway を優先し、CLI は adapter fallback にする
- validation: split strategy、metric、leakage check
- submission / PoC output: id column、target column、出力先

その後、aidlc-docs/construction/architecture.md と code-generation-plan.md に、疎結合な実装方針をまとめてください。
```

## 6. Baseline 実装依頼

```text
baseline 実装を開始してください。

実装前に以下を確認してください。

- aidlc-docs/inception/problem-overview.md
- 用途に応じた inception doc
- aidlc-docs/construction/implementation-questionnaire.md
- aidlc-docs/construction/architecture.md
- aidlc-docs/construction/experiment-plan.md または code-generation-plan.md

新規コードの場合は、以下を標準として実装してください。

- Hydra で設定管理する
- loguru で logging する
- MLflow で params / metrics / config / artifacts / submission を記録する
- Kaggle access は KaggleGateway interface 経由にし、MCP adapter 優先、CLI adapter fallback にする
- entrypoint は薄く保ち、data / features / models / validation / tracking / submission を分離する
- Notebook を作る場合も、core logic は `src/<package_name>/` から import する

実装後は、実行コマンドと結果を aidlc-docs/operations/experiment-log.md に記録してください。
```

## 7. Kaggle MCP 設計依頼

```text
Kaggle MCP の設計案を作ってください。

目的:
Kaggle の Competition / Discussion / Notebook / Dataset / Submission 取得を抽象化し、training code や feature code が Kaggle CLI に直接依存しないようにすること。

まず aidlc-docs/construction/kaggle-data-access.md を更新してください。

優先 tool:
1. kaggle_cli_version
2. kaggle_competitions_list
3. kaggle_competition_overview
4. kaggle_competition_files
5. kaggle_competition_download
6. kaggle_discussions_list
7. kaggle_discussion_get
8. kaggle_notebooks_search
9. kaggle_notebook_pull
10. kaggle_datasets_list
11. kaggle_dataset_download
12. kaggle_submissions_list

各 tool の input / output schema、認証情報の扱い、cache directory、rate limit / retry、audit log への記録方法を提案してください。
実装が必要な場合は、まず code-generation-plan.md に実装範囲と file 構成を書いてから進めてください。
```
