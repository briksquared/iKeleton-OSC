# Refresh harvest parts, Ableton place, patched toe, and index (no TouchDesigner UI).
$ErrorActionPreference = "Stop"
$Here = $PSScriptRoot
& "$Here\sync_harvest_parts.ps1"
& "$Here\sync_harvest_extended.ps1"
& "$Here\sync_harvest_vj_suite.ps1"
& "$Here\sync_harvest_glitch_fluid.ps1"
& "$Here\fix_ableton_tda_paths.ps1"
& "$Here\install_ableton_harvest_place.ps1"
& "$Here\fix_brikvj_brioch_toe.ps1"
& "$Here\scan_harvest_for_brikvj.ps1" -Quick
& "$Here\sync_scripts_to_documents.ps1"
Write-Host "BRIKVJ refresh complete. Open OPEN_BRIKVJ.cmd or run old_brik_vj_all_in_one.py inside TD."
