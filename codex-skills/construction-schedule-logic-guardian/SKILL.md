---
name: construction-schedule-logic-guardian
description: Audit and edit construction schedules in Microsoft Project or Project Plan 365 while preserving dependencies, actual progress, baselines, and native working-time calculations. Use for date requests, delays, schedule logic reviews, and feasibility checks.
---

# Construction Schedule Logic Guardian

Preserve the predecessor/successor network and test the requested date. Never make a date appear achievable by breaking logic. Written instructions and fixture tests do not guarantee correctness for a real project.

## Identify the actual application

Inspect the running application/product/version, document, file format, editability and available scheduling/export interfaces before editing. “Project 365” is ambiguous. Microsoft Project desktop and Housatonic Project Plan 365 are separate products. MPP compatibility does not imply COM compatibility.

Initial discovery found both products installed, with Microsoft Project desktop 16.0 actively editing MPP. The supplied adapter targets that actual environment. Project Plan 365's engine is **UNVERIFIED**, with no tested automation adapter. Read [native-workflow.md](references/native-workflow.md) before native operations and [test-coverage.md](references/test-coverage.md) before making validation claims. Recheck capabilities on each host/session.

## Interpret the date

- “This finished November 20” records actual completion; preserve existing history.
- “Must finish **on** November 20” is an exact requirement. It may authorize that task's corresponding constraint, after feasibility is checked under retained inputs.
- “Must finish **by** November 20” is a deadline, not Must Finish On.
- “Expect/target November 20” is a forecast comparison; do not force Start/Finish or add a hard constraint.

Ask one focused question if the distinction is material and unclear. Resolve year, time and working calendar. Date-only helper inputs default to 08:00 start / 17:00 finish; supply an explicit local timestamp when project shifts differ. Do not silently impose those defaults on a different calendar.

## Preserve, audit, edit and verify

1. Identify tasks by stable UID within the preserved project and verify name/GUID. Identify intended completion milestone and document legitimate open-end exceptions. Row order is not dependency order; SS, FF, SF and permitted overlap are valid.
2. Preserve original file and baselines. Work in an exclusive versioned copy unless explicitly directed otherwise. Capture original hash, full native XML, task identities, dependency types/lag/formats, calendars/holidays/exceptions, constraints, modes, resources, assignments and actuals. A reduced task table is not a preserved project.
3. Audit before editing. Recalculate affected upstream/downstream chains with the application's **native scheduling engine**, accounting for calendars, constraints, progress and resources where relevant. Never substitute a Python forward pass or calendar-day arithmetic. Do not recalculate unrelated open projects.
4. Apply only authorized UID/field changes. Never silently delete links, change FS/SS/FF/SF, adjust lag, shorten durations, change calendars, alter actuals, or switch scheduling modes to force a requested date.
5. If infeasible, retain the valid schedule. Explain the blocking chain, native earliest feasible forecast under retained inputs, and specific alternatives requiring approval. Identify constraints/resource limits that prevent proving a true earliest possible finish. Do not apply changes outside the instruction without approval. A blocked date request is FAIL, not successfully applied.
6. Recalculate, save the copy, close/reopen, export and audit again. Compare UIDs/GUIDs, full relationship tuples, calendars, constraints, modes, baselines and actuals. Confirm saving/importing did not lose fields or relationships. Compare dates, float, completion and critical path across the round trip.
7. Preserve conflicting actuals as history. Flag out-of-sequence progress, distinguish completed work from remaining-work implications, and explain any native changes. Quarantine candidates with unexpected protected changes or incomplete verification; do not present them as an approved working schedule.

Use [scripts/guardian.py](scripts/guardian.py) for read-only deterministic XML audits and [scripts/msproject_native.py](scripts/msproject_native.py) for the tested subset of native operations. Read [audit-contract.md](references/audit-contract.md) for policy/request inputs. Advanced or untested cases remain UNVERIFIED; never remove a gate to obtain PASS.

## Required pre/post logic audit

- Circular relationships, self-links, missing references, duplicate relationships and ambiguous identities.
- FS/SS/FF/SF endpoint violations with lag and calendar effects, using native working-time bounds.
- Missing expected predecessors/successors with documented exceptions for legitimate start/finish milestones and justified cases; disconnected chains that do not reach intended completion.
- Hard constraints and manual scheduling that can mask conflicts; negative float, missed deadlines and critical-path changes.
- Leads, long lags and summary-task links as review warnings, never automatically delete them. Unverifiable external dependencies remain UNVERIFIED.
- Construction requirements: inspection before concealment, curing before loading, and prerequisites for commissioning/occupancy. Heuristics are review findings; established project requirements may make them violations. Reachability alone does not prove that a relationship's type, overlap or lag meets a construction requirement.
- Existing errors remain visible and are distinguished from introduced and resolved errors.

## Required output after every use

Report **PASS**, **FAIL**, or **UNVERIFIED**, and provide:

- Requested change, interpretation, stable task identifiers and date/calendar basis; feasibility.
- Before/after dates for affected tasks and milestones; completion, critical path and float effects.
- New, existing and resolved findings with task identifiers/explanations. Disclose review warnings separately.
- Blocking chain and earliest native feasible forecast for a blocked date; specific decisions required for alternatives.
- Revised schedule copy (or unchanged review copy), concise change log, source/baseline preservation and saved/reopened evidence.

PASS requires successful native recalculation, saved-file verification, and no unresolved logic violations or unverified checks. FAIL means a blocked/unmet request or established violation. UNVERIFIED means missing evidence, unsupported interfaces/fields or untested scheduling behavior prevents validation. If violations and incomplete checks coexist, report FAIL and disclose both. A successful save alone is insufficient.

## Regression commands

Run `python scripts/test_guardian.py` for adversarial offline fixtures. Native fixtures use `python scripts/test_native.py --output-root <private-scratch-folder>` with Microsoft Project, pywin32 and saved open projects. Use no concurrent user edits. Invalid graph fixtures are audited offline instead of imported into a live app. See the test reference for the separate opt-in conflict test and its known modal limitation. Do not claim the entire native acceptance suite passed.
