---
name: oni-apps-script-guardrails
description: Safely modify Clinton Baird's ONI Google Apps Script workflows for Twilio SMS, Google Sheets response routing, hospital and surgery tabs, date normalization, header-based mappings, and controlled clasp operations. Use whenever inspecting, debugging, or changing these ONI Apps Script workflows.
---

# ONI Apps Script Guardrails

Use this skill when working on Clinton Baird's ONI Google Apps Script workflows, especially scripts that move Twilio SMS responses through Google Sheets tabs such as `Responses`, `Responses_SA`, `Hospitals`, surgery scheduling tabs, `SchAppts`, enrichment queues, or outbound physician SMS sheets.

## Core Rules

- Read the current code before making claims or edits. Do not assume line numbers, function names, headers, or existing behavior.
- If the user provides an attached/pasted code file and says to use only that file, use that attachment as the baseline. Do not silently switch to a workspace copy.
- When editing a local file, verify the edit with `rg` and a syntax check. Report the exact file path and line-level search proof.
- When the user says the code is not changed, create a new explicitly named file from the provided baseline, apply the requested change there, and compare it back to the baseline with `git diff --no-index`.
- Never hard-code spreadsheet column numbers for business logic. Build and use header maps with normalized header names.
- Keep secrets and spreadsheet IDs in Script Properties unless the user explicitly asks otherwise.
- Prefer small, auditable changes. Do not bundle unrelated workflow changes with a bug fix unless the user asks.

## Google Sheets Date Safety

Google Sheets and Apps Script can shift dates by timezone, often showing values such as `1/30/2026 23:00:00` when the intended text was `1/31/2026`.

For DOB:
- Treat DOB as a literal clinical identifier, not a timezone-aware timestamp.
- Prefer the original Twilio `body` CSV value over the already-parsed sheet cell.
- Write DOB as plain text using `setNumberFormat('@')`.
- After batch writes, rewrite DOB cells directly as text if needed.

For DOS:
- DOS may come from Twilio `timestamp`, but must be written as date-only.
- If the timestamp displays as late-night `23:00:00` and the workflow indicates the service date is the next calendar day, use a dedicated DOS normalizer rather than reusing DOB logic.
- Do not let `DOS` carry a time component into destination sheets.

Recommended helpers:
- `normalizeDateOnlyString_()`
- `normalizeDosDateOnlyString_()`
- `getHospitalSourceDob_()`
- `getHospitalSurgerySourceDob_()`
- destination format helpers that set DOB/DOS cells to plain text before or after writes when needed.

## Twilio Response Parsing

Expected `Responses` payload:

```text
Name, DOB, MRN, Location, Diagnosis
```

Expected `Responses_SA` payload:

```text
Name, DOB, MRN, Location, Surgery
```

Rules:
- Parse CSV using structured parsing where available.
- Support fallback field detection by header meaning, but reject random long SMS payloads.
- If payload is more than 10 words and does not clearly parse, do not sync it to workflow tabs.
- Do not overwrite already populated parsed Twilio fields unless the user explicitly requests a repair/backfill.

## Hospital Append Flow

For `Responses -> Hospitals`:
- Map by headers only.
- `timestamp -> DOS`.
- `Name -> Name`.
- `DOB -> DOB`, but use the original Twilio body DOB when available.
- `MRN -> MRN`.
- `Location -> Location`.
- `Diagnosis -> Diagnosis`.
- Map `Surgeon` from configured phone mapping, usually source `from` first, then `to` if needed.
- Write `TwilioSid` and `AdmissionUID` when available.
- Duplicate detection should prefer `AdmissionUID` or Twilio `sid`; old rows may fall back to patient/date keys.

## Responses_SA Surgery Flow

For `Responses_SA -> Surgery tabs`:
- Apply the same DOB/DOS date safety used for Hospitals.
- Use display values or original body values when date shifts are possible.
- Existing matched rows should not rewrite patient fields unless explicitly requested.
- For match status:
  - matched existing row: `comparedToResponse_SA = MatchSync`
  - new no-match row: `comparedToResponse_SA = noMatchSync`
- APP logic and surgeon-tab routing must be explicit and verified by phone/payload rules.

## Verification Checklist

Before final response after code edits:

- Run `rg` for the new helper/function/constant names.
- Run a syntax check by copying `.gs` to a temporary `.js` file and using `node --check`.
- If the user is comparing against an attachment, run `git diff --no-index` between the attachment and the new file.
- Report only what actually changed and where.
- If a Google Sheet data validation/dropdown may reject script-written values, call that out.

## Communication

- If something is ambiguous, say exactly which behavior is ambiguous and suggest the safest default.
- When the user asks for review only, do not edit.
- When the user asks for a new file, create a new named file and confirm with a comparison.
- Avoid broad rewrites. This workflow is operational; small, verifiable changes matter more than clever refactors.
