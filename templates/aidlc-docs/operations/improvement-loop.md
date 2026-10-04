# Improvement Loop

## Roles / Sources

- 人間: 成功条件、計算予算、採否、次の優先順位を判断する。
- Agent: 出典付き仮説を提案し、依頼範囲で実装・実行・結果記録・報告を行う。
- 正本: `aidlc-docs/` の Markdown。Metrics / artifacts は MLflow と local run directory。
- 閲覧面: `outputs/reports/improvement-report.html`、必要に応じて MLflow UI。

## Cycle

`idea -> selected -> specced -> implemented -> executed -> reviewed -> adopted / rejected / iterate`

1. 結果と失敗類型から仮説を立て、反証条件と予算を付ける。
2. 同一 data / split / metric で比較できる最小変更を選ぶ。
3. 小規模確認後に実行し、run の事実と限界を記録する。
4. 解釈と次候補を更新してから HTML を生成する。
5. 改善幅、ばらつき、費用、推論制約を含めて判断する。

依頼済み範囲は再承認を求めない。目的変更、予算増、未許可の提出・公開等が必要なら、その判断に必要な資料を先に揃える。

## Review Commands

```bash
uv run python scripts/render_improvement_report.py
uv run --group research mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1
```

Tracking URI を変更したら UI にも同じ URI を渡す。DB だけでなく artifact store も保全する。

## Current Review

- 比較 run / 判断したいこと: TBD
- 有力候補・理由・期待効果・費用: TBD
- 未確認事項と次に解消する作業: TBD

## 説明の確認

HTML の再生成前に次を確認する。詳しい方針は [用語と説明のガイド](../../docs/07_terminology.md)。

- 前の会話を知らなくても、対象のデータ・変更した処理・比較条件・結果が分かる。
- 略語は初出で説明し、繰り返し使う名称は [問題設定の用語集](../inception/problem-overview.md#用語と名称) と一致する。
- 独自の略語や比喩は具体的な表現に直す。必要な案件固有名には定義と参照を付ける。
- 実験は既存 ID と変更内容で示す。呼び名を変更した場合も過去の記録との対応を残す。
