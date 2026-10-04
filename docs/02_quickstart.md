# Quickstart

## 新規案件

GitHub の Use this template で案件専用リポジトリを作り、clone します。Python / uv の導入は [uv 公式手順](https://docs.astral.sh/uv/getting-started/installation/) を参照してください。

```bash
cd <your-project>
uv sync --locked
uv run scripts/init_aidlc_docs.sh --new-project
```

既存の AI-DLC 記録は backup を作ってから空の雛形へ切り替わります。
再開時は `aidlc-state.md` の次の作業から続けます。

## Agent に依頼する

[Agent 実行ガイド](01_agent_execution_guide.md) に従って起動し、普通に目的を伝えます。

```text
AGENTS.md と docs/00_project_concept.md、aidlc-docs/ の状態を確認してください。
対象は <コンペ slug / 技術テーマ> です。
今回は <調査まで / 設計まで / baseline 実行まで> を進めてください。
制約は <環境・時間・費用・データ利用範囲> です。
```

[詳細プロンプト](03_prompt_templates.md) は必要な項目だけ使います。
既存情報から答えられる項目は繰り返し質問しません。

## Kaggle を使う

[認証の設定](04_kaggle_auth_setup.md) と対象規約を確認します。

```bash
uv run kaggle --version
uv run kaggle --help
uv run kaggle competitions files <competition>
uv run scripts/download_kaggle_competition.sh <competition>
```

Wrapper は file 一覧を表示し、`data/raw/<competition>/` に download して安全に展開します。
巨大な dataset は必要 file だけ取得するなど、先に範囲とサイズを見積ります。
MCP を使う場合は [設定手順](05_mcp_setup.md) を参照します。

## Baseline の環境確認

```bash
uv sync --locked --group research
uv run --group research python -m baseline.train
```

`configs/baseline.yaml` は `data.mode=synthetic` を明示した例です。
比較用の単純 baseline と random forest を同じ CV で評価し、OOF、fold、config、model、manifest を run ごとに保存します。
Score は環境確認用です。

## Baseline を実データへ接続する

付属例は小規模 CSV の分類、stratified/kfold、1つの予測列に対応します。
欠損・category の前処理は sklearn Pipeline 内で fold ごとに fit します。
Group / time split、regression、画像、LLM、simulation は対象に合わせて実装します。

例: Titanic の label submission。データ取得と契約確認後に実行します。

```bash
uv run --group research python -m baseline.train \
  data.mode=csv data.raw_dir=data/raw/titanic \
  data.train_file=train.csv data.test_file=test.csv \
  data.sample_submission_file=gender_submission.csv \
  data.target=Survived data.id_column=PassengerId \
  submission.column=Survived submission.prediction=label
```

- 指定ファイルがない場合は停止します。
- 提出には sample submission と ID 列を必須にし、test の予測を sample の ID 順に整列します。
- Binary probability は `submission.prediction=probability` と `submission.positive_label` を指定します。
- 複数予測列や ID なしの提出形式は、自分の output contract に合わせて変更します。
- ID・target 以外を全て特徴にする例なので、未来情報・group key・target 派生列を事前に契約に沿って除外してください。
- sklearn scorer は大きいほど良い値です。negative error scorer の符号と、公式 metric の表示を評価契約で区別します。

## 閲覧と再開

```bash
uv run python scripts/render_improvement_report.py
uv run --group research mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1
```

HTML は `outputs/reports/improvement-report.html`。Tracking URI を変えた場合は UI にも同じ URI を渡します。
Run artifacts と tracking DB を両方保存します。

ブラウザーが local file の表示を拒否する環境では、report directory を localhost で表示できます。

```bash
uv run python -m http.server 8000 --bind 127.0.0.1 --directory outputs/reports
```

`http://127.0.0.1:8000/improvement-report.html` を開き、閲覧後は Ctrl+C で終了します。

## 初期化の使い分け

| Command | 挙動 |
| --- | --- |
| 引数なし | 欠落した雛形だけ補う |
| --check | 必要な雛形ファイルの存在を検査。記入内容の完成度は判定しない |
| --force | Backup を作り、雛形ファイルを上書き。独自ファイルは保全 |
| --new-project | Backup を作り、既存の docs を空の雛形に切り替える |
| --target <path> | 別の作業先・一時ディレクトリを指定 |

進行中の案件へテンプレート更新を取り込む場合は、引数なしで欠落補充し、既存文書の変更は diff を確認して移植します。
