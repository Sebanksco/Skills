---
name: oniseb-reliable-coding
description: Enforce source-of-truth inspection and safe production coding. Use whenever creating, reviewing, modifying, debugging, migrating, or deploying code; pulling or pushing Azure DevOps or Google Apps Script projects; using clasp in multi-project workspaces; working with spreadsheet headers, schemas, properties, secrets, APIs, SQL, webhooks, or automation; or saving generated files to an exact path. Requires verified project identity, no invented identifiers, name-based schema access, incremental changes, tests, and explicit deployment and rollback controls.
---

# ONISEB Reliable Coding

Use the authoritative live source, verify the exact target, inspect before editing, and fail closed when identity or schema facts are missing.

## 1. Establish the source of truth

Before changing code:

1. Identify the system of record, project, repository or script, environment, and deployment target.
2. Pull the current source into the exact local project directory.
3. Inspect the pulled code, configuration, manifests, callers, schemas, and deployment files directly.
4. Record facts as `Confirmed`, `Inferred`, `Missing`, or `Proposed`.
5. Do not implement from stale copies, browser snippets, memory, or assumptions when the source can be inspected.

### Azure DevOps and Git

- Treat the verified Azure DevOps repository and branch as the development source of truth.
- Before fetching or pulling, verify the organization, project, repository, `origin` URL, current branch, upstream, and `git status`.
- Do not pull over uncommitted work or discard unrelated user changes.
- Inspect the local checkout after pulling; do not rely only on the Azure browser view.
- Keep diagnosis and inventory read-only. Do not modify source files or permanent remote branches until implementation is requested.
- Perform implementation on a dedicated `codex/<task-name>` branch unless the user explicitly chooses another branch.
- Do not commit directly to `main`, `master`, `dev`, release, or production branches without explicit authorization.
- Never force-push, rewrite shared history, delete permanent branches or tags, or merge without explicit authorization.

### Google Apps Script and clasp

- Treat the intended Apps Script project as the source of truth and run `clasp pull` before inspection.
- Operate from the exact project directory. In a multi-project workspace, each Apps Script project must have its own directory and `.clasp.json`.
- Read `.clasp.json` and verify its `scriptId` against the intended Apps Script project before every `clasp pull` and every `clasp push`.
- Treat `scriptId` as the required routing key. Stop if it is missing, ambiguous, or does not match the intended project.
- Before `clasp push`, report the verified project directory and `scriptId`, run `clasp status`, inspect the diff, and confirm the push is within the requested scope.
- Do not copy or reuse `.clasp.json` between projects. Do not push from a parent directory containing multiple Apps Script projects.
- Do not use `clasp push --force` by default. Require a specific reason and explicit authorization.
- Separate code changes from deployment. A request to edit or debug does not automatically authorize `clasp push`, deployment creation, or version promotion.

## 2. Never invent identifiers

- Never make up property names, secret names, environment variables, spreadsheet headers, sheet names, table or column names, API fields, webhook parameters, IDs, endpoints, configuration keys, or deployment names.
- Discover identifiers from pulled code, manifests, schemas, property stores, environment templates, Key Vault references, connected systems, or user-provided documentation.
- Preserve existing spelling, casing, and scope.
- If an identifier cannot be verified, mark it `Missing` and stop the affected implementation or use an unmistakable placeholder only for a user-approved scaffold.
- Propose new identifiers separately. For new configuration keys, prefer descriptive `UPPER_SNAKE_CASE`, centralize them, document their scope, and never embed the secret value.

## 3. Access schemas and headers by name

- Access spreadsheet, CSV, API, and record fields by verified name, never by unexplained ordinal position.
- Before creating any database table, inventory every existing user table in
  the target schema (at minimum the complete `dbo` list), then inspect the
  columns, keys, indexes, constraints, row counts, relationships, and callers
  of every overlapping object. Classify the result as Reuse, Evolve, Bridge,
  or New; do not create a parallel authority without documented evidence.
- Read the header row at runtime, preserve original header text, normalize only for matching, and build a header-name-to-index map.
- Reject duplicate normalized headers and validate every required header before reading or writing data.
- Fail clearly on missing headers; never silently skip a field or shift to a nearby column.
- Avoid hard-coded column numbers. If an explicitly immutable external format requires positions, centralize and validate the mapping against expected header names.
- Apply the same principle to database schemas and API payloads: use verified field names and contracts rather than positional assumptions.

## 4. Implement conservatively

- Preserve repository language, formatting, naming, module, and error-handling conventions unless migration is requested.
- Establish the current build, test, lint, and runtime baseline before changing behavior.
- Make one logical change at a time and verify it before continuing.
- Avoid broad refactors, dependency upgrades, lockfile churn, or modernization during a targeted repair.
- Centralize configuration, timeouts, retry limits, feature flags, endpoint selection, and property-key names.
- Validate inputs and external responses at boundaries.
- Make retried or event-driven writes idempotent.
- Define retry, timeout, partial-failure, transaction, and rollback behavior.
- Add dry-run support for destructive, bulk, financial, migration, provisioning, or external-write operations.

### Enforce server authority

- Treat browser and client payloads as untrusted input. UI validation improves usability but never establishes final authority.
- Enforce authentication, authorization, project scope, canonical identity, allowed state transitions, and write constraints on the server.
- Re-read authoritative records and derive controlled values on the server. Ignore or reject conflicting browser-supplied values instead of trusting them.
- Test protected workflows through the API without the browser, including missing, conflicting, stale, unauthorized, and replayed requests.

### Prefer primary code; use helpers deliberately

- Implement behavior in the primary module that owns the workflow whenever that keeps the authority and control flow clear.
- Reuse an existing canonical helper before creating another one.
- Create or extend a helper only when it isolates a cohesive policy, normalization, or reusable operation; removes meaningful duplication; or is independently testable and shared by multiple callers.
- Do not create one-use pass-through wrappers, feature fragments, or helper files that hide the owning workflow without reducing complexity.
- Never place server authority in a browser helper or create a helper that becomes a competing source of truth.

### Preserve the established UI system

- Inspect the current page and its canonical sibling workspaces before changing UI code.
- Reuse existing layout containers, typography, spacing, colors, table hierarchy, dialogs, action buttons, status indicators, responsive behavior, and accessibility patterns.
- Keep state-aware labels, indicators, disabled states, selection behavior, and expand/collapse controls consistent with the existing application.
- Extend the existing stylesheet and component classes. Avoid inline styling, duplicate CSS, new visual systems, or cross-page navigation when the established workflow uses an in-page dialog.
- Make deviations from the established UI an explicit proposal. Verify changed views at representative desktop and narrow widths and update asset cache versions when required by the repository.

Read [references/coding-standards.md](references/coding-standards.md) for detailed Git, clasp, schema, security, testing, and deployment rules.

## 5. Protect secrets, production data, and PHI

- Keep credentials, tokens, secret values, connection strings, and private keys out of source, logs, spreadsheets, fixtures, documentation, and chat output.
- Use the project's approved secret manager and existing abstraction. Prefer Azure Key Vault when the Azure project already uses it.
- Never copy PHI or production patient data into tests, logs, screenshots, prompts, or local fixtures. Use redacted or synthetic data.
- Scan changed files and diffs for secrets, sensitive data, accidental destructive operations, and unintended generated files.

## 6. Verify before delivery

- Run applicable tests, linters, type checks, syntax checks, builds, and representative execution paths.
- Compare results to the recorded baseline.
- Label every check `Passed`, `Failed`, or `Not run`; never imply an unperformed check succeeded.
- Verify the diff contains only intended changes.
- Treat deployment, migration, secret rotation, infrastructure mutation, pipeline execution, and production writes as separate actions requiring explicit authorization.
- Record the pre-change commit or version and provide a tested or credible rollback path.

## 7. Save files deterministically

Follow [references/file-output-protocol.md](references/file-output-protocol.md) for generated or modified files. Never silently fall back to another directory, and never claim a file was saved without verifying the exact final path.

## 8. Deliver concisely

Report:

1. Verified target and source of truth
2. Confirmed facts, assumptions, and unresolved items
3. Changes and impact
4. Configuration and secret requirements
5. Tests performed and results
6. Deployment status and steps
7. Rollback
8. Exact files written
9. Remaining risks

Combine sections for small tasks without omitting material risks or verification gaps.
