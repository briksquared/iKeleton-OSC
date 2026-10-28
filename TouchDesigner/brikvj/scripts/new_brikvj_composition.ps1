# Duplicate a BRIKVJ Live composition folder and fix TDAbleton paths.
param(
    [int]$From = 1,
    [int]$To = 2
)
$ErrorActionPreference = "Stop"
$Root = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\ableton\compositions"
$SrcDir = Join-Path $Root ("{0:D2}" -f $From)
$DstDir = Join-Path $Root ("{0:D2}" -f $To)
if (-not (Test-Path $SrcDir)) { throw "Missing source: $SrcDir" }
if (Test-Path $DstDir) { throw "Already exists: $DstDir — pick another -To" }

Copy-Item $SrcDir $DstDir -Recurse
$OldName = "BRIKVJ_Composition_{0:D2}.als" -f $From
$NewName = "BRIKVJ_Composition_{0:D2}.als" -f $To
$OldPath = Join-Path $DstDir $OldName
$NewPath = Join-Path $DstDir $NewName
if (Test-Path $OldPath) { Rename-Item $OldPath $NewName }

$Readme = Join-Path $DstDir "README.md"
@"
# Composition $("{0:D2}" -f $To) — duplicate of $($From.ToString("00"))

**Set:** ``$NewName``

Same track layout as composition $($From.ToString("00")) — see ``PATCHWORKS_INTEGRATION.md`` (Rack Sub 3–4, Buddy 1–2, Sugar Bytes, TDA_Master).

Swap drum samples, px-stream M4L, or arrangement; keep **TDA_Master** on Master.
"@ | Set-Content $Readme -Encoding UTF8

& "$PSScriptRoot\fix_ableton_tda_paths.ps1" -AlsPaths @($NewPath)
Write-Host "Created $DstDir -> $NewName"
