$files = Get-ChildItem -Path . -Force
foreach ($file in $files) {
    if ([System.Text.Encoding]::UTF8.GetBytes($file.Name)[0] -eq 32) {
        Write-Host "Found file with space name: '$($file.Name)' with length $($file.Name.Length)"
        Remove-Item $file.FullName -Force
        Write-Host "Deleted file"
    }
}