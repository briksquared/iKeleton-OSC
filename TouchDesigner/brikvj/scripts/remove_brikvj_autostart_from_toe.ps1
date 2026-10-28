# Remove brikvj_build_autostart / old_brik_autostart from BRIKVJ.toe (stops startup error spam).
$ErrorActionPreference = "Stop"
$TdBin = "C:\Program Files\Derivative\TouchDesigner\bin"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"

if ((Get-Item $Toe).Length -lt 100000) {
    $bkp = Get-ChildItem (Join-Path $Base "BRIKVJ.toe.bkp*") | Sort-Object Length -Descending | Select-Object -First 1
    Copy-Item $bkp.FullName $Toe -Force
}

Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Push-Location $Base
$prev = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& "$TdBin\toeexpand.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $prev

$toc = Join-Path $Base "BRIKVJ.toe.toc"
$names = @("brikvj_build_autostart", "old_brik_autostart")
$data = [IO.File]::ReadAllBytes($toc)
$text = [Text.Encoding]::ASCII.GetString($data)
$lines = $text -split "`n", 0, "SimpleMatch"
$keep = $lines | Where-Object {
    $line = $_.TrimEnd("`r")
    if (-not $line) { return $false }
    $drop = $false
    foreach ($n in $names) {
        if ($line -like "project1/$n.*") { $drop = $true; break }
    }
    -not $drop
}
$newText = ($keep -join "`n") + "`n"
[IO.File]::WriteAllBytes($toc, [Text.Encoding]::ASCII.GetBytes($newText))

$proj = Join-Path $Base "BRIKVJ.toe.dir\project1"
foreach ($n in $names) {
    Remove-Item "$proj\$n.n", "$proj\$n.parm", "$proj\$n.text" -Force -ErrorAction SilentlyContinue
}

$prev = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& "$TdBin\toecollapse.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $prev
Pop-Location

if ((Get-Item $Toe).Length -lt 100000) { throw "toecollapse failed" }
Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Removed autostart Execute DATs from BRIKVJ.toe ($((Get-Item $Toe).Length) bytes)"
