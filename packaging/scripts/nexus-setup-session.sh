#!/usr/bin/env bash
# =============================================================================
# NEXUS OS — Dedicated First-Boot Account Setup Wayland Session Launcher
# Runs KWin Wayland with only the Setup Wizard in kiosk mode (no desktop chrome)
# =============================================================================
set -e

export QT_QUICK_CONTROLS_STYLE=Basic
export QT_WAYLAND_DISABLE_WINDOWDECORATION=1

# Ensure D-Bus session bus is running
if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
    eval $(dbus-launch --sh-syntax --exit-with-session 2>/dev/null || true)
fi

# Run kwin_wayland with the setup wizard as the sole session client
if command -v kwin_wayland >/dev/null 2>&1; then
    exec kwin_wayland --no-global-shortcuts --exit-with-session /usr/bin/nexus-setup
else
    exec /usr/bin/nexus-setup
fi
