# Kaggle / Technical Research AI-DLC Workflow 構想

## 1. 背景

Kaggle CLI の最近のアップデートにより、Competition / Dataset / Kernel / Model だけでなく、Discussion Forum も CLI から閲覧できるようになった。公式 CLI README でも “Browse and read discussion forums” が主要機能として明記されている。

また、competition discussion については、`kaggle competitions topics list` でトピック一覧を取得し、`kaggle competitions topics show <TOPIC_REF>` で本文とコメントツリーを表示できる。

この変化により、Kaggle Discussion / Notebook / Dataset / Model を coding agent から取得し、コンペ参加や技術調査の初動を大幅に標準化できる可能性がある。

参考:
- Kaggle CLI: competitions topics list / show
- Kaggle CLI: discussion forums browsing
- AWS AI-DLC / awslabs aidlc-workflows

## 2. 目的

本構想の目的は、以下の3用途を標準化することである。

1. Competition Starter
   - コンペ参加開始時に必要な基礎情報を整理する
   - コンペ概要、評価指標、データ構造、提出形式、EDA 方針を docs に残す

2. Competition Winning Research
   - Discussion / Notebook / Writeup から勝ち筋を抽出する
   - CV戦略、モデル、特徴量、外部データ、リーク、LB乖離、失敗例を整理する
   - その後の対話を通じて戦略立案につなげる

3. General Technical Research
   - Kaggle コンペ以外の技術収集にも使う
   - 業務テーマ、研究テーマ、PoC の初動調査を標準化する
   - Kaggle / GitHub / arXiv / Hugging Face / Papers with Code / 公式Docs などを対象にする

最終的には、情報収集で終わらず、以下まで到達する。

- 実装候補の整理
- プロジェクト構成案の作成
- baseline 実装方針の決定
- coding agent が実装を開始できる spec の作成

## 3. 設計思想

本ワークフローでは、AWS の AI-DLC 的な考え方を導入する。

AI-DLC は、AI を中心に据えた開発ライフサイクルであり、AI に実装を丸投げするのではなく、人間が判断者・検証者として関与しながら、要件、設計、実装、テスト、運用を段階的に進める考え方である。

awslabs/aidlc-workflows では、成果物を `aidlc-docs/` 配下に Markdown として蓄積し、`aidlc-state.md` で進捗を追跡し、`audit.md` で対話や判断を記録する構成が示されている。

本構想では、Kaggle / 技術調査を以下の AI-DLC フェーズに対応させる。

```text
Inception
  - 何を解くのか
  - 何が重要なのか
  - 既存知見は何か
  - 勝ち筋やリスクは何か

Construction
  - どう実装するか
  - どのコード構成にするか
  - どの baseline から始めるか
  - どう実験するか

Operations
  - 実験結果をどう記録するか
  - CV / LB / 業務評価をどう追うか
  - 得た知見をどう再利用資産化するか
```

## 4. MCP / Skills / CLI の役割分担

### 4.1 Skills

Skills は、作業手順・調査観点・出力形式を標準化するために使う。

本構想では、価値の中心は「情報取得」ではなく「情報をどう解釈し、実装に接続するか」にある。

そのため、Skills には以下を定義する。

- 調査順序
- 参照すべき情報源
- 重要視する観点
- 出力ドキュメントの形式
- coding agent への次アクション

### 4.2 CLI

Kaggle CLI は、現時点で最も軽量な実行手段として使う。

特に以下を想定する。

```bash
kaggle competitions list
kaggle competitions files -c <competition>
kaggle competitions download -c <competition>
kaggle competitions submissions -c <competition>

kaggle competitions topics list <competition> -s recent
kaggle competitions topics show <competition>/<topic-id>

kaggle kernels list --search "<query>"
kaggle kernels pull <owner>/<kernel> -p notebooks_external/<kernel>
kaggle kernels output <owner>/<kernel> -p outputs/kernels/<kernel>

kaggle datasets list -s "<query>"
kaggle datasets download <owner>/<dataset> -p data/external/<dataset>
```

### 4.3 MCP

MCP は必須ではない。

初期段階では、Skills + CLI で十分に始められる。

ただし、以下が必要になった場合は MCP 化を検討する。

- 毎回同じ CLI 操作が多い
- 出力パースが面倒
- Claude Desktop / Claude Code / Cursor / Copilot など複数環境から共通利用したい
- 認証、保存先、キャッシュ、レート制限、再試行処理を隠蔽したい
- `get_top_discussions_with_comments` のような高レベル操作を作りたい

整理すると以下である。

```text
Skills = 調査・実装開始までの作業標準
CLI    = 軽量な外部情報取得手段
MCP    = 必要に応じて作る高レベルな道具
```

## 5. 想定ディレクトリ構成

最初は以下の構成を標準とする。

```text
.
├── README.md
├── pyproject.toml
├── .gitignore
├── AGENTS.md
├── aidlc-docs/
│   ├── aidlc-state.md
│   ├── audit.md
│   ├── inception/
│   │   ├── problem-overview.md
│   │   ├── kaggle-starter.md
│   │   ├── winning-research.md
│   │   ├── technical-research.md
│   │   ├── risk-assessment.md
│   │   └── strategy.md
│   ├── construction/
│   │   ├── implementation-candidates.md
│   │   ├── architecture.md
│   │   ├── code-generation-plan.md
│   │   ├── experiment-plan.md
│   │   └── build-and-test/
│   │       ├── build-instructions.md
│   │       ├── unit-test-instructions.md
│   │       ├── validation-instructions.md
│   │       └── experiment-runbook.md
│   └── operations/
│       ├── improvement-loop.md
│       ├── experiment-log.md
│       ├── cv-lb-tracking.md
│       ├── lessons-learned.md
│       └── reusable-patterns.md
├── configs/
│   └── baseline.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── notebooks/                 # 必要に応じて作成する EDA / baseline / error analysis Notebook
├── notebooks_external/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data.py
│   ├── features.py
│   ├── model.py
│   ├── train.py
│   ├── predict.py
│   ├── evaluate.py
│   └── submission.py
├── scripts/
│   ├── download_data.sh
│   ├── run_eda.sh
│   ├── run_baseline.sh
│   └── make_submission.sh
└── outputs/
    ├── models/
    ├── predictions/
    ├── submissions/
    └── reports/
```

## 6. Workflow 全体像

### 6.1 Competition Starter

目的:

- コンペを理解する
- 最初の EDA / baseline に入れる状態にする

入力:

- Kaggle competition slug
- 例: `titanic`, `playground-series-s5e5`

実行内容:

- コンペ概要を確認
- 評価指標を確認
- データファイル一覧を取得
- データをダウンロード
- `train` / `test` / `sample_submission` を確認
- `target` / `id` / `submission columns` を特定
- 欠損、型、サイズ、分布を確認
- 最初の baseline 方針を作成

出力:

- `aidlc-docs/inception/kaggle-starter.md`
- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/construction/experiment-plan.md`
- 必要に応じて EDA / baseline Notebook の作成計画

完了条件:

- データが `data/raw/` に存在する
- 評価指標が説明されている
- `sample_submission` と同形式の提出ファイルを作る方針がある
- baseline 実装の対象ファイルが決まっている

### 6.2 Competition Winning Research

目的:

- Discussion / Notebook / Writeup から勝ち筋を整理する
- 戦略立案の材料を docs に残す

入力:

- Kaggle competition slug
- 任意: 調査対象トピック数、Notebook 数、重視観点

実行内容:

- Discussion topics を `recent` / `votes` / `comments` などで取得
- 上位トピックを読む
- コメントツリーを読む
- Notebook を検索・取得
- 使えそうな実装・特徴量・モデル・CV 戦略を抽出
- 禁止事項、リーク、LB 乖離、失敗例を整理
- 自分の戦略案に落とす

想定コマンド:

```bash
kaggle competitions topics list <competition> -s recent
kaggle competitions topics list <competition> -s hot
kaggle competitions topics show <competition>/<topic-id>

kaggle kernels list --search "<competition>"
kaggle kernels pull <owner>/<kernel> -p notebooks_external/<kernel>
```

出力:

- `aidlc-docs/inception/winning-research.md`
- `aidlc-docs/inception/risk-assessment.md`
- `aidlc-docs/inception/strategy.md`
- `aidlc-docs/construction/implementation-candidates.md`

完了条件:

- 有力手法が複数整理されている
- CV 戦略が整理されている
- 実装候補 Notebook / Code が特定されている
- 最初に試すべき実験が優先順位付きで整理されている

### 6.3 General Technical Research

目的:

- コンペ以外の技術調査にも同じ流れを適用する
- 業務テーマや研究テーマを PoC 開始可能な状態にする

入力:

技術テーマ
例:

- 衛星画像セグメンテーション
- 時系列予測

実行内容:

- 問題設定を明確化
- 既存手法を調査
- Kaggle Dataset / Notebook / Discussion を検索
- GitHub 実装を検索
- 公式 Docs / 論文 / Hugging Face model を確認
- 業務データへの適用可能性を評価
- PoC 実装方針を作る

出力:

- `aidlc-docs/inception/technical-research.md`
- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/inception/risk-assessment.md`
- `aidlc-docs/construction/architecture.md`
- `aidlc-docs/construction/code-generation-plan.md`

完了条件:

- 技術テーマの要約がある
- 候補手法が整理されている
- 実装候補がある
- PoC の最小スコープが定義されている
- baseline 実装に入れる

## 7. Skill 設計案

### 7.1 kaggle-starter Skill

役割:

- コンペ参加開始時に必要な情報を docs に整理する

必ず確認すること:

- コンペの目的
- タスク種別
- 評価指標
- データファイル
- target
- id column
- submission format
- データサイズ
- 欠損
- 代表的な EDA
- 最初の baseline

出力:

- `aidlc-docs/inception/kaggle-starter.md`
- `aidlc-docs/construction/experiment-plan.md`

### 7.2 kaggle-winning-research Skill

役割:

- Discussion / Notebook から勝ち筋を抽出する

必ず分類すること:

- CV
- Feature Engineering
- Model
- Loss / Metric
- Ensemble
- External Data
- Data Leakage
- LB shakeup
- Inference
- Runtime / Memory
- Failed approaches
- Reusable ideas

出力:

- `aidlc-docs/inception/winning-research.md`
- `aidlc-docs/inception/strategy.md`
- `aidlc-docs/construction/implementation-candidates.md`

### 7.3 technical-research Skill

役割:

- Kaggle 以外も含めた技術調査を行う

必ず確認すること:

- 問題設定
- 既存手法
- 代表論文
- GitHub 実装
- Kaggle 実装
- Hugging Face model / dataset
- 業務データへの転用可能性
- PoC スコープ
- 実装リスク

出力:

- `aidlc-docs/inception/technical-research.md`
- `aidlc-docs/construction/architecture.md`
- `aidlc-docs/construction/code-generation-plan.md`

### 7.4 implementation-harvest Skill

役割:

- Notebook / GitHub から使えるコード構成を抽出する

必ず分類すること:

- Dataset class
- Preprocessing
- Feature Engineering
- Model
- Loss
- Metric
- Training loop
- Inference
- Submission
- Config
- Dependency
- GPU / memory consideration

出力:

- `aidlc-docs/construction/implementation-candidates.md`

### 7.5 implementation-planner Skill

役割:

- 実装開始に必要な spec を作る

必ず決めること:

- baseline 方針
- ディレクトリ構成
- 実装対象ファイル
- 設定ファイル
- 実行コマンド
- テスト方針
- 最初の実験
- 完了条件

出力:

- `aidlc-docs/construction/code-generation-plan.md`
- `aidlc-docs/construction/build-and-test/build-instructions.md`
- `aidlc-docs/construction/build-and-test/validation-instructions.md`

## 8. Coding Agent への基本指示案

AGENTS.md または CLAUDE.md に以下のような方針を書く。

```markdown
# Agent Instructions

このプロジェクトでは、Kaggle / 技術調査から baseline 実装開始までを AI-DLC 風に進める。

## 基本ルール

1. 実装を始める前に、必ず `aidlc-docs/` を確認する。
2. 未確定事項がある場合は、実装前に質問する。
3. ただし、実装を大きく妨げない軽微な未確定事項は、合理的な仮定を置いて進め、`aidlc-docs/audit.md` に記録する。
4. 外部情報を取得した場合は、取得元、実行コマンド、日時を記録する。
5. Kaggle CLI を使う場合、実行前に `kaggle --version` と `kaggle --help` を確認する。
6. Discussion / Notebook / Dataset の内容は、必ず要約して docs に残す。
7. Notebook のコードを移植する場合、ライセンス、依存ライブラリ、前提データ構造を確認する。
8. 実装後は、実行コマンドと結果を `aidlc-docs/operations/experiment-log.md` に記録する。

## フェーズ

### Inception

- 問題設定を整理する
- データ、評価指標、制約を整理する
- Discussion / Notebook / 技術情報を調査する
- リスクを整理する

### Construction

- 実装方針を決める
- baseline を作る
- 実験計画を作る
- validation を実装する

### Operations

- 実験結果を記録する
- CV / LB / 業務評価を比較する
- 得られた知見を再利用可能な形に残す
```

## 9. Coding Agent が最初に質問すべきこと

coding agent は、最初に以下を確認する。

### 9.1 用途

今回の目的はどれか？

- competition-starter
- competition-winning
- technical-research
- implementation-only
- knowledge-reuse

### 9.2 対象

- Kaggle competition slug は何か？
- 技術調査テーマは何か？
- 業務データを想定するか？
- Kaggle 以外の情報源も使うか？

### 9.3 実行環境

- ローカルで実行するか？
- Kaggle Notebook 上で実行するか？
- Colab / Vast.ai / EC2 などを使うか？
- GPU は必要か？
- Python バージョンは？
- パッケージ管理は uv でよいか？

### 9.4 成果物

最終成果物は何か？

- 調査ドキュメント
- baseline notebook
- Python package
- submission file
- PoC script
- report

### 9.5 制約

- コンペルール上、外部データは使えるか？
- Internet access は使えるか？
- 実行時間制限はあるか？
- メモリ制限はあるか？
- チーム開発か個人開発か？

## 10. 日本語プロンプト群

coding agent に貼り付けるプロンプトは [docs/03_prompt_templates.md](03_prompt_templates.md) にまとめる。

このテンプレートのユーザーは日本語話者が多い想定のため、プロンプト本文、設計質問、実装前確認事項は日本語を標準とする。ライブラリ名、config key、module name、command などは英語表記のままでよい。

プロンプト群には以下を含める。

- 共通開始プロンプト
- Kaggle Starter
- Kaggle Winning Research
- Technical Research
- 実装前設計の擦り合わせ
- Baseline 実装依頼
- Kaggle MCP 設計依頼

## 11. 実装前設計の追加方針

Titanic での試行では、`train.py` に設定読込、特徴量、前処理、model factory、CV、保存処理が集中しやすく、モデル追加や validation 変更が同じファイルに波及しやすいことが分かった。

そのため、新規コードでは以下を標準方針とする。

- 新規設定管理は argparse ではなく Hydra。
- 実行ログは `print` ではなく loguru。
- 実験管理は MLflow を必須にし、Kaggle 提出用 artifact は local `outputs/` にも保存する。
- Notebook 管理を選ぶ場合も、core logic は `src/<package_name>/` から import する。
- Kaggle Discussion / Notebook / Dataset / Competition metadata の取得は、`tools/kaggle-mcp/` の MCP server または `KaggleGateway` interface を優先し、CLI は adapter fallback にする。
- Technical Research でも Kaggle Competition / Discussion / Notebook / Dataset を MCP 経由で探索し、論文・公式 Docs・GitHub・Hugging Face と比較して最良候補を選ぶ。
- 実装前に `aidlc-docs/construction/implementation-questionnaire.md` と `architecture.md` を埋める。

## 12. 完了条件

この workflow の最小完了条件は以下とする。

### Starter 完了条件

- コンペ概要が整理されている
- 評価指標が説明されている
- データ構造が把握されている
- 提出形式が把握されている
- EDA の開始方針がある
- baseline の開始方針がある

### Winning Research 完了条件

- 重要 Discussion が整理されている
- 有力 Notebook / Writeup が整理されている
- 勝ち筋の候補がある
- リスクと禁止事項が整理されている
- 最初の実験計画がある

### Technical Research 完了条件

- 技術テーマが整理されている
- 候補手法が整理されている
- 実装候補が整理されている
- PoC 方針がある
- baseline 実装計画がある

### Implementation Plan 完了条件

- ディレクトリ構成が決まっている
- 実装対象ファイルが決まっている
- 実行コマンドが決まっている
- validation 方法が決まっている
- 最初の実験が決まっている

## 13. 現在の実装状況

このテンプレートには、以下が既に含まれている。

- `AGENTS.md` / `CLAUDE.md` / `COPILOT.md` / `.github/copilot-instructions.md`
- `.codex/config.toml` の Codex project-scoped MCP 設定
- `aidlc-docs/` と `templates/aidlc-docs/` の初期テンプレート
- `.agents/skills/kaggle-starter/SKILL.md`
- `.agents/skills/kaggle-winning-research/SKILL.md`
- `.agents/skills/technical-research/SKILL.md`
- `scripts/init_aidlc_docs.sh`
- `scripts/download_kaggle_competition.sh`
- `tools/kaggle-mcp/` の最小 Kaggle MCP server
- `configs/baseline.yaml` と `src/baseline/` の Hydra / loguru / MLflow smoke baseline
- `aidlc-docs/operations/improvement-loop.md` による継続改善ループ定義
- `scripts/render_improvement_report.py` と `docs/assets/improvement-report.css` による人間向け HTML report 生成
- `.github/workflows/check-template-sync.yml` による `aidlc-docs/` 同期確認

Notebook template は標準同梱しない。Notebook が必要なプロジェクトでは、`aidlc-docs/construction/implementation-questionnaire.md` と `architecture.md` で方針を決めたうえで、必要に応じて作成する。

## 14. 今後の改善候補

将来的には以下を検討する。

- Kaggle MCP tool の高レベル化と出力 schema の安定化
- Discussion の embedding / RAG 化
- 必要に応じた Notebook code extraction
- winning pattern database
- reusable feature engineering library
- competition archetype classifier
- 業務テーマ向け PoC generator
- 実験ログ自動集計
- CV / LB tracking dashboard

---

補足すると、AWS の AI-DLC は `aidlc-docs/` 配下に成果物を生成・管理する考え方があり、`aidlc-state.md` や `audit.md` で状態追跡・監査ログを持つ構成が紹介されています。

また、Kaggle CLI は公式に Discussion forum の閲覧に対応しており、`kaggle competitions topics list` と `kaggle competitions topics show` でコンペ Discussion の一覧・本文・コメントツリーを扱えます。
