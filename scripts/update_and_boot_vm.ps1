# NEXUS OS — VirtualBox Test Automation Script
param(
    [string]$IsoPath = "D:\My own os\build\nexus-os-2026.1-x86_64.iso",
    [string]$VmName = "Nex OS"
)

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

if (-not (Test-Path $VBoxManage)) {
    Write-Error "VBoxManage.exe not found at $VBoxManage"
    exit 1
}

if (-not (Test-Path $IsoPath)) {
    Write-Error "ISO file not found at $IsoPath. Please place the downloaded nexus-os-2026.1-x86_64.iso into build/"
    exit 1
}

$isoItem = Get-Item $IsoPath
$sizeGB = [math]::Round($isoItem.Length / 1GB, 2)
Write-Host "[+] Found ISO: $IsoPath ($sizeGB GB)"

if ($isoItem.Length -lt 2GB) {
    Write-Warning "[!] The ISO in build/ is $sizeGB GB (the old broken image). The genuine Fedora 41 ISO is 4.31 GB."
    Write-Warning "[!] Please extract the new ISO from the GitHub Actions artifact zip into $IsoPath"
}

Write-Host "[+] Attaching ISO to VM '$VmName'..."
& $VBoxManage storageattach $VmName --storagectl "IDE" --port 0 --device 0 --type dvddrive --medium $IsoPath

Write-Host "[+] Starting VM '$VmName' in GUI mode..."
& $VBoxManage startvm $VmName --type gui

Write-Host "[+] VM launched successfully!"
