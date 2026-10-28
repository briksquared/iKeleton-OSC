# Expand BRIKVJ.toe briefly and check harvest stack nodes were saved into the project.
$ErrorActionPreference = "Stop"
$TdBin = "C:\Program Files\Derivative\TouchDesigner\bin\TouchDesigner.exe"
$ToeExpand = "C:\Program Files\Derivative\TouchDesigner\bin\toeexpand.exe"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
if (-not (Test-Path $Toe)) { throw "Missing $Toe" }
if (Get-Process TouchDesigner -ErrorAction SilentlyContinue) {
    Write-Host "stack verify: SKIP (TouchDesigner is open — close it first)"
    exit 2
}

$Dir = "$Toe.dir"
Remove-Item $Dir, "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Push-Location $Base
$prev = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $ToeExpand "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $prev
Pop-Location

$checks = @(
    @{ Label = "old_brik_vj stack"; Path = Join-Path $Dir "project1\old_brik_vj" }
    @{ Label = "brikvj_broadcast"; Path = Join-Path $Dir "project1\brikvj_broadcast" }
    @{ Label = "brikvj_router"; Path = Join-Path $Dir "project1\brikvj_router" }
    @{ Label = "kantanMapper"; Path = Join-Path $Dir "project1\mapping\kantanMapper" }
)

$missing = @()
foreach ($c in $checks) {
    if (Test-Path $c.Path) {
        Write-Host "OK $($c.Label)"
    } else {
        Write-Host "MISSING $($c.Label) — run TEXTPORT_BUILD in TD and Save"
        $missing += $c.Label
    }
}

Remove-Item $Dir, "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue

if ($missing.Count -gt 0) {
    Write-Host "stack verify: FAIL ($($missing.Count))"
    exit 1
}
Write-Host "stack verify: OK (saved stack in .toe)"
exit 0
