# Template Review — 2026-10-04

## 対象と方針

共通文書、AI-DLC 雛形、用途別スキル、Agent 入口・MCP 設定、初期化と取得 script、
baseline、HTML generator、依存関係、CI をレビューして改訂した。

目的は、調査と実験の判断根拠をつなぎ、派生案件で記録を保全しながら使えるテンプレートにすること。
既存 Python 3.13 と Hydra / loguru / MLflow は維持し、用途に応じて工程の深さを変える。

## Findings / Changes

| 既存の問題 | 改訂 | 利用者への影響 |
| --- | --- | --- |
| 案件 docs と seed の完全一致 CI | 構造・設定・リンク・実行契約の検査へ変更 | 案件記録を書いても CI が失敗しない |
| --force が記録を無保護で上書き | backup、missing-only、fresh project を分離 | 再開と新規案件を使い分けられる |
| 初期 audit に過去保守履歴を複製 | seed audit を空にし、保守記録は現在の docs に保存 | --new-project で案件固有の記録を開始できる |
| PoC でも Kaggle 調査を一律必須 | 関連する情報源・必要な工程だけ選択 | 調査だけの依頼や非 ML PoC にも使える |
| 外部主張の根拠・確度が曖昧 | source-register と coverage / failures | 報告、実測、推論を区別できる |
| CV・情報利用時点・出力の定義不足 | data / evaluation contract を追加 | group・時間・ID・予測方式を実装前に確定 |
| 業務評価と終了判断が不足 | PoC thresholds、poc-decision、引継ぎ | 品質・latency・費用を含め採否を判断 |
| 実機 CLI にない -c、--unzip、votes sort | positional args、top、safe local extraction | CLI の版・help に沿って取得 |
| MCP の timeout / failure / snapshot の不足 | 共通 CLI 境界、structured errors、一意 snapshot、bounded response | 失敗・未取得・切り詰めを見落としにくい |
| 指定データ欠落で synthetic へ切替 | explicit synthetic / csv、欠落エラー | smoke score を実データ結果と混同しない |
| 前処理・OOF・比較・提出整列が不足 | fold 内 Pipeline、dummy 比較、OOF、ID alignment、prediction mode | 評価と提出の対応を確認できる |
| 再現情報と artifact が分散 | run directory、config、manifest、data / split hash、versions、MLflow ID | 失敗も含めて再実行・追跡できる |
| Model 依存が自動 export 任せ / root に Hydra log | model requirements と model URI を明示、local / MLflow manifest を照合、loguru に集約 | モデルと実行記録を対応させて保全できる |
| 手書き Markdown rendering の制約 | markdown-it-py、raw HTML 無効、tables / safe links | 調査と PoC docs も HTML で閲覧 |
| 重複した agent instructions / commands | AGENTS と4 skills を正本にし commands は参照 | 更新箇所と判断の一貫性を保てる |
| 汎用 shell 許可、無固定の optional server | 共有許可を絞り、default MCP を Kaggle に整理 | 接続と追加依存を案件ごとに選べる |
| Notebook / columnar を research に全同梱 | optional groups に分離 | baseline に必要な環境を小さく保てる |
| 古い CI action と内容一致だけの検査 | 現行 action のタグを確認して SHA 固定、契約の回帰検証を追加 | 実装と派生運用の両方を検査 |

## Dependency / CLI Evidence

Kaggle CLI を 2.2.0 から2.2.4、yanked kagglesdk 0.1.27 を0.1.37へ更新し、lockfile を更新した。
確認した実機 help と公式 main の説明は区別する。2.2.4 の competition download も --unzip を持たない。
metadata の URL はページ本文の取得を意味しない。

Copilot の project MCP と Kiro の現行 custom-agent resources を公式資料で確認し、入口設定を更新した。
CI action は checkout v7.0.1 / setup-uv v10.1.0 のタグ・SHA を公開 git refs で確認して固定した。

## Validation

| Check | Observed result |
| --- | --- |
| Regression | 66 tests passed（初期化・派生案件・CLI・データ / 評価 / 提出・report・integration） |
| Lint / structure / skills | Ruff 成功、構造0 errors、4 skills valid |
| Actual local MCP | initialize、12 tools、Kaggle CLI 2.2.4 / help 取得成功 |
| Default baseline | synthetic 1,000 rows、seed42、5-fold、正常終了。OOF / config / manifest / model / MLflow を保存 |
| Report | Markdown semantic regression 成功、正本から standalone HTML を生成。Chrome / localhost で表・本文・section 移動を確認 |
| CI / wrappers | YAML 構造と shell syntax 成功。GitHub-hosted CI は未実行 |

Local 実行は Python 3.13.5 / macOS arm64。認証付き Kaggle API、各 coding client の対話起動、
別環境での model 環境再構築、実データ / LB / 業務性能は未検証。
Synthetic score をコンペや業務成果の根拠として扱わない。
Run ID、command、失敗と再試行は案件記録と生成 HTML に残した。

## Migration

新規派生案件:

```bash
uv sync --locked
uv run scripts/init_aidlc_docs.sh --new-project
```

既存案件:

1. aidlc-docs と tracker / artifacts を保全する。
2. 引数なしで欠落雛形を追加し、既存の決定を新しい data / evaluation 契約へ移す。
3. 古い完全一致 CI を、新しい validation workflow へ変更する。
4. CSV mode、sample submission、ID、予測方式、実験出力先を config で明示する。
5. CLI version、依存 lock、client からの MCP 起動を実環境で確認する。

--force は seed ファイルを上書きする。進行中案件の通常更新には使わない。
Backup は local の outputs/doc-backups/ に残るため、必要な案件記録は別途保全する。

## References

- [AWS adaptive workflow principles](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/)
- [Kaggle CLI](https://github.com/Kaggle/kaggle-cli)
- [uv dependency groups](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/quickstart/)
- [Codex skills](https://developers.openai.com/codex/skills) / [MCP](https://developers.openai.com/codex/mcp)
- [Claude project MCP](https://code.claude.com/docs/en/mcp)
- [Copilot project MCP](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers)
- [Kiro custom agents](https://kiro.dev/docs/custom-agents/configuration-reference/)
- [GitHub checkout](https://github.com/actions/checkout) / [Astral setup-uv](https://github.com/astral-sh/setup-uv)

## 追加改訂: 用語と説明

一般的ではない呼び名が増える問題に対し、共通指示と [説明ガイド](07_terminology.md) を追加した。
問題設定文書に用語表を設け、初出の説明、再開時の参照、実験名の具体化、報告前の確認を文書雛形に反映した。
用語表は既存の HTML 生成対象なので、生成プログラムの変更は不要。
この追加改訂は文書のみ。上記のテスト結果は先行する改訂の結果である。
