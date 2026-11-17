# mirror.ps1 — copia caliente en Supabase de una memoria del repo.
# Uso: powershell tools/mirror.ps1 [-Only <id>] [-DryRun]
# Requiere la clave publishable en la variable de entorno COQUITO_SUPABASE_KEY.
# Solo alta/edita: nunca borra filas.
param(
  [string]$Only = '',
  [switch]$DryRun,
  [string]$KeyEnv = 'COQUITO_SUPABASE_KEY',
  [string]$Url = 'https://qspbbcawyuoloiyzakmv.supabase.co/rest/v1'
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$root = Split-Path -Parent $PSScriptRoot
$path = Join-Path $root 'memories.jsonl'
$rows = @(Get-Content -LiteralPath $path -Encoding UTF8 |
  Where-Object { $_.Trim() } |
  ForEach-Object { $_ | ConvertFrom-Json })

if ($Only) {
  $rows = @($rows | Where-Object { $_.id -eq $Only })
  if ($rows.Count -eq 0) { throw "No existe el id $Only en memories.jsonl" }
}

if ($DryRun) {
  "DRYRUN rows=$($rows.Count) destino=$Url/agent_experiences"
  exit 0
}

$key = [Environment]::GetEnvironmentVariable($KeyEnv)
if (-not $key) { throw "Falta la variable de entorno $KeyEnv" }
$h = @{ apikey = $key; Authorization = "Bearer $key"; 'Content-Type' = 'application/json' }

$raw = Invoke-RestMethod -Uri "$Url/agent_experiences?select=id" -Headers $h -Method Get
$list = if ($raw -is [System.Array]) { $raw } else { @($raw) }
$existing = @{}
foreach ($e in $list) { $existing[[string]$e.id] = $true }

$ins = 0
$upd = 0
foreach ($r in $rows) {
  $sid = [string]$r.sid
  $body = [ordered]@{
    domain     = [string]$r.d
    kind       = [string]$r.k
    title      = [string]$r.t
    importance = [int]$r.imp
    summary    = ''
  }
  if ($r.PSObject.Properties.Name -contains 's') { $body['summary'] = [string]$r.s }
  foreach ($pair in @(@('solution', 'sol'), @('lessons_learned', 'less'), @('source_path', 'src'))) {
    $dest = $pair[0]
    $src  = $pair[1]
    if ($r.PSObject.Properties.Name -contains $src) { $body[$dest] = [string]$r.$src }
    else { $body[$dest] = $null }
  }
  if ($r.PSObject.Properties.Name -contains 'tags') { $body['tags'] = @($r.tags) }
  else { $body['tags'] = @() }

  if ($existing.ContainsKey($sid)) {
    $json = $body | ConvertTo-Json -Depth 6 -Compress
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    Invoke-RestMethod -Uri "$Url/agent_experiences?id=eq.$sid" -Headers $h -Method Patch -Body $bytes | Out-Null
    $upd++
  } else {
    $body['id'] = $sid
    if ($r.PSObject.Properties.Name -contains 'at') { $body['created_at'] = "$($r.at)T00:00:00Z" }
    $json = $body | ConvertTo-Json -Depth 6 -Compress
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    Invoke-RestMethod -Uri "$Url/agent_experiences" -Headers $h -Method Post -Body $bytes | Out-Null
    $ins++
  }
}

"OK insert=$ins update=$upd"
