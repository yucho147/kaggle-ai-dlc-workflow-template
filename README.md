# Kaggle / Technical Research AI-DLC Workflow Template

Kaggle コンペ参加、勝ち筋調査、業務 PoC / 技術調査を、問題設定から評価・改善・引継ぎまでつなぐ日本語テンプレートです。AI-DLC の考え方を、実験と調査向けに応用しています。

人間が目的・予算・採否を決め、agent が調査、設計、実装、実行記録を進めます。調査だけの依頼でも使えます。

## 新しい案件を始める

GitHub の **Use this template** で案件ごとのリポジトリを作り、clone します。

```bash
cd <your-project>
uv sync --locked
uv run scripts/init_aidlc_docs.sh --new-project
uv run python scripts/render_improvement_report.py
```

`--new-project` は既存の `aidlc-docs/` を `outputs/doc-backups/` に保管し、空の雛形から始めます。
通常の再開では初期化を繰り返す必要はありません。欠落ファイルだけ補う場合は引数なしで実行します。

Coding Agent に、そのまま依頼できます。

```text
titanic の参加準備をしてください。今回は調査と baseline 計画まで進めたいです。
異常検知の PoC を検討しています。現行ルールと比較し、2週間で採否を決めたいです。
```

[最短手順](docs/02_quickstart.md) · [用途別プロンプト](docs/03_prompt_templates.md) · [Agent 設定](docs/01_agent_execution_guide.md)

## 用途と到達点

| 用途 | 整理すること | 完了の目安 |
| --- | --- | --- |
| competition-starter | 規約、データ、評価、提出、初期 CV | 最初の baseline を試せる計画 |
| competition-winning | Discussion / 解法 / 実装の証拠と条件 | 優先仮説と反証方法 |
| technical-research | 現行手法、候補技術、自データへの適用 | PoC 範囲と go / no-go 条件 |
| implementation-only | 既存の決定を確認して実装 | 再実行可能な成果物と評価 |
| knowledge-reuse | 結果、失敗例、適用条件 | 根拠付き再利用知見 |

用途に関係する文書だけ埋めます。調査から実装へ進むときは、データと評価の契約、最小変更、構成、実行方法を確定します。
詳細は [設計方針とゲート](docs/00_project_concept.md) を参照してください。

## 付属ツールを使う

| 目的 | 依存関係 |
| --- | --- |
| 文書・HTML report・Kaggle CLI | `uv sync --locked` |
| baseline | `uv sync --locked --group research` |
| Kaggle MCP | `uv sync --locked --group mcp` |
| Notebook / 可視化 | `uv sync --locked --group research --group notebooks` |

### Kaggle 情報取得

```bash
uv run kaggle --version
uv run kaggle --help
uv run kaggle competitions files <competition>
uv run scripts/download_kaggle_competition.sh <competition>
```

ダウンロード先は `data/raw/<competition>/`。サイズ・規約・利用範囲を先に確認します。
[認証](docs/04_kaggle_auth_setup.md) · [MCP 設定](docs/05_mcp_setup.md) · [MCP の契約](tools/kaggle-mcp/README.md)

MCP は任意です。付属サーバーは取得用 CLI 境界であり、学習コードは固定した local data から実行します。

### 環境確認用 baseline

```bash
uv run --group research python -m baseline.train
```

合成データで Hydra / loguru / MLflow / fold 内前処理 / OOF 保存を確認する例です。
成果物は `outputs/runs/<run_id>/`、tracking は `sqlite:///mlruns.db`。**この score はコンペや業務の性能を示しません。**

CSV モードでは欠落したファイルをエラーにし、提出には sample submission・ID・予測方式を指定します。
[baseline の範囲と設定例](docs/02_quickstart.md#baseline-を実データへ接続する) を確認してから使います。

### 結果のレビュー

```bash
uv run python scripts/render_improvement_report.py
uv run --group research mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1
```

人間の閲覧先は `outputs/reports/improvement-report.html` と MLflow UI。agent は `aidlc-docs/` を編集し、HTML を再生成します。
Tracker が使えない環境では local artifacts を保全し、その限界を記録します。
ブラウザーで file を開けない場合は [localhost での閲覧手順](docs/02_quickstart.md#閲覧と再開) を使えます。

## 正本と記録

```text
docs/                       共通の使い方・プロンプト・保守履歴
templates/aidlc-docs/        空の雛形
aidlc-docs/                  現在の案件の状態・出典・契約・実験・判断
.agents/skills/             用途別の作業手順
configs/ / src/baseline/     環境確認と小規模 tabular 分類の実行例
scripts/                    初期化・取得・報告・構造検査
tools/kaggle-mcp/            Kaggle CLI の取得境界
tests/                      データ保持・評価・提出・外部境界の回帰検証
outputs/ / data/            local artifacts・取得データ（Git 管理対象外）
```

**`templates/aidlc-docs/` と `aidlc-docs/` の内容一致は要求しません。** CI は雛形・設定・実行契約を検査し、案件記録の編集を許容します。
このテンプレート自体の保守記録も `aidlc-docs/` にあります。新規案件では上記 `--new-project` で切り替えます。

```bash
# 欠落だけ補充 / 必要ファイルの存在を確認
uv run scripts/init_aidlc_docs.sh
uv run scripts/init_aidlc_docs.sh --check

# テンプレートと実装の検査
uv run python scripts/check_template.py
uv run --group research --group mcp pytest
```

2026-10-04 の詳細な変更理由・検証範囲は [改訂記録](docs/06_template_review.md) にまとめています。

## 後から読める用語と実験記録

Agent は一般的な用語と具体的な説明を使い、略語は初出で説明します。
繰り返し使う名称は問題設定文書の「用語と名称」に保存し、再開時に引き継ぎます。
実験名には ID と変更内容を添え、報告前に意味が伝わるか確認します。
詳細は [用語と説明のガイド](docs/07_terminology.md)。用語集は生成 HTML の Problem Overview にも表示されます。
