# Clean Brioch toe + inject brikvj_manual_build (no autostart on load).
$ErrorActionPreference = "Stop"
$Here = $PSScriptRoot
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$Td = "C:\Program Files\Derivative\TouchDesigner\bin"

$ea0 = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
taskkill /F /IM TouchDesigner.exe 2>$null | Out-Null
$ErrorActionPreference = $ea0
Start-Sleep 2

& "$Here\sync_scripts_to_documents.ps1"
& "$Here\fix_brikvj_brioch_toe.ps1"

Remove-Item "$Toe.dir", "$Toe.toc" -Force -ErrorAction SilentlyContinue
Push-Location $Base
$ea = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& "$Td\toeexpand.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $ea
Pop-Location

& python "$Here\inject_brikvj_manual_build.py" $Toe

Push-Location $Base
$ErrorActionPreference = "Continue"
& "$Td\toecollapse.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $ea
Pop-Location

if ((Get-Item $Toe).Length -lt 100000) { throw "collapse failed" }
Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Ready: open BRIKVJ.toe -> /project1/brikvj_manual_build -> pulse Start (once) -> Save"
