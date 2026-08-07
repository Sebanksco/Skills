---
name: scos-subcontract-award-pay-app
description: Compare one or more subcontractor takeoffs, bids, inclusions, and exclusions against construction plans and specifications; identify complete-scope gaps and contradictory scope; rank bids by scope coverage before price; prepare an unsaved SCOS recommendation, contingent Notice of Award, subcontract data, Schedule of Values, and subcontractor pay-app draft. Use for subcontract procurement, bid leveling, scope-gap review, Notice of Award preparation, subcontract agreement intake, AIA-style subcontract pay applications, SOV reconciliation, or SCOS Pay Apps portal population.
---

# SCOS Subcontract Award and Pay App

Prepare evidence-backed subcontract recommendations and pay-app data without awarding, binding, issuing, or authorizing payment.

## Required references

- Read [references/evidence-and-scope-standard.md](references/evidence-and-scope-standard.md) before comparing any bid to plans or specifications.
- Read [references/bid-ranking-standard.md](references/bid-ranking-standard.md) before ranking or recommending bidders.
- Read [references/field-contract.md](references/field-contract.md) before returning the SCOS draft.
- Read [references/portal-boundary.md](references/portal-boundary.md) before interacting with SCOS or preparing a Notice of Award.
- Use [assets/SCOS_Subcontract_Award_and_Pay_App_Template.xlsx](assets/SCOS_Subcontract_Award_and_Pay_App_Template.xlsx) for an Excel deliverable when requested.
- Use [assets/SEBANKS-white.png](assets/SEBANKS-white.png) unchanged on the standard navy SCOS document header. Preserve its proportions and do not redraw, stretch, crop, or recolor it.

## Workflow

### 1. Establish project evidence

1. Confirm the exact project and trade/buyout package.
2. Inventory each plan set, specification, addendum, RFI, bidder takeoff, proposal, inclusion list, exclusion list, allowance, alternate, and qualification.
3. Record filename, revision/date, page or sheet, document role, and hash when bytes are available.
4. Mark every extracted fact `VERIFIED`, `INFERRED`, `MISSING`, or `CONFLICTING` with confidence.

Block recommendation when the controlling plans, specifications, or bidder pricing are missing. Never silently treat missing documents as "no requirement."

### 2. Build the complete-scope baseline

Trace the trade scope across drawings, schedules, details, specifications, addenda, and RFIs. Build one normalized requirement register containing quantities when supported, products/systems, preparation, accessories, transitions, testing, warranties, closeout, temporary requirements, and coordination obligations.

Do not invent a quantity or obligation. Preserve conflicts between documents for human resolution.

### 3. Normalize every bid independently

For each bidder extract:

- bidder and proposal identity;
- base price, alternates, allowances, unit prices, taxes, bonds, insurance, mobilizations, schedule qualifications, and validity;
- takeoff quantities and units;
- inclusions, exclusions, qualifications, assumptions, and "unlisted scope excluded" clauses;
- proposal pages supporting every value.

Recalculate totals. Do not choose between conflicting totals.

### 4. Compare each bid to the complete scope

Map every scope requirement to each bidder as `COVERED`, `PARTIAL`, `EXCLUDED`, `NOT_STATED`, or `CONFLICTING`.

Highlight:

- direct inclusion/exclusion contradictions;
- exclusions that leave a project obligation unassigned;
- complete-scope gaps where no bidder covers a required item;
- quantity, product, preparation, accessory, testing, warranty, or coordination differences;
- bidder qualifications that transfer cost or risk to Sebanks or another trade.

### 5. Estimate gap exposure carefully

Use an estimated gap cost only when supported by another bid, a quoted alternate/unit price, the approved estimate, or a documented historical/project source. Record the method, source, page, confidence, and range when uncertainty is material.

Never invent a gap cost. If a material gap cannot be priced, leave it null and block a final recommendation until a person supplies or approves a value.

### 6. Rank scope first, then price

Follow `bid-ranking-standard.md`.

1. Eliminate or hold bids with unresolved critical scope gaps.
2. Rank remaining bids by scope coverage.
3. Compare evaluated price only within comparable coverage.
4. Calculate `evaluatedPrice = bidPrice + supportedGapCost`.
5. A bid that is $10,000 lower but has $20,000 of supported uncovered scope loses to the otherwise comparable bid.

Return the recommendation basis, coverage differences, raw price differences, supported gap exposure, evaluated price, confidence, and blockers. Never label a bidder "best" based on price alone.

### 7. Human review gate

Block agreement preparation when required documents, controlling quantities, material scope decisions, or supported gap values are missing. Require a human to confirm:

- complete-scope baseline;
- bidder coverage classifications;
- gap-cost sources;
- selected bidder and approved original subcontract amount;
- accepted exclusions, clarifications, alternates, schedule, and retainage;
- exact Buyout/commitment lineage.

### 8. Prepare the contingent Notice of Award

Only after the review gate passes, prepare the unsaved Notice of Award draft using verified project, vendor, trade, CSI section, proposal reference, approved price, scope, and conditions precedent.

The notice remains contingent on an executed subcontract, resolved gaps, insurance/bonds, schedule, and project compliance. It does not authorize work.

### 9. Prepare agreement data and SOV

Never invent contract language. Require the actual base subcontract before changing termination language. Enforce a seven-day notice-to-remedy requirement, but do not draft the replacement clause without the base language.

Build the proposed SOV from supported pricing. Require its total to equal the approved original subcontract amount to the cent. Block the first pay app on any variance.

### 10. Return the SCOS draft

Return the shape in `field-contract.md`, including field-level file/page provenance, confidence, evidence status, bid comparison, blockers, action items, Notice of Award readiness, agreement data, and SOV.

Return an unsaved draft for human review. Never award, bind, sign, issue, email, approve, upload, write SQL, post to QBO, or authorize payment.

Run before calling a manifest ready:

```powershell
python scripts/validate_subcontract_manifest.py path/to/subcontract-manifest.json
```

## Required handoff status

Use exactly one status:

- `BLOCKED - REQUIRED EVIDENCE MISSING`
- `READY FOR BID REVIEW`
- `READY FOR HUMAN SELECTION`
- `READY FOR CONTINGENT NOTICE OF AWARD`
- `READY FOR AGREEMENT DATA REVIEW`
- `READY FOR FIRST PAY APP`

Never use a later status while an earlier gate remains unresolved.
