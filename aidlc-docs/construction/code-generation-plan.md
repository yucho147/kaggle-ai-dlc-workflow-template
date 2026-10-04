# Code Generation Plan

## Scope / Inputs

ユーザーが依頼した template-maintenance。既存構想、全 tracked files、CLI help、公式資料をレビュー。
判断は problem-overview / questionnaire / architecture と audit に記録済み。

## Implementation

1. 共通 docs と27 seed docs を改訂。source / data / evaluation / PoC decision を追加。
2. 既存記録を保全する initializer と、shared CLI boundary を実装。
3. Baseline の silent fallback、fold 前処理、OOF、提出 ID / 予測方式、run 記録を修正。
4. Maintained Markdown parser で HTML を生成し、調査と PoC の文書も閲覧可能にする。
5. Canonical skill、thin commands、最小 client config、optional groups を整合。
6. Derived project の記録を許容する CI と意味のある回帰検証を実施。
7. 実行結果、audit、改訂理由を更新し HTML を生成。

## Required Checks

- initializer の missing-only / backup / fresh project と独自記録保全。
- CLI の actual parser、failure / timeout / bounded snapshots、取得先・archive 制約。
- Baseline の CSV missing failure、fold 内 fit、OOF coverage、単純比較、submission ID alignment。
- Report の tables / escaped HTML / unsafe links / root-relative local links。
- Template config / links / skill metadata / symlink の構造。
- End-to-end synthetic smoke と MCP initialize / tool list / version（network API とは区別）。

## Budget / Recovery

CPU の小規模 synthetic と local fixtures を使用。コンペデータ・GPU・クラウド実験を開始しない。
Run と reset は一意の directory に保存し、失敗時の証跡を保全する。
