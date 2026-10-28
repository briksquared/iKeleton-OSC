# Open a BRIKVJ composition in Ableton Live (first Live.exe found).
param(
    [ValidatePattern('^\d{2}$')]
    [string]$Composition = "01"
)
$ErrorActionPreference = "Stop"
$Als = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\ableton\compositions\$Composition\BRIKVJ_Composition_$Composition.als"
if (-not (Test-Path $Als)) { throw "Missing $Als" }

$candidates = @(
    "${env:ProgramFiles}\Ableton\Live 12 Suite\Program\Ableton Live 12 Suite.exe",
    "${env:ProgramFiles}\Ableton\Live 12 Standard\Program\Ableton Live 12 Standard.exe",
    "${env:ProgramFiles}\Ableton\Live 11 Suite\Program\Ableton Live 11 Suite.exe",
    "${env:ProgramFiles(x86)}\Ableton\Live 12 Suite\Program\Ableton Live 12 Suite.exe"
) | Where-Object { Test-Path $_ }

if (-not $candidates) {
    Write-Host "Live.exe not found — open manually:"
    Write-Host $Als
    Start-Process $Als
    exit 0
}

Start-Process -FilePath $candidates[0] -ArgumentList $Als
Write-Host "Launched $($candidates[0]) with composition $Composition"
