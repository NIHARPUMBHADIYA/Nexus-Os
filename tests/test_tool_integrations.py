"""
NEXUS OS — Modern AI Coding Tools Integration Test Suite
Verifies:
1. Catalog coverage of all 15 requested tools and licensing rules
2. Tool availability and configuration detection
3. Automatic safety backups (.bak.<timestamp>) and restoration
4. AI Profile injection across Zed, Continue, Aider, Cursor, and VS Code
5. Desktop shortcut (.desktop) generation and uninstallation workflows
6. QML Component compilation and reactive bridge binding
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

from src.integrations.tool_catalog import ToolCatalog
from src.integrations.tool_detector import ToolDetector
from src.integrations.config_adapter import ConfigAdapter
from src.integrations.launch_manager import LaunchManager
from src.integrations.integrations_bridge import ToolsIntegrationBridge

class TestToolIntegrations(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="nexus_tools_test_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_catalog_completeness(self):
        """Verify all 15 required tools exist in catalog with accurate metadata."""
        expected_tools = [
            "antigravity",
            "vscode",
            "vscodium",
            "cursor",
            "windsurf",
            "zed",
            "claude_code",
            "codex_cli",
            "gemini_cli",
            "opencode",
            "aider",
            "github_copilot",
            "cline",
            "roo_code",
            "continue"
        ]

        catalog = ToolCatalog()
        tools = catalog.TOOLS

        self.assertEqual(len(tools), 15)
        for t_id in expected_tools:
            self.assertIn(t_id, tools, f"Missing tool: {t_id}")
            t_data = tools[t_id]
            self.assertIn("name", t_data)
            self.assertIn("category", t_data)
            self.assertIn("licensing", t_data)
            self.assertIn("can_redistribute", t_data)
            self.assertIn("linux_compatibility", t_data)
            self.assertIn("install_methods", t_data)
            self.assertGreater(len(t_data["install_methods"]), 0)

        # Verify licensing accuracy: Proprietary vs FLOSS
        self.assertFalse(tools["antigravity"]["can_redistribute"])
        self.assertFalse(tools["cursor"]["can_redistribute"])
        self.assertTrue(tools["vscodium"]["can_redistribute"])
        self.assertTrue(tools["zed"]["can_redistribute"])
        self.assertTrue(tools["aider"]["can_redistribute"])

    def test_tool_detector_scans_without_fake_data(self):
        """Verify detector inspects real system state without faking installations."""
        detector = ToolDetector()
        results = detector.scan_all_tools()
        self.assertEqual(len(results), 15)

        for res in results:
            self.assertIn("installed", res)
            self.assertIn("version", res)
            self.assertIn("config_detected", res)
            self.assertIn("ai_endpoint_configured", res)
            self.assertIsInstance(res["installed"], bool)
            self.assertIsInstance(res["config_detected"], bool)

    def test_safe_config_backup_and_restore(self):
        """Verify timestamped backup creation before overwrite and restoration."""
        detector = ToolDetector()
        adapter = ConfigAdapter(detector)

        dummy_config = os.path.join(self.test_dir, "settings.json")
        original_content = '{"editor.fontSize": 14, "customKey": "keepMeSafe"}'

        with open(dummy_config, "w", encoding="utf-8") as f:
            f.write(original_content)

        # 1. Create backup
        backup_path = adapter.create_backup(dummy_config)
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.isfile(backup_path))
        self.assertIn(".bak.", backup_path)

        with open(backup_path, "r", encoding="utf-8") as f:
            backup_content = f.read()
        self.assertEqual(backup_content, original_content)

        # 2. List backups
        backups = adapter.list_backups(dummy_config)
        self.assertIn(backup_path, backups)

        # 3. Simulate destructive overwrite
        with open(dummy_config, "w", encoding="utf-8") as f:
            f.write('{"corrupted": true}')

        # 4. Restore backup
        restored = adapter.restore_backup(backup_path, dummy_config)
        self.assertTrue(restored)

        with open(dummy_config, "r", encoding="utf-8") as f:
            current_content = f.read()
        self.assertEqual(current_content, original_content)

    def test_ai_profiles_and_multi_format_injection(self):
        """Verify AI endpoint configuration across Zed, Continue, Aider, and Cursor formats."""
        detector = ToolDetector()
        adapter = ConfigAdapter(detector)

        profiles = adapter.get_profiles()
        self.assertEqual(len(profiles), 5)
        profile_ids = [p["id"] for p in profiles]
        self.assertIn("local_coding", profile_ids)
        self.assertIn("free_cloud", profile_ids)
        self.assertIn("premium_cloud", profile_ids)
        self.assertIn("reasoning", profile_ids)
        self.assertIn("fast_coding", profile_ids)

        # 1. Test Zed Settings Injector
        zed_cfg = os.path.join(self.test_dir, "zed_settings.json")
        adapter._configure_zed(zed_cfg, adapter.PROFILES["local_coding"])
        with open(zed_cfg, "r", encoding="utf-8") as f:
            zed_data = json.load(f)
        self.assertEqual(zed_data["assistant"]["default_model"]["model"], "nexus:default")
        self.assertEqual(zed_data["language_models"]["openai"]["api_url"], "http://localhost:11430/v1")

        # 2. Test Continue Config Injector
        cont_cfg = os.path.join(self.test_dir, "continue_config.json")
        adapter._configure_continue(cont_cfg, adapter.PROFILES["free_cloud"])
        with open(cont_cfg, "r", encoding="utf-8") as f:
            cont_data = json.load(f)
        self.assertEqual(cont_data["models"][0]["model"], "llama-3.3-70b-versatile")
        self.assertEqual(cont_data["models"][0]["apiBase"], "http://localhost:11430/v1")

        # 3. Test Aider YAML Injector
        aider_cfg = os.path.join(self.test_dir, ".aider.conf.yml")
        adapter._configure_aider(aider_cfg, adapter.PROFILES["reasoning"])
        with open(aider_cfg, "r", encoding="utf-8") as f:
            aider_text = f.read()
        self.assertIn("openai-api-base: http://localhost:11430/v1", aider_text)
        self.assertIn("model: openai/deepseek-r1:8b", aider_text)

        # 4. Test Cursor Injector
        cursor_cfg = os.path.join(self.test_dir, "cursor_settings.json")
        adapter._configure_cursor(cursor_cfg, adapter.PROFILES["fast_coding"])
        with open(cursor_cfg, "r", encoding="utf-8") as f:
            cursor_data = json.load(f)
        self.assertEqual(cursor_data["cursor.general.customBaseUrl"], "http://localhost:11430/v1")
        self.assertEqual(cursor_data["cursor.general.modelName"], "nexus:fast")

    def test_launch_manager_and_desktop_shortcuts(self):
        """Verify FreeDesktop .desktop generation and uninstallation workflows."""
        detector = ToolDetector()
        launcher = LaunchManager(detector)

        # Desktop Shortcut Generation
        shortcut_res = launcher.generate_desktop_shortcut("zed", dest_dir=self.test_dir)
        self.assertTrue(shortcut_res["success"])
        shortcut_path = shortcut_res["shortcut_path"]
        self.assertTrue(os.path.isfile(shortcut_path))

        with open(shortcut_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Name=Zed Editor", content)
        self.assertIn("Exec=zed %F", content)
        self.assertIn("Categories=Development;IDE;Programming;", content)

        # Uninstall Info
        u_info = launcher.get_uninstall_info("vscode")
        self.assertIn("uninstall_command", u_info)
        self.assertIn("remove", u_info["uninstall_command"])

    def test_qml_view_compilation(self):
        """Verify QML compilation of NexusToolsIntegrationView.qml with bridge attached."""
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QGuiApplication
        from PyQt6.QtQuick import QQuickView

        app = QGuiApplication.instance() or QGuiApplication(sys.argv)
        view = QQuickView()

        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        tools_qml = os.path.join(base_dir, "src", "integrations", "qml")

        view.engine().addImportPath(ds_qml)
        view.engine().addImportPath(tools_qml)

        bridge = ToolsIntegrationBridge()
        view.rootContext().setContextProperty("toolsBridge", bridge)

        qml_path = os.path.join(tools_qml, "NexusToolsIntegrationView.qml")
        view.setSource(QUrl.fromLocalFile(qml_path))

        status = view.status()
        self.assertEqual(
            status,
            QQuickView.Status.Ready,
            f"NexusToolsIntegrationView.qml failed compilation with status {status}"
        )

if __name__ == "__main__":
    unittest.main()
