# SCOS subcontract AI field contract

Return one JSON object with these top-level sections:

- `readiness`: status, missing documents, missing decisions, binding blockers, Notice of Award readiness.
- `requirements`: normalized plans/specifications scope register.
- `bids`: one normalized record per bidder with proposal identity, price, takeoff, inclusions, exclusions, qualifications, coverage, supported gap cost, and evaluated price.
- `comparison`: requirement-by-bid coverage matrix and complete-scope gaps.
- `recommendation`: recommended bidder when supportable, scope-first basis, price comparison, confidence, and blocked flag.
- `noticeOfAward`: editable contingent draft fields or null/blank fields while blocked.
- `agreement`: vendor, proposal, approved original amount, retainage, terms, seven-day cure control, and base-template status.
- `scheduleOfValues`: line, description, amount, and source; total must equal the approved original amount.
- `actionItems`: owner, action, due-before-award/agreement flags, and status.
- `warnings`: unresolved inconsistencies and calculation exceptions.
- `provenance`: field, filename, page/sheet/spec reference, confidence, and evidence status.

Use null for unsupported numbers. Never substitute zero for unknown cost, quantity, retainage, duration, or gap exposure.
