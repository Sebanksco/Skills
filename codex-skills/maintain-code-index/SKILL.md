---
name: maintain-code-index
description: Maintain project index files and code inventory documentation for local repositories, Apps Script clasp projects, GitHub remotes, OneDrive or SharePoint synced copies, and Codex skills. Use when the user asks to update an index, refresh INDEX.md, document current code locations, record deployment IDs, reconcile project boundaries, or create a current map of code/documentation/skills.
---

# Maintain Code Index

## Overview

Use this skill to update index documentation from live local state. Treat an index as an operational map: where code lives, what project each folder belongs to, what can be pushed together, and what must stay separate.

## Workflow

1. Read the existing index file first, usually `INDEX.md`.
2. Gather live state before editing:
   - `rg --files` for project files.
   - Git remote, branch, latest commit, and `git status --short` when inside a repo.
   - `.clasp.json`, `appsscript.json`, and `clasp status` for Apps Script projects when relevant.
   - Existing synced folders under OneDrive or SharePoint paths when the index mentions them.
3. Identify project boundaries before summarizing:
   - Apps Script projects by script ID and clasp folder.
   - GitHub repos and PRs by remote URL and branch.
   - Sync copies by exact local path.
   - Temporary inspection, pull, or publish folders that should not be treated as source.
4. Update the index with current facts only. Do not infer a successful push, deploy, sync, or merge unless verified.
5. Keep the index concise and scannable. Prefer sections with bullets over long narrative.
6. Preserve warnings about dangerous boundaries, especially "do not push this folder to that script/repo" notes.
7. After editing, verify by reading the changed index and checking the most important paths still exist.

## Index Contents

For an application workspace, include:

- Last updated timestamp with timezone.
- Canonical working folder.
- Synced copy paths.
- GitHub remote, branch, PRs, and dirty working tree notes.
- Apps Script IDs and local clasp folders.
- Source files and README/documentation files.
- Push boundaries: what belongs in each project and what must be excluded.
- Deployment or test status when recently verified.
- Security notes for credentials, script properties, or secrets.

For a multi-project workspace, give each project its own section and avoid mixing responsibilities.

## Path Rules

- Use exact Windows paths when the user works on Windows.
- Distinguish local working folders from OneDrive or SharePoint synced copies.
- Treat `OneDrive - <org>` and `Sharepoint - <org>` as local sync roots, not as proof of cloud upload completion.
- Mark temporary folders such as `.deployed-inspection`, `.deployed-version-1`, and `.publish-*` as inspection artifacts unless the user intentionally promotes them.

## Apps Script Rules

- Always inspect `.clasp.json` before describing or pushing a clasp project.
- Record the Apps Script ID and local folder together.
- If one folder contains files for multiple Apps Script projects, flag it as a boundary problem.
- Use `.claspignore` or separate folders to prevent cross-project pushes.

## Reference

Read `references/index-structure.md` when creating a new index from scratch or when the existing index is badly stale.
