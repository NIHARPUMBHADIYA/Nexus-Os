"""
NEXUS OS — Developer Hub PyQt6 Bridge
Bridges DeveloperHubCore to QML for the Project Dashboard, Wizard, and Workspace.
"""

import os
import json
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from .hub_core import get_hub, DEFAULT_TEMPLATES

class DeveloperHubBridge(QObject):
    projectsUpdated = pyqtSignal()
    projectCreated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hub = get_hub()

    @pyqtSlot(result=str)
    def getProjectsJson(self) -> str:
        projects = self.hub.get_projects()
        return json.dumps(projects)

    @pyqtSlot(str, result=bool)
    def toggleFavorite(self, project_id: str) -> bool:
        res = self.hub.toggle_favorite(project_id)
        self.projectsUpdated.emit()
        return res

    @pyqtSlot(result=str)
    def getTemplatesJson(self) -> str:
        templates_list = []
        for key, tpl in DEFAULT_TEMPLATES.items():
            templates_list.append({
                "key": key,
                "name": tpl["name"],
                "category": tpl["category"],
                "language": tpl["language"],
                "framework": tpl["framework"],
                "file_count": len(tpl["files"]),
                "commands": list(tpl.get("dev_commands", {}).keys())
            })
        return json.dumps(templates_list)

    @pyqtSlot(result=str)
    def getEnvironmentStatusJson(self) -> str:
        return json.dumps(self.hub.get_environment_status())

    @pyqtSlot(str, str, str, bool, bool, str, result=str)
    def createProject(self, template_key: str, name: str, location_dir: str,
                      enable_git: bool, enable_ai: bool, dev_env: str) -> str:
        if not location_dir:
            location_dir = os.path.expanduser("~/Projects")
        res = self.hub.create_project(template_key, name, location_dir, enable_git, enable_ai, dev_env)
        self.projectsUpdated.emit()
        self.projectCreated.emit(json.dumps(res))
        return json.dumps(res)

    @pyqtSlot(str, str, result=bool)
    def saveSession(self, project_path: str, session_json: str) -> bool:
        try:
            data = json.loads(session_json)
            self.hub.save_session(project_path, data)
            return True
        except Exception:
            return False

    @pyqtSlot(str, result=str)
    def loadSession(self, project_path: str) -> str:
        session = self.hub.load_session(project_path)
        return json.dumps(session)

    @pyqtSlot(str, str, result=str)
    def launchExternalIDE(self, ide_name: str, project_path: str) -> str:
        res = self.hub.launch_external_ide(ide_name, project_path)
        return json.dumps(res)

    @pyqtSlot(str, result=str)
    def getProjectFiles(self, project_path: str) -> str:
        """Returns relative paths of files in project root (max 2 levels)."""
        clean_path = os.path.expanduser(project_path)
        if not os.path.isdir(clean_path):
            return json.dumps([])

        files = []
        try:
            for root, dirs, filenames in os.walk(clean_path):
                # Filter out hidden and build dirs
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", "target", "build", "dist"]]
                rel_dir = os.path.relpath(root, clean_path)
                for f in filenames:
                    rel_path = f if rel_dir == "." else os.path.join(rel_dir, f)
                    files.append(rel_path.replace("\\", "/"))
                if len(files) > 100:
                    break
        except Exception:
            pass
        return json.dumps(files[:60])

    @pyqtSlot(str, result=str)
    def readFileContent(self, file_path: str) -> str:
        if not os.path.isfile(file_path):
            return ""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(50000)
        except Exception as e:
            return f"Error reading file: {e}"

    @pyqtSlot(str, str, result=bool)
    def writeFileContent(self, file_path: str, content: str) -> bool:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception:
            return False
