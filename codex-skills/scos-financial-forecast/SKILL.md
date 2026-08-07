---
name: scos-financial-forecast
description: Review SCOS project or portfolio financial position using controlled QBO, Buyout, Pay App, Change Order, schedule, labor, material, and cash evidence. Use for Financial AI Assist runs, construction cash forecasts, KPI reviews, end-of-project cash or remaining-obligation estimates, and requests for the top schedule/cost/cash actions.
---

# SCOS Financial Forecast

Produce a dated, evidence-backed interpretation without replacing SCOS accounting or schedule authorities.

## Workflow

1. Identify the project, as-of time, source timestamps, and requested horizon.
2. Read [references/metric-authority.md](references/metric-authority.md) before calculating or interpreting metrics.
3. Separate controlled, provisional, and missing sources. Treat project-matched QBO lines as provisional until Buyout allocation review is complete.
4. Calculate deterministic monetary and schedule measures outside the language model whenever the source contract permits it.
5. Return exactly three actions most likely to affect schedule, cost, or cash. State the evidence, impact, urgency, and accountable next step.
6. Report every requested KPI as `AVAILABLE`, `PROVISIONAL`, or `NOT_AVAILABLE`. Use a null value when authority is missing; never substitute an industry benchmark for project evidence.
7. Label the result `AI Enriched: <date/time>` and retain source dates and limitations.

## Guardrails

- Do not treat billed Owner Pay Apps as cash received.
- Do not combine QBO AP and subcontract Pay App balances without identifying possible overlap.
- Do not calculate CPI or SPI without controlled earned-value and planned-value inputs.
- Do not calculate DSO without controlled invoice and receipt dates.
- Do not infer rework, safety, equipment utilization, or bid win rate from unrelated records.
- Do not modify QBO, Pay Apps, Change Orders, schedules, budgets, commitments, payments, or source records.
- Do not hide stale, unmapped, incomplete, or conflicting evidence.

## Output

Return:

- a concise executive forecast;
- exactly three ranked actions;
- the standard KPI set with authority status;
- projected cash remaining, remaining owed, and forecast cost at completion only when supported;
- missing inputs and double-count risks.
