# File output protocol

Use this protocol for every generated or modified local file.

## Resolve the destination

Choose exactly one destination in this order:

1. Explicit path in the current user request
2. Repository-approved path in project instructions
3. Approved output-root environment variable
4. Stop because the path is unresolved

Resolve a relative path only against the verified repository root or approved output root. Never resolve it against an incidental shell directory.

Before writing:

- Resolve and display the canonical absolute path.
- Confirm the path is within the authorized workspace.
- Confirm whether the file exists.
- Preserve unrelated content and user changes.
- Create parent directories only when authorized.
- Stop if the requested path is unavailable, ambiguous, unsafe, or outside permitted storage.

Never silently substitute:

- Current working directory
- Home directory
- Repository root
- Temporary directory
- Downloads or Desktop
- `/mnt/data`
- Any other fallback

## Write and verify

Prefer an atomic write when the format and tool support it:

1. Write a temporary file in the destination directory.
2. Flush and close it.
3. Validate its format and expected content.
4. Atomically rename or replace it.
5. Verify the final path is a regular file.

Verify as applicable:

- Exact canonical path
- Expected extension
- Nonzero size
- Parse or format validity
- Expected sheet, document, or archive structure
- Checksum for important binary artifacts
- No unexpected sibling or fallback output

Never state that a file was saved unless verification succeeded. Report every exact file path written and identify overwritten files explicitly.

## Source-code files

For repository files:

- Inspect the existing file before editing.
- Preserve encoding and line-ending conventions where practical.
- Review the final diff.
- Do not overwrite unrelated changes.
- Do not generate build artifacts, caches, credentials, or local configuration into tracked paths unless requested.

Mark validation as `Passed`, `Failed`, or `Not run`.
