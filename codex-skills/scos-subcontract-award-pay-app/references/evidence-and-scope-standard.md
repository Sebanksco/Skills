# Evidence and scope standard

## Requirement register

Create one row per distinct obligation. Capture requirement ID, discipline/trade, description, quantity/unit when supported, plan sheet/detail, specification section/page, addendum/RFI, and evidence status.

Include visible incidental scope needed for a complete installation when the contract documents expressly require it. Do not infer ordinary trade practice as a contract requirement without labeling it `INFERRED`.

## Bid coverage states

- `COVERED`: bid expressly includes the requirement.
- `PARTIAL`: bid covers only part of the requirement, quantity, location, or system.
- `EXCLUDED`: bid expressly excludes it.
- `NOT_STATED`: bid is silent.
- `CONFLICTING`: inclusion, exclusion, takeoff, price, or qualification conflicts.

An inclusion does not override a contradictory exclusion. Mark `CONFLICTING` and require clarification.

## Complete-scope gap

Mark a requirement as a complete-scope gap when the plans/specifications require it and every compared bidder either excludes it, partially covers it, is silent, or conflicts. Identify the likely responsible trade only as a proposed decision, never as confirmed scope.

## Required evidence

Every extracted field and comparison finding must identify source filename, page or sheet/detail/spec section, confidence from 0 through 1, and `VERIFIED`, `INFERRED`, `MISSING`, or `CONFLICTING` status.
