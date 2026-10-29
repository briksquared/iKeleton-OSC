# One-shot next-session bootstrap → logs/SESSION_BRIEF.md (kit + Documents).
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Repo = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC"

& "$PSScriptRoot\sync_scripts_to_documents.ps1" 2>&1 | Out-Null
& "$PSScriptRoot\brikvj_gap_report.ps1"
$gapExit = $LASTEXITCODE
& "$PSScriptRoot\brikvj_research_diff.ps1"

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

$sprint = if ($gapExit -ne 0) { "Sprint P0 (OPERATIONS.md §C) — fix GAPS_REPORT first" } else { "Sprint R — integrate from RESEARCH_DIFF + RESEARCH_BACKLOG open items" }

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

**$sprint**

## Plans (full stack)

1. NEXT_SESSION_PLAN.md — short  
2. NEXT_SESSION_PLAN_DEEP.md — architecture + protocol  
3. NEXT_SESSION_OPERATIONS.md — commands + sprints  
4. RESEARCH_BACKLOG.md — RB-xxx queue  
5. PLAN_INDEX.md — master TOC  

## Auto reports (detail)

### GAPS_REPORT (summary)

$(if ($gap) { ($gap -split "`n" | Select-Object -First 25) -join "`n" } else { "(missing)" })

### RESEARCH_DIFF (head)

$(if ($diff) { ($diff -split "`n" | Select-Object -First 35) -join "`n" } else { "(missing)" })

## New-chat prompt

``````text
BRIKVJ: Read logs/SESSION_BRIEF.md and NEXT_SESSION_OPERATIONS.md. Execute recommended sprint with evidence. Push fork. SSOT Documents\TouchDesigner\BRIKVJ. No Textport asks.
``````
"@

foreach ($dir in @((Join-Path $Kit "logs"), (Join-Path $Live "logs"))) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $brief | Set-Content (Join-Path $dir "SESSION_BRIEF.md") -Encoding utf8
}
Write-Host "SESSION_BRIEF.md written (sprint: $sprint)"
exit $gapExit
