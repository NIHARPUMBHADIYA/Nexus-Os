"""
NEXUS OS — Settings Application Test Suite (`tests/test_settings_app.py`)
Verifies:
1. Complete 21 categories and 7 groups catalog completeness.
2. Settings persistence and schema defaults.
3. Strict zero-telemetry security invariant (cannot be enabled).
4. Settings search across categories, keywords, and setting keys.
5. Keyboard shortcut editor with normalization and conflict detection.
6. Storage analysis with capacity and category breakdowns.
7. Indexing exclusions management.
8. System services monitoring and autostart configuration.
9. About NEXUS OS hardware and system information.
10. QML compilation and reactive bridge property bindings.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.settings.settings_schema import SETTINGS_GROUPS, SETTINGS_CATEGORIES, DEFAULT_SETTINGS
from src.settings.settings_engine import SettingsEngine
from src.settings.settings_bridge import SettingsBridge


class TestSettingsApp(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="nexus_settings_test_")
        self.engine = SettingsEngine(self.test_dir)
        self.bridge = SettingsBridge(self.engine)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_21_categories_and_groups_completeness(self):
        """Verify all 21 requested settings categories and 7 groups are properly defined."""
        categories = self.engine.get_categories()
        self.assertEqual(len(categories), 21, f"Expected 21 categories, got {len(categories)}")

        expected_ids = [
            "appearance", "desktop", "dock", "keyboard", "spotlight",
            "display", "network", "bluetooth", "sound", "notifications",
            "storage", "applications", "developer", "aicore", "models",
            "services", "security", "privacy", "indexing", "updates", "about"
        ]

        cat_ids = [c["id"] for c in categories]
        for cid in expected_ids:
            self.assertIn(cid, cat_ids, f"Category '{cid}' is missing from categories list.")

        groups = self.engine.get_groups()
        self.assertEqual(len(groups), 7)
        group_ids = [g["id"] for g in groups]
        self.assertIn("personalization", group_ids)
        self.assertIn("hardware", group_ids)
        self.assertIn("connectivity", group_ids)
        self.assertIn("system", group_ids)
        self.assertIn("development", group_ids)
        self.assertIn("ai", group_ids)
        self.assertIn("security", group_ids)

    def test_settings_persistence_and_defaults(self):
        """Verify settings load defaults, update values, and persist atomically to disk."""
        # Check initial default
        theme = self.engine.get_setting("appearance.theme")
        self.assertEqual(theme, "midnight")

        # Update setting
        success = self.engine.set_setting("appearance.theme", "tokyo-night")
        self.assertTrue(success)
        self.assertEqual(self.engine.get_setting("appearance.theme"), "tokyo-night")

        # Verify disk persistence
        settings_file = os.path.join(self.test_dir, "settings.json")
        self.assertTrue(os.path.isfile(settings_file))
        with open(settings_file, "r", encoding="utf-8") as f:
            persisted = json.load(f)
        self.assertEqual(persisted.get("appearance.theme"), "tokyo-night")

        # Reload new engine instance from same dir
        fresh_engine = SettingsEngine(self.test_dir)
        self.assertEqual(fresh_engine.get_setting("appearance.theme"), "tokyo-night")

        # Test reset category
        fresh_engine.reset_category("appearance")
        self.assertEqual(fresh_engine.get_setting("appearance.theme"), "midnight")

    def test_strict_zero_telemetry_policy(self):
        """Verify that zero telemetry is strictly enforced and cannot be enabled."""
        self.assertFalse(self.engine.get_setting("privacy.telemetry_enabled"))

        # Attempt to enable telemetry
        result = self.engine.set_setting("privacy.telemetry_enabled", True)
        self.assertFalse(result, "Engine must reject enabling telemetry")
        self.assertFalse(self.engine.get_setting("privacy.telemetry_enabled"))

    def test_settings_search(self):
        """Verify search finds matching categories, keywords, and individual settings."""
        # 1. Search category name
        res_cat = self.engine.search_settings("keyboard")
        self.assertTrue(any(r["category_id"] == "keyboard" for r in res_cat))

        # 2. Search keyword
        res_kw = self.engine.search_settings("vram")
        self.assertTrue(any(r["category_id"] == "models" for r in res_kw))

        # 3. Search setting key
        res_key = self.engine.search_settings("proxy_port")
        self.assertTrue(any("proxy_port" in str(r.get("key", "")) for r in res_key))

    def test_shortcut_normalization_and_conflict_detection(self):
        """Verify shortcut key normalization and conflict validation."""
        # Normalization
        norm1 = self.engine.normalize_shortcut("super+space")
        self.assertEqual(norm1, "Meta+Space")

        norm2 = self.engine.normalize_shortcut("ctrl+alt+t")
        self.assertEqual(norm2, "Ctrl+Alt+T")

        # Reserved shortcut conflict
        conflict_reserved = self.engine.check_shortcut_conflict("Alt+Tab")
        self.assertTrue(conflict_reserved["has_conflict"])
        self.assertTrue(conflict_reserved["is_reserved"])

        # Existing shortcut conflict
        conflict_existing = self.engine.check_shortcut_conflict("Meta+Space", target_id="terminal")
        self.assertTrue(conflict_existing["has_conflict"])
        self.assertIn("Universal Spotlight Search", conflict_existing["conflicts_with"])

        # Available shortcut
        conflict_none = self.engine.check_shortcut_conflict("Meta+Shift+K")
        self.assertFalse(conflict_none["has_conflict"])

        # Update shortcut successfully
        res = self.engine.update_shortcut("terminal", "Meta+Shift+T")
        self.assertTrue(res["success"])
        self.assertEqual(self.engine.get_setting("shortcuts.terminal"), "Meta+Shift+T")

    def test_indexing_exclusions(self):
        """Verify adding and removing directory patterns from indexing exclusions."""
        initial = self.engine.get_indexing_exclusions()
        self.assertIn("~/.ssh", initial)
        self.assertIn("**/node_modules", initial)

        # Add new exclusion
        ok = self.engine.add_indexing_exclusion("~/.my_secret_keys")
        self.assertTrue(ok)
        self.assertIn("~/.my_secret_keys", self.engine.get_indexing_exclusions())

        # Remove exclusion
        ok_rem = self.engine.remove_indexing_exclusion("~/.my_secret_keys")
        self.assertTrue(ok_rem)
        self.assertNotIn("~/.my_secret_keys", self.engine.get_indexing_exclusions())

    def test_storage_analysis(self):
        """Verify storage capacity calculation and breakdown categories."""
        storage = self.engine.get_storage_analysis()
        self.assertIn("total_bytes", storage)
        self.assertIn("used_bytes", storage)
        self.assertIn("free_bytes", storage)
        self.assertGreater(storage["total_bytes"], 0)
        self.assertIn("total_formatted", storage)
        self.assertIn("breakdown", storage)

        breakdown_ids = [item["id"] for item in storage["breakdown"]]
        self.assertIn("system", breakdown_ids)
        self.assertIn("home", breakdown_ids)
        self.assertIn("dev", breakdown_ids)
        self.assertIn("ai_models", breakdown_ids)
        self.assertIn("containers", breakdown_ids)

    def test_system_services_status(self):
        """Verify system daemons and autostart toggle."""
        services = self.engine.get_system_services()
        service_ids = [s["id"] for s in services]
        self.assertIn("nexus-aid", service_ids)
        self.assertIn("nexus-searchd", service_ids)
        self.assertIn("omniroute", service_ids)
        self.assertIn("ollama", service_ids)

        # Toggle service autostart
        self.bridge.toggleServiceAutostart("omniroute", False)
        self.assertFalse(self.engine.get_setting("aicore.autostart_omniroute"))

        self.bridge.toggleServiceAutostart("omniroute", True)
        self.assertTrue(self.engine.get_setting("aicore.autostart_omniroute"))

    def test_about_system_specs(self):
        """Verify about info collects OS, kernel, and hardware specifications."""
        about = self.engine.get_about_info()
        self.assertEqual(about["os_name"], "NEXUS OS")
        self.assertIn("2026.1", about["os_version"])
        self.assertIn("Fedora", about["os_base"])
        self.assertIn("KDE", about["desktop_shell"])
        self.assertGreater(about["cpu_cores"], 0)
        self.assertIn("RAM", about["ram_total"])
        self.assertIn("architecture", about)

    def test_qml_view_compilation(self):
        """Verify that NexusSettingsView.qml compiles cleanly without syntax errors in QML engine."""
        from PyQt6.QtGui import QGuiApplication
        from PyQt6.QtQuick import QQuickView
        from PyQt6.QtCore import QUrl

        app = QGuiApplication.instance() or QGuiApplication(sys.argv)

        view = QQuickView()
        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        settings_qml = os.path.join(base_dir, "src", "settings", "qml")

        view.engine().addImportPath(ds_qml)
        view.engine().addImportPath(settings_qml)
        view.rootContext().setContextProperty("settingsBridge", self.bridge)

        qml_path = os.path.join(settings_qml, "NexusSettingsView.qml")
        self.assertTrue(os.path.isfile(qml_path))

        view.setSource(QUrl.fromLocalFile(qml_path))
        status = view.status()

        # Check for errors
        errors = view.errors()
        err_messages = [e.toString() for e in errors]
        self.assertEqual(len(errors), 0, f"QML compilation errors: {err_messages}")
        self.assertEqual(status, QQuickView.Status.Ready, f"View status expected Ready, got {status}")


if __name__ == "__main__":
    unittest.main()
