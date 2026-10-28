# Scan expanded BRIKVJ.toe.dir for paths/devices that spam TouchDesigner errors on Windows.
param(
    [string]$Dir = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe.dir"
)
$patterns = @(
    @{ Name = "Mac Loopback"; Regex = "rogueamoeba|com\.rogueamoeba" },
    @{ Name = "Mac volume path"; Regex = "/System/Volumes/" },
    @{ Name = "Mac home path"; Regex = "(?<!:)/Users/[a-zA-Z]" },
    @{ Name = "Markus softedge"; Regex = "C:/Users/Markus" },
    @{ Name = "Relative ./assets"; Regex = "\./assets/" },
    @{ Name = "Jeremy sample"; Regex = "JeremyCaulfield" },
    @{ Name = "Invalid audio switch"; Regex = "swi453tch4\.parm[\s\S]*?index 67108864 [4-9]" }
)
if (-not (Test-Path $Dir)) {
    Write-Host "No expanded dir at $Dir — run fix_brikvj_brioch_toe.ps1 first."
    exit 2
}
$issues = @()
Get-ChildItem $Dir -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($Dir.Length + 1)
    if ($_.Extension -notin ".parm", ".n", ".text", ".build") { return }
    $raw = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $raw) { return }
    foreach ($p in $patterns) {
        if ($raw -match $p.Regex) {
            $issues += [pscustomobject]@{ Kind = $p.Name; File = $rel }
        }
    }
}
# swi453tch4 special (file path)
$sw = Join-Path $Dir "project1\swi453tch4.parm"
if (Test-Path $sw) {
    $s = Get-Content $sw -Raw
    if ($s -match 'index 67108864 ([4-9])') {
        $issues += [pscustomobject]@{ Kind = "swi453tch4 index out of range"; File = "project1\swi453tch4.parm" }
    }
}
if ($issues.Count -eq 0) {
    Write-Host "audit: OK (0 issues)"
    exit 0
}
$issues | Group-Object Kind | ForEach-Object { Write-Host ("  {0}: {1}" -f $_.Name, $_.Count) }
$issues | Select-Object -First 25 | Format-Table -AutoSize
Write-Host "audit: FAIL ($($issues.Count) issues)"
exit 1
