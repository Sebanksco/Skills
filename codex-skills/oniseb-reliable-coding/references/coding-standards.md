# Coding standards

Use this reference when pulling, inspecting, changing, testing, or deploying production code.

## Target identity and source control

### Azure DevOps

Before work, confirm:

- Azure organization
- Project
- Repository
- Fetch and push remote URLs
- Current local branch
- Upstream branch
- Working-tree status
- Commit selected as the baseline

Pull or fetch from the verified remote before inspection. If the working tree is dirty, preserve the changes and determine their ownership before pulling or switching branches.

Use a dedicated `codex/<task-name>` branch for implementation. Keep discovery, permission checks, and diagnosis read-only. Do not directly change protected or shared branches unless the user explicitly authorizes that exact target.

Forbidden without explicit authorization:

- Force-pushing
- Rewriting or rebasing shared history
- Hard-resetting user work
- Deleting permanent remote branches or tags
- Merging or completing pull requests
- Triggering releases or production pipelines

### Google Apps Script and clasp

In multi-project workspaces, use one directory per Apps Script project. The local `.clasp.json` is project-specific configuration and must not be shared across projects.

Before `clasp pull` or `clasp push`:

1. Resolve the canonical project directory.
2. Read `.clasp.json`.
3. Extract and display the `scriptId`.
4. Compare it with the intended Apps Script project.
5. Stop on a missing or mismatched ID.
6. Confirm `rootDir` when present.
7. Run the operation only from that project directory.

Before `clasp push`:

1. Pull and inspect the current remote source.
2. Preserve or resolve local changes.
3. Run `clasp status`.
4. Review the exact files to be pushed.
5. Re-verify `scriptId`.
6. Push only the requested change.
7. Verify the remote state afterward when supported.

Do not use `--force` as a recovery shortcut. Do not assume that editing authorizes pushing or deploying.

## Identifiers and configuration

Existing code and connected configuration are authoritative. Never guess:

- Script, spreadsheet, folder, tenant, subscription, project, or resource IDs
- Property or environment-variable names
- Key Vault secret names
- Sheet, table, column, queue, topic, or container names
- API routes, fields, scopes, claims, webhook keys, or status values
- Deployment, pipeline, service-connection, or environment names

Classify findings:

- `Confirmed`: directly verified
- `Inferred`: supported but not directly verified
- `Missing`: required and unavailable
- `Proposed`: a new value offered for approval

Stop the affected operation when a required identifier is `Missing`. Never convert an inference into a production constant.

For an approved new configuration key:

- Use a descriptive `UPPER_SNAKE_CASE` name unless repository conventions differ.
- Define the name once in centralized configuration.
- Document required scope and format.
- Store secret values only in the approved secret store.
- Validate presence and format at startup or the system boundary.

## Headers and schemas

Use names as the contract.

### Mandatory database-object inventory before DDL

Before proposing, generating, previewing, or applying any new database table:

1. Connect read-only to the exact target server, database, and environment.
2. Pull the complete existing user-object inventory for the target schema
   (at minimum every `dbo` table; include views, procedures, functions,
   synonyms, and sequences when relevant).
3. Record table row counts, columns and types, primary/unique/index keys,
   foreign keys in both directions, defaults, checks, and known callers for
   every existing object that overlaps the proposed domain.
4. Search migrations and application code for differently named objects that
   serve the same entity or relationship.
5. Classify the decision as `Reuse`, `Evolve`, `Bridge`, or `New`. Prefer
   reusing or evolving an authoritative object over creating a parallel
   table. A new object requires documented evidence that no existing object
   owns that entity or relationship.
6. Run idempotent schema and data previews inside a rollback transaction
   before any production DDL.

Do not infer that two tables duplicate each other from their names alone.
Compare their keys, lifecycle, relationships, callers, and source-of-truth
ownership. Conversely, do not create a second master table merely because an
existing relationship table also stores descriptive snapshots.

For spreadsheets and CSV files:

1. Read the configured header row at runtime.
2. Preserve original values for display and writes.
3. Normalize only for matching, normally by trimming and applying consistent case rules.
4. Build a name-to-index map.
5. Reject duplicate normalized names.
6. Validate the full required-header set before processing records.
7. Resolve every read and write through the map.
8. Fail with the missing or duplicate header names.

Do not silently:

- Fall back to fixed column numbers
- Use the nearest matching column
- Create a missing header
- Skip a required write
- Treat blank headers as valid schema

For APIs, JSON, databases, and event payloads:

- Read fields by verified property or column name.
- Validate required fields, types, formats, nullability, and allowed values at boundaries.
- Treat field order as irrelevant unless an external protocol explicitly defines it.
- For an immutable positional format, centralize the mapping and validate positions against the documented contract.

## Change discipline

Before editing:

- Read the target and directly related code.
- Identify callers, downstream consumers, schemas, contracts, runtime, and deployment path.
- Record the current failing and passing baseline.

During editing:

- Preserve established conventions.
- Make one logical change at a time.
- Avoid unrelated cleanup.
- Avoid broad dependency upgrades.
- Do not regenerate lockfiles unless the dependency change requires it.
- Make external writes idempotent where retry is possible.
- Use structured errors and correlation identifiers without sensitive payloads.

After editing:

- Review the diff.
- Run focused tests first, then the broader available suite.
- Verify normal, empty, malformed, unauthorized, timeout, retry, duplicate, and partial-failure paths as applicable.
- Scan for secrets, PHI, destructive calls, debug code, disabled security checks, and unintended generated files.

## Server authority and code placement

The server is the final authority for every protected or controlled workflow.

- Treat all browser fields, hidden inputs, query parameters, local state, and client-calculated values as untrusted.
- Perform boundary validation before store calls, then validate referenced records again inside the transactional server/store path when their current state affects the write.
- Resolve project ownership, active status, permissions, canonical classifications, derived values, and allowed transitions from authoritative server-side data.
- When a selected authoritative entity owns a value, derive that value from the entity and ignore or reject any conflicting client value.
- Make transactions, idempotency, concurrency checks, and audit evidence server-owned. A disabled button or browser confirmation is never a security or integrity control.
- Add API tests that bypass the UI and prove invalid, stale, cross-project, unauthorized, duplicate, and conflicting requests fail closed.

Place new behavior in the primary code path that owns it:

1. Find the existing owner of the workflow, policy, state transition, or data write.
2. Modify that primary module when the behavior has one clear owner and keeping it there makes the flow easier to inspect.
3. Search for an existing canonical helper before adding one.
4. Extract a helper only when it represents a cohesive reusable policy or normalization, materially removes duplication, or creates an independently testable boundary used by multiple callers.
5. Keep helpers pure when practical. Pass required context explicitly and do not let helpers silently fetch or mutate alternate authority.
6. Reject pass-through wrappers, one-call helper files, and near-duplicate utilities that add indirection without reducing concepts.

## UI implementation consistency

Before editing a UI, inspect the target page, its stylesheet, shared UI utilities, and the closest canonical sibling page. Use those inspected patterns as the design contract.

- Preserve existing page hierarchy, container widths, typography, spacing, borders, corner radii, colors, and responsive breakpoints.
- Reuse the established table contract for parent/child rows, selection, bulk actions, state-aware expand/collapse, empty/loading/error states, and row-level actions.
- Reuse established dialogs for in-context create and edit flows. Do not redirect to another workspace when the existing pattern keeps the workflow in a popup.
- Reuse state-aware action-button shape, indicator placement, color meaning, disabled behavior, and label transitions.
- Keep status indicators attached to the established field or action when the application pattern does so; do not add a new status column without an approved design reason.
- Preserve keyboard access, labels, focus behavior, semantic controls, sufficient contrast, and responsive table usability.
- Prefer existing classes and design tokens. Do not add inline styles, duplicate selectors, a new UI framework, or a bespoke component system for a local change.
- Use concise operational labels and actionable errors. Do not expose internal UIDs, implementation details, or raw infrastructure failures to users.
- Update the repository's cache-busting asset version when a changed production asset would otherwise remain stale.
- Verify representative desktop and narrow layouts, normal and empty data, loading and error states, and enabled and disabled action states before delivery.

## Security and healthcare data

- Never commit credentials or secret values.
- Never log access tokens, authorization headers, connection strings, full webhook payloads, or patient identifiers.
- Never place PHI or production patient records in prompts, fixtures, screenshots, documentation, or test output.
- Use synthetic or irreversibly redacted test data.
- Use least-privilege identities and the project's existing secret-management abstraction.
- Treat changes to authentication, authorization, audit logging, encryption, retention, and consent as high-risk and require explicit impact analysis.

## External writes and deployment

Editing code does not authorize:

- `git push`
- `clasp push`
- Pull-request merge
- Pipeline or workflow execution
- Deployment or version promotion
- Database or schema migration
- Infrastructure mutation
- Secret creation or rotation
- Production data writes

Obtain explicit authorization for the applicable action and exact target. Prefer dry-run, preview, staging, or a temporary isolated target first.

For each deployment or migration, document:

- Target environment
- Preconditions
- Exact command or workflow
- Expected result
- Verification
- Failure and partial-failure handling
- Rollback steps
- Pre-change commit, version, or backup

## Evidence and reporting

Report checks as:

- `Passed`: executed successfully
- `Failed`: executed and failed, with concise evidence
- `Not run`: not executed, with the reason

Do not claim access, saving, pushing, deployment, migration, or testing succeeded without an authoritative result.
