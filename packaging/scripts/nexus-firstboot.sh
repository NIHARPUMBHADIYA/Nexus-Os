#!/usr/bin/env bash
# =============================================================================
# NEXUS OS — First-Boot Provisioning & User Environment Initialization
# =============================================================================
set -euo pipefail

LOG_FILE="/var/log/nexus-firstboot.log"
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting NEXUS OS First-Boot Setup..."

# 1. Enforce Zero Telemetry Policy
mkdir -p /etc/nexus
cat << 'EOF' > /etc/nexus/system_policy.json
{
  "privacy.telemetry_enabled": false,
  "security.loopback_only": true,
  "security.polkit_required": true,
  "created_at": "2026-11-23"
}
EOF
chmod 0644 /etc/nexus/system_policy.json
echo "✓ Zero-telemetry policy enforced."

# 2. Configure Local AI Loopback Ports & Security
# RULE: Do not download huge AI models during installation. Let users choose after.
mkdir -p /etc/nexus/ai
cat << 'EOF' > /etc/nexus/ai/daemon_config.json
{
  "proxy_port": 11430,
  "omniroute_port": 20128,
  "ollama_port": 11434,
  "vram_headroom_mb": 2048,
  "auto_download_models": false,
  "bind_address": "127.0.0.1"
}
EOF
chmod 0644 /etc/nexus/ai/daemon_config.json
echo "✓ AI Core daemons configured for 127.0.0.1 loopback isolation."

# 3. Add Flathub remote for non-redistributable developer tools
if command -v flatpak >/dev/null 2>&1; then
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo || true
    echo "✓ Flathub remote configured."
fi

# 4. Initialize Skel Directories for Future User Accounts
mkdir -p /etc/skel/Projects
mkdir -p /etc/skel/.config/nexus
mkdir -p /etc/skel/.local/share/nexus

# 5. Automatically configure SDDM autologin for the user created during initial setup
FIRST_USER=$(awk -F: '$3 == 1000 {print $1}' /etc/passwd || true)
if [ -n "${FIRST_USER}" ]; then
    mkdir -p /etc/sddm.conf.d
    cat << EOF > /etc/sddm.conf.d/autologin.conf
[Autologin]
User=${FIRST_USER}
Session=plasma
Relogin=false
EOF
    echo "✓ SDDM autologin configured for newly created user: ${FIRST_USER}"
fi

# 6. Disable firstboot service so it only runs once
if command -v systemctl >/dev/null 2>&1; then
    systemctl disable nexus-firstboot.service || true
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] NEXUS OS First-Boot Initialization Complete!"
exit 0
