# Problem Overview

## Summary / Goal

2026-10-04、ユーザーからこのリポジトリの詳細な精査と改訂を依頼された。
Kaggle 参加・解法調査・業務 PoC / 技術調査を、用途と予算に応じた工程で進め、
根拠、評価条件、実験、採否、引継ぎを追跡できるテンプレートにする。

今回は `template-maintenance`。新しいコンペや業務モデルの開発ではない。

## Scope

- 共通 docs、27 seed docs、4 skills、Agent 入口と MCP 設定。
- 記録を保全する初期化、Kaggle 取得境界、baseline、HTML generator、依存 lock、CI。
- 現在の案件記録と空の雛形を分離し、派生案件の実際の記入を許容する。

## Success Criteria

| Criterion | Evidence |
| --- | --- |
| 初期化で既存記録と独自ファイルを保全 | missing-only / backup / fresh project 回帰検証 |
| 記入済みの派生案件が構造検査を通る | derived project fixture と validation workflow |
| 外部仕様の版と取得内容を明示 | source register、actual CLI help、MCP response contract |
| 指定データ欠落と不正な出力で停止 | CSV / submission 回帰検証 |
| 前処理・OOF・比較・実験証跡が対応 | fold 内 fit、dummy 比較、manifest / MLflow |
| 結果と限界を閲覧できる | 生成 HTML、移行手順、実行記録 |

## Constraints / Assumptions

- 既存 Python 3.13 と Hydra / loguru / MLflow を継続する。
- CPU の小規模 synthetic と local fixtures を使う。コンペデータ取得、提出、クラウド実験は実施しない。
- 学習コードに汎用 gateway framework を持ち込まず、情報取得の境界だけ共有する。
- 実データの品質やモデル性能、各 client の認証・対話起動は今回のローカル検証では確定しない。

改訂内容は [Technical Research](technical-research.md)、検証は [Experiment Log](../operations/experiment-log.md) にまとめる。

## 追加の到達点: 後から理解できる用語と記録

ユーザーから、Coding Agent が一般的ではない用語を使い、後から記録を理解できなくなる問題への対策を依頼された。
共通指示に具体的な表現・初出の説明・名称の一貫性・報告前の確認を追加する。
用語の定義はこの節の下に保存し、生成 HTML からも読めるようにする。
新しいファイル形式や検査プログラムは追加せず、既存の記録・報告経路を使う。

## 用語と名称

| 名称 / 略語 | 種別 | 平易な意味・適用範囲 | 具体例 / コード / 出典 | 旧名・変更理由・日付 |
| --- | --- | --- | --- | --- |
| CV（Cross-validation） | 一般用語 | データを分け、学習に使わなかった部分で性能を評価する交差検証 | この baseline は 5 分割。分割方法は evaluation-contract.md | 該当なし |
| OOF（Out-of-fold prediction） | 一般用語 | 各行を学習に含めなかったモデルが出した予測 | outputs/runs/ の oof.csv。列・対応は実験の manifest を参照 | 該当なし |
| LB（Leaderboard） | 公式名称 | Kaggle の提出結果を掲載する順位表。Public と Private では評価対象が異なる | 対象コンペの公式評価説明を参照。今回の保守では提出なし | 該当なし |
| PoC（Proof of concept） | 一般用語 | 業務で使う前に、実現可能性と効果を限定した範囲で確かめる検証 | operations/poc-decision.md に採否と条件を記録 | 該当なし |
| baseline | 一般用語 | 改善案と比較する基準の実装・結果 | 付属 src/baseline/ は合成データによる動作確認と表形式分類の例 | 該当なし |
| seed docs | 案件固有 | 新しい案件へコピーする、未記入の文書雛形。このリポジトリ内での呼称 | templates/aidlc-docs/。案件の実記録は aidlc-docs/ | 今後の説明では「文書雛形」を優先。2026-10-04 |
| artifact | 一般用語 | 実行で生成・保存されたファイルなどの成果物 | 予測 CSV、モデル、確定した設定。outputs/runs/ と MLflow に保存 | 該当なし |
| run manifest | 案件固有 | 一回の実行と、その入力・設定・結果・保存先の対応を記録したファイル | src/baseline/train.py が生成する manifest.json | 今後の説明では「実行の対応記録」を併記。2026-10-04 |
| Gate（G0〜G3） | 案件固有 | 各工程の完了条件と、その確認状況。このテンプレートでの区分 | aidlc-state.md の Gates 表。問題設定・実装準備・結果確認・引継ぎ | 今後の説明では「工程の完了条件」を併記。2026-10-04 |

既存記録の識別子は保全する。新しい案件では、その案件に必要な名称だけを定義する。
具体例と報告前の確認は [用語と説明のガイド](../../docs/07_terminology.md) を参照する。
