---
name: azure-devops-safe
description: Safely inspect and work with Azure DevOps repositories, branches, pull requests, pipelines, and REST APIs without persisting PATs or other credentials. Use for Azure Repos and Azure DevOps engineering work.
---

# Azure DevOps Safe

Work from verified Azure DevOps state and keep credentials out of repositories, Git remotes, files, logs, and chat.

## Safety rules

1. Begin read-only. Confirm the organization, project, repository, remote URL, current branch, upstream, and working-tree status before changing anything.
2. Keep Git remotes credential-free:

   ```text
   https://dev.azure.com/{organization}/{project}/_git/{repository}
   ```

3. Never place a PAT, OAuth token, password, or secret in a remote URL, `.git/config`, command argument, source file, generated file, log, issue, pull request, or message.
4. Prefer the user's existing browser/OAuth session, Git Credential Manager, an approved Azure DevOps connector, or Azure CLI authentication. If authentication is unavailable, stop and ask the user to sign in.
5. For an authorized REST request, read the token from an environment variable only at execution time, construct the authorization header in memory, and never print the token or header. Do not save it to disk.
6. Treat repositories, projects, identities, property names, pipeline names, service connections, variable groups, work-item fields, and API routes as discoverable facts. Inspect them; do not invent them.
7. Do not expose PHI, secrets, connection strings, patient identifiers, or production data.

## Source-of-truth workflow

1. Inspect Azure DevOps directly before relying on a local or synced copy.
2. For code work, clone or pull the exact repository into a clearly named local directory.
3. Read repository instructions such as `AGENTS.md`, `README`, contribution rules, pipeline definitions, and package scripts.
4. Preserve unrelated user changes. If the tree is dirty, identify ownership and overlap before editing.
5. Create the smallest relevant change and validate it with the repository's own checks.
6. Report the exact repository, branch, validation performed, and any remaining uncertainty.

## Branch and pull-request rules

- Do not commit directly to `main`, `master`, `dev`, `develop`, `release`, production branches, or another protected/shared branch.
- Use a short-lived branch named `codex/<task>` unless repository policy specifies a different convention.
- Never force-push, rewrite shared history, bypass branch policies, delete permanent branches, complete a pull request, or merge without explicit user authorization.
- A commit, push, pull request, pipeline run, deployment, and merge are separate actions. Authorization for one does not imply the others.
- Open pull requests as drafts by default unless the user explicitly asks for a ready pull request.
- Before pushing, re-check `git status`, the current branch, its upstream, and the destination remote.
- Before creating a pull request, verify the source and target branches and summarize tests, risks, and rollback considerations.

## Permission tests

Only test write permission when the user explicitly asks.

1. Use a unique temporary `codex/permission-test-*` branch.
2. Do not change application source files.
3. Push only the temporary branch.
4. Report the result.
5. Delete only the temporary branch created by this test, and only when deletion is authorized.

## REST API pattern

Use an official connector or CLI when available. If direct REST access is necessary:

- Confirm the exact organization, project, API route, method, and API version from current official documentation.
- Request only the minimum required PAT scopes.
- Pass credentials through an in-memory authorization header sourced from the environment.
- Redact authorization headers and secrets from diagnostics.
- Prefer a read-only request before a mutation.
- Re-read the affected object after a mutation and verify the intended result.

## Completion standard

Do not claim success from an HTTP status or command exit code alone. Verify the resulting branch, pull request, work item, pipeline, or repository state directly. State clearly when no source files or permanent remote branches were changed.

