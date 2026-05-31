# Kaggle / Technical Research AI-DLC Workflow Template

Kaggle コンペ参加、勝ち筋調査、業務 PoC / 技術調査を AI-DLC 風に進めるためのテンプレートです。

詳細な構想は [docs/00_project_concept.md](docs/00_project_concept.md) を参照してください。

## 新しいプロジェクトを始める

**このリポジトリは GitHub Template Repository です。**

新しい Kaggle コンペや技術調査プロジェクトを始めるときは、このリポジトリをコピーして専用リポジトリを作ります。

1. GitHub の **「Use this template」** ボタン → 「Create a new repository」
2. 新しいリポジトリに clone して作業を開始する

```bash
git clone https://github.com/<your-org>/<your-project>.git
cd <your-project>
uv sync
```

3. Coding Agent を起動して、やりたいことを話しかける

```
titanic コンペの参加準備をしたい
異常検知の PoC を始めたい
```

どう話しかければいいか迷ったときは [docs/03_prompt_templates.md](docs/03_prompt_templates.md) を参考にしてください。

> **このテンプレートリポジトリを直接の作業場として使わないでください。**
> `aidlc-docs/` はプロジェクト固有のドキュメントを書く場所です。テンプレート側を汚染しないよう、新規プロジェクトごとに別リポジトリを作ってください。

---

## 目的

このテンプレートは、情報収集で止めずに以下まで進めることを目的にします。

- 問題設定、評価指標、データ構造の整理
- Discussion / Notebook / 既存実装からの知見抽出
- baseline 実装方針の決定
- coding agent が実装を開始できる spec の作成
- 実験ログと判断履歴の蓄積

## 派生リポジトリでの初期化

新しいリポジトリを作った後、依存関係を同期します。

```bash
uv sync
```

`aidlc-docs/` はすでにプレースホルダーが入った状態で含まれています。そのまま Coding Agent を起動して作業を開始してください。

最短手順は [docs/02_quickstart.md](docs/02_quickstart.md) を参照してください。

## Coding Agent での実行

Codex、GitHub Copilot CLI、Claude Code を起動して、やりたいことを普通に話しかけるだけで動きます。

```
titanic コンペの参加準備をしたい
異常検知の PoC を始めたい
```

どう話しかければいいか迷ったときは [docs/03_prompt_templates.md](docs/03_prompt_templates.md) に用途別のプロンプト例をまとめています。

各ツールのセットアップは [docs/01_agent_execution_guide.md](docs/01_agent_execution_guide.md) を参照してください。

Claude Code 向けの入口は [CLAUDE.md](CLAUDE.md)、GitHub Copilot CLI 向けの入口は [COPILOT.md](COPILOT.md) と [.github/copilot-instructions.md](.github/copilot-instructions.md) にも置いています。

## Kaggle データ取得

Kaggle の Competition / Discussion / Notebook / Dataset 情報取得は、MCP または `KaggleGateway` 境界を通す方針を標準にします。このテンプレートには最小 MCP server を `tools/kaggle-mcp/` に含めています。

```bash
uv run --group mcp python tools/kaggle-mcp/server.py
```

MCP server の詳細は [tools/kaggle-mcp/README.md](tools/kaggle-mcp/README.md) を参照してください。
Kaggle 認証の初期設定は [docs/04_kaggle_auth_setup.md](docs/04_kaggle_auth_setup.md) を参照してください。

MCP が使えない場合は CLI adapter fallback として、Kaggle API 認証設定済みの環境で `uv run` 経由の Kaggle CLI を使います。

```bash
uv run scripts/download_kaggle_competition.sh <competition-slug>
```

例:

```bash
uv run scripts/download_kaggle_competition.sh titanic
```

ダウンロード先は `data/raw/<competition-slug>/` です。

## 新規実装の標準

既存コードの制約がない場合、新規 baseline は以下を標準にします。

- 設定管理: Hydra
- Logging: loguru
- 実験管理: MLflow
- 共通ロジック: `src/<package_name>/` 配下に分離
- Notebook: EDA / orchestration として使い、core logic は `src` から import
- Kaggle access: MCP / Gateway 優先、CLI adapter fallback

## ディレクトリ構成と役割

```text
.
├── docs/                      # ワークフロー解説・プロンプト集（テンプレート共通）
├── templates/aidlc-docs/      # aidlc-docs/ の正本テンプレート
├── aidlc-docs/                # プロジェクト固有のドキュメント（派生リポジトリで記入する）
├── .agents/skills/            # Coding Agent skill 定義
├── scripts/                   # 初期化・データ取得スクリプト
├── configs/                   # Hydra 設定テンプレート
├── data/                      # データ（raw/interim/processed/external）
├── notebooks/                 # EDA・baseline Notebook
├── notebooks_external/        # 外部 Notebook キャッシュ
├── src/                       # 共通ロジック
├── tools/kaggle-mcp/          # Kaggle MCP server
└── outputs/                   # モデル・予測・提出ファイル
```

`templates/aidlc-docs/` と `aidlc-docs/` は常に同一内容を保ちます。CI がこれを検証します（`.github/workflows/check-template-sync.yml`）。  
`aidlc-docs/` のファイルをテンプレートにリセットしたい場合:

```bash
uv run scripts/init_aidlc_docs.sh --force
```

テンプレートとの差分を確認したい場合:

```bash
uv run scripts/init_aidlc_docs.sh --check
```
