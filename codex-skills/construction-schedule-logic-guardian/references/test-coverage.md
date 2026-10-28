# Acceptance evidence and remaining work

Initial testing: Microsoft Project desktop 16.0 on Windows, 2026-10-28; pywin32 312. Generated fixture schedules and private runtime logs remain outside this public package. No production construction schedule is a test fixture.

Publication regression: **12 offline tests passed**, including stable changed-finding classification and the inspection/concealment overlap verification gate. Independent offline review confirmed these fixes. Skill metadata validation and Python compilation also passed. These checks do not establish native engine certification.

| Acceptance case | Observed evidence |
| --- | --- |
| 1 Feasible finish preserves dependencies | Native fixture passed after switching to byte-copy plus FileSave; full relationship and saved/reopened checks passed. |
| 2 Impossible earlier finish | Native fixture passed: request blocked, upstream network reported, unchanged review state preserved. |
| 3 Delayed predecessor | Native fixture passed: authorized duration increase moved successor work. |
| 4 SS / FF valid overlap | Native fixture passed; overlap retained without changing relationship types. |
| 5 Lag, weekends, holidays, task exception | Native fixture passed with a project holiday and separate successor-calendar exception. |
| 6 Cycles, missing references, disconnected tasks | Offline adversarial fixture passed; corrupt graph is not imported into Project. |
| 7 Conflicting actual progress | Native fixture passed: out-of-sequence finding, unchanged actual start. |
| 8 Hard/manual conflict masking | Offline detection passed. Full native combined test blocked by a Planning Wizard modal; not certified. |
| 9 Saved/reopened field retention | Included in passed native cases 1–5 and 7. Dedicated deadline round-trip case did not finish after the modal blocked the suite. |
| 10 Existing versus introduced findings | Offline delta test passed. Dedicated native deadline/error-delta case did not finish after the modal blocked the suite. |

Overall native acceptance status: **UNVERIFIED**, not a claim that all native cases passed. Resource/leveling behavior, elapsed/percentage lag, advanced progress/splits, Project Plan 365 and other builds need additional application-specific validation. The fixture results only support the tested subset.

The published revision includes subsequent protective checks and documentation improvements. That exact revision has offline regression verification; its full native suite has not been rerun since the interrupted dialog test. Do not inherit earlier native passes as full certification of this revision.

The default native suite skips the known interactive hard/manual conflict case and records it UNVERIFIED; `--interactive-conflicts` explicitly opts into that separate test. It can require clearing a native dialog. Do not run it unattended or change global scheduling-warning settings to pass it. The suite records partial results as it goes, so a blocked native call does not erase earlier evidence.

Offline tests are portable and read-only. Re-run after code changes. Native results are environment-specific; don't claim saved-file validation from an offline pass.
