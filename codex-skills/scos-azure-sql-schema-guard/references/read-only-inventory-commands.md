# Read-only Azure and SQL inventory commands

These commands list existing resources. They do not create or modify Azure or SQL objects.

## Confirm Azure context

```powershell
az account show --query "{Subscription:name,SubscriptionId:id,TenantId:tenantId,Account:user.name}" -o table
```

## Resource groups

```powershell
az group list --query "[].{ResourceGroup:name,Location:location}" -o table
```

## Key Vaults

```powershell
az keyvault list --query "[].{KeyVault:name,ResourceGroup:resourceGroup,Location:location}" -o table
```

List secret names only for one vault; this does not display values:

```powershell
az keyvault secret list --vault-name kv-scos-prod --query "[].name" -o tsv
```

## SQL servers

```powershell
az sql server list --query "[].{Server:name,ResourceGroup:resourceGroup,Location:location,FQDN:fullyQualifiedDomainName}" -o table
```

## All SQL databases on every discovered server

```powershell
$servers = az sql server list -o json | ConvertFrom-Json
foreach ($server in $servers) {
    az sql db list `
      --resource-group $server.resourceGroup `
      --server $server.name `
      --query "[].{Server:'$($server.name)',Database:name,Status:status,SKU:currentSku.name}" `
      -o table
}
```

## Tables in the selected SSMS database

Run in an SSMS query window after selecting the intended database:

```sql
SELECT
    s.name AS SchemaName,
    t.name AS TableName,
    SUM(CASE WHEN p.index_id IN (0, 1) THEN p.rows ELSE 0 END) AS RowCount
FROM sys.tables AS t
JOIN sys.schemas AS s ON s.schema_id = t.schema_id
LEFT JOIN sys.partitions AS p ON p.object_id = t.object_id
GROUP BY s.name, t.name
ORDER BY s.name, t.name;
```

## Columns, types, defaults, and identity settings

```sql
SELECT
    s.name AS SchemaName,
    t.name AS TableName,
    c.column_id AS ColumnOrder,
    c.name AS ColumnName,
    ty.name AS DataType,
    c.max_length AS MaxLengthBytes,
    c.[precision] AS [Precision],
    c.scale AS Scale,
    c.is_nullable AS IsNullable,
    c.is_identity AS IsIdentity,
    dc.definition AS DefaultDefinition
FROM sys.tables AS t
JOIN sys.schemas AS s ON s.schema_id = t.schema_id
JOIN sys.columns AS c ON c.object_id = t.object_id
JOIN sys.types AS ty ON ty.user_type_id = c.user_type_id
LEFT JOIN sys.default_constraints AS dc ON dc.object_id = c.default_object_id
ORDER BY s.name, t.name, c.column_id;
```

## Full guarded refresh

```powershell
& "$HOME\.codex\skills\scos-azure-sql-schema-guard\scripts\Update-ScosAzureSqlSchemaGuard.ps1"
```

