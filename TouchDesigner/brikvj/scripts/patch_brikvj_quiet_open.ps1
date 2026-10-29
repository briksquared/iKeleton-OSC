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
& python (Join-Path $Here "inject_brikvj_dialog_prefs.py") $Toe

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

Push-Location $Base
$ErrorActionPreference = "Continue"
& "$TdBin\toecollapse.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = "Stop"
Pop-Location
Clear-ToeExpandArtifacts $Toe

Write-Host "Quiet-open patch applied -> $((Get-Item $Toe).Length) bytes"
