"""
NEXUS OS — Developer Packs PyQt6 Bridge (`devpack_bridge.py`)
Exposes reactive pack lists, multi-pack selection, dependency preview, live progress,
log streaming, and installation actions to QML.
"""

from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from dataclasses import asdict

from .devpack_catalog import DEVELOPER_PACKS, get_pack_by_id, get_all_packs
from .devpack_resolver import DevPackResolver, ResolutionPlan
from .devpack_engine import DevPackEngine


class DevPackBridge(QObject):
    """
    Reactive PyQt6 Bridge for Developer Packs UI.
    """

    selectionChanged = pyqtSignal()
    planChanged = pyqtSignal()
    statusChanged = pyqtSignal()
    logsChanged = pyqtSignal()
    installedPacksChanged = pyqtSignal()
    activePackDetailChanged = pyqtSignal()

    def __init__(self, engine: Optional[DevPackEngine] = None, parent=None):
        super().__init__(parent)
        self._engine = engine or DevPackEngine()
        self._resolver = DevPackResolver()

        self._selected_pack_ids: List[str] = ["vibecoder"]  # Default selection
        self._active_pack_detail_id: str = "vibecoder"
        self._plan_data: Dict[str, Any] = {}
        self._status_message: str = "Ready"

        # Wire engine callbacks
        self._engine.on_progress = self._handle_progress
        self._engine.on_log = self._handle_log
        self._engine.on_finished = self._handle_finished

        self._update_plan()

    def _update_plan(self):
        plan = self._resolver.resolve(self._selected_pack_ids, include_optional=False)
        self._plan_data = {
            "selected_pack_ids": plan.selected_pack_ids,
            "selected_pack_names": plan.selected_pack_names,
            "total_size_mb": plan.total_size_mb,
            "total_size_formatted": plan.total_size_formatted,
            "free_disk_mb": plan.free_disk_mb,
            "has_sufficient_disk": plan.has_sufficient_disk,
            "hardware_warnings": plan.hardware_warnings,
            "conflicts": plan.conflicts,
            "stages": plan.stages,
            "tools_count": len(plan.resolved_tools),
            "tools": [
                {
                    "id": t.id,
                    "name": t.name,
                    "category": t.category,
                    "backend": t.backend,
                    "size_mb": t.size_mb,
                    "is_required": t.is_required
                } for t in plan.resolved_tools
            ]
        }
        self.planChanged.emit()

    def _handle_progress(self, progress: float, message: str):
        self._status_message = message
        self.statusChanged.emit()

    def _handle_log(self, line: str):
        self.logsChanged.emit()

    def _handle_finished(self, success: bool, reason: str):
        self._status_message = "Installation Completed Successfully!" if success else f"Installation Failed: {reason}"
        self.statusChanged.emit()
        self.installedPacksChanged.emit()
        self.selectionChanged.emit()

    # --- Properties ---

    @pyqtProperty(QVariant, notify=installedPacksChanged)
    def packsList(self):
        """Returns the list of 15 developer packs with installed status."""
        packs = []
        for p in DEVELOPER_PACKS:
            d = asdict(p)
            d["is_installed"] = self._engine.is_pack_installed(p.id)
            d["is_selected"] = p.id in self._selected_pack_ids
            packs.append(d)
        return packs

    @pyqtProperty(QVariant, notify=selectionChanged)
    def selectedPackIds(self):
        return list(self._selected_pack_ids)

    @pyqtProperty(QVariant, notify=planChanged)
    def resolutionPlan(self):
        return self._plan_data

    @pyqtProperty(bool, notify=statusChanged)
    def isRunning(self):
        return self._engine.is_running()

    @pyqtProperty(float, notify=statusChanged)
    def progress(self):
        return self._engine.get_progress()

    @pyqtProperty(str, notify=statusChanged)
    def statusMessage(self):
        return self._status_message

    @pyqtProperty(str, notify=statusChanged)
    def currentTool(self):
        return self._engine.get_current_status().get("current_tool", "")

    @pyqtProperty(QVariant, notify=logsChanged)
    def logLines(self):
        return self._engine.get_current_status().get("log_lines", [])

    @pyqtProperty(QVariant, notify=installedPacksChanged)
    def installedPackIds(self):
        return self._engine.get_installed_packs()

    @pyqtProperty(QVariant, notify=activePackDetailChanged)
    def activePackDetail(self):
        pack = get_pack_by_id(self._active_pack_detail_id)
        if pack:
            d = asdict(pack)
            d["is_installed"] = self._engine.is_pack_installed(pack.id)
            d["is_selected"] = pack.id in self._selected_pack_ids
            return d
        return asdict(DEVELOPER_PACKS[0])

    # --- Slots ---

    @pyqtSlot(str)
    def togglePackSelection(self, pack_id: str):
        """Toggles a pack in the multi-pack selection list."""
        if pack_id in self._selected_pack_ids:
            self._selected_pack_ids.remove(pack_id)
        else:
            self._selected_pack_ids.append(pack_id)
        self.selectionChanged.emit()
        self._update_plan()

    @pyqtSlot()
    def clearSelection(self):
        """Clears all selected packs."""
        self._selected_pack_ids.clear()
        self.selectionChanged.emit()
        self._update_plan()

    @pyqtSlot()
    def selectAll(self):
        """Selects all 15 packs."""
        self._selected_pack_ids = [p.id for p in DEVELOPER_PACKS]
        self.selectionChanged.emit()
        self._update_plan()

    @pyqtSlot(str)
    def inspectPack(self, pack_id: str):
        """Sets active pack for detail inspection."""
        self._active_pack_detail_id = pack_id
        self.activePackDetailChanged.emit()

    @pyqtSlot(bool, bool)
    def startInstallation(self, include_optional: bool = False, rollback_on_failure: bool = True):
        """Starts background installation of currently selected packs."""
        if not self._selected_pack_ids:
            return
        self._status_message = "Starting installation..."
        self.statusChanged.emit()
        self._engine.start_installation(
            self._selected_pack_ids,
            include_optional=include_optional,
            rollback_on_failure=rollback_on_failure
        )

    @pyqtSlot()
    def cancelInstallation(self):
        """Cancels running installation."""
        self._engine.cancel()

    @pyqtSlot(str, result=bool)
    def uninstallPack(self, pack_id: str) -> bool:
        """Uninstalls a developer pack."""
        success = self._engine.uninstall_pack(pack_id)
        if success:
            self.installedPacksChanged.emit()
            self.selectionChanged.emit()
        return success
