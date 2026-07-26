---
name: oniseb-reliable-coding
description: Enforce reliable production coding and deterministic file saving for Codex and ChatGPT coding tasks. Use whenever creating, reviewing, modifying, debugging, migrating, or deploying code; working with Google Apps Script, Google Sheets, SQL, Azure Key Vault, APIs, webhooks, or automation; or generating files that must be saved to an exact user-specified path. Requires inspection of existing code and schemas, dynamic header validation, centralized configuration and secret access, explicit assumptions, tests, deployment notes, and verified no-fallback file writes.
---

# ONISEB Reliable Coding

Apply this workflow before producing or modifying production code or saving generated files.

## 1. Inspect before implementing

- Read the existing target file and directly related functions before changing code.
- Identify callers, downstream dependencies, schemas, headers, table names, property keys, API contracts, runtime, and deployment environment.
- Never invent an identifier that can be read from existing code, configuration, schemas, connected systems, or user-provided files.
- Classify task facts as `Confirmed`, `Inferred`, `Missing`, or `Proposed`.
- When required information cannot be verified, mark it unresolved and use a clearly named placeholder only when necessary to deliver a safe scaffold.

## 2. Enforce uniform coding standards

- Preserve the repository's existing language, formatting, naming, module, and error-handling conventions unless the user requests a migration.
- Centralize configuration, property-key names, endpoint URLs, timeouts, retry limits, feature flags, and environment selection.
- Keep secret values out of source code, logs, spreadsheets, and generated documentation.
- Access secrets through one approved secret-management abstraction. Prefer Azure Key Vault when the project uses Azure.
- Validate inputs, external responses, database records, and spreadsheet schemas at system boundaries.
- Use stable identifiers rather than names for joins, updates, deduplication, and synchronization.
- Make writes idempotent where retries or duplicate events are possible.
- Use structured errors and structured logging with correlation identifiers.
- Add dry-run support for destructive, bulk, financial, migration, provisioning, or external-write operations.
- Describe transaction boundaries, retry behavior, partial-failure handling, and rollback.

Read the applicable standards in `references/coding-standards.md`.

## 3. Read and validate spreadsheet headers

For spreadsheet work:

- Read the configured header row at runtime.
- Preserve original header values for display and writes.
- Normalize only for matching.
- Build a header-to-column-index map.
- Reject duplicate normalized headers.
- Validate all required headers before reading or writing rows.
- Never silently skip a missing header.
- Avoid hard-coded column numbers unless the file format is explicitly immutable.
- Batch reads and writes; avoid cell-by-cell access.

Use or adapt `scripts/header_validator.js` when working in Google Apps Script.

## 4. Save files deterministically

Follow `references/file-output-protocol.md` for every generated or modified file.

Non-negotiable rules:

1. Resolve one canonical absolute destination path before writing.
2. Treat the user-specified directory and filename as authoritative.
3. Never silently substitute the current directory, home directory, repository root, `/tmp`, `/mnt/data`, Downloads, Desktop, or another fallback path.
4. If the requested path is unavailable, unsafe, ambiguous, or outside the permitted workspace, stop and report the exact issue. Do not save elsewhere.
5. Create parent directories only when the user requested or authorized directory creation.
6. Write to a temporary file in the destination directory, flush and close it, then atomically rename or replace it into the final path when supported.
7. Verify the final file exists at the exact canonical path and is a regular file.
8. Verify expected extension, nonzero size when applicable, and optionally checksum or format validity for important artifacts.
9. Never state that a file was saved unless verification succeeded.
10. Report the exact verified path and any overwritten file explicitly.

Use `scripts/safe_write.py` for deterministic local writes when Python execution is appropriate.

## 5. Resolve output paths in this order

Use exactly one destination source, in this precedence order:

1. Explicit destination in the current user request.
2. Repository-approved destination documented in project instructions.
3. Approved output-root environment variable, such as `ONISEB_OUTPUT_ROOT`.
4. Stop with an unresolved-path error.

Never add a silent fallback destination.

For relative paths, resolve them only against the detected repository root or the explicitly configured output root. Never resolve them against an incidental shell working directory.

## 6. Test and review

Before delivering code:

- Run available tests, linters, type checks, syntax checks, and representative execution paths.
- Include tests for normal input, missing required fields, missing headers, duplicate records, malformed identifiers, unauthorized access, timeouts, retries, partial failures, empty datasets, and unexpected external responses as applicable.
- Scan for embedded secrets and accidental destructive operations.
- Review file writes for path traversal, fallback paths, filename collisions, and unverified success claims.

## 7. Deliver in a standard format

Provide:

1. `Understanding`
2. `Verified structure`
3. `Assumptions and unresolved items`
4. `Impact analysis`
5. `Implementation`
6. `Configuration and secrets`
7. `Tests performed`
8. `Deployment steps`
9. `Rollback`
10. `Files written`, listing each exact verified absolute path
11. `Remaining risks`

For small tasks, combine sections without omitting material risks or file-path verification.
