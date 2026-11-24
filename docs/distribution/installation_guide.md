# NEXUS OS — Installation & Deployment Guide (`installation_guide.md`)

> **Operating System**: NEXUS OS 2026.1 (Aether Edition)  
> **Base Environment**: Fedora Linux 41 Workstation / Wayland Native  
> **Installer**: Anaconda Graphical Installer (Live Session)  
> **Default Filesystem**: Btrfs with Subvolumes (`@` root, `@home`, `/var`)  

---

## 1. Hardware Requirements & Tiers

| Hardware Tier | CPU | RAM | Storage | Graphics / Display | Intended Workload |
|---|---|---|---|---|---|
| **Tier 1 (Minimal)** | 2 Cores (x86_64) | 4 GB | 25 GB SSD | Basic OpenGL / Mesa | Lightweight scripting, Python, web browsing |
| **Tier 2 (Standard)** | 4+ Cores (x86_64) | 8–12 GB | 60 GB SSD | Intel / AMD / NVIDIA | Full-stack web, Rust, C++, microservices |
| **Tier 3 (Performance)** | 8+ Cores (x86_64) | 16–32+ GB | 120+ GB NVMe | NVIDIA RTX / AMD ROCm | Local AI models, PyTorch, ROS 2, Godot 4 |

---

## 2. Pre-Installation BIOS / UEFI Setup

1. **Boot Mode**: Set firmware boot mode to **UEFI** (Legacy BIOS is supported via El Torito hybrid MBR).
2. **Secure Boot**: Supported out-of-the-box via Fedora signed `shim-x64.efi`. If custom third-party kernel modules (e.g. proprietary NVIDIA drivers) are built locally, enroll the local Machine Owner Key (MOK).
3. **Hardware Virtualization**: Ensure **Intel VT-x** or **AMD-V / SVM** is enabled in firmware for Podman rootless containers and Android emulators.
4. **SATA / NVMe Controller**: Set disk mode to **AHCI / NVMe** (disable Intel RST / RAID).

---

## 3. Live Environment Experience

1. Insert bootable USB drive and power on the computer.
2. Select your USB drive from the firmware boot menu (typically `F12`, `F11`, or `Delete`).
3. In the bootloader menu, select **Start NEXUS OS 2026.1 (Live Desktop)**.
4. The system automatically launches the **Aether Wayland Desktop** session under the `liveuser` account.
5. In the live session, you can:
   - Test Wi-Fi and Bluetooth connectivity via the Quick Settings popover.
   - Test audio playback and volume control via PipeWire.
   - Open Universal Spotlight with `Win + Space`.
   - Launch Terminal (`Win + T`) or Developer Hub (`Win + D`).

---

## 4. Step-by-Step Installation to Disk

Double-click the **Install NEXUS OS to Disk** icon on the live desktop.

### Step 1: Language & Keyboard
- Select your primary language (default: `English (United States)`).
- Select your keyboard layout.

### Step 2: Storage Destination & Partitioning
- Select the target installation drive.
- Choose **Automatic Partitioning (Recommended)**:
  - Creates an EFI System Partition (`/boot/efi`, 600 MB).
  - Creates a Boot partition (`/boot`, 1 GB).
  - Creates a **Btrfs** volume with subvolumes:
    - `root` (`/`) — Operating system files and systemd units.
    - `home` (`/home`) — User projects, model caches, and personal configurations.
- Optional: Check **Encrypt my data** to enable LUKS2 full-disk encryption with a passphrase.

### Step 3: Network & Hostname
- Set the system hostname (default: `nexus-workstation`).
- Ensure active network connection (Ethernet or Wi-Fi).

### Step 4: User Account Setup
- Create your primary developer account:
  - Enter your full name and username.
  - Check **Make this user administrator** (adds user to `wheel` group for Polkit privilege separation).
  - Set a strong password.

### Step 5: Begin Installation
- Click **Begin Installation**. Anaconda writes the system packages and kernel to disk.
- Once completed, click **Reboot System** and remove the USB installation drive.

---

## 5. First Boot & Post-Installation Setup

Upon first boot, the system executes the **NEXUS First-Boot Provisioning Service** (`nexus-firstboot.service`):

1. **Zero-Telemetry Policy Enforcement**:
   - `privacy.telemetry_enabled` is locked to `false` in `/etc/nexus/system_policy.json`.
2. **Local AI Loopback Isolation**:
   - Configures `nexus-aid` (:11430), `omniroute` (:20128), and `ollama` (:11434) to bind strictly to `127.0.0.1`.
   - *Note*: Huge AI models are **not** downloaded during installation to conserve disk bandwidth. Users can browse and pull models via the Settings or Model Center after boot.
3. **Developer Packs Selection**:
   - Launch **Developer Packs** (`Win + I` or via App Launcher) to install complete curated toolsets (Vibe Coder, AI/ML, Full-Stack, Robotics, Android, etc.) with automated deduplication.
4. **Flathub Remote**:
   - Flathub is registered to allow clean, unprivileged installations of proprietary or third-party developer tools (Cursor, Discord, Slack, Spotify).

---

## 6. System Updates & Rollback

### Method A: Cloud-Native Image Mode (`bootc`)
```bash
# Check for and stage atomic OS update
sudo bootc update

# Reboot into the updated OS snapshot
sudo systemctl reboot

# If an issue occurs, instantly rollback to the prior snapshot
sudo bootc rollback
```

### Method B: Native Fedora DNF
```bash
# Check for package updates
dnf check-update

# Apply updates safely
sudo dnf upgrade --refresh
```
