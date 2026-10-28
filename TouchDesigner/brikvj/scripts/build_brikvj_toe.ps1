# Deploy BRIKVJ.toe (Brioch performance base) + sync harvest parts → repo + Documents
$ErrorActionPreference = "Stop"
$RepoTd = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner"
$Src = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\brioch-audio-reactive-vjing\briochSceno.beta.toe"
$Toe = Join-Path $RepoTd "BRIKVJ.toe"
$DocToe = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe"
$Sync = Join-Path $RepoTd "brikvj\scripts\sync_harvest_parts.ps1"

& $Sync
if (-not (Test-Path $Src)) { throw "Missing harvest toe: $Src" }
Copy-Item $Src $Toe -Force
New-Item -ItemType Directory -Force -Path (Split-Path $DocToe) | Out-Null
Copy-Item $Toe $DocToe -Force
Copy-Item (Join-Path $RepoTd "brikvj\scripts\*.py") "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\scripts\" -Force
$Fix = Join-Path $RepoTd "brikvj\scripts\fix_brikvj_brioch_toe.ps1"
& $Fix
Write-Host "Deployed + Windows-patched BRIKVJ.toe $((Get-Item $DocToe).Length) bytes"
