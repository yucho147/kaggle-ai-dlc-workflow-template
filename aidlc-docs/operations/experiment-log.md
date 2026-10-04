# Experiment Log

## Verification — 2026-10-04 JST

実行環境: Python 3.13.5 / macOS 26.7.1 arm64 / local CPU。
Git: 1f23cf401b813dbeb634b5cab087f3fcd5c4194b、dirty=true（今回の改訂、未コミット）。
Command には `UV_CACHE_DIR=.cache/uv` を付けた。GPU・クラウド・実コンペの API / download / submission は使用していない。

| Check | Command / method | Result |
| --- | --- | --- |
| Dependency lock / install | uv lock、Kaggle / SDK の targeted upgrade、uv sync --locked --group research --group mcp | succeeded |
| Regression | uv run --no-sync pytest -q | 最終66 passed in 10.20s、exit 0 |
| Lint | uv run --no-sync ruff check . | All checks passed、exit 0 |
| Structural validation | uv run --no-sync python scripts/check_template.py | 0 errors。記入内容と seed の一致は要求しない |
| Skills | skill-creator quick_validate.py を4つの SKILL.md に実行 | 4件とも valid |
| Shell wrappers | bash -n、initializer --check | syntax / missing-file check 成功 |
| MCP protocol fixture | pytest の stdio ClientSession | initialize / 12 tools / annotations / fake CLI version 成功 |
| MCP actual CLI | stdio ClientSession → kaggle_cli_version | initialize / 12 tools / Kaggle 2.2.4 / help ok。認証付き API は未確認 |
| Report | Markdown / links / table / raw HTML / navigation regression、正本から再生成、Chrome / localhost 閲覧 | semantic checks 成功。desktop の表・本文・section link を確認 |
| CI workflow | YAML parse / trigger / permission / steps の local check | 成功。GitHub-hosted 実行は未実施 |

## smoke001 — Standard Synthetic Baseline

- Status / exit code: succeeded / 0。
- Command: `uv run --locked --group research --group mcp python -m baseline.train`。
- Resolved config / artifacts: `outputs/runs/20261004T030812209639Z-ef8af264/config.yaml`、`manifest.json`、`metrics.json`、`oof.csv`、`model.joblib`、`run.log`。
- Local run ID: `20261004T030812209639Z-ef8af264`。
- MLflow URI / run ID: `sqlite:///mlruns.db`（実行時に root 基準の絶対 URI へ解決） / `2306cd91e5424639b9a4ba8358e39215`。
- Model URI: `models:/m-7f985cd4945b4086ab64a57d99c9c70d`。読み込み時は同じ tracking URI を指定する。
- Start / finish UTC: 2026-10-04T03:08:12.217976+00:00 / 2026-10-04T03:08:14.226268+00:00。
- Manifest duration: 2.017s（最終 artifact upload 前まで、local runtime。費用は計測していない）。
- Data: synthetic、1,000 rows、20 numeric features、seed42、SHA256 `e32beae901edd99eb707cab4eb3d42acd6194d56142653c3b2b61162a3777413`。
- Split: stratified 5-fold、SHA256 `d415982608d84a14922ce9a6ab49dff9d07de76b19fd580409a6cb1f3c4afd34`。
- Metric: accuracy / maximize / unweighted fold mean。Fold scores: 0.870, 0.935, 0.905, 0.870, 0.870。
- Candidate mean / std: 0.8900 / 0.02627。Dummy mean / std: 0.5000 / 0.0000。
- OOF の全行・fold 対応と local / MLflow artifacts の保存を確認。Submission は test 未指定のため生成しない。
- **Score は環境確認用であり、コンペや業務での品質を示さない。**

## Failures / Revisions During Verification

- Lint が unused import を検出し、削除して再実行した。
- 65件の拡張検証時に1件失敗。`models:/` の解決が test process の default tracking URI を参照していた。対象 URI を明示して復元する test に修正し、再実行で成功。
- Boolean-only features が SimpleImputer の bool dtype 制約で失敗することを観測。Categorical 入力を object に変換する処理と回帰検証を追加。
- Hydra が root に train.log を作っていたため、job logging を無効化して loguru の run.log に集約。生成済み log は旧 run directory へ保全。
- MLflow の自動 uv export は group の実行依存を完全に表すとは限らないため、model の pip requirements を明示。回帰検証で requirements と model artifact、local / MLflow manifest の一致を確認。
- HTML の file URL は Chrome で ERR_ACCESS_DENIED。生成 report directory だけを localhost に一時配信して表示・表・section 移動を確認した。小さい画面の実機表示は未検証。

## Not Run / Limits

認証付き Kaggle API、private resource、各 coding client の対話起動、GitHub-hosted Linux CI、
別環境での model requirements 再構築、実コンペデータ・LB・業務評価は未実行。
完了は依頼されたテンプレート改訂と local validation の範囲。

## 追加改訂: 用語と説明のルール

- Date: 2026-10-04（JST）。文書の変更であり、学習実験ではない。
- Changes: 共通指示、説明ガイド、用語表、再開時の参照、実験名の書き方、報告前の確認を追加。
- Command: `UV_CACHE_DIR=.cache/uv uv run --no-sync python scripts/render_improvement_report.py --title 'AI-DLC テンプレート改訂レビュー — 用語と説明のガードレール'`
- Result: exit code 0、outputs/reports/improvement-report.html を生成。用語表は既存の Problem Overview セクションに含める。
- この文書改訂でテストは実行していない。先行するテンプレート改訂の 66 件成功とは区別する。
