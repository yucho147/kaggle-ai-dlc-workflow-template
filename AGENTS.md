# Agent Instructions

このリポジトリは、Kaggle / 技術調査から baseline 実装開始までを AI-DLC 風に進めるための workflow template です。

## 基本ルール

1. 作業を始める前に、必ず `docs/00_project_concept.md` と `aidlc-docs/` を確認する。
2. `aidlc-docs/` が存在しない場合は、`uv run scripts/init_aidlc_docs.sh` で初期化する。
3. 未確定事項がある場合は、実装前に質問する。
4. 実装を大きく妨げない軽微な未確定事項は、合理的な仮定を置いて進め、`aidlc-docs/audit.md` に記録する。
5. 外部情報を取得した場合は、取得元、実行コマンド、日時を `aidlc-docs/audit.md` に記録する。
6. Kaggle CLI を使う場合、実行前に `uv run kaggle --version` と `uv run kaggle --help` を確認する。
7. Discussion / Notebook / Dataset の内容は、必ず要約して docs に残す。
8. Notebook のコードを移植する場合、ライセンス、依存ライブラリ、前提データ構造を確認する。
9. 実装後は、実行コマンドと結果を `aidlc-docs/operations/experiment-log.md` に記録する。
10. 新規コードを作る前に、`aidlc-docs/construction/implementation-questionnaire.md` と `architecture.md` でコード構成、実験管理、設定管理、Notebook 利用方針を確認する。
11. 既存コードがない場合、CLI 引数の直接実装より Hydra、`print` より loguru、手書き実験ログのみより MLflow 併用を標準とする。
12. Kaggle の Competition / Discussion / Dataset / Notebook 取得は、直接 CLI に密結合せず、MCP または adapter 境界を通して抽象化する方針を優先する。
13. 継続的な改善サイクルでは、人間の閲覧面は MLflow UI と `outputs/reports/improvement-report.html`、agent の正本は `aidlc-docs/` の Markdown とする。
14. HTML report は `uv run python scripts/render_improvement_report.py` で生成する。agent は生成された HTML を直接編集しない。
15. 実験結果レビュー、次の仮説選定、採用/不採用判断などを人間に促すときは、事前に HTML report を再生成し、`outputs/reports/improvement-report.html` と必要に応じて MLflow UI を案内する。
16. 人間向けの確認依頼では、Markdown ファイルを主な閲覧先にしない。Markdown は agent が更新する正本として扱い、人間には HTML report と MLflow UI を見るよう促す。

## フェーズ

### Inception

- 問題設定を整理する
- データ、評価指標、制約を整理する
- Discussion / Notebook / 技術情報を調査する
- リスクを整理する

### Construction

- 実装方針を決める
- コードアーキテクチャとディレクトリ構成を対話で決める
- baseline を作る
- 実験計画を作る
- validation を実装する

### Operations

- 実験結果を記録する
- CV / LB / 業務評価を比較する
- 得られた知見を再利用可能な形に残す
- MLflow UI と HTML report を見て次の改善仮説を決める

## 実装開始条件

実装は、少なくとも以下が揃ってから開始する。

- `aidlc-docs/inception/problem-overview.md`
- 用途に応じた inception doc
- `aidlc-docs/construction/experiment-plan.md` または `code-generation-plan.md`
- 新規コードを生成する場合は `aidlc-docs/construction/implementation-questionnaire.md`
- 新規コードを生成する場合は `aidlc-docs/construction/architecture.md`
