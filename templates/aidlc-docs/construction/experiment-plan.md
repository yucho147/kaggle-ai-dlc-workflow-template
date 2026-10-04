# Experiment Plan

## Objective / Baseline

- 評価契約 / 比較 baseline run: TBD
- Data / split version: TBD
- 予算・期限・実行環境: TBD

## Experiments

| ID | Status | Priority | Hypothesis / source | Change | Expected impact | Budget | Stop / acceptance condition | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exp001 | idea | P1 | TBD | TBD | TBD | TBD | TBD | TBD |

States: `idea -> selected -> specced -> implemented -> executed -> reviewed -> adopted / rejected / iterate`。
失敗した実行は `failed`。実行の事実と採否判断は区別する。候補は agent も提案でき、採否・優先順位は依頼範囲に従う。

## Comparison

- 変更する変数 / 固定する条件: TBD
- Ablation・baseline 対比・slice の確認: TBD
- Fold / seed のばらつき、最小改善幅: TBD
- 最終 holdout / Public LB を消費する条件: TBD
- 費用対効果・実装複雑度・再現性: TBD

## Commands

```bash
TBD
```

## Review

`uv run python scripts/render_improvement_report.py` で HTML を生成し、必要なら同じ tracking URI の MLflow UI を案内する。
人間が判断する前に、結果と次の候補を docs に反映する。
