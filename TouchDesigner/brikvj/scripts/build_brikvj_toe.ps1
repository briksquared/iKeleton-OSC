# Deploy Brioch base → Documents BRIKVJ.toe (no iKeleton-only copy).
$ErrorActionPreference = "Stop"
$KitRoot = Split-Path $PSScriptRoot -Parent
$Src = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\brioch-audio-reactive-vjing\briochSceno.beta.toe"
$DocToe = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe"
$Sync = Join-Path $PSScriptRoot "sync_harvest_parts.ps1"

& $Sync
if (-not (Test-Path $Src)) { throw "Missing harvest toe: $Src" }
New-Item -ItemType Directory -Force -Path (Split-Path $DocToe) | Out-Null
Copy-Item $Src $DocToe -Force
New-Item -ItemType Directory -Force -Path (Split-Path (Join-Path $KitRoot "scripts")) | Out-Null
& (Join-Path $PSScriptRoot "sync_scripts_to_documents.ps1")
& (Join-Path $PSScriptRoot "fix_brikvj_brioch_toe.ps1")
Write-Host "Deployed + patched $DocToe $((Get-Item $DocToe).Length) bytes"
