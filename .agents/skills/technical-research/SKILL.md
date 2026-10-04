---
name: technical-research
description: Investigate a business PoC or technical theme, compare primary evidence and implementations with the current baseline, and define scope, evaluation and go/no-go criteria. Use outside Kaggle participation setup.
metadata:
  short-description: Research and scope a PoC
---

# Technical Research

Read AGENTS.md and the current state. Establish the business or research decision, requested arrival point, current method, available data, deadline and compute budget.
Ask only for missing decisions that affect success, scope, evaluation or data permissions.

## Investigation

- Choose relevant primary papers, official docs and original implementations. Use Kaggle, arXiv or Hugging Face when they help answer the question; no source is mandatory for every topic.
- Record query/coverage/cutoff, source revisions, retrieval dates, short claims and confidence in source-register.md and audit.md.
- Compare the current or simplest method with promising candidates using the same decision criteria: quality, data fit, runtime, cost, licensing, maintenance and reproducibility.
- Capture negative evidence, incompatible assumptions and unknowns. Do not treat a benchmark on another dataset as local proof.
- Inspect implementation license, dependencies, expected schema, hardware and fit/inference boundaries before proposing a port.

## PoC Plan

Update problem-overview.md, technical-research.md and relevant risks.
Define a small number of hypotheses, a fixed evaluation dataset, a comparison baseline, acceptance/iteration/stop thresholds and a decision owner.
For temporal tasks specify as-of information, horizon and label delay. For LLM/RAG specify failure categories, groundedness, judge calibration, contamination and token cost where relevant.

When implementation is requested, complete data/evaluation contracts, questionnaire, architecture and the minimal generation/experiment plan.
When results exist, populate poc-decision.md with evidence, constraints, go/iterate/no-go and handoff requirements.
Do not invent an unperformed experiment or human decision. Update state and regenerate the HTML report.
