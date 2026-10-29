# Stop startup error / newer-tox modal spam in Documents BRIKVJ.toe (no TouchDesigner UI).
$ErrorActionPreference = "Stop"
$TdBin = "C:\Program Files\Derivative\TouchDesigner\bin"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$Here = $PSScriptRoot

function Clear-ToeExpandArtifacts {
    param([string]$ToePath)
    cmd /c "rd /s /q `"$ToePath.dir`" 2>nul" | Out-Null
    Remove-Item "$ToePath.toc" -Force -ErrorAction SilentlyContinue
}

if ((Get-Item $Toe).Length -lt 100000) {
    throw "BRIKVJ.toe missing or truncated"
}

Clear-ToeExpandArtifacts $Toe
Push-Location $Base
$ErrorActionPreference = "Continue"
& "$TdBin\toeexpand.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = "Stop"
Pop-Location

Remove-Item (Join-Path $Base "RUN_BUILD.flag") -Force -ErrorAction SilentlyContinue

& python (Join-Path $Here "inject_kantan_boot.py") $Toe
if ($LASTEXITCODE -ne 0) { throw "inject_kantan_boot failed" }
& python (Join-Path $Here "inject_brikvj_dialog_prefs.py") $Toe
if ($LASTEXITCODE -ne 0) { throw "inject_brikvj_dialog_prefs failed" }

$strip = @("brikvj_build_autostart", "old_brik_autostart", "brikvj_error_snapshot")
$tocPath = Join-Path $Base "BRIKVJ.toe.toc"
$text = [Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($tocPath))
$keep = foreach ($line in ($text -split "`n", 0, "SimpleMatch")) {
    $l = $line.TrimEnd("`r")
    if (-not $l) { continue }
    $drop = $false
    foreach ($n in $strip) {
        if ($l -like "project1/$n.*") { $drop = $true; break }
    }
    if (-not $drop) { $l }
}
[IO.File]::WriteAllBytes($tocPath, [Text.Encoding]::ASCII.GetBytes(($keep -join "`n") + "`n"))
$dir = "$Toe.dir"
foreach ($n in $strip) {
    Remove-Item "$dir\project1\$n.*" -Force -ErrorAction SilentlyContinue
}

# MOTU live in (Brioch analyseAudio needs audio cooking, not modal errors on null CHOPs)
$devIn = "$dir\project1\audiodevin1.parm"
if (Test-Path $devIn) {
    Set-Content $devIn @"
?
device 67108864 ""
active 67108864 on
channel 67108864 3-4
timeslice 67108864 on
autoexportroot 201326609 "" parent()
?
"@ -NoNewline
}

$preCollapse = (Get-Item $Toe).Length
if ($preCollapse -lt 100000) { throw "Refusing toecollapse — toe too small ($preCollapse B)" }

Push-Location $Base
$ErrorActionPreference = "Continue"
& "$TdBin\toecollapse.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = "Stop"
Pop-Location
Clear-ToeExpandArtifacts $Toe

$final = (Get-Item $Toe).Length
if ($final -lt 100000) {
    $bkp = Get-ChildItem (Join-Path $Base "BRIKVJ.toe.bkp*") | Sort-Object Length -Descending | Select-Object -First 1
    if ($bkp) {
        Copy-Item $bkp.FullName $Toe -Force
        throw "toecollapse truncated toe — restored from $($bkp.Name); fix inject scripts and retry"
    }
    throw "toecollapse truncated toe ($final B) and no backup found"
}
Write-Host "Quiet-open patch applied -> $final bytes"
