"""
NEXUS OS — Tool Availability & Configuration Detector
Scans the local workstation to detect:
1. Binary or extension installation status
2. Installed version
3. Configuration file presence on disk
4. Active AI endpoint configuration (nexus-aid, OmniRoute, Ollama)
5. Update availability
"""

import os
import sys
import json
import shutil
import subprocess
from typing import Dict, Any, Optional, List
from .tool_catalog import ToolCatalog

class ToolDetector:
    """
    Detects presence, configuration, and AI routing state for all catalog tools.
    """

    def __init__(self, catalog: Optional[ToolCatalog] = None):
        self.catalog = catalog or ToolCatalog()

    @staticmethod
    def resolve_path(raw_path: str) -> str:
        """Expand ~ and Windows environment variables."""
        if not raw_path:
            return ""
        path = os.path.expanduser(raw_path)
        if sys.platform == "win32":
            for env_var in ("APPDATA", "LOCALAPPDATA", "USERPROFILE"):
                val = os.environ.get(env_var)
                if val:
                    path = path.replace(f"%{env_var}%", val)
                    path = path.replace(f"${{{env_var}}}", val)
        return os.path.normpath(path)

    def detect_tool(self, tool_id: str) -> Dict[str, Any]:
        """Inspect a specific tool on the system."""
        info = self.catalog.get_tool(tool_id)
        if not info:
            return {"installed": False, "error": f"Unknown tool: {tool_id}"}

        installed = False
        binary_path = ""
        version = ""
        is_extension = info.get("category") == "extension"

        # 1. Detection: Binaries
        for b_name in info.get("binary_names", []):
            found = shutil.which(b_name)
            if found:
                installed = True
                binary_path = found
                break

        # 2. Detection: VS Code Extensions (if extension)
        if is_extension:
            ext_id = info.get("extension_id", "").lower()
            ext_dirs = [
                os.path.expanduser(os.path.join("~", ".vscode", "extensions")),
                os.path.expanduser(os.path.join("~", ".vscode-oss", "extensions")),
                os.path.expanduser(os.path.join("~", ".cursor", "extensions")),
            ]
            for edir in ext_dirs:
                if os.path.isdir(edir):
                    try:
                        for entry in os.listdir(edir):
                            if entry.lower().startswith(ext_id):
                                installed = True
                                binary_path = os.path.join(edir, entry)
                                # Read version from extension package.json
                                pkg_json = os.path.join(binary_path, "package.json")
                                if os.path.isfile(pkg_json):
                                    with open(pkg_json, "r", encoding="utf-8", errors="ignore") as f:
                                        data = json.load(f)
                                        version = data.get("version", "")
                                break
                    except Exception:
                        pass
                if installed:
                    break

        # If binary found, try getting version
        if installed and not version and binary_path and not is_extension:
            try:
                res = subprocess.run([binary_path, "--version"], capture_output=True, text=True, timeout=1.5)
                if res.returncode == 0 and res.stdout.strip():
                    version = res.stdout.strip().splitlines()[0][:30]
            except Exception:
                version = "installed"

        # 3. Configuration Detection
        plat_key = "windows" if sys.platform == "win32" else "linux"
        config_path_raw = info.get("config_paths", {}).get(plat_key) or info.get("config_paths", {}).get("linux", "")
        resolved_config = self.resolve_path(config_path_raw)
        config_exists = os.path.isfile(resolved_config) if resolved_config else False

        # 4. AI Endpoint Configuration Detection
        ai_endpoint_configured = False
        active_ai_provider = "none"

        if config_exists:
            try:
                with open(resolved_config, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Check for local nexus-aid (11430), omniroute (20128), or ollama (11434)
                if "11430" in content or "nexus:default" in content or "nexus-aid" in content:
                    ai_endpoint_configured = True
                    active_ai_provider = "nexus-aid (:11430)"
                elif "20128" in content or "omniroute" in content.lower():
                    ai_endpoint_configured = True
                    active_ai_provider = "omniroute (:20128)"
                elif "11434" in content or "ollama" in content.lower():
                    ai_endpoint_configured = True
                    active_ai_provider = "ollama (:11434)"
            except Exception:
                pass

        return {
            "id": tool_id,
            "name": info["name"],
            "category": info["category"],
            "type": info["type"],
            "description": info["description"],
            "licensing": info["licensing"],
            "can_redistribute": info["can_redistribute"],
            "installed": installed,
            "binary_path": binary_path,
            "version": version or ("Not installed" if not installed else "Detected"),
            "config_path": resolved_config,
            "config_detected": config_exists,
            "supports_ai_endpoint": info.get("supports_ai_endpoint", False),
            "ai_endpoint_configured": ai_endpoint_configured,
            "active_ai_provider": active_ai_provider,
            "icon": info.get("icon", "💻"),
            "install_methods": info.get("install_methods", []),
            "uninstall_command": info.get("uninstall_command", ""),
            "website": info.get("website", "")
        }

    def scan_all_tools(self) -> List[Dict[str, Any]]:
        """Scan and return status for all 15 tools in the catalog."""
        results = []
        for tool_id in self.catalog.TOOLS:
            results.append(self.detect_tool(tool_id))
        return results
