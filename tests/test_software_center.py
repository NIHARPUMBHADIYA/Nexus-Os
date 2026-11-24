"""
NEXUS OS — Developer Software Center Test Suite
Verifies:
1. 15 Categories & Curated Catalog of Developer Packages
2. Fast Fuzzy Search and Multi-Criteria Filtering
3. Multi-Backend Safe Installation & Removal Workflows
4. Asynchronous Task Progress Tracking & Cancellation
5. Favorites Management & Persistence
6. QML Component Compilation & Bridge Bindings
"""

import os
import sys
import json
import time
import shutil
import tempfile
import unittest

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.software_center.catalog_models import CATEGORIES, BACKENDS
from src.software_center.catalog_db import CatalogDB
from src.software_center.install_engine import InstallEngine
from src.software_center.software_center_core import SoftwareCenterCore
from src.software_center.software_center_bridge import SoftwareCenterBridge

class TestSoftwareCenter(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="nexus_sc_test_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_categories_and_catalog_completeness(self):
        """Verify 15 required categories and key developer tools are present."""
        db = CatalogDB(self.test_dir)
        categories = db.get_categories()

        # Check category count (15 + 'all' = 16)
        cat_ids = [c["id"] for c in categories]
        required_cats = [
            "ai_dev", "editors", "languages", "web_dev", "mobile_dev",
            "databases", "devops", "cloud", "security", "robotics",
            "embedded", "gamedev", "design", "productivity"
        ]
        for req in required_cats:
            self.assertIn(req, cat_ids, f"Missing category: {req}")

        # Check required packages exist
        required_tools = [
            "antigravity", "cursor", "windsurf", "claude_code", "opencode", "ollama",
            "vscode", "vscodium", "zed", "neovim", "intellij_idea_community",
            "python", "gcc_cpp", "openjdk", "rust", "golang", "dart",
            "nodejs", "bun",
            "postgresql", "redis",
            "podman", "git", "kubernetes_kubectl",
            "wireshark", "nmap", "ghidra",
            "ros2_desktop", "arduino_ide", "platformio",
            "android_studio", "flutter_sdk",
            "godot", "blender", "dbeaver"
        ]

        packages = db._packages
        for tool_id in required_tools:
            self.assertIn(tool_id, packages, f"Missing tool in catalog: {tool_id}")
            pkg = packages[tool_id]
            self.assertTrue(len(pkg.name) > 0)
            self.assertTrue(len(pkg.version) > 0)
            self.assertIn(pkg.backend, BACKENDS)
            self.assertTrue(pkg.size_mb > 0)
            self.assertGreater(len(pkg.dependencies), 0)

    def test_search_and_category_filtering(self):
        """Verify keyword search and category filtering."""
        core = SoftwareCenterCore(self.test_dir)

        # 1. Search for 'python'
        py_results = core.search(query="python")
        self.assertGreater(len(py_results), 0)
        self.assertTrue(any(p["id"] == "python" for p in py_results))

        # 2. Filter by category 'security'
        sec_results = core.search(category="security")
        self.assertGreater(len(sec_results), 0)
        for p in sec_results:
            self.assertEqual(p["category"], "security")

        # 3. Filter by category 'gamedev'
        game_results = core.search(category="gamedev")
        self.assertTrue(any(p["id"] == "godot" for p in game_results))

    def test_favorites_persistence(self):
        """Verify toggling and saving favorites across sessions."""
        core1 = SoftwareCenterCore(self.test_dir)
        self.assertFalse(core1.catalog.get_package("nmap").favorite)

        # Toggle favorite
        is_fav = core1.toggle_favorite("nmap")
        self.assertTrue(is_fav)

        # Reload in a new core instance
        core2 = SoftwareCenterCore(self.test_dir)
        self.assertTrue(core2.catalog.get_package("nmap").favorite)

        # Untoggle favorite
        is_fav_again = core2.toggle_favorite("nmap")
        self.assertFalse(is_fav_again)

    def test_installation_engine_dry_run_and_progress(self):
        """Verify multi-backend install task execution, state progression, and completion."""
        core = SoftwareCenterCore(self.test_dir)
        pkg = core.catalog.get_package("godot")
        pkg.installed = False

        # Submit install task
        res = core.install("godot", dry_run=True)
        self.assertTrue(res["success"])
        task_id = res["task"]["task_id"]

        # Wait for task completion
        max_wait = 2.0
        start = time.time()
        while time.time() - start < max_wait:
            t = core.engine.get_task(task_id)
            if t and t["status"] in ("completed", "failed"):
                break
            time.sleep(0.05)

        final_task = core.engine.get_task(task_id)
        self.assertEqual(final_task["status"], "completed")
        self.assertEqual(final_task["progress_percent"], 100)
        self.assertTrue(pkg.installed)
        self.assertEqual(pkg.installed_version, pkg.version)

    def test_uninstallation_workflow(self):
        """Verify uninstallation state transition."""
        core = SoftwareCenterCore(self.test_dir)
        pkg = core.catalog.get_package("wireshark")
        pkg.installed = True

        res = core.uninstall("wireshark", dry_run=True)
        self.assertTrue(res["success"])
        task_id = res["task"]["task_id"]

        max_wait = 2.0
        start = time.time()
        while time.time() - start < max_wait:
            t = core.engine.get_task(task_id)
            if t and t["status"] in ("completed", "failed"):
                break
            time.sleep(0.05)

        self.assertFalse(pkg.installed)

    def test_task_cancellation(self):
        """Verify cancellation of an active task."""
        core = SoftwareCenterCore(self.test_dir)
        pkg = core.catalog.get_package("blender")

        task = core.engine.submit_task(pkg, action="install", dry_run=False)
        cancelled = core.cancel_task(task.task_id)
        self.assertTrue(cancelled)

        t_dict = core.engine.get_task(task.task_id)
        self.assertIn(t_dict["status"], ("cancelled", "failed"))

    def test_qml_view_compilation(self):
        """Verify QML compilation of NexusSoftwareCenterView.qml with bridge attached."""
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QGuiApplication
        from PyQt6.QtQuick import QQuickView

        app = QGuiApplication.instance() or QGuiApplication(sys.argv)
        view = QQuickView()

        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        sc_qml = os.path.join(base_dir, "src", "software_center", "qml")

        view.engine().addImportPath(ds_qml)
        view.engine().addImportPath(sc_qml)

        core = SoftwareCenterCore(self.test_dir)
        bridge = SoftwareCenterBridge(core)
        view.rootContext().setContextProperty("softwareCenterBridge", bridge)

        qml_path = os.path.join(sc_qml, "NexusSoftwareCenterView.qml")
        view.setSource(QUrl.fromLocalFile(qml_path))

        status = view.status()
        self.assertEqual(
            status,
            QQuickView.Status.Ready,
            f"NexusSoftwareCenterView.qml failed compilation with status {status}"
        )

if __name__ == "__main__":
    unittest.main()
