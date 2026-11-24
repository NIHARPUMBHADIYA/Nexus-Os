"""
NEXUS OS — Tools Integration PyQt6 Bridge (`ToolsIntegrationBridge`)
Connects the QML Tools Integration View to the backend catalog, detector,
safe config adapter, and launch manager.
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from .tool_catalog import ToolCatalog
from .tool_detector import ToolDetector
from .config_adapter import ConfigAdapter
from .launch_manager import LaunchManager

class ToolsIntegrationBridge(QObject):
    """
    QObject bridge exposing modern AI coding tools status and actions to QML.
    """

    toolsChanged = pyqtSignal()
    statsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.catalog = ToolCatalog()
        self.detector = ToolDetector(self.catalog)
        self.config_adapter = ConfigAdapter(self.detector)
        self.launch_manager = LaunchManager(self.detector)

        self._tools = self.detector.scan_all_tools()
        self._profiles = self.config_adapter.get_profiles()
        self._update_stats()

    def _update_stats(self):
        installed_cnt = sum(1 for t in self._tools if t.get("installed"))
        configured_cnt = sum(1 for t in self._tools if t.get("config_detected"))
        ai_cnt = sum(1 for t in self._tools if t.get("ai_endpoint_configured"))

        self._stats = {
            "total": len(self._tools),
            "installed": installed_cnt,
            "configured": configured_cnt,
            "ai_connected": ai_cnt
        }

    # --- Properties ---

    @pyqtProperty(QVariant, notify=toolsChanged)
    def toolsList(self):
        return self._tools

    @pyqtProperty(QVariant, constant=True)
    def profilesList(self):
        return self._profiles

    @pyqtProperty(QVariant, notify=statsChanged)
    def stats(self):
        return self._stats

    # --- Invokable Slots ---

    @pyqtSlot()
    def scanTools(self):
        self._tools = self.detector.scan_all_tools()
        self._update_stats()
        self.toolsChanged.emit()
        self.statsChanged.emit()

    @pyqtSlot(str, str, result=QVariant)
    def applyProfile(self, toolId: str, profileId: str):
        res = self.config_adapter.apply_ai_profile(toolId, profileId)
        # Re-detect after config update
        self._tools = self.detector.scan_all_tools()
        self._update_stats()
        self.toolsChanged.emit()
        self.statsChanged.emit()
        return res

    @pyqtSlot(str, str, result=QVariant)
    def launchTool(self, toolId: str, projectPath: str = ""):
        return self.launch_manager.launch_tool(toolId, projectPath if projectPath else None)

    @pyqtSlot(str, result=QVariant)
    def createDesktopShortcut(self, toolId: str):
        return self.launch_manager.generate_desktop_shortcut(toolId)

    @pyqtSlot(str, result=QVariant)
    def getBackups(self, toolId: str):
        tool = self.catalog.get_tool(toolId)
        if not tool:
            return []
        import sys
        plat_key = "windows" if sys.platform == "win32" else "linux"
        config_path_raw = tool.get("config_paths", {}).get(plat_key) or tool.get("config_paths", {}).get("linux", "")
        resolved = self.detector.resolve_path(config_path_raw)
        return self.config_adapter.list_backups(resolved)

    @pyqtSlot(str, str, result=bool)
    def restoreBackup(self, toolId: str, backupPath: str):
        tool = self.catalog.get_tool(toolId)
        if not tool:
            return False
        import sys
        plat_key = "windows" if sys.platform == "win32" else "linux"
        config_path_raw = tool.get("config_paths", {}).get(plat_key) or tool.get("config_paths", {}).get("linux", "")
        resolved = self.detector.resolve_path(config_path_raw)
        success = self.config_adapter.restore_backup(backupPath, resolved)
        if success:
            self.scanTools()
        return success
