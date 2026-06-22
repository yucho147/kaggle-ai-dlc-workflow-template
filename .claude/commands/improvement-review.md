---
description: 継続改善サイクルのレビュー準備をする。HTML report を再生成し、次の仮説選定を人間に案内する
allowed-tools: Bash, Read, Write, Edit
---

継続的な改善サイクルのレビュー準備をしてください。

## 手順

1. `aidlc-docs/operations/improvement-loop.md` を読んでください。
2. 以下を確認してください。
   - `aidlc-docs/construction/experiment-plan.md`
   - `aidlc-docs/operations/experiment-log.md`
   - `aidlc-docs/operations/cv-lb-tracking.md`
   - `aidlc-docs/operations/lessons-learned.md`
3. HTML report を再生成してください。
   ```bash
   uv run python scripts/render_improvement_report.py
   ```
4. 人間には Markdown ではなく、`outputs/reports/improvement-report.html` と MLflow UI を見て、次の仮説選定または採用/不採用判断をするよう案内してください。
5. 次に試すべき実験候補を優先順位付きで `aidlc-docs/operations/improvement-loop.md` または `aidlc-docs/construction/experiment-plan.md` に記録してください。
