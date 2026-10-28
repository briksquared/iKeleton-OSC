# Rewire TDAbleton M4L device paths in .als to this PC's User Library.
param(
    [string[]]$AlsPaths = @()
)
if ($AlsPaths.Count -eq 0) {
    $base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\ableton"
    $AlsPaths = @(
        "$base\BRIKVJ_Drums_TDAbleton.als",
        "$base\BRIKVJ_DrumLoop.als"
    )
    if (Test-Path "$base\compositions") {
        $AlsPaths += Get-ChildItem "$base\compositions" -Filter "*.als" -Recurse | ForEach-Object { $_.FullName }
    }
}
$ErrorActionPreference = "Stop"
$TdaRoot = "C:/Users/briks/Documents/Ableton/User Library/TDAbleton"
$map = @{
    "TDA_Ignore_MIDI.amxd" = "$TdaRoot/TDA_Ignore_MIDI.amxd"
    "TDA_MIDI.amxd" = "$TdaRoot/TDA_MIDI.amxd"
    "TDA_Ignore.amxd" = "$TdaRoot/TDA_Ignore.amxd"
    "TDA_Master.amxd" = "$TdaRoot/TDA_Master.amxd"
    "TDA_Level.amxd" = "$TdaRoot/TDA_Level.amxd"
    "TDA_Mapper.amxd" = "$TdaRoot/TDA_Mapper.amxd"
}

function Compress-Als($xmlPath, $alsPath) {
    $xml = [IO.File]::ReadAllBytes($xmlPath)
    $ms = New-Object IO.MemoryStream
    $gz = New-Object IO.Compression.GzipStream($ms, [IO.Compression.CompressionMode]::Compress)
    $gz.Write($xml, 0, $xml.Length)
    $gz.Close()
    [IO.File]::WriteAllBytes($alsPath, $ms.ToArray())
    $ms.Close()
}

foreach ($als in $AlsPaths) {
    if (-not (Test-Path $als)) { Write-Warning "Skip missing $als"; continue }
    $tmp = Join-Path $env:TEMP ("brikvj_als_" + [guid]::NewGuid().ToString("n"))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    $xml = Join-Path $tmp "set.xml"
    $bytes = [IO.File]::ReadAllBytes($als)
    $ms = New-Object IO.MemoryStream(,$bytes)
    $gz = New-Object IO.Compression.GzipStream($ms, [IO.Compression.CompressionMode]::Decompress)
    $sr = New-Object IO.StreamReader($gz)
    [IO.File]::WriteAllText($xml, $sr.ReadToEnd())
    $sr.Close(); $gz.Close(); $ms.Close()

    $content = Get-Content $xml -Raw
    $content = $content -replace "C:/Users/sunsp/[^<""]+TDA_Ignore_MIDI\.amxd", $map["TDA_Ignore_MIDI.amxd"]
    $content = $content -replace "C:/Users/sunsp/[^<""]+TDA_MIDI\.amxd", $map["TDA_MIDI.amxd"]
    $content = $content -replace "C:/Users/sunsp/[^<""]+TDA_Ignore\.amxd", $map["TDA_Ignore.amxd"]
    $content = $content -replace "C:/Users/sunsp/[^<""]+TDA_Master\.amxd", $map["TDA_Master.amxd"]
    $content = $content -replace "C:/Users/sunsp/[^<""]+TDA_Level\.amxd", $map["TDA_Level.amxd"]
    $content = $content -replace "C:/Users/sunsp/[^<""]+TDA_Mapper\.amxd", $map["TDA_Mapper.amxd"]
    # Relative sample refs for BRIKVJ composition folder
    $content = $content -replace "C:/Users/sunsp/Desktop/Derivative/TDSystemII/Testing Ground/TDADemo Live Set/Samples/Imported/[^""<]+", "C:/Users/briks/Documents/TouchDesigner/BRIKVJ/ableton/samples/brikvj_drum_loop.mp3"
    Set-Content $xml $content -NoNewline
    Compress-Als $xml $als
    Write-Host "Fixed TDA paths -> $als"
    Remove-Item $tmp -Recurse -Force
}
