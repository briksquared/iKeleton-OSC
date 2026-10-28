# Remove half-built brikvj_* ops from expanded toe (run after toeexpand, before collapse).
$ErrorActionPreference = "Stop"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Dir = Join-Path $Base "BRIKVJ.toe.dir"
$proj = Join-Path $Dir "project1"
if (-not (Test-Path $proj)) { Write-Host "Skip — expand toe first"; exit 0 }

$removeNames = @(
    "brikvj_autopilot", "brikvj_keys", "brikvj_key_execute", "brikvj_key_callbacks", "brikvj_key_help",
    "brikvj_on_start", "brikvj_router", "brikvj_broadcast", "brikvj_osc", "brikvj_osc_callbacks",
    "brikvj_osc_help", "brikvj_level_drive", "tda_mapper_parexec", "old_brik_vj"
)

$toc = Join-Path $Base "BRIKVJ.toe.toc"
if (-not (Test-Path $toc)) { exit 0 }

$data = [IO.File]::ReadAllBytes($toc)
$text = [Text.Encoding]::ASCII.GetString($data)
$lines = $text -split "`n", 0, "SimpleMatch"
$prefixes = $removeNames | ForEach-Object { "project1/$_" }
$keep = @()
foreach ($line in $lines) {
    $l = $line.TrimEnd("`r")
    if (-not $l) { continue }
    $drop = $false
    foreach ($p in $prefixes) {
        if ($l -eq "$p.n" -or $l -eq "$p.parm" -or $l -eq "$p.text" -or $l -like "$p/*") {
            $drop = $true
            break
        }
    }
    if ($l -like "project1/old_brik_vj/*") { $drop = $true }
    if ($l -like "project1/brikvj_broadcast/*") { $drop = $true }
    if ($l -like "project1/brikvj_router/*") { $drop = $true }
    if ($l -like "project1/windows/*") { $drop = $true }
    if (-not $drop) { $keep += $l }
}
[IO.File]::WriteAllBytes($toc, [Text.Encoding]::ASCII.GetBytes(($keep -join "`n") + "`n"))

Get-ChildItem $proj -Directory | Where-Object { $_.Name -in $removeNames -or $_.Name -eq "old_brik_vj" -or $_.Name -eq "brikvj_broadcast" -or $_.Name -eq "brikvj_router" -or $_.Name -eq "windows" } | Remove-Item -Recurse -Force
foreach ($n in $removeNames) {
    Remove-Item "$proj\$n.n", "$proj\$n.parm", "$proj\$n.text" -Force -ErrorAction SilentlyContinue
}
Write-Host "Stripped broken/partial brikvj stack from toc + project1"
