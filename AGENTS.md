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

## 実装開始条件

実装は、少なくとも以下が揃ってから開始する。

- `aidlc-docs/inception/problem-overview.md`
- 用途に応じた inception doc
- `aidlc-docs/construction/experiment-plan.md` または `code-generation-plan.md`

