# =============================================================================
# NEXUS OS — Live Workstation & Installation Kickstart Specification
# Target: Fedora 41 x86_64 Hybrid Live Media / ISO Installation Image
# =============================================================================

# System authorization & display
version=F41
keyboard --vckeymap=us --xlayouts='us'
lang en_US.UTF-8
timezone UTC --utc
network --bootproto=dhcp --device=link --activate

# Installation target and storage partitioning
# Default: Btrfs with standard Fedora subvolume layout (@ and @home)
clearpart --all --initlabel
bootloader --location=mbr --append="rhgb quiet splash rd.live.image"
autopart --type=btrfs --fstype=btrfs

# Live environment user configuration
selinux --enforcing
firewall --enabled --service=ssh,mdns

# Repositories (Official Fedora 41 Everything & Updates)
url --url="https://dl.fedoraproject.org/pub/fedora/linux/releases/41/Everything/x86_64/os/"
repo --name="fedora" --baseurl="https://dl.fedoraproject.org/pub/fedora/linux/releases/41/Everything/x86_64/os/"
repo --name="updates" --baseurl="https://dl.fedoraproject.org/pub/fedora/linux/updates/41/Everything/x86_64/"

# =============================================================================
# Curated Package Manifest
# =============================================================================
%packages
@core
@standard
@base-x
@kde-desktop
plasma-workspace-wayland
kwin-wayland
sddm
sddm-kcm

# Audio & Multimedia (Low-latency PipeWire)
pipewire
pipewire-pulseaudio
pipewire-alsa
wireplumber

# Network & Connectivity
NetworkManager
NetworkManager-wifi
bluez
bluez-tools

# Developer Toolchain & Containers
podman
podman-docker
git
git-lfs
gh
curl
wget
zsh
htop
btop
fastfetch
neovim
sqlite
sqlite-devel
gcc
gcc-c++
make
cmake
ninja-build
python3
python3-devel
python3-pip

# Qt6 Runtime & QML Graphics
qt6-qtbase
qt6-qtbase-gui
qt6-qtdeclarative
qt6-qtquickcontrols2
qt6-qtsvg

# Installer & Live System Utilities
anaconda
anaconda-live
livemedia-creator
dracut-live
btrfs-progs
efibootmgr
grub2-efi-x64
grub2-pc
shim-x64
isolinux
syslinux

-gnome-shell
-sendmail
%end

# =============================================================================
# Post-Installation & Live Environment Provisioning
# =============================================================================
%post
echo "=== Configuring NEXUS OS Live & Installed Environment ==="

# 1. Create Live Desktop User (liveuser) with sudo privileges
useradd -m -c "NEXUS Live User" -G wheel liveuser || true
passwd -d liveuser || true

# 2. Configure SDDM Autologin for Live Session
mkdir -p /etc/sddm.conf.d
cat << 'EOF' > /etc/sddm.conf.d/live_autologin.conf
[Autologin]
User=liveuser
Session=plasma

[Theme]
Current=breeze

[General]
DisplayServer=wayland
EOF

# 3. Create Desktop Icon to Launch Anaconda Installer
mkdir -p /home/liveuser/Desktop
cat << 'EOF' > /home/liveuser/Desktop/liveinst.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Install NEXUS OS to Disk
Comment=Launch the graphical system installer
Exec=liveinst
Icon=system-software-install
Terminal=false
StartupNotify=true
Categories=System;
EOF
chmod 0755 /home/liveuser/Desktop/liveinst.desktop
chown -R liveuser:liveuser /home/liveuser/Desktop || true

# 4. Enforce Zero Telemetry Policy
mkdir -p /etc/nexus
cat << 'EOF' > /etc/nexus/system_policy.json
{
  "privacy.telemetry_enabled": false,
  "security.loopback_only": true,
  "security.polkit_required": true,
  "release_version": "2026.1"
}
EOF
chmod 0644 /etc/nexus/system_policy.json

# 5. Enable Systemd Services
systemctl enable sddm.service
systemctl enable NetworkManager.service
systemctl enable bluetooth.service
systemctl enable podman.socket

echo "=== Post-Installation Configuration Complete ==="
%end
