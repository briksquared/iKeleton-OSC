$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$bkp = Get-ChildItem $Base -Filter "BRIKVJ.toe.bkp*" | Sort-Object Length -Descending | Select-Object -First 1
if (-not $bkp) { throw "No BRIKVJ.toe.bkp* found" }
Copy-Item $bkp.FullName $Toe -Force
Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Restored $($bkp.Name) -> BRIKVJ.toe ($((Get-Item $Toe).Length) bytes)"
