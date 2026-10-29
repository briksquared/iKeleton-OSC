try {
    $td = New-Object -ComObject TouchDesigner.Application
    $td | Get-Member -MemberType Method | Select-Object -First 20 Name
} catch {
    Write-Host "COM failed:" $_.Exception.Message
    exit 1
}
