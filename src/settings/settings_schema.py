"""
NEXUS OS — Settings Categories & Configuration Schema
Defines the 21 settings categories, groups, and default values.
"""

from typing import Dict, Any, List

SETTINGS_GROUPS = [
    {"id": "personalization", "name": "Personalization"},
    {"id": "development", "name": "Apps & Development"},
    {"id": "ai", "name": "AI & Intelligence"},
    {"id": "hardware", "name": "Hardware & Input"},
    {"id": "connectivity", "name": "Connectivity"},
    {"id": "security", "name": "Security & Privacy"},
    {"id": "system", "name": "System & Maintenance"}
]

SETTINGS_CATEGORIES = [
    # 1. Personalization
    {"id": "appearance", "name": "Appearance", "icon": "🎨", "group": "personalization", "keywords": ["theme", "color", "dark", "light", "accent", "contrast"]},
    {"id": "desktop", "name": "Desktop", "icon": "🖥️", "group": "personalization", "keywords": ["wallpaper", "background", "workspace", "virtual"]},
    {"id": "dock", "name": "Dock", "icon": "⚓", "group": "personalization", "keywords": ["dock", "position", "autohide", "dodge", "size"]},
    
    # 2. Hardware & Input
    {"id": "keyboard", "name": "Keyboard & Shortcuts", "icon": "⌨️", "group": "hardware", "keywords": ["shortcut", "hotkey", "binding", "meta", "space", "key"]},
    {"id": "display", "name": "Display", "icon": "📺", "group": "hardware", "keywords": ["resolution", "scale", "refresh", "monitor", "hdr"]},
    {"id": "sound", "name": "Sound", "icon": "🔊", "group": "hardware", "keywords": ["volume", "audio", "mic", "output", "pipewire"]},

    # 3. Connectivity
    {"id": "network", "name": "Network", "icon": "📶", "group": "connectivity", "keywords": ["wifi", "ethernet", "ip", "dns", "vpn", "proxy"]},
    {"id": "bluetooth", "name": "Bluetooth", "icon": "ᛒ", "group": "connectivity", "keywords": ["bluetooth", "device", "pair", "wireless"]},

    # 4. System & Search
    {"id": "spotlight", "name": "Spotlight", "icon": "🔍", "group": "system", "keywords": ["search", "spotlight", "provider", "fuzzy", "meta+space"]},
    {"id": "indexing", "name": "Indexing", "icon": "🗂️", "group": "system", "keywords": ["index", "exclude", "ignore", "fts5", "cache"]},
    {"id": "notifications", "name": "Notifications", "icon": "🔔", "group": "system", "keywords": ["alert", "dnd", "banner", "sound", "popup"]},
    {"id": "storage", "name": "Storage", "icon": "💾", "group": "system", "keywords": ["disk", "space", "partition", "vram", "clean"]},

    # 5. Apps & Development
    {"id": "applications", "name": "Applications", "icon": "📦", "group": "development", "keywords": ["app", "default", "uninstall", "flatpak", "rpm"]},
    {"id": "developer", "name": "Developer Environment", "icon": "🛠️", "group": "development", "keywords": ["ide", "cursor", "vscode", "zed", "podman", "mise", "terminal"]},

    # 6. AI & Intelligence
    {"id": "aicore", "name": "AI Core", "icon": "⚡", "group": "ai", "keywords": ["proxy", "omniroute", "port", "daemon", "service"]},
    {"id": "models", "name": "Models", "icon": "🧠", "group": "ai", "keywords": ["vram", "ollama", "gguf", "governor", "headroom", "timeout"]},

    # 7. Security & Privacy
    {"id": "security", "name": "Security", "icon": "🛡️", "group": "security", "keywords": ["polkit", "root", "firewall", "selinux", "sandbox"]},
    {"id": "privacy", "name": "Privacy", "icon": "🔒", "group": "security", "keywords": ["telemetry", "vault", "secrets", "keyring", "key"]},

    # 8. System Services, Updates & About
    {"id": "services", "name": "System Services", "icon": "⚙️", "group": "system", "keywords": ["systemd", "daemon", "start", "stop", "restart", "log"]},
    {"id": "updates", "name": "Updates", "icon": "🔄", "group": "system", "keywords": ["dnf", "upgrade", "channel", "kernel", "version"]},
    {"id": "about", "name": "About NEXUS OS", "icon": "ℹ️", "group": "system", "keywords": ["about", "specs", "system", "kernel", "fedora", "cpu", "memory"]}
]

DEFAULT_SETTINGS: Dict[str, Any] = {
    # Appearance
    "appearance.theme": "midnight",
    "appearance.mode": "dark",
    "appearance.accent": "#6366F1",
    "appearance.corner_radius": "medium",
    "appearance.blur_enabled": True,
    "appearance.reduced_motion": False,

    # Desktop & Dock
    "desktop.wallpaper": "nebula",
    "desktop.wallpaper_blur": 15,
    "dock.position": "bottom",
    "dock.size": "medium",
    "dock.auto_dodge": True,

    # Keyboard Shortcuts
    "shortcuts.spotlight": "Meta+Space",
    "shortcuts.terminal": "Meta+T",
    "shortcuts.devhub": "Meta+D",
    "shortcuts.settings": "Meta+S",
    "shortcuts.editor": "Meta+E",
    "shortcuts.tools": "Meta+I",

    # Spotlight & Indexing
    "spotlight.max_results": 10,
    "spotlight.enable_web": False,
    "spotlight.enable_commands": True,
    "spotlight.enable_ai": True,
    "indexing.excluded_paths": [
        "~/.ssh",
        "~/.gnupg",
        "~/.aws",
        "~/.docker",
        "**/node_modules",
        "**/target",
        "**/.git",
        "**/__pycache__"
    ],

    # Developer & Containers
    "developer.default_ide": "cursor",
    "developer.default_terminal": "zsh",
    "developer.container_engine": "podman",
    "developer.mise_enabled": True,

    # AI Core & Local Models
    "aicore.proxy_port": 11430,
    "aicore.omniroute_port": 20128,
    "aicore.ollama_port": 11434,
    "aicore.autostart_omniroute": True,
    "aicore.autostart_ollama": True,
    "aicore.vram_headroom_mb": 2048,
    "aicore.idle_timeout_minutes": 15,

    # Security & Privacy
    "security.polkit_required": True,
    "security.loopback_only": True,
    "privacy.telemetry_enabled": False,  # Strict zero-telemetry
    "privacy.crash_reporting": False,

    # Notifications & Display
    "notifications.dnd": False,
    "notifications.timeout_secs": 5,
    "display.scale_factor": 1.0,
    "sound.master_volume": 75,

    # Updates
    "updates.channel": "stable",
    "updates.auto_check": True
}
