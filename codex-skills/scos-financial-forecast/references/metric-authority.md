# SCOS financial metric authority

## Source order

| Measure | Primary authority | Treatment |
|---|---|---|
| Cost baseline | Approved estimate baseline and Buyout budget | Controlled after approval |
| Actual material/other cost | Approved QBO allocation | Controlled; project-matched unallocated lines are provisional |
| Labor actual | Approved Timeclock hours with loaded-rate snapshot | Controlled when approved |
| AP due | QBO Bill balance, due date, and BillPayment application | Provisional until exact allocation/payment reconciliation is complete |
| Owner billing | Approved Owner Pay App | Billing, not cash receipt |
| Subcontract obligation | Current commitment and latest approved subcontract Pay App | Identify overlap with QBO Bills |
| Change exposure | Executed Owner Change Orders and current PCO revisions | Separate approved value from unapproved risk |
| Schedule | Current imported schedule activity version and baseline | Report freshness and linkage coverage |
| Cash | Approved bank-account snapshot plus controlled receipt/payment events | Never infer receipts from billing |

## Standard KPI rules

- Gross profit margin: require current contract value and forecast cost at completion.
- CPI: require earned value and actual cost for the same cutoff and scope.
- Cash flow and DSO: require controlled cash events; DSO requires invoice and receipt dates.
- Backlog: require active signed contract value less completed recognized work across projects.
- SPI: require earned value and planned value for the same cutoff and scope.
- Change Order rate: distinguish executed change value from pending PCO exposure; state the denominator.
- Rework rate: require costs or hours explicitly classified as rework.
- Hit/win rate: require submitted-bid and signed-award outcomes for a defined period.
- Labor productivity: require comparable installed units and approved labor hours; hours alone are burn, not productivity.
- Safety incident rate: require controlled recordable incidents and hours worked.
- Equipment utilization: require controlled available and active runtime.
- Cash at completion: require forecast cost, remaining obligations, controlled cash on hand, and modeled future owner receipts.

When a rule is not satisfied, return `NOT_AVAILABLE` with the missing authority. Use `PROVISIONAL` when a valid calculation relies on incomplete mappings, projections, or unapproved evidence.

## Action ranking

Prioritize:

1. a dated schedule threat that can delay procurement, billing, or completion;
2. a cost/commitment variance likely to change forecast at completion;
3. a cash timing or evidence gap likely to change the next 13 weeks.

Do not rank a large number solely because it is large. Rank the actionable variance, deadline, or missing control.
