# Improvement Loop

## Current Review

今回のテンプレート改訂と local checks は完了。
ユーザーが改訂内容を読めるよう、正本から HTML report を生成する。
Synthetic の比較結果は環境確認。次のモデル改善仮説を選ぶ根拠ではない。

## Next Use

1. 新規案件では `--new-project` で保守記録を backup し、空の seed に切り替える。
2. 目的・到達点・環境・予算から workflow と必要文書を選ぶ。
3. 出典、data / evaluation contract、最小 baseline と停止条件を決める。
4. 同一評価条件で実験し、失敗・slice・費用・限界を記録する。
5. 次候補を docs に反映して HTML を再生成し、採否と優先順位を判断する。

## Maintenance Follow-up

実案件で、質問の繰返し、契約の不足、再開のしやすさを観測する。
Dependency / CLI / client を更新した場合は version / help / protocol / regression を再実行する。

```bash
uv run python scripts/render_improvement_report.py
uv run --group research mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1
```

Tracking URI を変更したら UI にも同じ URI を渡す。DB と artifact store を両方保存する。

## 説明の確認

HTML の再生成前に次を確認する。詳しい方針は [用語と説明のガイド](../../docs/07_terminology.md)。

- 前の会話を知らなくても、対象のデータ・変更した処理・比較条件・結果が分かる。
- 略語は初出で説明し、繰り返し使う名称は [問題設定の用語集](../inception/problem-overview.md#用語と名称) と一致する。
- 独自の略語や比喩は具体的な表現に直す。必要な案件固有名には定義と参照を付ける。
- 実験は既存 ID と変更内容で示す。呼び名を変更した場合も過去の記録との対応を残す。
