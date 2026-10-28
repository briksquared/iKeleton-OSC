# Mirror brikvj/scripts → Documents/BRIKVJ/scripts (TD Text DAT paste path).
$ErrorActionPreference = "Stop"
$Src = Join-Path $PSScriptRoot "."
$Dst = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\scripts"
New-Item -ItemType Directory -Force -Path $Dst | Out-Null
Get-ChildItem $Src -Filter "*.py" | Copy-Item -Destination $Dst -Force
Get-ChildItem $Src -Filter "*.ps1" | Where-Object { $_.Name -notmatch "^_" } | Copy-Item -Destination $Dst -Force
@"
@echo off
echo Run inside TouchDesigner Textport or Text DAT:
echo   exec(open(r'%Dst%\old_brik_vj_all_in_one.py').read())
echo.
echo Or paste old_brik_vj_all_in_one.py into a Text DAT and Run Script.
pause
"@ | Set-Content (Join-Path $Dst "RUN_ALL_IN_ONE.txt") -Encoding ASCII
Write-Host "Synced scripts -> $Dst"
