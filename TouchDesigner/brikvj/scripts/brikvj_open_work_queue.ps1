# Aggregate gaps, build failures, RB open, unwired head → logs/OPEN_WORK_QUEUE.md + OPEN_WORK.json
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$OutMd = Join-Path $Kit "logs\OPEN_WORK_QUEUE.md"
$OutJson = Join-Path $Kit "logs\OPEN_WORK.json"

$items = New-Object System.Collections.Generic.List[hashtable]

function Add-Work($id, $prio, $kind, $title, $action, $evidence) {
    $items.Add(@{
        id       = $id
        priority = $prio
        kind     = $kind
        title    = $title
        action   = $action
        evidence = $evidence
    })
}

# GAPS_REPORT bullets
$gapPath = Join-Path $Kit "logs\GAPS_REPORT.md"
if (Test-Path $gapPath) {
    $gapRaw = Get-Content $gapPath -Raw
    $inGaps = $false
    foreach ($line in ($gapRaw -split "`n")) {
        if ($line -match '^## Gaps') { $inGaps = $true; continue }
        if ($line -match '^## OK') { break }
        if ($inGaps -and $line -match '^- (.+)') {
            $t = $Matches[1]
            $prio = if ($t -match 'Traceback|MISSING|small \(') { 'P0' } elseif ($t -match 'newer tox|td_errors') { 'P1' } else { 'P2' }
            Add-Work ("GAP-" + ($items.Count + 1)) $prio "gap" $t "See NEXT_SESSION_OPERATIONS.md failure matrix" $t
        }
    }
}

# build.log last Traceback block
$buildLog = Join-Path $Live "logs\build.log"
if (Test-Path $buildLog) {
    $bl = Get-Content $buildLog -Raw
    if ($bl -match 'Traceback[\s\S]{0,1200}') {
        $tb = $Matches[0].Trim()
        $script = if ($tb -match 'File "[^"]+\\([^\\]+\.py)"') { $Matches[1] } else { "unknown" }
        $err = if ($tb -match '(\w+Error: .+)') { $Matches[1] } else { "see build.log" }
        Add-Work "BLD-001" "P0" "build" "Mega step failed: $script" "Fix scripts\$script; sync; user Textport TEXTPORT_MEGA.txt + Save (no auto TD launch)" $err
    }
}

# RESEARCH_BACKLOG open rows
$rbPath = Join-Path $Kit "RESEARCH_BACKLOG.md"
if (Test-Path $rbPath) {
    foreach ($line in Get-Content $rbPath) {
        if ($line -match '\|\s*(RB-\d+)\s*\|\s*([^|]+)\|\s*open\s*\|') {
            Add-Work $Matches[1] "P1" "backlog" $Matches[2].Trim() "RESEARCH_BACKLOG + DEEPER §6 scoring" $Matches[1]
        }
    }
}

# Unwired tox head from RESEARCH_DIFF
$diffPath = Join-Path $Kit "logs\RESEARCH_DIFF.md"
$unwiredSample = @()
if (Test-Path $diffPath) {
    $pick = $false
    foreach ($line in Get-Content $diffPath) {
        if ($line -match '^## Unwired') { $pick = $true; continue }
        if ($pick -and $line -match '^## ') { break }
        if ($pick -and $line -match '^- (.+\.tox)') { $unwiredSample += $Matches[1] }
        if ($unwiredSample.Count -ge 8) { break }
    }
}
if ($unwiredSample.Count) {
    Add-Work "RES-001" "P2" "integrate" "Wire scored unwired tox (sample)" ($unwiredSample -join "; ") "RESEARCH_DIFF.md"
}

$ordered = $items | Sort-Object { switch ($_.priority) { 'P0' { 0 } 'P1' { 1 } default { 2 } } }, { $_.id }

$session1 = ($ordered | Where-Object { $_.priority -eq 'P0' } | Select-Object -First 5)
$session2 = ($ordered | Where-Object { $_.priority -eq 'P1' } | Select-Object -First 5)
$session3 = @($ordered | Where-Object { $_.priority -eq 'P2' } | Select-Object -First 3) + @(
    @{ id = "DISC-001"; priority = "P2"; kind = "discovery"; title = "DEEPER §4 discovery pass"; action = "transcript + USER_REQUESTS diff"; evidence = "WORKLOG entry" }
)

function Format-Items($arr) {
    if (-not $arr -or $arr.Count -eq 0) { return "- (none — run gap_report)" }
    ($arr | ForEach-Object { "- **$($_.id)** [$($_.priority)] $($_.title)`n  - Do: $($_.action)`n  - Evidence: $($_.evidence)" }) -join "`n`n"
}

$md = @"
# BRIKVJ open work queue (generated $(Get-Date -Format o))

Auto: ``scripts/brikvj_open_work_queue.ps1``. Read with [NEXT_SESSION_PLAN_DEEPEST.md](../NEXT_SESSION_PLAN_DEEPEST.md).

**Total items:** $($ordered.Count) | **Next agent:** do Session 1 top to bottom, then re-run ``brikvj_session_start.ps1``.

## Session 1 — Finish / stop pain (P0)

$(Format-Items $session1)

## Session 2 — Compat + stack quality (P1)

$(Format-Items $session2)

## Session 3 — Research + integrate (P2)

$(Format-Items $session3)

## Full ordered queue

| ID | P | Kind | Title |
|----|---|------|-------|
$(($ordered | ForEach-Object { "| $($_.id) | $($_.priority) | $($_.kind) | $($_.title.Substring(0, [Math]::Min(60, $_.title.Length))) |" }) -join "`n")
"@

$jsonObj = @{
    generated_at = (Get-Date -Format o)
    count        = $ordered.Count
    sessions     = @{
        session1 = @($session1 | ForEach-Object { $_ })
        session2 = @($session2 | ForEach-Object { $_ })
        session3 = @($session3 | ForEach-Object { $_ })
    }
    queue        = @($ordered | ForEach-Object { $_ })
}

foreach ($dir in @((Join-Path $Kit "logs"), (Join-Path $Live "logs"))) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $md | Set-Content (Join-Path $dir "OPEN_WORK_QUEUE.md") -Encoding utf8
    ($jsonObj | ConvertTo-Json -Depth 6) | Set-Content (Join-Path $dir "OPEN_WORK.json") -Encoding utf8
}
Write-Host "OPEN_WORK_QUEUE.md ($($ordered.Count) items)"
exit 0
