# import.ps1 — trae a memories.jsonl las experiencias que viven solo en Supabase.
#
# La memoria del repo es la fuente de verdad: este script SOLO suma filas cuyo
# sid todavia no esta en el archivo. Nunca pisa ni borra una linea existente,
# asi que una edicion hecha en git no se pierde porque Supabase quedo atras.
#
# Uso: powershell tools/import.ps1 [-DryRun]
# Requiere la clave publishable en la variable de entorno COQUITO_SUPABASE_KEY.

param(
  [switch]$DryRun,
  [string]$KeyEnv = 'COQUITO_SUPABASE_KEY',
  [string]$Url = 'https://qspbbcawyuoloiyzakmv.supabase.co/rest/v1'
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$root = Split-Path -Parent $PSScriptRoot
$mem  = Join-Path $root 'memories.jsonl'

$key = [Environment]::GetEnvironmentVariable($KeyEnv)
if (-not $key) { throw "Falta la variable de entorno $KeyEnv" }
$h = @{ apikey = $key; Authorization = "Bearer $key" }

$sel = 'id,domain,kind,title,importance,summary,solution,lessons_learned,source_path,tags,created_at'
$raw = Invoke-RestMethod -Uri "$Url/agent_experiences?select=$sel" -Headers $h -Method Get
$rows = if ($raw -is [System.Array]) { $raw } else { @($raw) }

$locales = @{}
if (Test-Path -LiteralPath $mem) {
  Get-Content -LiteralPath $mem -Encoding UTF8 |
    Where-Object { $_.Trim() } |
    ForEach-Object { $o = $_ | ConvertFrom-Json; $locales[[string]$o.sid] = $true }
}

$nuevas = @($rows | Where-Object { -not $locales.ContainsKey([string]$_.id) })
"supabase=$($rows.Count) archivo=$($locales.Count) nuevas=$($nuevas.Count)"

if ($DryRun) {
  foreach ($r in $nuevas) { "  + $($r.domain)/$($r.title)" }
  exit 0
}
if ($nuevas.Count -eq 0) { "OK nada nuevo"; exit 0 }

$tmp = Join-Path ([IO.Path]::GetTempPath()) ("coquito-import-" + [Guid]::NewGuid().ToString('N') + '.json')
# seed.py exige una lista: con una sola fila, ConvertTo-Json devuelve un objeto.
$json = if ($nuevas.Count -eq 1) {
  '[' + (ConvertTo-Json -InputObject $nuevas[0] -Depth 6 -Compress) + ']'
} else {
  ConvertTo-Json -InputObject $nuevas -Depth 6 -Compress
}
[IO.File]::WriteAllText($tmp, $json, [Text.UTF8Encoding]::new($false))

try {
  python (Join-Path $PSScriptRoot 'seed.py') --input $tmp --merge
  if ($LASTEXITCODE -ne 0) { throw "seed.py fallo con $LASTEXITCODE" }
  python (Join-Path $PSScriptRoot 'check.py') --reindex
  if ($LASTEXITCODE -ne 0) { throw "check.py fallo con $LASTEXITCODE" }
}
finally {
  Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
}
