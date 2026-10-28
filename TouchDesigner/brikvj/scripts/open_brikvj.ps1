# Open Old Brik V J — only run when YOU want TD (does not run build scripts).
$Td = "C:\Program Files\Derivative\TouchDesigner\bin\TouchDesigner.exe"
$Toe = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe"
$Fix = Join-Path $PSScriptRoot "fix_brikvj_brioch_toe.ps1"
if (-not (Test-Path $Toe) -or (Get-Item $Toe).Length -lt 100000) {
    & $Fix
}
Start-Process -FilePath $Td -ArgumentList $Toe
