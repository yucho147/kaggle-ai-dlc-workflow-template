# Lessons Learned

| Lesson | Evidence | Applicability |
| --- | --- | --- |
| 空の雛形と記入済み案件を同一視しない | 旧完全一致 CI、derived project test | workflow template の初期化・更新・再開 |
| Installed help を外部 main の文書と区別する | Kaggle 2.2.4 download に --unzip がない | CLI / SDK 更新時の互換性確認 |
| 取得した本文と metadata を区別する | 旧 overview、metadata_only contract | Web / MCP を使う調査全般 |
| Data fallback は明示的な mode にする | 欠落 CSV regression | baseline / PoC の結果解釈 |
| 前処理と出力対応を契約として検証する | fold fit spy、OOF、ID permutation tests | tabular 分類。時間・group には別評価が必要 |
| Model の tracker と依存を記録する | model URI resolution / requirements / manifest tests | MLflow 3 local tracking。別環境再構築は追加確認 |
| Workflow は依頼の目的に合わせる | src001、4 skills のレビュー | 調査のみ・非 Kaggle PoC・実装のみの依頼 |

最後の workflow 有用性は設計上の判断。実際の案件での質問数や時間削減を実測したとは扱わない。

## 後から理解できる説明

- 普通の操作に独自の略語や比喩を作らず、対象と操作を書く。
- 一般的な専門用語は初出で説明する。繰り返し使う名称の定義は問題設定文書に保存し、再開時に読む。
- 実験 ID と変更内容を併記し、比較条件と実測値を具体的に残す。
- 報告前に、前の会話を知らない読み手にも対象・変更・比較・結果が分かるか確認する。
- 書き方の例と名称の変更方法は [用語と説明のガイド](../../docs/07_terminology.md) を参照する。
