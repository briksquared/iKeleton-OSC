# Patch Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe (Brioch) for this Windows studio.
param(
    [switch]$InjectBuildAutostart
)
# Fixes: Mac Loopback device, invalid audio switch index, missing Jeremy mp3, stopped timeline.
$ErrorActionPreference = "Stop"
$TdBin = "C:\Program Files\Derivative\TouchDesigner\bin"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$Src = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\brioch-audio-reactive-vjing\briochSceno.beta.toe"
$Mp3 = "C:/Users/briks/Documents/TouchDesigner/BRIKVJ/ableton/samples/brikvj_drum_loop.mp3"
$Kan = "C:/Users/briks/Desktop/GitHub/audio/ableton/github/_sweep3/touchdesigner/brioch-audio-reactive-vjing/assets/audio/Kanine - Set It Off.mp3"
$Nec = "C:/Users/briks/Desktop/GitHub/audio/ableton/github/_sweep3/touchdesigner/brioch-audio-reactive-vjing/assets/audio/06 Necronomicon ft. Bohemian Club.mp3"

if (-not (Test-Path $Mp3)) {
    Write-Error "Missing test audio: $Mp3"
}
if ((Get-Item $Toe -ErrorAction SilentlyContinue).Length -lt 100000) {
    Copy-Item $Src $Toe -Force
}

Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Push-Location $Base
& "$TdBin\toeexpand.exe" "BRIKVJ.toe" | Out-Null

$dir = "$Toe.dir"
$startFile = Join-Path $dir ".start"
if (Test-Path $startFile) {
    $sc = Get-Content $startFile -Raw
    $sc = $sc -replace '#expectednodes[^\r\n]*\r?\n', ''
    Set-Content $startFile $sc -NoNewline
}

function Set-AudioFile($path, $file) {
    if (-not (Test-Path $path)) { return }
    $c = Get-Content $path -Raw
    $c = $c -replace "file 201326609[^\r\n]+", "file 201326609 "" "" '$file'"
    $c = $c -replace "file 201326608[^\r\n]+", "file 201326608 "" "" '$file'"
    if ($c -notmatch 'play 67108864 on') {
        $c = $c -replace '(\?\r?\n)', "`$1play 67108864 on`r`n"
    }
    Set-Content $path $c -NoNewline
}

$dir = "$Toe.dir"
Set-AudioFile "$dir\project1\analyseAudio\audioAnalysis\audiofilein1.parm" $Mp3
Set-AudioFile "$dir\project1\audiofilein1.parm" $Mp3
Set-AudioFile "$dir\project1\meshParticles\audioAnalysis\audiofilein1.parm" $Mp3
Set-AudioFile "$dir\project1\Kanine___Set_It_Off.parm" $Kan
Set-AudioFile "$dir\project1\06_Necronomicon_ft__Bohemian_Club.parm" $Nec

Set-Content "$dir\project1\audiodevin1.parm" @"
?
device 67108864 ""
active 67108864 on
channel 67108864 1-2
timeslice 67108864 on
autoexportroot 201326609 "" parent()
?
"@ -NoNewline

Set-Content "$dir\project1\swi453tch4.parm" @"
?
indexfirst 67108864 on
index 67108864 2
autoexportroot 201326609 "" parent()
?
"@ -NoNewline

$wp = "$dir\project1\whiteScreenControler.parm"
if (Test-Path $wp) {
    Set-Content $wp ((Get-Content $wp -Raw) -replace 'value1 67108864 0\.5', 'value1 67108864 0') -NoNewline
}
Set-Content "$dir\local\time.parm" ((Get-Content "$dir\local\time.parm" -Raw) -replace 'play 67108864 0', 'play 67108864 1') -NoNewline

$assetsSrc = Join-Path (Split-Path $Src -Parent) "assets"
$assetsDst = Join-Path $Base "assets"
if (Test-Path $assetsSrc) {
    Copy-Item $assetsSrc $assetsDst -Recurse -Force
}
$fbxC = "C:/Users/briks/Documents/TouchDesigner/BRIKVJ/assets/3d/croissant.fbx"
$fbxB = "C:/Users/briks/Documents/TouchDesigner/BRIKVJ/assets/3d/brioche-2.4.fbx"
$banana = "app.samplesFolder + '/Map/Banana.tif'"
Get-ChildItem $dir -Recurse -Filter "*.parm" | ForEach-Object {
    $c = Get-Content $_.FullName -Raw
    $changed = $false
    if ($c -match '\./assets/3d/croissant') {
        $c = $c -replace 'file 201326608 \./assets/3d/croissant\.fbx[^\r\n]+', "file 201326608 "" "" '$fbxC'"
        $changed = $true
    }
    if ($c -match '\./assets/3d/brioche') {
        $c = $c -replace 'file 201326608 \./assets/3d/brioche-2\.4\.fbx[^\r\n]+', "file 201326608 "" "" '$fbxB'"
        $changed = $true
    }
    if ($c -match '/System/Volumes/Data/Users/abigaelle') {
        $c = $c -replace 'file 201326608 /System/Volumes/Data/Users/abigaelle/Downloads/croissant\.fbx[^\r\n]+', "file 201326608 "" "" '$fbxC'"
        $changed = $true
    }
    if ($c -match 'C:/Users/Markus/Desktop/softedge\.png') {
        $c = $c -replace 'file 201326608 C:/Users/Markus/Desktop/softedge\.png[^\r\n]+', "file 201326608 "" "" `"$banana`""
        $changed = $true
    }
    if ($c -match 'rogueamoeba|com\.rogueamoeba') {
        $c = $c -replace 'device 67108864 com\.rogueamoeba[^\r\n]+', 'device 67108864 ""'
        $changed = $true
    }
    if ($_.Name -like 'importselect*.parm' -and $c -match 'geometry 67108864 /') {
        $c = $c -replace 'geometry 67108864 /(\S+)', 'geometry 67108864 $1'
        $changed = $true
    }
    if ($changed) { Set-Content $_.FullName $c -NoNewline }
}

# MIDI file demo is optional; keyboard CHOPs drive scenes — silence missing-device spam.
$midi = "$dir\project1\midiin2.parm"
if (Test-Path $midi) {
    Set-Content $midi ((Get-Content $midi -Raw) -replace 'active 67108864 on', 'active 67108864 off') -NoNewline
    if ((Get-Content $midi -Raw) -notmatch 'active 67108864') {
        $c = Get-Content $midi -Raw
        Set-Content $midi ($c -replace '(\?\r?\n)', "`$1active 67108864 off`r`n") -NoNewline
    }
}

$tocPath = Join-Path $Base "BRIKVJ.toe.toc"
if (Test-Path $tocPath) {
    $strip = @("brikvj_build_autostart", "old_brik_autostart", "brikvj_error_snapshot")
    $text = [Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($tocPath))
    $keep = foreach ($line in ($text -split "`n", 0, "SimpleMatch")) {
        $l = $line.TrimEnd("`r")
        if (-not $l) { continue }
        $drop = $false
        foreach ($n in $strip) {
            if ($l -like "project1/$n.*") { $drop = $true; break }
            if ($l -like "project1/mapping/kantanMapper/ui/$n.*") { $drop = $true; break }
        }
        if (-not $drop) { $l }
    }
    [IO.File]::WriteAllBytes($tocPath, [Text.Encoding]::ASCII.GetBytes(($keep -join "`n") + "`n"))
}
foreach ($n in @("brikvj_build_autostart", "old_brik_autostart", "brikvj_error_snapshot")) {
    Remove-Item "$dir\project1\$n.n", "$dir\project1\$n.parm", "$dir\project1\$n.text" -Force -ErrorAction SilentlyContinue
    Remove-Item "$dir\project1\mapping\kantanMapper\ui\$n.n", "$dir\project1\mapping\kantanMapper\ui\$n.parm", "$dir\project1\mapping\kantanMapper\ui\$n.text" -Force -ErrorAction SilentlyContinue
}
if ($InjectBuildAutostart) {
    $Inject = Join-Path $PSScriptRoot "inject_brikvj_build_autostart.py"
    $Kantan = Join-Path $PSScriptRoot "inject_kantan_boot.py"
    & python $Inject $Toe
    if ($LASTEXITCODE -ne 0) { Write-Error "inject_brikvj_build_autostart failed" }
    & python $Kantan $Toe
    if ($LASTEXITCODE -ne 0) { Write-Warning "inject_kantan_boot skipped or failed (non-fatal)" }
} else {
    foreach ($n in @("brikvj_build_autostart", "old_brik_autostart", "brikvj_error_snapshot")) {
        Remove-Item "$dir\project1\$n.n", "$dir\project1\$n.parm", "$dir\project1\$n.text" -Force -ErrorAction SilentlyContinue
    }
}
$Kantan = Join-Path $PSScriptRoot "inject_kantan_boot.py"
$Dlg = Join-Path $PSScriptRoot "inject_brikvj_dialog_prefs.py"
if (Test-Path $Kantan) { & python $Kantan $Toe }
if (Test-Path $Dlg) { & python $Dlg $Toe }
$prevEa = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& "$TdBin\toecollapse.exe" "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $prevEa
if ((Get-Item $Toe -ErrorAction SilentlyContinue).Length -lt 100000) {
    Write-Error "toecollapse failed — BRIKVJ.toe is truncated. Restore newest BRIKVJ.toe.bkp* and re-run."
}
Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Pop-Location
Push-Location $Base
& "$TdBin\toeexpand.exe" "BRIKVJ.toe" | Out-Null
Pop-Location
& "$PSScriptRoot\audit_brikvj_toe.ps1" -Dir (Join-Path $Base "BRIKVJ.toe.dir")
$auditExit = $LASTEXITCODE
Remove-Item (Join-Path $Base "BRIKVJ.toe.dir"), (Join-Path $Base "BRIKVJ.toe.toc") -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Patched BRIKVJ.toe -> $((Get-Item $Toe).Length) bytes"
if ($auditExit -ne 0) { exit $auditExit }
