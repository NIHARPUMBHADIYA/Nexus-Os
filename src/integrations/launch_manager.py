"""
NEXUS OS — Tool Launch Manager & Desktop Shortcut Integrator
Handles:
1. Safe process execution for project-specific launching
2. XDG .desktop shortcut generation
3. Uninstallation command dispatch
"""

import os
import sys
import shutil
import subprocess
from typing import Dict, Any, Optional
from .tool_catalog import ToolCatalog
from .tool_detector import ToolDetector

class LaunchManager:
    """
    Manages launching tools into project directories and creating desktop shortcuts.
    """

    def __init__(self, detector: Optional[ToolDetector] = None):
        self.detector = detector or ToolDetector()
        self.catalog = self.detector.catalog

    def launch_tool(self, tool_id: str, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Launch a tool, optionally opening a specific project directory."""
        tool_status = self.detector.detect_tool(tool_id)
        if not tool_status["installed"]:
            return {
                "success": False,
                "error": f"{tool_status['name']} is not installed on this workstation."
            }

        bin_path = tool_status["binary_path"]
        if not bin_path:
            return {
                "success": False,
                "error": f"Binary path not found for {tool_status['name']}."
            }

        cmd = [bin_path]
        if project_path and os.path.exists(project_path):
            cmd.append(os.path.abspath(project_path))

        try:
            # Safe process dispatch without shell concatenation
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True if sys.platform != "win32" else False
            )
            return {
                "success": True,
                "tool_id": tool_id,
                "tool_name": tool_status["name"],
                "project_path": project_path or "Default workspace",
                "message": f"Successfully launched {tool_status['name']}."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to launch {tool_status['name']}: {e}"
            }

    def generate_desktop_shortcut(self, tool_id: str, dest_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a compliant FreeDesktop .desktop shortcut file.
        Installs to ~/.local/share/applications/ or specified directory.
        """
        tool_info = self.catalog.get_tool(tool_id)
        if not tool_info:
            return {"success": False, "error": f"Unknown tool: {tool_id}"}

        target_dir = dest_dir or os.path.expanduser(os.path.join("~", ".local", "share", "applications"))
        os.makedirs(target_dir, exist_ok=True)
        desktop_file = os.path.join(target_dir, f"nexus-{tool_id}.desktop")

        bin_name = tool_info["binary_names"][0] if tool_info.get("binary_names") else tool_id
        is_terminal = tool_info.get("category") == "terminal_agent"

        content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={tool_info['name']}
Comment={tool_info['description']}
Exec={bin_name} %F
Icon=applications-development
Terminal={'true' if is_terminal else 'false'}
Categories=Development;IDE;Programming;
StartupNotify=true
StartupWMClass={bin_name}
Keywords=developer;ai;coding;editor;{tool_id};
"""
        try:
            with open(desktop_file, "w", encoding="utf-8") as f:
                f.write(content)

            if sys.platform != "win32":
                try:
                    os.chmod(desktop_file, 0o755)
                except Exception:
                    pass

            return {
                "success": True,
                "tool_id": tool_id,
                "shortcut_path": desktop_file,
                "message": f"Created desktop shortcut at {desktop_file}"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to create desktop shortcut: {e}"}

    def get_uninstall_info(self, tool_id: str) -> Dict[str, Any]:
        """Retrieve verified uninstallation command for the tool."""
        tool_info = self.catalog.get_tool(tool_id)
        if not tool_info:
            return {"error": f"Unknown tool: {tool_id}"}

        return {
            "tool_id": tool_id,
            "name": tool_info["name"],
            "uninstall_command": tool_info.get("uninstall_command", "Manual uninstallation required."),
            "requires_root": "sudo" in tool_info.get("uninstall_command", "")
        }
