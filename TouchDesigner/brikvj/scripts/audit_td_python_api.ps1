# Offline scan — TouchDesigner Python patterns that fail at runtime (no TD launch).
$Here = $PSScriptRoot
$bad = @()
Get-ChildItem $Here -Filter "*.py" | ForEach-Object {
    $lines = Get-Content $_.FullName
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $n = $i + 1
        $l = $lines[$i]
        if ($l -match '\.tags\.add\([^)]+,') { $bad += "$($_.Name):$n tags.add multi-arg" }
        if ($l -match '\.par\.label\s*=' -and $_.Name -ne "brikvj_td_helpers.py") {
            $bad += "$($_.Name):$n par.label (use set_label)"
        }
        if ($l -match 'runpy\.run_path') { $bad += "$($_.Name):$n runpy without TD globals" }
    }
}
if ($bad.Count -eq 0) {
    Write-Host "audit_td_python_api: OK"
    exit 0
}
$bad | ForEach-Object { Write-Host $_ }
Write-Host "audit_td_python_api: FAIL ($($bad.Count))"
exit 1
