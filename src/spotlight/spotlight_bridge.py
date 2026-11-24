"""
NEXUS OS — Spotlight QML Bridge (PyQt6)
Exposes the Python/SQLite search engine and safety policies to the QML interface.
"""

import json
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from .search_engine import get_engine, SpotlightEngine

class SpotlightBridge(QObject):
    # Signals to QML
    resultsUpdated = pyqtSignal(str)
    actionExecuted = pyqtSignal(str, str)
    confirmationRequired = pyqtSignal(str, str, str) # action_id, warning_message, metadata_json

    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine: SpotlightEngine = get_engine()

    @pyqtSlot(str, str, result=str)
    def query(self, search_text: str, category_filter: str = "All") -> str:
        cat = None if category_filter in ["All", ""] else category_filter
        results = self.engine.search(search_text, category_filter=cat, limit=12)
        results_json = json.dumps(results)
        self.resultsUpdated.emit(results_json)
        return results_json

    @pyqtSlot(str)
    def recordLaunch(self, item_id: str):
        self.engine.record_launch(item_id)

    @pyqtSlot(str, str, result=str)
    def executeAction(self, action_id: str, item_json: str) -> str:
        try:
            item = json.loads(item_json)
        except Exception:
            item = {}

        # Check if the requested action is flagged as destructive
        actions = item.get("actions", [])
        is_dest = False
        warning_msg = ""
        for act in actions:
            if act.get("id") == action_id:
                if act.get("destructive", False):
                    is_dest = True
                    warning_msg = act.get("warning", "This action may affect system state. Are you sure?")
                break

        if is_dest:
            self.confirmationRequired.emit(action_id, warning_msg, item_json)
            return json.dumps({"status": "confirmation_required", "warning": warning_msg})

        # Safe execution
        self.engine.record_launch(item.get("id", ""))
        self.actionExecuted.emit(action_id, item.get("title", ""))
        return json.dumps({"status": "executed", "action": action_id, "title": item.get("title", "")})

    @pyqtSlot(str, str, result=str)
    def confirmAction(self, action_id: str, item_json: str) -> str:
        try:
            item = json.loads(item_json)
        except Exception:
            item = {}

        self.engine.record_launch(item.get("id", ""))
        self.actionExecuted.emit(action_id, item.get("title", ""))
        return json.dumps({"status": "confirmed_and_executed", "action": action_id})

    @pyqtSlot(result=str)
    def checkShortcutConflict(self) -> str:
        status = self.engine.check_shortcut_conflict("Meta+Space")
        return json.dumps(status)

    @pyqtSlot(result=str)
    def getIndexStats(self) -> str:
        stats = self.engine.db.get_stats()
        return json.dumps(stats)

    @pyqtSlot(result=bool)
    def rebuildIndex(self) -> bool:
        self.engine.db.clear_index()
        return True
