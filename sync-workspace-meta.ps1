$ErrorActionPreference = "Stop"

$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$noteSrc = Join-Path $sourceDir "workspace_meta_sync\chatboxjimbo-integration.md"
$statusSrc = Join-Path $sourceDir "workspace_meta_sync\ai-status-update.chatboxjimbo-cli.json"

$targetRoot = "T:\ZENO_THE_COMMAND_CENTER\WORKSPACE_META_TEMPLATE"
$noteDst = Join-Path $targetRoot ".workspace_meta\notes\chatboxjimbo-integration.md"
$updatesPath = Join-Path $targetRoot "GIT_HOOB_catalogi\ai-status-updates.json"

if (!(Test-Path -LiteralPath $noteSrc)) {
  Write-Warning "Brak pliku źródłowego notatki: $noteSrc"
  exit 0
}
if (!(Test-Path -LiteralPath $statusSrc)) {
  Write-Warning "Brak pliku źródłowego statusu: $statusSrc"
  exit 0
}
if (!(Test-Path -LiteralPath $updatesPath)) {
  Write-Warning "Brak pliku docelowego: $updatesPath"
  exit 0
}

try {
  Copy-Item -LiteralPath $noteSrc -Destination $noteDst -Force
  Write-Output "OK: note -> $noteDst"
} catch {
  Write-Warning "Nie udało się skopiować notatki: $($_.Exception.Message)"
}

try {
  $updateEntry = Get-Content -Raw -LiteralPath $statusSrc | ConvertFrom-Json
  $json = Get-Content -Raw -LiteralPath $updatesPath | ConvertFrom-Json
  if (-not $json.updates) {
    $json | Add-Member -NotePropertyName updates -NotePropertyValue @() -Force
  }
  $json.updates += $updateEntry
  $json | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $updatesPath -Encoding UTF8
  Write-Output "OK: update appended -> $updatesPath"
} catch {
  Write-Warning "Nie udało się dopisać statusu: $($_.Exception.Message)"
}

exit 0
