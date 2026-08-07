[CmdletBinding()]
param(
    [string]$OutputRoot = (Join-Path $PSScriptRoot '..\references'),
    [switch]$Preview
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$expectedSubscriptionId = '6cc6256f-30f9-4da3-b5ff-e4cccdd909b7'
$expectedTenantId = '8e7f5440-e6ff-4280-a2de-66224e5310f6'
$generatedAt = (Get-Date).ToUniversalTime()
$delimiter = [char]31

foreach ($command in @('az', 'sqlcmd')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command is not installed: $command"
    }
}

function Invoke-AzJson {
    param([Parameter(Mandatory)][string[]]$Arguments)
    $raw = & az @Arguments --output json
    if ($LASTEXITCODE -ne 0) { throw "Azure CLI failed: az $($Arguments -join ' ')" }
    if (-not $raw) { return @() }
    return $raw | ConvertFrom-Json
}

function Get-SecretNameList {
    param([Parameter(Mandatory)][string]$Vault)
    try {
        $names = & az keyvault secret list --vault-name $Vault --query '[].name' --output tsv 2>$null
        if ($LASTEXITCODE -ne 0) { return $null }
        return @($names | Where-Object { $_ } | Sort-Object)
    } catch { return $null }
}

function Get-EphemeralSecret {
    param([Parameter(Mandatory)][string]$Vault, [Parameter(Mandatory)][string]$Name)
    $value = & az keyvault secret show --vault-name $Vault --name $Name --query value --output tsv 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $value) { throw "Secret is unavailable: $Vault/$Name" }
    return [string]$value
}

function Convert-BooleanText {
    param([string]$Value)
    return $Value -eq '1'
}

function Convert-NullableInt {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
    return [int]$Value
}

function Invoke-DatabaseSchemaInventory {
    param(
        [Parameter(Mandatory)][string]$Label,
        [Parameter(Mandatory)][string]$Server,
        [Parameter(Mandatory)][string]$Database,
        [Parameter(Mandatory)][string]$User,
        [Parameter(Mandatory)][string]$Password
    )

    $d = "NCHAR(31)"
    $query = @"
SET NOCOUNT ON;

SELECT N'TABLE'+$d+(s.name COLLATE DATABASE_DEFAULT)+$d+(t.name COLLATE DATABASE_DEFAULT)+$d+CONVERT(nvarchar(30),SUM(CASE WHEN p.index_id IN (0,1) THEN p.rows ELSE 0 END))
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id=t.schema_id
LEFT JOIN sys.partitions p ON p.object_id=t.object_id
GROUP BY s.name,t.name;

SELECT N'COLUMN'+$d+(s.name COLLATE DATABASE_DEFAULT)+$d+(t.name COLLATE DATABASE_DEFAULT)+$d+CONVERT(nvarchar(10),c.column_id)+$d+(c.name COLLATE DATABASE_DEFAULT)+$d+(ty.name COLLATE DATABASE_DEFAULT)+$d+
       CONVERT(nvarchar(10),c.max_length)+$d+CONVERT(nvarchar(10),c.precision)+$d+CONVERT(nvarchar(10),c.scale)+$d+
       CONVERT(nvarchar(1),c.is_nullable)+$d+CONVERT(nvarchar(1),c.is_identity)+$d+
       ISNULL(REPLACE(REPLACE(dc.definition COLLATE DATABASE_DEFAULT,CHAR(13),N' '),CHAR(10),N' '),N'')+$d+
       ISNULL(REPLACE(REPLACE(cc.definition COLLATE DATABASE_DEFAULT,CHAR(13),N' '),CHAR(10),N' '),N'')
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.columns c ON c.object_id=t.object_id
JOIN sys.types ty ON ty.user_type_id=c.user_type_id
LEFT JOIN sys.default_constraints dc ON dc.object_id=c.default_object_id
LEFT JOIN sys.computed_columns cc ON cc.object_id=c.object_id AND cc.column_id=c.column_id;

SELECT N'PK'+$d+(s.name COLLATE DATABASE_DEFAULT)+$d+(t.name COLLATE DATABASE_DEFAULT)+$d+(kc.name COLLATE DATABASE_DEFAULT)+$d+CONVERT(nvarchar(10),ic.key_ordinal)+$d+(c.name COLLATE DATABASE_DEFAULT)
FROM sys.key_constraints kc
JOIN sys.tables t ON t.object_id=kc.parent_object_id
JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.index_columns ic ON ic.object_id=t.object_id AND ic.index_id=kc.unique_index_id
JOIN sys.columns c ON c.object_id=t.object_id AND c.column_id=ic.column_id
WHERE kc.type='PK';

SELECT N'FK'+$d+(ps.name COLLATE DATABASE_DEFAULT)+$d+(pt.name COLLATE DATABASE_DEFAULT)+$d+(fk.name COLLATE DATABASE_DEFAULT)+$d+(pc.name COLLATE DATABASE_DEFAULT)+$d+(rs.name COLLATE DATABASE_DEFAULT)+$d+(rt.name COLLATE DATABASE_DEFAULT)+$d+(rc.name COLLATE DATABASE_DEFAULT)+$d+
       (fk.delete_referential_action_desc COLLATE DATABASE_DEFAULT)+$d+(fk.update_referential_action_desc COLLATE DATABASE_DEFAULT)
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id=fk.object_id
JOIN sys.tables pt ON pt.object_id=fk.parent_object_id
JOIN sys.schemas ps ON ps.schema_id=pt.schema_id
JOIN sys.columns pc ON pc.object_id=pt.object_id AND pc.column_id=fkc.parent_column_id
JOIN sys.tables rt ON rt.object_id=fk.referenced_object_id
JOIN sys.schemas rs ON rs.schema_id=rt.schema_id
JOIN sys.columns rc ON rc.object_id=rt.object_id AND rc.column_id=fkc.referenced_column_id;

SELECT N'INDEX'+$d+(s.name COLLATE DATABASE_DEFAULT)+$d+(t.name COLLATE DATABASE_DEFAULT)+$d+(i.name COLLATE DATABASE_DEFAULT)+$d+CONVERT(nvarchar(1),i.is_unique)+$d+
       CONVERT(nvarchar(1),i.is_primary_key)+$d+CONVERT(nvarchar(1),i.is_unique_constraint)+$d+
       CONVERT(nvarchar(10),ic.key_ordinal)+$d+CONVERT(nvarchar(1),ic.is_included_column)+$d+(c.name COLLATE DATABASE_DEFAULT)+$d+
       ISNULL(REPLACE(REPLACE(i.filter_definition COLLATE DATABASE_DEFAULT,CHAR(13),N' '),CHAR(10),N' '),N'')
FROM sys.indexes i
JOIN sys.tables t ON t.object_id=i.object_id
JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.index_columns ic ON ic.object_id=i.object_id AND ic.index_id=i.index_id
JOIN sys.columns c ON c.object_id=i.object_id AND c.column_id=ic.column_id
WHERE i.index_id>0 AND i.name IS NOT NULL;

SELECT N'CHECK'+$d+(s.name COLLATE DATABASE_DEFAULT)+$d+(t.name COLLATE DATABASE_DEFAULT)+$d+(cc.name COLLATE DATABASE_DEFAULT)+$d+
       REPLACE(REPLACE(cc.definition COLLATE DATABASE_DEFAULT,CHAR(13),N' '),CHAR(10),N' ')
FROM sys.check_constraints cc
JOIN sys.tables t ON t.object_id=cc.parent_object_id
JOIN sys.schemas s ON s.schema_id=t.schema_id;
"@

    $previousPassword = $env:SQLCMDPASSWORD
    try {
        $env:SQLCMDPASSWORD = $Password
        $raw = & sqlcmd -S $Server -d $Database -U $User -C -Q $query -h -1 -W -w 65535 2>&1
        if ($LASTEXITCODE -ne 0) {
            return [pscustomobject]@{ Label=$Label; Server=$Server; Database=$Database; Status='Unverified'; Error='SQL connection or schema query failed'; Tables=@(); Columns=@(); PrimaryKeys=@(); ForeignKeys=@(); Indexes=@(); Checks=@() }
        }

        $tables = [System.Collections.Generic.List[object]]::new()
        $columns = [System.Collections.Generic.List[object]]::new()
        $primaryKeys = [System.Collections.Generic.List[object]]::new()
        $foreignKeys = [System.Collections.Generic.List[object]]::new()
        $indexes = [System.Collections.Generic.List[object]]::new()
        $checks = [System.Collections.Generic.List[object]]::new()

        foreach ($line in $raw) {
            $parts = ([string]$line).Split($delimiter)
            if ($parts.Count -lt 2) { continue }
            switch ($parts[0].Trim()) {
                'TABLE' {
                    if ($parts.Count -ge 4) { [void]$tables.Add([pscustomobject]@{ Schema=$parts[1]; Table=$parts[2]; Rows=[int64]$parts[3] }) }
                }
                'COLUMN' {
                    if ($parts.Count -ge 13) {
                        [void]$columns.Add([pscustomobject]@{ Schema=$parts[1]; Table=$parts[2]; Ordinal=[int]$parts[3]; Column=$parts[4]; DataType=$parts[5]; MaxLength=[int]$parts[6]; Precision=[int]$parts[7]; Scale=[int]$parts[8]; Nullable=(Convert-BooleanText $parts[9]); Identity=(Convert-BooleanText $parts[10]); Default=$parts[11]; Computed=$parts[12] })
                    }
                }
                'PK' {
                    if ($parts.Count -ge 6) { [void]$primaryKeys.Add([pscustomobject]@{ Schema=$parts[1]; Table=$parts[2]; Constraint=$parts[3]; Ordinal=[int]$parts[4]; Column=$parts[5] }) }
                }
                'FK' {
                    if ($parts.Count -ge 10) { [void]$foreignKeys.Add([pscustomobject]@{ Schema=$parts[1]; Table=$parts[2]; Constraint=$parts[3]; Column=$parts[4]; ReferencedSchema=$parts[5]; ReferencedTable=$parts[6]; ReferencedColumn=$parts[7]; OnDelete=$parts[8]; OnUpdate=$parts[9] }) }
                }
                'INDEX' {
                    if ($parts.Count -ge 11) { [void]$indexes.Add([pscustomobject]@{ Schema=$parts[1]; Table=$parts[2]; Index=$parts[3]; Unique=(Convert-BooleanText $parts[4]); PrimaryKey=(Convert-BooleanText $parts[5]); UniqueConstraint=(Convert-BooleanText $parts[6]); KeyOrdinal=[int]$parts[7]; Included=(Convert-BooleanText $parts[8]); Column=$parts[9]; Filter=$parts[10] }) }
                }
                'CHECK' {
                    if ($parts.Count -ge 5) { [void]$checks.Add([pscustomobject]@{ Schema=$parts[1]; Table=$parts[2]; Constraint=$parts[3]; Definition=$parts[4] }) }
                }
            }
        }

        return [pscustomobject]@{
            Label=$Label; Server=$Server; Database=$Database; Status='Verified'; Error=''
            Tables=@($tables | Sort-Object Schema,Table)
            Columns=@($columns | Sort-Object Schema,Table,Ordinal)
            PrimaryKeys=@($primaryKeys | Sort-Object Schema,Table,Ordinal)
            ForeignKeys=@($foreignKeys | Sort-Object Schema,Table,Constraint,Column)
            Indexes=@($indexes | Sort-Object Schema,Table,Index,KeyOrdinal,Column)
            Checks=@($checks | Sort-Object Schema,Table,Constraint)
        }
    } finally {
        $env:SQLCMDPASSWORD = $previousPassword
        $Password = $null
    }
}

$account = Invoke-AzJson @('account','show')
if ($account.id -ne $expectedSubscriptionId -or $account.tenantId -ne $expectedTenantId) {
    throw "Azure context mismatch. Expected subscription $expectedSubscriptionId in tenant $expectedTenantId; found $($account.id) in $($account.tenantId)."
}

$resourceGroups = @(Invoke-AzJson @('group','list')) | Sort-Object name
$vaults = @(Invoke-AzJson @('keyvault','list')) | Sort-Object name
$sqlServers = @(Invoke-AzJson @('sql','server','list')) | Sort-Object name
$databases = [System.Collections.Generic.List[object]]::new()
foreach ($server in $sqlServers) {
    foreach ($database in @(Invoke-AzJson @('sql','db','list','--resource-group',$server.resourceGroup,'--server',$server.name)) | Where-Object name -ne 'master') {
        [void]$databases.Add([pscustomobject]@{ Server=$server.name; ResourceGroup=$server.resourceGroup; Database=$database.name; Status=$database.status; Sku=$database.currentSku.name })
    }
}

$vaultInventory = foreach ($vault in $vaults) {
    $names = Get-SecretNameList $vault.name
    [pscustomobject]@{
        Name=$vault.name
        ResourceGroup=$vault.resourceGroup
        Location=$vault.location
        MetadataAccess=if ($null -eq $names) {'Unverified'} else {'Verified'}
        SecretCount=if ($null -eq $names) {$null} else {@($names).Count}
    }
}

$schemaInventories = [System.Collections.Generic.List[object]]::new()
try {
    [void]$schemaInventories.Add((Invoke-DatabaseSchemaInventory -Label 'SCOS production' -Server (Get-EphemeralSecret 'kv-scos-prod' 'SQL-SERVER') -Database (Get-EphemeralSecret 'kv-scos-prod' 'SQL-DATABASE') -User (Get-EphemeralSecret 'kv-scos-prod' 'SQL-USER') -Password (Get-EphemeralSecret 'kv-scos-prod' 'SQL-PASSWORD')))
} catch {
    [void]$schemaInventories.Add([pscustomobject]@{ Label='SCOS production'; Server='sql-scos-prod.database.windows.net'; Database='db-scos-prod'; Status='Unverified'; Error=$_.Exception.Message; Tables=@(); Columns=@(); PrimaryKeys=@(); ForeignKeys=@(); Indexes=@(); Checks=@() })
}

foreach ($mapping in @(
    @{Label='ONI medication confirmation'; DatabaseSecret='ONI-MEDCONF-DATABASE'; UserSecret='ONI-MEDCONF-SQL-USER'; PasswordSecret='ONI-MEDCONF-SQL-PASSWORD'},
    @{Label='ONI RxNorm'; DatabaseSecret='ONI-RXNORM-DATABASE'; UserSecret='ONI-RXNORM-READER-SQL-USER'; PasswordSecret='ONI-RXNORM-READER-SQL-PASSWORD'}
)) {
    try {
        $databaseName = Get-EphemeralSecret 'kv-oniseb-prod' $mapping.DatabaseSecret
        $databaseResource = @($databases | Where-Object Database -eq $databaseName)[0]
        if (-not $databaseResource) { throw "Azure SQL database resource was not found: $databaseName" }
        [void]$schemaInventories.Add((Invoke-DatabaseSchemaInventory -Label $mapping.Label -Server ($databaseResource.Server + '.database.windows.net') -Database $databaseName -User (Get-EphemeralSecret 'kv-oniseb-prod' $mapping.UserSecret) -Password (Get-EphemeralSecret 'kv-oniseb-prod' $mapping.PasswordSecret)))
    } catch {
        [void]$schemaInventories.Add([pscustomobject]@{ Label=$mapping.Label; Server=''; Database=''; Status='Unverified'; Error=$_.Exception.Message; Tables=@(); Columns=@(); PrimaryKeys=@(); ForeignKeys=@(); Indexes=@(); Checks=@() })
    }
}

$oniRequired = @('ONI-SQL-SERVER','ONI-SQL-DATABASE','ONI-SQL-USER','ONI-SQL-PASSWORD')
$oniNames = Get-SecretNameList 'kv-oniseb-prod'
if ($null -ne $oniNames -and @($oniRequired | Where-Object { $_ -notin $oniNames }).Count -eq 0) {
    try {
        [void]$schemaInventories.Add((Invoke-DatabaseSchemaInventory -Label 'ONI production' -Server (Get-EphemeralSecret 'kv-oniseb-prod' 'ONI-SQL-SERVER') -Database (Get-EphemeralSecret 'kv-oniseb-prod' 'ONI-SQL-DATABASE') -User (Get-EphemeralSecret 'kv-oniseb-prod' 'ONI-SQL-USER') -Password (Get-EphemeralSecret 'kv-oniseb-prod' 'ONI-SQL-PASSWORD')))
    } catch {
        [void]$schemaInventories.Add([pscustomobject]@{ Label='ONI production'; Server='sql-oni-prod.database.windows.net'; Database='db-oni-prod'; Status='Unverified'; Error=$_.Exception.Message; Tables=@(); Columns=@(); PrimaryKeys=@(); ForeignKeys=@(); Indexes=@(); Checks=@() })
    }
} else {
    [void]$schemaInventories.Add([pscustomobject]@{ Label='ONI production'; Server='sql-oni-prod.database.windows.net'; Database='db-oni-prod'; Status='Unverified'; Error='Dedicated ONI-SQL-* credential names are not present in kv-oniseb-prod'; Tables=@(); Columns=@(); PrimaryKeys=@(); ForeignKeys=@(); Indexes=@(); Checks=@() })
}

$snapshot = [pscustomobject]@{
    GeneratedAtUtc=$generatedAt.ToString('o')
    Subscription=[pscustomobject]@{ Name=$account.name; Id=$account.id; TenantId=$account.tenantId }
    ResourceGroups=@($resourceGroups | ForEach-Object { [pscustomobject]@{ Name=$_.name; Location=$_.location } })
    KeyVaults=@($vaultInventory)
    SqlServers=@($sqlServers | ForEach-Object { [pscustomobject]@{ Name=$_.name; ResourceGroup=$_.resourceGroup; Location=$_.location; Fqdn=$_.fullyQualifiedDomainName } })
    Databases=@($databases | Sort-Object Server,Database)
    SchemaInventories=@($schemaInventories)
}

$verified = @($schemaInventories | Where-Object Status -eq 'Verified')
$tableCount = ($verified | ForEach-Object { @($_.Tables).Count } | Measure-Object -Sum).Sum
$columnCount = ($verified | ForEach-Object { @($_.Columns).Count } | Measure-Object -Sum).Sum

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('# Current Azure and SQL Schema Inventory')
$lines.Add('')
$lines.Add("Generated: $($generatedAt.ToString('yyyy-MM-dd HH:mm:ss')) UTC")
$lines.Add('')
$lines.Add('## Safety boundary')
$lines.Add('')
$lines.Add('- This inventory contains resource names and schema metadata only; it contains no secret values.')
$lines.Add('- An `Unverified` database is not empty; its schema could not be confirmed with the available credentials.')
$lines.Add('- Do not create resource groups, Key Vaults, SQL servers, or databases without explicit permission.')
$lines.Add('')
$lines.Add('## Azure context')
$lines.Add('')
$lines.Add("- Subscription: ``$($account.name)``")
$lines.Add("- Subscription ID: ``$($account.id)``")
$lines.Add("- Tenant ID: ``$($account.tenantId)``")
$lines.Add('')
$lines.Add('## Resource groups')
$lines.Add('')
foreach ($item in $resourceGroups) { $lines.Add("- ``$($item.name)`` ($($item.location))") }
$lines.Add('')
$lines.Add('## Key Vaults')
$lines.Add('')
$lines.Add('| Key Vault | Resource group | Metadata | Secret count |')
$lines.Add('|---|---|---|---:|')
foreach ($item in $vaultInventory) { $lines.Add("| $($item.Name) | $($item.ResourceGroup) | $($item.MetadataAccess) | $($item.SecretCount) |") }
$lines.Add('')
$lines.Add('## SQL servers and databases')
$lines.Add('')
$lines.Add('| Server | Resource group | Database | Status | SKU |')
$lines.Add('|---|---|---|---|---|')
foreach ($item in $databases | Sort-Object Server,Database) { $lines.Add("| $($item.Server) | $($item.ResourceGroup) | $($item.Database) | $($item.Status) | $($item.Sku) |") }
$lines.Add('')
$lines.Add('## Database verification')
$lines.Add('')
$lines.Add('| Logical area | Server | Database | Verification | Tables | Columns | Gap |')
$lines.Add('|---|---|---|---|---:|---:|---|')
foreach ($item in $schemaInventories) {
    $gap = ([string]$item.Error).Replace('|','\|').Replace("`r",' ').Replace("`n",' ')
    $lines.Add("| $($item.Label) | $($item.Server) | $($item.Database) | $($item.Status) | $(@($item.Tables).Count) | $(@($item.Columns).Count) | $gap |")
}
$lines.Add('')
$lines.Add("Verified totals: **$tableCount tables** and **$columnCount columns**.")
$lines.Add('')
$lines.Add('## Table index')
foreach ($inventory in $schemaInventories) {
    $lines.Add('')
    $lines.Add("### $($inventory.Label): ``$($inventory.Database)``")
    $lines.Add('')
    if ($inventory.Status -ne 'Verified') {
        $lines.Add("Unverified: $($inventory.Error)")
        continue
    }
    $lines.Add('| Schema | Table | Rows | Columns | PK columns | Foreign keys | Indexes |')
    $lines.Add('|---|---|---:|---:|---:|---:|---:|')
    foreach ($table in $inventory.Tables) {
        $columnMatches = @($inventory.Columns | Where-Object { $_.Schema -eq $table.Schema -and $_.Table -eq $table.Table })
        $primaryKeyMatches = @($inventory.PrimaryKeys | Where-Object { $_.Schema -eq $table.Schema -and $_.Table -eq $table.Table })
        $foreignKeyMatches = @($inventory.ForeignKeys | Where-Object { $_.Schema -eq $table.Schema -and $_.Table -eq $table.Table })
        $indexMatches = @($inventory.Indexes | Where-Object { $_.Schema -eq $table.Schema -and $_.Table -eq $table.Table } | Select-Object -ExpandProperty Index -Unique)
        $lines.Add("| $($table.Schema) | $($table.Table) | $($table.Rows) | $($columnMatches.Count) | $($primaryKeyMatches.Count) | $($foreignKeyMatches.Count) | $($indexMatches.Count) |")
    }
}

$markdown = ($lines -join "`r`n") + "`r`n"
if ($Preview) {
    $markdown
    Write-Host "Preview complete: $tableCount verified tables and $columnCount columns. No files written."
    return
}

New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
$jsonPath = Join-Path $OutputRoot 'current-azure-sql-schema.json'
$markdownPath = Join-Path $OutputRoot 'current-azure-sql-schema.md'
$snapshot | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $jsonPath -Encoding utf8
$markdown | Set-Content -LiteralPath $markdownPath -Encoding utf8
Write-Host "Updated: $markdownPath"
Write-Host "Updated: $jsonPath"
Write-Host "Verified tables: $tableCount"
Write-Host "Verified columns: $columnCount"
Write-Host "Unverified databases: $(@($schemaInventories | Where-Object Status -ne 'Verified').Count)"

