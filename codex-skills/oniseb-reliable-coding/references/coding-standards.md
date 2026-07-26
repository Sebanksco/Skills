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
