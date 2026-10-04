# 日本語プロンプト集

必要な例を選び、環境や予算が決まっていれば添えます。調査だけの依頼は実装開始まで進める必要はありません。

## 共通開始 / 再開

```text
AGENTS.md、docs/00_project_concept.md、aidlc-docs/ の状態と関連文書を読んでください。
対象: <コンペ slug / 技術テーマ>
到達点: <調査 / 設計 / baseline 実行 / 改善 / 引継ぎ>
環境・予算: <local / Kaggle / cloud、時間・費用上限>
既存の決定を引き継ぎ、重大な未決事項だけ質問してください。
軽微な設計は理由付き仮定を記録して進めてください。
```

## Kaggle Starter

```text
<competition-slug> の参加準備をしてください。
.agents/skills/kaggle-starter/SKILL.md に従い、公式規約・評価・データ・提出形式を確認してください。
今回は <調査と計画まで / baseline 実行まで> を依頼します。
データと評価の契約、最初の baseline、CV の根拠、予算内の実験計画を残してください。
本文未取得や規約未確認は明示し、HTML report を生成してください。
```

## 勝ち筋調査

```text
<competition-slug> の勝ち筋を調査してください。
.agents/skills/kaggle-winning-research/SKILL.md を読み、<優先観点> を重点的に調べてください。
調査上限は <時間 / topic・notebook 件数> です。
Discussion 本文・コメント、writeup、原実装から出典付きの知見を整理してください。
著者の主張と実測を区別し、失敗例、CV/LB の違い、転用条件、優先仮説と反証方法を残してください。
```

## 業務 PoC / 技術調査

```text
<technical-theme> の技術調査と PoC 計画を作ってください。
.agents/skills/technical-research/SKILL.md に従ってください。
業務上の問題: <具体例>
現行の方法: <比較対象>
利用データ・制約: <利用可能な情報 / latency / 費用 / 権限>
期限: <日時>
候補を原資料で比較し、最小 PoC、評価データ、成功・継続・中止の条件を決めてください。
関連する場合は Kaggle / Hugging Face の実装も調べてください。
```

## 実装前設計

```text
今回は設計まで進めてください。
対象: <theme>
既存の問題設定・data / evaluation contract を確認し、
implementation-questionnaire.md、architecture.md、code-generation-plan.md に
最小の構成、設定、tracker、Notebook 方針、実行・検証コマンドを記録してください。
過剰な共通 framework を作らず、実際の変更境界を決めてください。
```

## Baseline / PoC 実装

```text
決定済みの <experiment / hypothesis ID> を実装し、<予算> の範囲で実行してください。
問題、data / evaluation contract、architecture、実験計画を確認し、
不足する重大判断だけ質問してください。
Hydra / loguru / MLflow を標準とし、fold 内 fit と出力契約を検証してください。
Resolved config、data / split version、run ID、OOF、artifact、失敗を含む結果を残し、
HTML report を生成してください。
```

## 継続改善レビュー

```text
.agents/skills/improvement-review/SKILL.md に従い、レビュー資料を準備してください。
同じ評価条件の run を比較し、改善幅・ばらつき・費用・未確認事項を整理してください。
次の仮説を根拠・反証条件・予算付きで提案し、docs を更新してから HTML を生成してください。
採否と次の優先順位を判断できる状態にしてください。
```

## 知見の再利用 / 引継ぎ

```text
<対象 run / 過去案件> の知見を再利用可能に整理してください。
出典、実測、失敗例、適用条件、license、再実行方法を確認し、
lessons-learned.md と reusable-patterns.md に記録してください。
PoC の場合は poc-decision.md に採否・残課題・引継ぎ先を記録してください。
```

## テンプレートの保守

```text
このリポジトリ自体を改善してください。
docs と seed、skills、client 設定、scripts、baseline、report、CI をレビューし、
派生案件の記録を保全できることを確認してください。
変更理由と検証範囲を docs/06_template_review.md と aidlc-docs/ に残してください。
```
