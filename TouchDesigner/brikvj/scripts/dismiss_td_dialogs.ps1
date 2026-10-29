# Headless: dismiss modal TD dialogs during unattended builds (newer .tox / OK spam).
param(
    [int]$MaxMinutes = 50,
    [int]$IntervalMs = 400
)
$ErrorActionPreference = "SilentlyContinue"
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class TdDlg {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc lpEnumFunc, IntPtr lParam);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
}
"@
$shell = New-Object -ComObject WScript.Shell
$deadline = (Get-Date).AddMinutes($MaxMinutes)
$patterns = @("TouchDesigner", "Warning", "Load .tox", "newer", "Compatibility", "Error", "Operator Error", "Dialog Error")
while ((Get-Date) -lt $deadline) {
    if (-not (Get-Process TouchDesigner -ErrorAction SilentlyContinue)) { break }
    $hits = New-Object System.Collections.Generic.List[IntPtr]
    [TdDlg+EnumProc]$cb = {
        param($h, $l)
        if (-not [TdDlg]::IsWindowVisible($h)) { return $true }
        $sb = New-Object System.Text.StringBuilder 512
        [void][TdDlg]::GetWindowText($h, $sb, 512)
        $t = $sb.ToString()
        foreach ($p in $patterns) {
            if ($t -like "*$p*") { $hits.Add($h); break }
        }
        return $true
    }
    [TdDlg]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
    foreach ($h in $hits) {
        [void][TdDlg]::SetForegroundWindow($h)
        Start-Sleep -Milliseconds 80
        $shell.SendKeys("{ENTER}")
        Start-Sleep -Milliseconds 80
        $shell.SendKeys("{ESC}")
    }
    Start-Sleep -Milliseconds $IntervalMs
}
