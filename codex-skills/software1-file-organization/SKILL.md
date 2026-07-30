---
name: software1-file-organization
description: Use this skill when Codex is doing coding work for Clinton and needs to create, copy, organize, index, migrate, or place project files under the Cura Digital Health Solutions Software folder and its required Google Drive mirror. Trigger for requests mentioning Software, Software1, coding work file locations, Google Drive project mirrors, Code/Documentation/SDK placement, file organization, migration indexes, non-destructive copies, or project folder conventions.
---

# Software File Organization

## Core Rule

Use this folder as Clinton's default home for coding work:

`C:\Users\ClintonBaird\Cura Digital Health Solutions\Cura Digital Health Solutions Team Site - Documents\Software`

For any project that combines a Google Sheet or other business data workbook with code, Apps Script, scripts, or automation logic, the canonical project folder must be created under:

`C:\Users\ClintonBaird\Cura Digital Health Solutions\Cura Digital Health Solutions Team Site - Documents\Software\Code\<Project Name>`

Do not treat `C:\Users\ClintonBaird\OneDrive - Cura Digital Health Solutions\DIC\BackOffice\ClaudeAI_Documentation` as the canonical location for sheet-and-code projects. That OneDrive path may be used only as a known legacy/scratch/workspace location when unavoidable, and any useful code or documentation created there must be moved or mirrored into the matching `Software` project folder before completion.

Place coding-work files under one of these top-level folders inside `Software`:

- `Code`
- `Documentation`
- `SDK`

If the project does not already have a logical folder under the right category, create a named project folder first. If there is no clear logical folder or project name, ask Clinton before placing the file.

## Google Drive Mirror

Mirror every final coding-work file to this Google Drive root:

`https://drive.google.com/drive/folders/1Xc4q5mRjb_Gk5PnGF-3sBaCWa0yXJYt6`

Use this hierarchy:

`<Type>/<Project Name>/Code`

`<Type>/<Project Name>/Documentation`

Approved `Type` values:

- `Software`
- `Twilio WebDev`

Determine `<Project Name>` from the active project, such as `QBO` or `Field Assets`. If it is unclear, ask Clinton rather than guessing.

Before saving:

1. Inspect the Drive root and reuse an exact existing type/project folder.
2. Create the type folder when it does not exist.
3. Create the project folder when it does not exist.
4. Ensure both `Code` and `Documentation` exist inside every created project folder.
5. Mirror source code, scripts, Apps Script, SQL, configuration, and SDK artifacts to `Code`.
6. Mirror Markdown, Word, PDF, spreadsheets, reports, screenshots, and implementation notes to `Documentation`.
7. Preserve the local Software canonical project folder as the working source of truth; the Google Drive location is the required cloud mirror.
8. Never overwrite an existing Drive file silently. Compare or version it, and report the exact destination URL.

## Standing Save And Log Rules

For Clinton's coding work, follow these rules without needing to be asked each time:

- Interpret **"save to path"** as an instruction to save the same final files to both:
  - the canonical local SharePoint/Software synced project path; and
  - the matching Google Drive `<Type>/<Project Name>/Code` or `Documentation` folder.
- Interpret **"save to git"** as an instruction to commit and push the relevant project changes to the project's existing Git repository.
- Before a Git save, inspect the repository, current branch, remote, and worktree. Stage only files belonging to the requested work and do not include unrelated user changes.
- If the project has no Git repository, no configured remote, or an ambiguous repository destination, ask Clinton for the repository URL. Do not initialize a repository, create a remote, or guess a destination.
- A **"save to path"** request does not imply a Git commit or push. Git operations occur only when Clinton says **"save to git"**, **"commit"**, **"push"**, or otherwise explicitly requests version-control publication.
- Work/edit/push from the SharePoint/Software synced project folder when the project has business data sheets plus code, Apps Script, scripts, or automation logic.
- If an older OneDrive synced workspace repo exists, use it only long enough to migrate or reconcile changes into the matching `Software\Code\<Project Name>` folder.
- Save or mirror clean copies of changed project files to the SharePoint/Software synced project path before completion.
- Save the same final files to the matching Google Drive `<Type>/<Project Name>/Code` or `Documentation` folder before completion.
- Commit and push important versions to the project's GitHub versioned source when Clinton asks to commit, push, or publish the work.
- On every new Git commit, add or update a project index/change-log entry with the commit hash, summary, repo URL, important files, and timestamp when an index or log exists for that project.
- On any file change, ensure the changed source is saved in the appropriate Software `Code`, `Documentation`, or `SDK` project path. For sheet-and-code projects, create that Software project folder first if it does not already exist.
- If the correct project index/log does not exist yet, create a simple Markdown command/index file in the project folder and mirror it to Software.


## Storage Terminology

Use these terms consistently across projects and chats:

- **Software canonical project folder** means `C:\Users\ClintonBaird\Cura Digital Health Solutions\Cura Digital Health Solutions Team Site - Documents\Software\...`: the preferred local synced SharePoint team-site folder used as the organized shared source location for code, documentation, and SDK files.
- **OneDrive synced workspace** means `C:\Users\ClintonBaird\OneDrive - Cura Digital Health Solutions\...`: a local filesystem folder on Clinton's computer that is cloud-synced by OneDrive. For sheet-and-code projects, treat this as a legacy/scratch/workspace location, not the source of truth.
- **SharePoint/Software synced archive** means the same `Software` path above when referring to shared archived copies of generated or historical project files.
- **GitHub versioned source** means the Git remote/repository used for commit history, branches, and versioned code source.

Do not imply that OneDrive is not cloud storage. When referring to paths under OneDrive or SharePoint, distinguish between the local synced filesystem path and the cloud-backed storage location.

## Non-Destructive Organization

When organizing or migrating files:

- Do not overwrite existing files unless Clinton explicitly approves it.
- Do not delete source files unless Clinton explicitly approves it.
- Prefer copy-only migrations when Clinton asks to organize an existing folder.
- Skip files that already exist at the destination and report the skip count.
- Preserve relative structure inside the selected project folder when that structure is meaningful.
- Use a migration/index plan before large copy operations.

## Category Guidance

Use `Code` for source code, scripts, apps, Apps Script, SQL, PowerShell, shell files, configuration that belongs with code, and runnable project folders.

Use `Documentation` for Markdown, Word, PDF, Excel, CSV, generated reports, screenshots, reference material, implementation notes, and migration indexes.

Use `SDK` for SDK packages, API client packages, generated SDK artifacts, and explicit SDK folders.

Known exception: `BashMedia Content` may exist inside older Software folders incorrectly. Do not move it unless Clinton explicitly asks.

## Indexing Workflow

When Clinton asks for an index:

1. Inventory the source and target folders.
2. Create a local workbook index with at least a summary sheet, existing target files, and a migration plan.
3. Convert or upload it as a native Google Sheet when the Google Drive connector is available and Clinton requested a Google Sheet.
4. Store a copy of the workbook under `Software\Documentation` in a named project folder.

## Current Helper Files

The current migration helpers live here:

- `C:\Users\ClintonBaird\OneDrive - Cura Digital Health Solutions\DIC\BackOffice\ClaudeAI_Documentation\tools\software1_migration_index.mjs`
- `C:\Users\ClintonBaird\OneDrive - Cura Digital Health Solutions\DIC\BackOffice\ClaudeAI_Documentation\tools\copy_software1_migration.mjs`

Use or adapt these helpers when repeating the Software index/copy workflow.
