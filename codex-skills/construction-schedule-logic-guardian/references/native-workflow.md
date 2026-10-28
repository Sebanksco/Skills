# Native workflow and limitations

Inspect running executable/product/version, current document, MPP association and available interfaces. Microsoft Project exposes `MSProject.Application`; Project Plan 365 COM compatibility is unproven. Initial local discovery found Microsoft Project 16.0 and Project Plan 365 25.54, with an MPP open in Microsoft Project. Do not assume this on another host.

For the Microsoft adapter, use Python with `pywin32`, attach to the running Project via `GetActiveObject` and obtain the typed wrapper using `gencache.EnsureDispatch`. Do not launch a replacement application or new instance unnecessarily. The helper creates an exclusive timestamped directory and byte-copies the MPP **before** opening it, preserving the original. Save user edits before copying. Do not touch unrelated projects.

`CalculateProject()` recalculates the active project only; never use CalculateAll. Native dates arrive as wall-clock values even when Python tags them UTC; avoid timezone conversion and naive datetime-to-COM assignments. Use tested local date strings and verify native XML ISO values. The date-only defaults are 08:00 / 17:00, so explicitly override when work shifts differ.

Native MPP Save As to a new filename was observed to regenerate GUIDs. The helper copies bytes first and uses **FileSave** on that copy. XML export did not change the active MPP filename in the tested build. Do not normalize away identity changes just to pass comparison.

The helper exports captured/before/after/reopened XML, native bound evidence, `report.json` and a candidate MPP. A failed candidate is for investigation only. Retain the unchanged source as the valid schedule. Temporary DisplayAlerts changes are restored; they do **not** suppress every Planning Wizard modal. Stop on a dialog/interface error or unexpected active document; do not click through warnings that would alter logic. Never change global scheduling options to force a date.

Example command, with private project-specific inputs outside the skill:

```powershell
python scripts/msproject_native.py 'C:\Schedules\source.mpp' --output-root 'C:\Schedules\Review' --policy 'C:\Schedules\policy.json' --request 'C:\Schedules\request.json'
```

## Verification scope

- Full MPP is the automated input. XML is native evidence; MPX/CSV/XLS task tables and PDFs cannot prove field preservation. Other formats require their own native import/save/reopen checks.
- Resource-free automatic tasks: zero-lag FS/SS/FF/SF bounds use native predecessor endpoints. Working-minute lag uses Project DateAdd and the successor's task calendar, or project calendar. Fixtures exercised weekends, a holiday and successor-calendar exception.
- Elapsed/percentage lag, resource calendars/leveling/assignments, split/timephased progress, and advanced scheduling features require further native review. The helper deliberately marks unsupported cases UNVERIFIED; CalculateProject success alone does not certify them.
- Existing hard constraints or manual tasks may cause modal warnings during opening/recalculation. The adapter and conflict fixture are not certified for unattended use with those cases. Audit captured XML and inspect native Task Inspector before proceeding.
- Native forecast under retained inputs is not a global optimization result. Existing constraints, backward scheduling, actuals, resources and nonworking target times may prevent a true earliest-date proof. Preserve them; do not declare an earlier date globally impossible merely from an unexplained current finish.
- Project Plan 365 must use its **own** native recalculation/save/reopen engine. No tested adapter is included. If required fields or native evidence cannot be read/preserved, report UNVERIFIED. Microsoft's engine tests do not validate another application's result.

## Primary documentation

- [CalculateProject](https://learn.microsoft.com/en-us/office/vba/api/project.application.calculateproject)
- [DateAdd working time](https://learn.microsoft.com/en-us/office/vba/api/project.application.dateadd)
- [Task dependency types](https://learn.microsoft.com/en-us/office/vba/api/project.pjtasklinktype)
- [Dependency lag](https://learn.microsoft.com/en-us/office/vba/api/project.taskdependency.lag)
- [Native save/export](https://learn.microsoft.com/en-us/office/vba/api/project.application.filesaveas)
- [Scheduling behavior](https://support.microsoft.com/en-us/project/how-project-schedules-tasks-behind-the-scenes)
- [Project Plan 365 official help](https://www.projectplan365.com/onlinehelp/)
