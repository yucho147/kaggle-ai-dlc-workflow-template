# kaggle-starter

Kaggle competition の参加開始時に、データ、評価指標、提出形式、初期 EDA / baseline 方針を整理するための skill です。

## 入力

- Kaggle competition slug
- 任意: 実行環境、GPU 有無、Notebook first / script first の希望

## 手順

1. `docs/00_project_concept.md` と `AGENTS.md` を読む。
2. `aidlc-docs/` がなければ `scripts/init_aidlc_docs.sh` を実行する。
3. Kaggle CLI の利用可否を確認する。
   - `kaggle --version`
   - `kaggle --help`
4. コンペ情報を確認する。
   - `kaggle competitions files -c <competition>`
   - 必要に応じて Kaggle Web ページや rules / overview / evaluation を確認する。
5. データを `data/raw/<competition>/` に取得する。
   - `scripts/download_kaggle_competition.sh <competition>`
6. `train` / `test` / `sample_submission` の構造を確認する。
7. 評価指標、target、id column、submission columns を特定する。
8. 欠損、型、サイズ、分布、リーク可能性を確認する。
9. 最初の baseline 方針と validation 方針を作る。
10. 判断、仮定、外部情報源を `aidlc-docs/audit.md` に記録する。

## 出力

- `aidlc-docs/inception/kaggle-starter.md`
- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/construction/experiment-plan.md`
- 必要に応じて `notebooks/00_eda.ipynb` / `notebooks/01_baseline.ipynb` の作成計画

## 完了条件

- コンペ概要が整理されている。
- 評価指標が説明されている。
- データファイルと主要カラムが把握されている。
- `sample_submission` と同形式の提出ファイルを作る方針がある。
- 最初に作る baseline と validation 方法が決まっている。

