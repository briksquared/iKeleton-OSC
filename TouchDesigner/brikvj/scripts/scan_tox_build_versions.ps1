# Index .tox TouchDesigner source builds (via toeexpand .build) → parts/TOX_BUILDS.json
param(
    [string[]]$OnlySubdirs = @("generative", "harvest_pick", "vj_suite", "extra", "glitch_fluid")
)
$ErrorActionPreference = "Stop"
$ToeExpand = "C:\Program Files\Derivative\TouchDesigner\bin\toeexpand.exe"
$Parts = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\parts"
$KitParts = Join-Path (Split-Path $PSScriptRoot -Parent) "parts"
if (-not (Test-Path $Parts)) { $Parts = $KitParts }
$OutJson = Join-Path $Parts "TOX_BUILDS.json"
$HostBuild = "2023.12370"

function Parse-Build([string]$line) {
    if ($line -match "build\s+(\d{4})\.(\d+)") {
        return @{ major = [int]$matches[1]; minor = [int]$matches[2]; raw = "$($matches[1]).$($matches[2])" }
    }
    if ($line -match "build\s+(\d+)") {
        return @{ major = 0; minor = [int]$matches[1]; raw = $matches[1] }
    }
    return $null
}

function Compare-Build($a, $b) {
    if (-not $a) { return -1 }
    $ha = Parse-Build "build $($a.raw)"
    $hb = Parse-Build "build $($b.raw)"
    if ($ha.major -ne $hb.major) { return [Math]::Sign($ha.major - $hb.major) }
    return [Math]::Sign($ha.minor - $hb.minor)
}

$hostParsed = Parse-Build "build $HostBuild"
$index = @{}
if (Test-Path $OutJson) {
    try {
        $prev = Get-Content $OutJson -Raw | ConvertFrom-Json
        foreach ($prop in $prev.files.PSObject.Properties) {
            $index[$prop.Name] = $prop.Value
        }
    } catch { }
}
$toxFiles = @()
foreach ($sub in ($OnlySubdirs | Select-Object -Unique)) {
    $d = Join-Path $Parts $sub
    if (Test-Path $d) {
        $toxFiles += Get-ChildItem $d -Recurse -Filter "*.tox" -File -ErrorAction SilentlyContinue
    }
}
if ($toxFiles.Count -eq 0) {
    $toxFiles = Get-ChildItem $Parts -Recurse -Filter "*.tox" -File -ErrorAction SilentlyContinue
}
$toxFiles | ForEach-Object {
    $tox = $_.FullName
    $dir = "$tox.dir"
    $toc = "$tox.toc"
    Remove-Item $dir, $toc -Recurse -Force -ErrorAction SilentlyContinue
    $ErrorActionPreference = "Continue"
    & $ToeExpand $tox 2>&1 | Out-Null
    $ErrorActionPreference = "Stop"
    $buildFile = Join-Path $dir ".build"
    $raw = $null
    $newer = $false
    if (Test-Path $buildFile) {
        $line = (Get-Content $buildFile -TotalCount 3 | Where-Object { $_ -match "build" } | Select-Object -First 1)
        $parsed = Parse-Build $line
        if ($parsed) {
            $raw = $parsed.raw
            if ($parsed.major -gt $hostParsed.major) { $newer = $true }
            elseif ($parsed.major -eq $hostParsed.major -and $parsed.minor -gt $hostParsed.minor) { $newer = $true }
        }
    }
    $rel = $tox.Substring($Parts.Length).TrimStart("\")
    $index[$rel] = @{ build = $raw; newerThanHost = $newer }
    Remove-Item $dir, $toc -Recurse -Force -ErrorAction SilentlyContinue
}

$report = @{
    generated = (Get-Date).ToString("o")
    hostBuild = $HostBuild
    count = $index.Count
    newerCount = (@($index.Values | Where-Object { $_.newerThanHost }).Count)
    files = $index
}
$report | ConvertTo-Json -Depth 4 | Set-Content $OutJson -Encoding utf8
Write-Host "TOX_BUILDS.json — $($index.Count) tox, $($report.newerCount) newer than $HostBuild"
