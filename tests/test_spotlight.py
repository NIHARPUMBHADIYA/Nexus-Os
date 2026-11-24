#!/usr/bin/env python3
"""
NEXUS OS — Universal Spotlight Test Suite
Tests SQLite FTS5 indexing, fuzzy ranking, usage boost, sensitive file exclusions,
destructive command safety, shortcut conflict detection, and QML overlay loading.
"""

import unittest
import os
import sys
import tempfile
import json

# Setup headless QGuiApplication and Basic controls
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, QQmlComponent

from src.spotlight.search_engine import (
    SearchDatabase, SpotlightEngine, FileProvider, CommandProvider,
    ApplicationProvider, ProjectProvider, AIModelProvider, SystemActionsProvider
)
from src.spotlight.spotlight_bridge import SpotlightBridge

class TestSpotlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_db_fd, cls.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(cls.temp_db_fd)
        cls.engine = SpotlightEngine(cls.temp_db_path)

        if not QGuiApplication.instance():
            cls.app = QGuiApplication(sys.argv)
        else:
            cls.app = QGuiApplication.instance()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_db_path):
            try:
                os.remove(cls.temp_db_path)
            except Exception:
                pass

    def test_sqlite_fts5_indexing_and_query(self):
        db = self.engine.db
        db.insert_or_update(
            "test:1", "Applications", "Nexus Terminal",
            "Zsh shell with starship prompt and AI tools",
            path="/usr/bin/nexus-terminal"
        )
        db.insert_or_update(
            "test:2", "Projects", "nexus-os",
            "Developer-first Linux operating system",
            path="d:/My own os"
        )

        results = db.query_fts("Terminal")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "test:1")

        proj_results = db.query_fts("operating system")
        self.assertGreaterEqual(len(proj_results), 1)
        self.assertEqual(proj_results[0]["id"], "test:2")

    def test_usage_frequency_and_recency_boost(self):
        db = self.engine.db
        item_id = "app:terminal"

        # Record multiple launches
        db.record_usage(item_id)
        db.record_usage(item_id)
        db.record_usage(item_id)

        stats = db.get_stats()
        self.assertIn("total_indexed", stats)

        # Query via engine and verify usage boost improves score
        res = self.engine.search("Terminal")
        self.assertGreaterEqual(len(res), 1)
        top = res[0]
        self.assertEqual(top["id"], item_id)
        # Score must be greater than standard 800-1000 due to usage boost (+25 * 3 + 50 recency)
        self.assertGreater(top["score"], 800)

    def test_sensitive_file_and_credential_exclusion(self):
        file_provider = FileProvider()

        # Sensitive credential files must NEVER be indexed
        self.assertFalse(file_provider.is_safe_path("/home/user/.ssh/id_rsa"))
        self.assertFalse(file_provider.is_safe_path("/home/user/.ssh/id_ed25519"))
        self.assertFalse(file_provider.is_safe_path("/home/user/project/.env"))
        self.assertFalse(file_provider.is_safe_path("/home/user/project/.env.local"))
        self.assertFalse(file_provider.is_safe_path("/home/user/certs/private.key"))
        self.assertFalse(file_provider.is_safe_path("/home/user/certs/cert.pem"))
        self.assertFalse(file_provider.is_safe_path("/home/user/project/node_modules/index.js"))
        self.assertFalse(file_provider.is_safe_path("/home/user/project/target/debug/app"))

        # Safe files must be allowed
        self.assertTrue(file_provider.is_safe_path("d:/My own os/Cargo.toml"))
        self.assertTrue(file_provider.is_safe_path("d:/My own os/README.md"))
        self.assertTrue(file_provider.is_safe_path("d:/My own os/src/main.rs"))

    def test_command_safety_and_destructive_detection(self):
        cmd_provider = CommandProvider()

        # Destructive commands must be flagged
        self.assertTrue(cmd_provider.is_destructive("rm -rf /tmp/test"))
        self.assertTrue(cmd_provider.is_destructive("rm -f file.txt"))
        self.assertTrue(cmd_provider.is_destructive("dd if=/dev/zero of=/dev/sda"))
        self.assertTrue(cmd_provider.is_destructive("mkfs.ext4 /dev/nvme0n1p2"))
        self.assertTrue(cmd_provider.is_destructive("shutdown -h now"))
        self.assertTrue(cmd_provider.is_destructive("reboot"))
        self.assertTrue(cmd_provider.is_destructive("kill -9 1234"))
        self.assertTrue(cmd_provider.is_destructive("systemctl stop docker.service"))

        # Safe commands must not be flagged
        self.assertFalse(cmd_provider.is_destructive("cargo build"))
        self.assertFalse(cmd_provider.is_destructive("cargo test"))
        self.assertFalse(cmd_provider.is_destructive("git status"))
        self.assertFalse(cmd_provider.is_destructive("podman ps"))
        self.assertFalse(cmd_provider.is_destructive("uname -a"))

        # Test command search with destructive warning
        res = cmd_provider.search("> rm -rf /tmp/scratch")
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0].actions[0]["destructive"])
        self.assertIn("Confirm execution", res[0].actions[0]["warning"])

    def test_spotlight_bridge_and_confirmation(self):
        bridge = SpotlightBridge()
        json_results = bridge.query("Terminal", "All")
        results = json.loads(json_results)
        self.assertGreaterEqual(len(results), 1)

        # Test safe action execution
        safe_item = json.dumps({"id": "app:terminal", "title": "Terminal", "actions": [{"id": "open", "destructive": False}]})
        exec_res = json.loads(bridge.executeAction("open", safe_item))
        self.assertEqual(exec_res["status"], "executed")

        # Test destructive action confirmation requirement
        dest_item = json.dumps({"id": "sys:shutdown", "title": "Shut Down", "actions": [{"id": "shutdown", "destructive": True, "warning": "Will power off"}]})
        dest_res = json.loads(bridge.executeAction("shutdown", dest_item))
        self.assertEqual(dest_res["status"], "confirmation_required")
        self.assertIn("Will power off", dest_res["warning"])

    def test_shortcut_conflict_detection(self):
        conflict = self.engine.check_shortcut_conflict("Meta+Space")
        self.assertIn("shortcut", conflict)
        self.assertIn("has_conflict", conflict)
        self.assertIn("recommended_alternatives", conflict)
        self.assertIn("Alt+Space", conflict["recommended_alternatives"])

    def test_spotlight_qml_overlay_compiles_and_instantiates(self):
        engine = QQmlApplicationEngine()
        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        spotlight_qml = os.path.join(base_dir, "src", "spotlight", "qml")
        engine.addImportPath(ds_qml)
        engine.addImportPath(spotlight_qml)

        overlay_file = os.path.join(spotlight_qml, "NexusSpotlightOverlay.qml")
        self.assertTrue(os.path.isfile(overlay_file))

        component = QQmlComponent(engine, QUrl.fromLocalFile(overlay_file))
        if component.isError():
            errors = [e.toString() for e in component.errors()]
            self.fail(f"NexusSpotlightOverlay.qml failed to compile: {errors}")

        overlay = component.create()
        self.assertIsNotNone(overlay)

        # Test properties
        overlay.setProperty("openState", True)
        self.assertTrue(overlay.property("openState"))
        overlay.setProperty("activeCategory", "Applications")
        self.assertEqual(overlay.property("activeCategory"), "Applications")

if __name__ == "__main__":
    unittest.main()
