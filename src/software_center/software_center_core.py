"""
NEXUS OS — Developer Software Center Core Coordinator
Unites the Catalog Database and Installation Engine.
"""

import os
from typing import Dict, Any, List, Optional
from .catalog_models import CATEGORIES, SoftwarePackage
from .catalog_db import CatalogDB
from .install_engine import InstallEngine, InstallTask

class SoftwareCenterCore:
    """
    Central business logic coordinator for the Developer Software Center.
    """

    def __init__(self, config_dir: Optional[str] = None):
        self.catalog = CatalogDB(config_dir)
        self.engine = InstallEngine()

    def get_categories(self) -> List[Dict[str, Any]]:
        return self.catalog.get_categories()

    def get_package(self, package_id: str) -> Optional[Dict[str, Any]]:
        pkg = self.catalog.get_package(package_id)
        return pkg.to_dict() if pkg else None

    def search(
        self,
        query: str = "",
        category: str = "all",
        filter_installed: bool = False,
        filter_favorites: bool = False
    ) -> List[Dict[str, Any]]:
        return self.catalog.search_packages(query, category, filter_installed, filter_favorites)

    def install(self, package_id: str, version: Optional[str] = None, dry_run: bool = False) -> Dict[str, Any]:
        pkg = self.catalog.get_package(package_id)
        if not pkg:
            return {"success": False, "error": f"Package '{package_id}' not found in catalog."}

        task = self.engine.submit_task(pkg, action="install", version=version, dry_run=dry_run)
        return {"success": True, "task": task.to_dict()}

    def uninstall(self, package_id: str, dry_run: bool = False) -> Dict[str, Any]:
        pkg = self.catalog.get_package(package_id)
        if not pkg:
            return {"success": False, "error": f"Package '{package_id}' not found in catalog."}

        task = self.engine.submit_task(pkg, action="uninstall", dry_run=dry_run)
        return {"success": True, "task": task.to_dict()}

    def update(self, package_id: str, dry_run: bool = False) -> Dict[str, Any]:
        pkg = self.catalog.get_package(package_id)
        if not pkg:
            return {"success": False, "error": f"Package '{package_id}' not found in catalog."}

        task = self.engine.submit_task(pkg, action="update", dry_run=dry_run)
        return {"success": True, "task": task.to_dict()}

    def toggle_favorite(self, package_id: str) -> bool:
        return self.catalog.toggle_favorite(package_id)

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        return self.engine.get_active_tasks()

    def cancel_task(self, task_id: str) -> bool:
        return self.engine.cancel_task(task_id)

    def get_stats(self) -> Dict[str, Any]:
        packages = list(self.catalog._packages.values())
        installed_cnt = sum(1 for p in packages if p.installed)
        fav_cnt = len(self.catalog._favorites)
        return {
            "total_packages": len(packages),
            "installed_count": installed_cnt,
            "favorites_count": fav_cnt,
            "categories_count": len(CATEGORIES) - 1
        }
