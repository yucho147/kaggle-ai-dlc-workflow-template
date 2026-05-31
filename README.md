# Kaggle / Technical Research AI-DLC Workflow Template

Kaggle コンペ参加、勝ち筋調査、業務 PoC / 技術調査を AI-DLC 風に進めるためのテンプレートです。

詳細な構想は [docs/00_project_concept.md](docs/00_project_concept.md) を参照してください。

## 目的

このテンプレートは、情報収集で止めずに以下まで進めることを目的にします。

- 問題設定、評価指標、データ構造の整理
- Discussion / Notebook / 既存実装からの知見抽出
- baseline 実装方針の決定
- coding agent が実装を開始できる spec の作成
- 実験ログと判断履歴の蓄積

## 初期化

新しい案件で AI-DLC docs を作る場合:

```bash
scripts/init_aidlc_docs.sh
```

既存ファイルは上書きしません。テンプレートは `templates/aidlc-docs/` にあります。

最短手順は [docs/02_quickstart.md](docs/02_quickstart.md) を参照してください。

## Coding Agent での実行

Codex、GitHub Copilot CLI、Claude Code での実行方法は [docs/01_agent_execution_guide.md](docs/01_agent_execution_guide.md) にまとめています。

Claude Code 向けの入口は [CLAUDE.md](CLAUDE.md)、GitHub Copilot CLI 向けの入口は [COPILOT.md](COPILOT.md) にも置いています。

## Kaggle データ取得

Kaggle CLI と認証設定が済んでいる場合:

```bash
scripts/download_kaggle_competition.sh <competition-slug>
```

例:

```bash
scripts/download_kaggle_competition.sh titanic
```

ダウンロード先は `data/raw/<competition-slug>/` です。

## 標準ディレクトリ

```text
.
├── docs/
├── templates/aidlc-docs/
├── aidlc-docs/
├── skills/
├── scripts/
├── configs/
├── data/
├── notebooks/
├── notebooks_external/
├── src/
└── outputs/
```

`aidlc-docs/` は案件ごとの作業ログです。テンプレートリポジトリでは `scripts/init_aidlc_docs.sh` で生成します。
