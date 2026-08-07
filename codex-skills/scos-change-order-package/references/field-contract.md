# SCOS field contract

Use the live schema as authority. This reference records the verified July 2026 contract and must be revalidated before any write.

## Current dashboard-preserving inputs

| Portal input | SCOS header | Rule |
| --- | --- | --- |
| Change Order ID | `ChangeOrderID` | Immutable after creation; leave blank only when the current writer assigns the next project PCO ID. |
| Active project | `ProjectID` | Required; exact live ProjectID. |
| Buyout package | `BuyoutUID`, `Buyout Package` | Resolve from the live project Buyout source; never invent. |
| Drawings page | `Drawing Page` | Exact sheet identifiers, maximum 80 characters. Use a compact comma-separated list when several sheets apply. |
| Detail / section | `Detail / Section` | Exact detail, revision, cloud, room, grid, or schedule reference, maximum 120 characters. |
| Description | `Description` | Required; concise ownership narrative explaining prior condition, change, and justification. Maximum 2,000 characters. |
| Source document URL | `Source Document URL` | HTTPS link to the controlling package or source. Do not use an expiring download URL. |
| Subcontractor CO | `Buyout Cost Change Amount` | Required numeric downstream cost. |
| GC overhead and profit | Derived for display | `Owner Change Amount - Buyout Cost Change Amount`. Do not assume a percentage. |
| Proposed final OCO | `Owner Change Amount`, `Total Cost Change` | Required numeric owner-facing amount. |

The current output remains:

`CO | Stage | Scope/description | Buyout package | Drawing | Subcontractor CO | GC O&P | Final OCO | Budget | Action`

## Enriched automatically from verified lineage

- `Project Name` from the exact ProjectID.
- `CSI DIV`, `CSI Description`, and `Buyout Package` from the exact BuyoutUID when supported by the current writer.
- `Requested By` from the authenticated actor.
- `Last Updated` from the system clock.
- `Status = PENDING` and `Approved = false` for a new PCO draft.

## Ownership approval fields

These require an explicit approval action and must not be inferred from documents:

- `Status = APPROVED`
- `Approved = true`
- `Approval Date`
- `Approved By`
- approved `Owner Change Amount`
- approved `Buyout Cost Change Amount`
- `BudgetAdjustmentUID` produced by the authorized posting workflow

The immutable `ChangeOrderID` remains a PCO-form identifier when the displayed stage becomes OCO.

## Package-only detail

Keep these in the package/manifest unless the live schema is deliberately extended:

- architect directive type and number;
- subcontractor proposal number and date;
- prepared by and reviewed by;
- prior condition, detailed change, and cost justification as separate narrative sections;
- multiple drawing-reference rows;
- revision/cloud descriptions and issue dates;
- detailed quantities, units, unit costs, labor rates, tax, overhead, fee, and bond;
- inclusions, exclusions, validity, supporting-document checklist, and schedule impact.

Do not add dashboard columns merely because the package contains richer evidence.
