"""
NEXUS OS — Settings PyQt6 Bridge (`SettingsBridge`)
Provides reactive properties, category switching, search filtering, shortcut editing,
and live storage/service inspection for QML.
"""

from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from .settings_engine import SettingsEngine


class SettingsBridge(QObject):
    """
    Reactive PyQt6 Bridge for NEXUS OS Settings View.
    Exposes all 21 categories, settings search, shortcut editor, storage stats,
    service health, and exclusion paths to QML.
    """

    settingsChanged = pyqtSignal()
    activeCategoryChanged = pyqtSignal()
    searchQueryChanged = pyqtSignal()
    searchResultsChanged = pyqtSignal()
    storageDataChanged = pyqtSignal()
    shortcutsChanged = pyqtSignal()
    servicesChanged = pyqtSignal()
    indexingExclusionsChanged = pyqtSignal()

    def __init__(self, engine: Optional[SettingsEngine] = None, parent=None):
        super().__init__(parent)
        self._engine = engine or SettingsEngine()
        self._active_category_id = "appearance"
        self._search_query = ""
        self._search_results: List[Dict[str, Any]] = []
        self._storage_data = self._engine.get_storage_analysis()
        self._shortcuts_list = self._engine.get_shortcuts()
        self._services_list = self._engine.get_system_services()
        self._about_info = self._engine.get_about_info()

    # --- Properties ---

    @pyqtProperty(QVariant, notify=settingsChanged)
    def allSettings(self):
        """Returns the full dictionary of active settings."""
        return self._engine.get_all_settings()

    @pyqtProperty(QVariant, constant=True)
    def categoriesList(self):
        """Returns the list of 21 categories."""
        return self._engine.get_categories()

    @pyqtProperty(QVariant, constant=True)
    def groupsList(self):
        """Returns the list of 7 category groups."""
        return self._engine.get_groups()

    @pyqtProperty(str, notify=activeCategoryChanged)
    def activeCategoryId(self):
        return self._active_category_id

    @pyqtProperty(QVariant, notify=activeCategoryChanged)
    def activeCategory(self):
        """Returns metadata for the currently active category."""
        for cat in self._engine.get_categories():
            if cat["id"] == self._active_category_id:
                return cat
        return self._engine.get_categories()[0]

    @pyqtProperty(str, notify=searchQueryChanged)
    def searchQuery(self):
        return self._search_query

    @pyqtProperty(QVariant, notify=searchResultsChanged)
    def searchResults(self):
        return self._search_results

    @pyqtProperty(QVariant, notify=storageDataChanged)
    def storageData(self):
        return self._storage_data

    @pyqtProperty(QVariant, notify=shortcutsChanged)
    def shortcutsList(self):
        return self._shortcuts_list

    @pyqtProperty(QVariant, notify=servicesChanged)
    def servicesList(self):
        return self._services_list

    @pyqtProperty(QVariant, constant=True)
    def aboutInfo(self):
        return self._about_info

    @pyqtProperty(QVariant, notify=indexingExclusionsChanged)
    def indexingExclusions(self):
        return self._engine.get_indexing_exclusions()

    # --- Slots ---

    @pyqtSlot(str)
    def setActiveCategory(self, category_id: str):
        """Switches the active settings category."""
        if category_id != self._active_category_id:
            self._active_category_id = category_id
            self.activeCategoryChanged.emit()

    @pyqtSlot(str, result=QVariant)
    def getSetting(self, key: str):
        """Retrieves a single setting value."""
        return self._engine.get_setting(key)

    @pyqtSlot(str, QVariant, result=bool)
    def setSetting(self, key: str, value: Any) -> bool:
        """Sets a setting value and notifies QML of changes."""
        success = self._engine.set_setting(key, value)
        if success:
            self.settingsChanged.emit()
            if key.startswith("shortcuts."):
                self._shortcuts_list = self._engine.get_shortcuts()
                self.shortcutsChanged.emit()
            elif key.startswith("indexing."):
                self.indexingExclusionsChanged.emit()
        return success

    @pyqtSlot()
    def resetToDefaults(self):
        """Resets all settings to system defaults."""
        self._engine.reset_to_defaults()
        self._shortcuts_list = self._engine.get_shortcuts()
        self.settingsChanged.emit()
        self.shortcutsChanged.emit()
        self.indexingExclusionsChanged.emit()

    @pyqtSlot(str)
    def resetCategory(self, category_id: str):
        """Resets all settings in a specific category."""
        self._engine.reset_category(category_id)
        self._shortcuts_list = self._engine.get_shortcuts()
        self.settingsChanged.emit()
        self.shortcutsChanged.emit()
        self.indexingExclusionsChanged.emit()

    @pyqtSlot(str)
    def search(self, query: str):
        """Performs live settings search."""
        self._search_query = query
        self.searchQueryChanged.emit()
        self._search_results = self._engine.search_settings(query)
        self.searchResultsChanged.emit()

    @pyqtSlot(str, str, result=QVariant)
    def updateShortcut(self, shortcut_id: str, key_combination: str):
        """Validates and updates a keyboard shortcut."""
        res = self._engine.update_shortcut(shortcut_id, key_combination)
        if res.get("success"):
            self._shortcuts_list = self._engine.get_shortcuts()
            self.shortcutsChanged.emit()
            self.settingsChanged.emit()
        return res

    @pyqtSlot(str, str, result=QVariant)
    def checkShortcutConflict(self, key_combination: str, target_id: str = ""):
        """Checks if a key combination conflicts with existing shortcuts."""
        return self._engine.check_shortcut_conflict(key_combination, target_id=target_id or None)

    @pyqtSlot(str, result=bool)
    def addIndexingExclusion(self, path: str) -> bool:
        """Adds a path to indexing exclusions."""
        ok = self._engine.add_indexing_exclusion(path)
        if ok:
            self.indexingExclusionsChanged.emit()
            self.settingsChanged.emit()
        return ok

    @pyqtSlot(str, result=bool)
    def removeIndexingExclusion(self, path: str) -> bool:
        """Removes a path from indexing exclusions."""
        ok = self._engine.remove_indexing_exclusion(path)
        if ok:
            self.indexingExclusionsChanged.emit()
            self.settingsChanged.emit()
        return ok

    @pyqtSlot()
    def refreshStorage(self):
        """Re-analyzes storage usage."""
        self._storage_data = self._engine.get_storage_analysis()
        self.storageDataChanged.emit()

    @pyqtSlot()
    def refreshServices(self):
        """Refreshes status of system services."""
        self._services_list = self._engine.get_system_services()
        self.servicesChanged.emit()

    @pyqtSlot(str, bool, result=bool)
    def toggleServiceAutostart(self, service_id: str, enable: bool) -> bool:
        """Toggles background autostart policy for services."""
        if service_id == "omniroute":
            self._engine.set_setting("aicore.autostart_omniroute", enable)
        elif service_id == "ollama":
            self._engine.set_setting("aicore.autostart_ollama", enable)
        self.refreshServices()
        return True
