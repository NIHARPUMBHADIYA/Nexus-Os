"""
NEXUS OS — Software Center PyQt6 Bridge (`SoftwareCenterBridge`)
Connects the QML Software Center UI to SoftwareCenterCore.
"""

from typing import Optional, List, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from .software_center_core import SoftwareCenterCore

class SoftwareCenterBridge(QObject):
    """
    QObject bridge for reactive Software Center property bindings and slots.
    """

    packagesChanged = pyqtSignal()
    tasksChanged = pyqtSignal()
    statsChanged = pyqtSignal()

    def __init__(self, core: Optional[SoftwareCenterCore] = None, parent=None):
        super().__init__(parent)
        self._core = core or SoftwareCenterCore()
        self._selected_category = "all"
        self._search_query = ""
        self._filter_installed = False
        self._filter_favorites = False

        self._categories = self._core.get_categories()
        self._packages = self._core.search()
        self._stats = self._core.get_stats()

    # --- Properties ---

    @pyqtProperty(QVariant, constant=True)
    def categoriesList(self):
        return self._categories

    @pyqtProperty(QVariant, notify=packagesChanged)
    def packagesList(self):
        return self._packages

    @pyqtProperty(QVariant, notify=tasksChanged)
    def activeTasks(self):
        return self._core.get_active_tasks()

    @pyqtProperty(QVariant, notify=statsChanged)
    def stats(self):
        return self._stats

    # --- Slots ---

    @pyqtSlot(str)
    def selectCategory(self, categoryId: str):
        self._selected_category = categoryId
        self._filter_installed = (categoryId == "installed_view")
        self._filter_favorites = (categoryId == "favorites_view")
        cat = "all" if self._filter_installed or self._filter_favorites else categoryId

        self._packages = self._core.search(
            query=self._search_query,
            category=cat,
            filter_installed=self._filter_installed,
            filter_favorites=self._filter_favorites
        )
        self.packagesChanged.emit()

    @pyqtSlot(str)
    def search(self, queryText: str):
        self._search_query = queryText
        cat = "all" if self._filter_installed or self._filter_favorites else self._selected_category
        self._packages = self._core.search(
            query=self._search_query,
            category=cat,
            filter_installed=self._filter_installed,
            filter_favorites=self._filter_favorites
        )
        self.packagesChanged.emit()

    @pyqtSlot(str, str, result=QVariant)
    def installPackage(self, packageId: str, version: str = ""):
        res = self._core.install(packageId, version if version else None, dry_run=True)
        self._packages = self._core.search(
            query=self._search_query,
            category="all" if self._filter_installed or self._filter_favorites else self._selected_category,
            filter_installed=self._filter_installed,
            filter_favorites=self._filter_favorites
        )
        self._stats = self._core.get_stats()
        self.packagesChanged.emit()
        self.tasksChanged.emit()
        self.statsChanged.emit()
        return res

    @pyqtSlot(str, result=QVariant)
    def uninstallPackage(self, packageId: str):
        res = self._core.uninstall(packageId, dry_run=True)
        self._packages = self._core.search(
            query=self._search_query,
            category="all" if self._filter_installed or self._filter_favorites else self._selected_category,
            filter_installed=self._filter_installed,
            filter_favorites=self._filter_favorites
        )
        self._stats = self._core.get_stats()
        self.packagesChanged.emit()
        self.tasksChanged.emit()
        self.statsChanged.emit()
        return res

    @pyqtSlot(str, result=bool)
    def toggleFavorite(self, packageId: str):
        is_fav = self._core.toggle_favorite(packageId)
        self._packages = self._core.search(
            query=self._search_query,
            category="all" if self._filter_installed or self._filter_favorites else self._selected_category,
            filter_installed=self._filter_installed,
            filter_favorites=self._filter_favorites
        )
        self._stats = self._core.get_stats()
        self.packagesChanged.emit()
        self.statsChanged.emit()
        return is_fav

    @pyqtSlot(str, result=bool)
    def cancelTask(self, taskId: str):
        cancelled = self._core.cancel_task(taskId)
        self.tasksChanged.emit()
        return cancelled

    @pyqtSlot()
    def refresh(self):
        self._packages = self._core.search(
            query=self._search_query,
            category="all" if self._filter_installed or self._filter_favorites else self._selected_category,
            filter_installed=self._filter_installed,
            filter_favorites=self._filter_favorites
        )
        self._stats = self._core.get_stats()
        self.packagesChanged.emit()
        self.tasksChanged.emit()
        self.statsChanged.emit()
