# Input and evidence contract

Stable UID is scoped to the preserved project. Verify the name/GUID before changing it. Task ID/row position is not a durable key. Preserve original link direction, type, lag, lag format and cross-project metadata.

Example policy (replace with verified task UIDs and project-specific reasons):

```json
{
  "completion_uid": "300",
  "open_end_exceptions": {
    "10": {"predecessor": "Approved notice-to-proceed milestone"},
    "300": {"successor": "Intended project completion milestone"}
  },
  "long_lag_tenths_minutes": 24000,
  "required_sequences": [
    {"before": "120", "after": "130", "reason": "Inspection before concealment required by specification"}
  ]
}
```

Long-lag threshold is a review threshold in tenths of minutes, not an assumed workweek. Document legitimate exceptions individually. Required sequences check graph reachability. A missing path is an error; a path alone is UNVERIFIED until type, lag, overlap and native timing are independently established. The current helper deliberately cannot certify these requirements into PASS.

Example request:

```json
{"uid":"130","intent":"deadline","date":"2026-11-20T17:00:00"}
```

Supported intents: `deadline`, `exact_finish`, `exact_start`, `target`, `actual_finish`, `duration` (with e.g. `"duration":"6d"`). An exact date permits only the named task's constraint/date. A target creates a comparison with no forced date. Actual finish may imply an actual start; unapproved changes are rejected. `allow_derived_actual_start: true` requires explicit user authorization and disclosure. No request command changes links, calendars or modes.

Link types: 0 FF, 1 FS, 2 SF, 3 SS. XML LinkLag and float are tenths of minutes; format is preserved. Relationship bounds must come from the native engine, never calendar-day arithmetic. Full calendar/resource payloads and baselines are compared. Assignment forecast dates and Type 1 remaining-work timephasing are calculated outputs; actual/baseline/unknown timephasing remains protected.

The read-only auditor does not calculate schedules. Without fresh native evidence it remains UNVERIFIED. Standalone audits cannot prove saved-file verification, even if evidence JSON is supplied. Do not fabricate evidence or reuse it after an edit. Evidence keys contain full link tuples and the native adapter generates them in the export session.

Reports retain task before/after fields, completion UID, critical task UID sets, float, all findings/deltas, source hash, candidate location, change log and round-trip results. Render a human response explaining completion-date impact, float units and decisions. An upstream list is a blocking **network**, not proof of a single driving chain; use retained link/evidence data to explain which predecessors and constraints drive the date.

Audit the captured XML before explicit recalculation, then the recalculated pre-edit state, then after-edit/reopened states. Report recalculation-resolved preexisting findings separately. Opening an MPP can itself trigger native calculation; this capture is not proof of the pre-open state on disk. When that distinction matters, obtain a prior native export or report the limit. Findings use stable code/task/link identities; changed diagnostic dates remain existing findings with changed details, not falsely resolved/new errors.

Missing fields, partial exports, unsupported calendars/resources/lag formats and unverifiable external links cannot be waived into PASS. Existing errors stay visible; actual-history conflicts must be distinguished from remaining-work implications.
