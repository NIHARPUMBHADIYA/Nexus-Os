# NEXUS OS Fedora Workstation Kickstart Specification
# Target: Fedora 41 x86_64 Live ISO / Installation Media

text
lang en_US.UTF-8
keyboard us
timezone UTC

# Partitioning and bootloader
bootloader --location=mbr
clearpart --all --initlabel
autopart --type=btrfs

# Package selection
%packages
@core
@kde-desktop
plasma-workspace-wayland
podman
git
curl
wget
zsh
htop
%end

%post
echo "Configuring NEXUS OS default desktop session..."
# Set default SDDM theme to Nexus Aether
sed -i 's/^Current=.*/Current=org.nexus.aether.desktop/' /etc/sddm.conf.d/kde_settings.conf || true
%end
