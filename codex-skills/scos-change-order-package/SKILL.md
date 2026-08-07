---
name: scos-change-order-package
description: Trace architect-directed construction changes through referenced drawing pages, reconcile subcontractor proposals, assemble an ownership-review PCO/OCO PDF package, and operate the SCOS Change Orders portal to select a project, create and populate a PCO draft, link supporting documents, and prepare controlled client review. Use for PCR, ASI, RFI, CCD, owner directive, revised drawing, subcontractor estimate, change-order package, PCO preparation, OCO approval support, SCOS change-order field population, portal entry, supporting-document attachment, or client-review issuance.
---

# SCOS Change Order Package

Build an evidence-backed change-order record and ownership package while preserving the current SCOS dashboard output. Treat AI output as a draft until the required human gates are satisfied.

## Required references

- Read [references/field-contract.md](references/field-contract.md) before preparing SCOS fields or a manifest.
- Read [references/package-standard.md](references/package-standard.md) before tracing drawings or generating a package.
- Read [references/portal-workflow.md](references/portal-workflow.md) before opening SCOS, attaching documents, saving a PCO, or preparing client review.
- Read [references/integration-design.md](references/integration-design.md) when designing or implementing the SCOS AI-assisted PCO connection.
- Use [references/example-manifest.json](references/example-manifest.json) as a shape example only; never copy its identifiers or values into production work.

## Workflow

### 1. Establish the source of truth

1. Confirm the exact ProjectID and project.
2. Inventory every uploaded file with filename, document role, issue/revision date, page count, and cryptographic hash when local bytes are available.
3. Classify files as architect directive, construction drawing, subcontractor proposal, pricing detail, correspondence, or prior approved package.
4. Preserve originals. Work from copies and temporary rendered pages.
5. Record all facts as `Confirmed`, `Inferred`, `Missing`, or `Proposed`.

Stop if the project is ambiguous or the architect directive cannot be linked to the intended project.

### 2. Extract the architect-directed change

Extract the directive type and number, issue date, stated reason, disciplines affected, cited sheets/details, revision or cloud references, and requested response. Do not reduce the description to the directive number alone.

Separate the full architect directive from the trade-specific scope being priced. Do not assign unrelated architectural, electrical, plumbing, mechanical, structural, or med-gas changes to the subcontractor proposal.

### 3. Trace the construction documents

For every cited sheet or detail:

1. Locate the exact construction-document page.
2. Verify sheet number, sheet title, revision, issue date, and PDF page number.
3. Inspect the clouded, highlighted, or revision-marked area visually.
4. Record the room, grid, equipment, schedule row, detail, or other location when visible.
5. Write a concise description of the actual change shown.
6. Link the finding to its source file and page.

If both baseline and revised sheets exist, compare them. If only the revised sheet exists, state that the trace relies on revision marks and the architect narrative rather than a baseline-to-revision comparison. Never claim a trace is confirmed when the cited page is missing, unreadable, or inconsistent.

### 4. Extract and reconcile the subcontractor estimate

Extract vendor, proposal number, proposal date, project number, scope inclusions and exclusions, labor hours and rates, materials, equipment, subcontractors, tax, overhead, fee, bond, total, validity period, and stated schedule impact.

Recalculate every subtotal and markup. Compare:

- detailed line-item sum;
- subcontractor proposal total;
- SCOS downstream/Buyout cost;
- GC overhead and profit;
- final owner-facing amount.

Report every variance, including rounding. Do not choose between conflicting totals. Mark the financial gate `BLOCKED` until an authorized person selects the controlling value.

### 5. Resolve SCOS lineage and draft fields

Read the live, project-scoped Buyout source and resolve the exact BuyoutUID and label. Never infer or invent an identifier. Use the exact current Change Orders headers and the mapping in `field-contract.md`.

Create a change-order manifest. Run:

```powershell
python scripts/validate_manifest.py path/to/change-order-manifest.json
```

Resolve every `ERROR` before calling the record SCOS-ready. Present `WARNING` items for human review.

### 6. Human scope and financial review

Require confirmation of:

- trade scope and exclusions;
- drawing trace completeness;
- Buyout package;
- subcontractor amount;
- GC overhead and profit;
- final owner amount;
- schedule impact;
- unresolved discrepancies.

Keep schedule impact editable. When schedule impact is `0` days, require the user to confirm that zero is intentional and set `schedule.zeroDaysConfirmed = true` in the manifest. Do not advance a zero-day manifest without that confirmation.

Do not mark ownership approval or post financial values during this gate.

### 7. Assemble the ownership-review package

Follow `package-standard.md`. Generate a single PDF containing the ownership summary followed by unmodified supporting documents. Keep the original subcontractor proposal and architect documents intact in the attachment section.

Render every final page to images and inspect legibility, page order, clipping, overlaps, currency formatting, drawing readability, and checklist state. Save final packages under `output/pdf/` when working in a repository unless the user specifies another exact path.

### 8. Prepare the SCOS portal draft

Follow `portal-workflow.md`. Use the browser-control skill when the user requests portal operation.

1. Open `https://scos.sebanksco.com/`, confirm the signed-in identity, and select the exact project on Home.
2. Open **Change Orders**, confirm the displayed project, and verify the project is enabled for the controlled SQL workflow.
3. Select **Create New** and populate the existing form from the validated manifest.
4. Resolve Buyout and commitment choices only from the live project-scoped options.
5. Add references and supporting-document metadata using verified stable SharePoint URLs and hashes.
6. Stop at the populated form for human review unless the user explicitly authorizes **Save Draft**.

Never paste values into an unverified project, infer a portal selector after the page changes, or bypass SCOS by writing directly to SQL.

### 9. Controlled SCOS save and client review

Default to a dry-run field payload and package preview. Write to SCOS only when the user explicitly authorizes the write and the authenticated role, idempotency key, exact ProjectID, exact ChangeOrderID, and live headers are verified.

After authorized **Save Draft**, re-read the saved PCO in the Change Orders list and verify its number, status, revision, amount, Buyout lineage, references, and attachments. Treat these as separate explicit actions:

1. submit for internal review;
2. record the internal decision;
3. issue the exact approved revision to configured client reviewers;
4. record an authenticated client response or supported written-approval evidence;
5. post the approved OCO through the existing controlled financial workflow.

Before client issuance, require the final package PDF to be present as a stable SharePoint attachment on the exact revision. Verify every intended reviewer is active and client-review enabled. Confirm that the email notification links to the authenticated client-review page and that the page exposes the exact package attachment. If the requested behavior is a direct PDF link in the email, report it as a portal implementation dependency until the live notification template is verified to provide it.

Treat ownership approval as a separate action. Do not set `Approved`, `Approval Date`, `Approved By`, or `BudgetAdjustmentUID` from document inference. After an authorized write, re-read the exact row and verify every intended field.

## Required handoff

Return:

1. evidence inventory;
2. drawing trace table;
3. cost reconciliation;
4. SCOS field payload with field-level provenance;
5. missing or blocked items;
6. ownership package path or preview;
7. portal state, saved-list verification, notification state, and write/deployment status.

State clearly whether the result is `DRAFT`, `READY FOR HUMAN REVIEW`, `READY FOR OWNERSHIP REVIEW`, or `APPROVED/POSTED`. Never use the final status without verified evidence.
