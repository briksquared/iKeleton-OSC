param(
    [Parameter(Mandatory = $true)]
    [string]$ToePath
)

# Expand -> inject autostart -> collapse for BRIKVJ / NewProject .toe files
$ErrorActionPreference = "Stop"
$TdBin = "C:\Program Files\Derivative\TouchDesigner\bin"
$ToeExpand = Join-Path $TdBin "toeexpand.exe"
$ToeCollapse = Join-Path $TdBin "toecollapse.exe"
$Inject = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\scripts\inject_brikvj_autostart.py"

$ToePath = (Resolve-Path $ToePath).Path
$DirPath = "$ToePath.dir"

if (Test-Path $DirPath) { Remove-Item $DirPath -Recurse -Force }
& $ToeExpand $ToePath | Out-Null
if (-not (Test-Path $DirPath)) { throw "toeexpand did not create $DirPath" }

python $Inject $ToePath
if ($LASTEXITCODE -ne 0) { throw "inject failed" }

$Parent = Split-Path $ToePath -Parent
$Leaf = Split-Path $ToePath -Leaf
Push-Location $Parent
try {
    $out = & $ToeCollapse $Leaf 2>&1
    $out | ForEach-Object { $_ }
    $collapsed = Get-Item $ToePath -ErrorAction SilentlyContinue
    if (-not $collapsed -or $collapsed.Length -lt 100) {
        throw "toecollapse produced invalid toe (see warnings above)"
    }
}
finally {
    Pop-Location
}

Get-Item $ToePath | Select-Object FullName, Length, LastWriteTime
