"""
NEXUS OS — Developer Software Center Models
Data definitions for categories, packages, dependencies, and installation backends.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

CATEGORIES = [
    {"id": "all", "name": "All Categories", "icon": "🌐"},
    {"id": "ai_dev", "name": "AI Development", "icon": "🧠"},
    {"id": "editors", "name": "IDEs and Editors", "icon": "💻"},
    {"id": "languages", "name": "Programming Languages", "icon": "🔤"},
    {"id": "web_dev", "name": "Web Development", "icon": "🕸️"},
    {"id": "mobile_dev", "name": "Mobile Development", "icon": "📱"},
    {"id": "ai_ml", "name": "AI and Machine Learning", "icon": "🤖"},
    {"id": "databases", "name": "Databases", "icon": "🗄️"},
    {"id": "devops", "name": "DevOps", "icon": "🔄"},
    {"id": "cloud", "name": "Cloud", "icon": "☁️"},
    {"id": "security", "name": "Cybersecurity", "icon": "🛡️"},
    {"id": "robotics", "name": "Robotics", "icon": "🦾"},
    {"id": "embedded", "name": "Embedded Systems", "icon": "📟"},
    {"id": "gamedev", "name": "Game Development", "icon": "🎮"},
    {"id": "design", "name": "Design", "icon": "🎨"},
    {"id": "productivity", "name": "Productivity", "icon": "⚡"}
]

BACKENDS = {
    "dnf": {"name": "Native RPM (DNF)", "icon": "📦", "sandboxed": False, "requires_root": True},
    "flatpak": {"name": "Flatpak (Flathub)", "icon": "🧊", "sandboxed": True, "requires_root": False},
    "mise": {"name": "Mise Toolchain", "icon": "🛠️", "sandboxed": False, "requires_root": False},
    "appimage": {"name": "AppImage Portable", "icon": "📄", "sandboxed": False, "requires_root": False},
    "container": {"name": "OCI Container (Podman)", "icon": "🦭", "sandboxed": True, "requires_root": False},
    "vendor_pkg": {"name": "Official Vendor Installer", "icon": "🏷️", "sandboxed": False, "requires_root": False}
}

@dataclass
class SoftwarePackage:
    """Represents a developer software package in the NEXUS OS Catalog."""
    id: str
    name: str
    category: str
    description: str
    long_description: str
    version: str
    available_versions: List[str]
    maintainer: str
    license: str
    homepage: str
    icon: str
    backend: str              # "dnf", "flatpak", "mise", "appimage", "container", "vendor_pkg"
    package_ref: str          # Name in package manager (e.g. "godot", "org.godotengine.Godot")
    dependencies: List[str]   # Prerequisite packages
    size_mb: int
    compatibility: List[str]  # e.g. ["Fedora 41+", "x86_64", "Wayland Native"]
    check_binary: str         # Binary to check on PATH (e.g. "godot", "wireshark")
    install_args: List[str]   # Safe argument list for installation
    uninstall_args: List[str] # Safe argument list for uninstallation
    favorite: bool = False
    installed: bool = False
    update_available: bool = False
    installed_version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["backend_info"] = BACKENDS.get(self.backend, {"name": self.backend, "icon": "📦"})
        return d
