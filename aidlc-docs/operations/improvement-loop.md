# Improvement Loop

## Purpose

継続的な精度改善では、人間が仮説と優先順位を決め、agent が実装、実行、ログ記録を担当する。
このドキュメントは、その役割分担と成果物の置き場所を固定する。

## Source of Truth

| 種別 | ファイル / 画面 | 役割 | 編集者 |
| --- | --- | --- | --- |
| Human review | MLflow UI | metrics、params、artifacts、model を比較する | 人間が閲覧 |
| Human review | `outputs/reports/improvement-report.html` | 実験候補、結果、CV/LB、学びをブラウザで読む | script で生成 |
| Agent source | `aidlc-docs/construction/experiment-plan.md` | 仮説、期待効果、実験候補、優先順位 | 人間 + agent |
| Agent source | `aidlc-docs/construction/code-generation-plan.md` | 次に agent が実装する狭い spec | agent |
| Agent source | `aidlc-docs/operations/experiment-log.md` | 実行 command、config、MLflow run、結果の事実 | agent |
| Agent source | `aidlc-docs/operations/cv-lb-tracking.md` | CV/LB の比較と信頼度 | 人間 + agent |
| Agent source | `aidlc-docs/operations/lessons-learned.md` | 採用、不採用、再利用知見 | 人間 + agent |

HTML は閲覧用の生成物であり、正本ではない。agent は HTML を直接編集しない。

## Loop State

```text
idea
  -> selected
  -> specced
  -> implemented
  -> executed
  -> reviewed
  -> adopted / rejected / iterate
```

## Human Responsibilities

- MLflow UI と `outputs/reports/improvement-report.html` を見て、次に試す仮説を選ぶ。
- `experiment-plan.md` の priority、expected impact、stop condition を更新する。
- CV と LB の乖離、リーク懸念、実行コストを判断する。
- `lessons-learned.md` に採用・不採用理由を残す。

## Agent Responsibilities

- 実装前に `experiment-plan.md` と `code-generation-plan.md` を確認する。
- 実装内容を小さく保ち、Hydra config / loguru / MLflow logging を維持する。
- 実行後に `experiment-log.md` と `cv-lb-tracking.md` を更新する。
- HTML report を再生成する。
- 実験結果レビュー、次の仮説選定、採用/不採用判断を人間に依頼するときは、Markdown ではなく MLflow UI と HTML report に誘導する。

## Human Confirmation Prompt

agent が人間に判断を依頼する場合は、以下の順序にする。

1. `uv run python scripts/render_improvement_report.py` を実行して HTML report を更新する。
2. MLflow UI が必要な場合は、起動コマンドまたは URL を案内する。
3. `outputs/reports/improvement-report.html` を案内する。
4. 人間には「MLflow UI と HTML report を見て判断してください」と依頼する。
5. Markdown は必要に応じて参照元として示すが、主な閲覧先にはしない。

## Commands

MLflow UI:

```bash
uv run --group research mlflow ui --backend-store-uri sqlite:///mlruns.db
```

Human review HTML:

```bash
uv run python scripts/render_improvement_report.py
```

出力先:

```text
outputs/reports/improvement-report.html
```

## Rules

- 実験 ID は `exp001`, `exp002` のように連番にする。
- 人間の仮説は、実装前に `experiment-plan.md` に残す。
- agent は実行後、command、config、data、CV、LB、MLflow run ID、artifact path を `experiment-log.md` に残す。
- 結果レビュー後、status は `adopted`, `rejected`, `iterate` のいずれかに寄せる。
- HTML の見た目は `docs/assets/improvement-report.css` で管理する。
- 人間への確認依頼では、`outputs/reports/improvement-report.html` と MLflow UI を優先して案内する。
