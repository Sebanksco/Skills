---
name: scos-azure-sql-schema-guard
description: Inspect and refresh Clinton's verified Azure resource and SQL schema inventory before designing, reviewing, or implementing SCOS, SEBANKS, Maintenance, QBO, ONI, portal, careers, or shared-reference database changes. Use when Codex needs resource group, Key Vault, SQL server, database, table, column, key, constraint, or index names, or when creating migrations and new dbo tables without inventing infrastructure names.
---

# SCOS Azure SQL Schema Guard

Use verified live inventory before proposing or applying database structure changes.

## Mandatory safeguards

- Never create or rename a resource group, Key Vault, SQL server, or database without Clinton's explicit permission for that exact resource.
- Do not infer resource names from folders, code, or naming patterns.
- Never print or persist secret values. Retrieve SQL credentials only into ephemeral process variables.
- Treat an inaccessible database as `Unverified`, never as empty.
- New tables requested for the shared production database must use the existing `sql-scos-prod` / `db-scos-prod` target and `dbo` schema unless Clinton explicitly approves another verified target.
- Before a `CREATE TABLE` migration, search the current inventory for naming collisions and related tables, columns, keys, and indexes.
- Preserve existing objects. Do not drop, rename, truncate, or destructively alter objects unless the user explicitly authorizes the exact operation.
- Prepare and review the migration first. Apply it only when the active request authorizes deployment.
- Use idempotent guards for additive migrations, record a migration identifier, and verify the resulting schema after application.

## Workflow

1. If `references/current-azure-sql-schema.md` or `.json` is absent, run `scripts/Update-ScosAzureSqlSchemaGuard.ps1` before proceeding. Generated live inventories are intentionally excluded from the public skill repository.
2. Read `references/current-azure-sql-schema.md` for resource and database verification status.
3. Search `references/current-azure-sql-schema.json` for exact table and column details. Prefer `rg` instead of loading the entire JSON file.
4. If the inventory is stale or the requested object is absent, run `scripts/Update-ScosAzureSqlSchemaGuard.ps1`.
5. State the exact resource group, SQL server, database, and schema targeted by the proposed change.
6. Reuse existing naming, data types, audit fields, foreign-key patterns, and indexes where the inventory shows a clear precedent.
7. Identify collisions, related tables, and compatibility risks before writing migration code.
8. Validate syntax and run a no-write inspection before any authorized deployment.
9. After deployment, refresh the inventory and confirm the expected table, columns, constraints, and indexes exist.

## Refresh commands

```powershell
& "$HOME\.codex\skills\scos-azure-sql-schema-guard\scripts\Update-ScosAzureSqlSchemaGuard.ps1"
```

Preview in memory without replacing reference files:

```powershell
& "$HOME\.codex\skills\scos-azure-sql-schema-guard\scripts\Update-ScosAzureSqlSchemaGuard.ps1" -Preview
```

For reusable read-only Azure and SSMS commands, read `references/read-only-inventory-commands.md`.

## Migration response requirements

For any proposed database structure change, report:

- verified target resource group, server, database, and schema;
- existing related objects found;
- objects to be added or changed;
- whether the change is additive, reversible, and idempotent;
- indexes and constraints included;
- verification query;
- anything unverified or requiring user permission.

