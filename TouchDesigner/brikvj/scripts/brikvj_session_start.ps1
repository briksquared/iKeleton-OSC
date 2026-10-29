# One-shot next-session bootstrap → logs/SESSION_BRIEF.md (kit + Documents).
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Repo = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC"

& "$PSScriptRoot\sync_scripts_to_documents.ps1" 2>&1 | Out-Null
& "$PSScriptRoot\brikvj_gap_report.ps1"
$gapExit = $LASTEXITCODE
& "$PSScriptRoot\brikvj_research_diff.ps1"
& "$PSScriptRoot\brikvj_open_work_queue.ps1" 2>&1 | Out-Null
& "$PSScriptRoot\brikvj_bug_scan.ps1" 2>&1 | Out-Null
& "$PSScriptRoot\brikvj_research_pass.ps1" 2>&1 | Out-Null

$gap = Get-Content (Join-Path $Kit "logs\GAPS_REPORT.md") -Raw -ErrorAction SilentlyContinue
$diff = Get-Content (Join-Path $Kit "logs\RESEARCH_DIFF.md") -Raw -ErrorAction SilentlyContinue
$backlog = Get-Content (Join-Path $Kit "RESEARCH_BACKLOG.md") -Raw -ErrorAction SilentlyContinue
$openRb = [regex]::Matches($backlog, '\|\s*RB-\d+.*\|\s*open\s*\|').Count

$gitLine = "unknown"
if (Test-Path $Repo) {
    Push-Location $Repo
    $gitLine = (git status -sb 2>$null | Select-Object -First 1)
    $gitLog = (git log -1 --oneline 2>$null)
    Pop-Location
} else { $gitLog = "repo path missing" }

$toeLen = if (Test-Path "$Live\BRIKVJ.toe") { (Get-Item "$Live\BRIKVJ.toe").Length } else { 0 }
$tdRun = [bool](Get-Process TouchDesigner -ErrorAction SilentlyContinue)

$gapCount = 0
if ($gap -match '## Gaps \((\d+)\)') { $gapCount = [int]$Matches[1] }

$unwiredCount = 0
$newerCount = 0
if ($diff -match '## Unwired \.tox \((\d+)\)') { $unwiredCount = [int]$Matches[1] }
if ($diff -match '## Newer than host \((\d+)\)') { $newerCount = [int]$Matches[1] }

$buildLog = Join-Path $Live "logs\build.log"
$megaSaveOk = $false
$buildTraceback = $false
if (Test-Path $buildLog) {
    $bl = Get-Content $buildLog -Raw -ErrorAction SilentlyContinue
    if ($bl -match '\[BRIKVJ mega\] project\.save\(\) OK') { $megaSaveOk = $true }
    if ($bl -match 'Traceback') { $buildTraceback = $true }
}

$sprint = if ($buildTraceback -or -not $megaSaveOk -or $toeLen -lt 2000000) { "Sprint P0" }
elseif ($megaSaveOk -and $toeLen -ge 9000000 -and -not $buildTraceback) { "Sprint R2 — roadmap step 2 (quiet open)" }
elseif ($gapExit -ne 0) { "Sprint P0 or R (see GAPS_REPORT)" }
elseif ($tdRun) { "Sprint D or capture-only (TD running)" }
else { "Sprint R" }

$milestones = @{
    M1_stable_open = ($gapCount -eq 0 -or ($gap -notmatch 'dialog|Error dialogs' -and $gap -notmatch 'td_errors'))
    M2_stack_saved = $megaSaveOk
    M3_show_bus    = ($toeLen -ge 4000000)
    M4_harvest     = ($unwiredCount -lt 120)
    M5_live        = $false
    M6_kit_clean   = ($gitLine -notmatch '\?\?| M ')
}

$continuity = @{
    generated_at           = (Get-Date -Format o)
    live_toe_bytes         = $toeLen
    touchdesigner_running  = $tdRun
    git_branch_status      = $gitLine
    git_head               = $gitLog
    gap_report_exit        = $gapExit
    gap_count              = $gapCount
    unwired_tox_count      = $unwiredCount
    newer_tox_count        = $newerCount
    open_rb_count          = $openRb
    mega_save_ok           = $megaSaveOk
    build_traceback        = $buildTraceback
    recommended_sprint     = $sprint
    milestones             = $milestones
    read_next              = @(
        "logs/HANDOFF_DETAILED_2026-10-29.md",
        "logs/SESSION_BRIEF.md",
        "logs/CONTINUITY.json",
        "logs/ROADMAP_STATUS.md",
        "NEXT_SESSION_OPERATIONS.md"
    )
}
$continuityJson = $continuity | ConvertTo-Json -Depth 5

$brief = @"
# BRIKVJ SESSION BRIEF (generated $(Get-Date -Format o))

**Read next:** [NEXT_SESSION_OPERATIONS.md](../NEXT_SESSION_OPERATIONS.md) → suggested sprint below.

## State

| Check | Value |
|-------|-------|
| Live toe | $toeLen bytes |
| TouchDesigner running | $tdRun |
| Git | $gitLine |
| HEAD | $gitLog |
| RESEARCH_BACKLOG open | $openRb rows |
| gap_report exit | $gapExit |

## Recommended sprint

**$sprint** — see NEXT_SESSION_PLAN_DEEPER.md §3 picker.

## CONTINUITY snapshot

| Field | Value |
|-------|-------|
| mega_save_ok | $megaSaveOk |
| build_traceback | $buildTraceback |
| unwired tox | $unwiredCount |
| newer tox | $newerCount |
| gaps | $gapCount |

Full JSON: ``logs/CONTINUITY.json``

## Plans (full stack)

1. NEXT_SESSION_PLAN.md — short  
2. NEXT_SESSION_PLAN_DEEP.md — architecture + protocol  
3. NEXT_SESSION_OPERATIONS.md — commands + sprints  
4. NEXT_SESSION_PLAN_DEEPER.md — **meta loop, discovery, closure graph**  
5. RESEARCH_BACKLOG.md — RB-xxx queue  
6. PLAN_INDEX.md — master TOC  

## Auto reports (detail)

### GAPS_REPORT (summary)

$(if ($gap) { ($gap -split "`n" | Select-Object -First 25) -join "`n" } else { "(missing)" })

### RESEARCH_DIFF (head)

$(if ($diff) { ($diff -split "`n" | Select-Object -First 35) -join "`n" } else { "(missing)" })

## New-chat prompt

``````text
BRIKVJ: session_start done. Read logs/SESSION_BRIEF.md, logs/CONTINUITY.json, NEXT_SESSION_PLAN_DEEPER.md §1–3. Execute recommended sprint (OPERATIONS §C). One closure-graph node minimum. WORKLOG + push fork. SSOT Documents\TouchDesigner\BRIKVJ. No Textport asks.
``````
"@

foreach ($dir in @((Join-Path $Kit "logs"), (Join-Path $Live "logs"))) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $brief | Set-Content (Join-Path $dir "SESSION_BRIEF.md") -Encoding utf8
    $continuityJson | Set-Content (Join-Path $dir "CONTINUITY.json") -Encoding utf8
}
Write-Host "SESSION_BRIEF.md written (sprint: $sprint)"
exit $gapExit
