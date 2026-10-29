# Mirror kit → Documents\TouchDesigner\BRIKVJ (live BRIKVJ — not iKeleton-OSC at runtime).
$ErrorActionPreference = "Stop"
$KitRoot = Split-Path $PSScriptRoot -Parent
$BrikHome = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Dst = Join-Path $BrikHome "scripts"
$RepoKit = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\scripts"
$Src = if ((Resolve-Path $PSScriptRoot -ErrorAction SilentlyContinue).Path -eq (Resolve-Path $Dst -ErrorAction SilentlyContinue).Path -and (Test-Path $RepoKit)) {
    $RepoKit
} else {
    Join-Path $PSScriptRoot "."
}
New-Item -ItemType Directory -Force -Path $Dst | Out-Null
Get-ChildItem $Src -Filter "*.py" | Copy-Item -Destination $Dst -Force
Get-ChildItem $Src -Filter "*.ps1" | Where-Object { $_.Name -notmatch "^_" } | Copy-Item -Destination $Dst -Force
$PartsSrc = Join-Path $KitRoot "parts"
$PartsDst = Join-Path $BrikHome "parts"
if (Test-Path $PartsSrc) {
    New-Item -ItemType Directory -Force -Path $PartsDst | Out-Null
    & robocopy $PartsSrc $PartsDst /E /XO /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null
}
$ScanTox = Join-Path $Src "scan_tox_build_versions.ps1"
if (Test-Path $ScanTox) {
    & $ScanTox -OnlySubdirs @("generative", "harvest_pick", "research") 2>&1 | Out-Null
}
@"
@echo off
echo Run inside TouchDesigner Textport or Text DAT:
echo   exec(open(r'%Dst%\old_brik_vj_all_in_one.py').read())
echo.
echo Or paste old_brik_vj_all_in_one.py into a Text DAT and Run Script.
pause
"@ | Set-Content (Join-Path $Dst "RUN_ALL_IN_ONE.txt") -Encoding ASCII
Write-Host "Synced scripts -> $Dst"
