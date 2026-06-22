---
name: improvement-review
description: Use when preparing for a continuous improvement cycle review. Regenerates the HTML report and guides the human to choose the next experiment hypothesis using the HTML report and MLflow UI instead of Markdown.
metadata:
  short-description: Prepare improvement cycle review
---

# improvement-review

継続的な改善サイクルのレビュー準備をする skill です。HTML report を再生成し、次の仮説選定を人間に案内します。

## 入力

なし（`aidlc-docs/operations/` 配下の Markdown を自動的に読み込みます）

## 手順

1. `docs/00_project_concept.md` と `AGENTS.md` を読む。
2. 以下の Operations ドキュメントを読む。
   - `aidlc-docs/operations/improvement-loop.md`
   - `aidlc-docs/construction/experiment-plan.md`
   - `aidlc-docs/operations/experiment-log.md`
   - `aidlc-docs/operations/cv-lb-tracking.md`
   - `aidlc-docs/operations/lessons-learned.md`
3. HTML report を再生成する。
   ```bash
   uv run python scripts/render_improvement_report.py
   ```
4. 人間には Markdown ではなく `outputs/reports/improvement-report.html` と MLflow UI を見て、次の仮説選定または採用/不採用判断をするよう案内する。
5. 次に試すべき実験候補を優先順位付きで `aidlc-docs/operations/improvement-loop.md` または `aidlc-docs/construction/experiment-plan.md` に記録する。

## 出力

- 再生成済み `outputs/reports/improvement-report.html`
- `aidlc-docs/operations/improvement-loop.md` または `aidlc-docs/construction/experiment-plan.md` に優先順位付きの次実験候補

## 完了条件

- HTML report が最新状態で生成されている。
- 次に試すべき実験候補に優先順位が付いている。
- 人間が `outputs/reports/improvement-report.html` と MLflow UI を見て判断できる状態になっている。
