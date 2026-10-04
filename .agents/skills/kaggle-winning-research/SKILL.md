---
name: kaggle-winning-research
description: Research Kaggle discussions, final writeups and implementations to derive evidence-backed hypotheses, CV design, failure cases and reuse conditions. Use for solution research, not routine competition setup.
metadata:
  short-description: Investigate winning approaches
---

# Kaggle Winning Research

Read AGENTS.md, the current state and competition constraints.
Define whether the target is an active competition, retrospective analysis or transfer to another task.
Record search cutoff, budget, topic/notebook coverage and prioritized questions.

## Evidence Collection

- Use the actual installed CLI help. Bundled topics sort supports top/hot/recent; votes is not a valid sort. A leaderboard is not a substitute for discussion content.
- Read topic bodies and relevant comments, following pagination within the budget. Search notebooks with the competition filter and inspect original writeups and repositories.
- Record title, author, URL/ref, publication and retrieval dates, revision and snapshot. Separate observed facts, reported results and inferred hypotheses.
- Compare CV, features, model/loss, ensembles, external data, leakage, Public/Private shakeup, inference constraints and failed approaches where relevant.
- Distinguish information available during the competition from post-deadline knowledge. Popularity, Public LB and final Private results are different evidence.
- For reuse, inspect license, dependencies, data shape, fit boundaries, compute requirements and offline inference. Unclear license remains unknown.

## Synthesis

Update winning-research.md, source-register.md, relevant risks, strategy.md and implementation-candidates.md.
Prioritize a few falsifiable hypotheses with applicable conditions, minimum experiments, cost and rejection criteria.
A reported winning method becomes a local recommendation only after considering the current data and evaluation contract.

If implementation is requested, update the relevant contracts and construction decisions.
For a research-only request, do not require finalized code architecture.
Write retrieval failures and assumptions in audit.md, update state, and regenerate the HTML report.
