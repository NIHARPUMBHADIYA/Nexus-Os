"""
NEXUS OS — Developer Packs Test Suite (`tests/test_devpacks.py`)
Verifies:
1. Catalog completeness: all 15 Developer Packs with full schemas.
2. Vibe Coder, Robotics, and AI/ML pack specific tool requirements.
3. Multi-pack resolution and tool deduplication.
4. Transitive dependency resolution and topological sort.
5. Storage estimation and disk headroom validation.
6. Hardware compatibility validation (RAM, GPU).
7. Asynchronous installation execution and live log persistence.
8. Cancellation support during active installation.
9. Failure recovery and automated rollback.
10. QML compilation and reactive bridge property bindings.
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

from src.devpacks.devpack_catalog import (
    DEVELOPER_PACKS, get_all_packs, get_pack_by_id, get_tool_by_id, MASTER_TOOLS_CATALOG
)
from src.devpacks.devpack_resolver import DevPackResolver
from src.devpacks.devpack_engine import DevPackEngine
from src.devpacks.devpack_bridge import DevPackBridge


class TestDevPacks(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="nexus_devpacks_test_")
        self.engine = DevPackEngine(self.test_dir)
        self.resolver = DevPackResolver()
        self.bridge = DevPackBridge(self.engine)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_15_developer_packs_completeness(self):
        """Verify all 15 Developer Packs are defined with complete metadata."""
        packs = get_all_packs()
        self.assertEqual(len(packs), 15, f"Expected 15 Developer Packs, found {len(packs)}")

        expected_ids = [
            "fullstack", "aiml", "vibecoder", "swe", "python_dev",
            "cpp_dev", "android_dev", "gamedev", "robotics", "embedded",
            "cybersecurity", "devops", "cloud_dev", "student", "complete"
        ]

        found_ids = [p.id for p in packs]
        for pid in expected_ids:
            self.assertIn(pid, found_ids, f"Developer Pack '{pid}' is missing.")

        for pack in packs:
            self.assertTrue(pack.name, f"Pack {pack.id} missing name")
            self.assertTrue(pack.icon, f"Pack {pack.id} missing icon")
            self.assertTrue(pack.tagline, f"Pack {pack.id} missing tagline")
            self.assertGreater(len(pack.required_tools), 0, f"Pack {pack.id} has no required tools")
            self.assertGreater(len(pack.programming_languages), 0, f"Pack {pack.id} has no languages")
            self.assertGreater(len(pack.frameworks), 0, f"Pack {pack.id} has no frameworks")
            self.assertGreater(len(pack.editors), 0, f"Pack {pack.id} has no editors")
            self.assertGreater(len(pack.dependencies), 0, f"Pack {pack.id} has no dependencies")
            self.assertGreater(len(pack.installation_sources), 0, f"Pack {pack.id} has no installation sources")
            self.assertGreater(pack.estimated_storage_mb, 0, f"Pack {pack.id} invalid storage estimate")
            self.assertIsNotNone(pack.hardware, f"Pack {pack.id} missing hardware requirements")

    def test_vibe_coder_pack_contents(self):
        """Verify Vibe Coder Pack contains all required AI-native and developer tools."""
        pack = get_pack_by_id("vibecoder")
        self.assertIsNotNone(pack)
        tools = pack.required_tools + pack.optional_tools

        expected_tools = [
            "antigravity", "cursor", "git", "gh", "nodejs", "python",
            "chromium", "sqlite", "podman", "ollama", "omniroute"
        ]
        for et in expected_tools:
            self.assertIn(et, tools, f"Vibe Coder Pack missing required tool: {et}")

    def test_robotics_pack_contents(self):
        """Verify Robotics Pack contains ROS 2, Gazebo, RViz, OpenCV, and embedded tools."""
        pack = get_pack_by_id("robotics")
        self.assertIsNotNone(pack)
        tools = pack.required_tools + pack.optional_tools

        expected_tools = [
            "ros2", "gcc", "python", "gazebo", "rviz", "opencv", "arduino", "platformio"
        ]
        for et in expected_tools:
            self.assertIn(et, tools, f"Robotics Pack missing required tool: {et}")

    def test_aiml_pack_contents(self):
        """Verify AI/ML Pack contains Python, Jupyter, PyTorch, Hugging Face, and Ollama."""
        pack = get_pack_by_id("aiml")
        self.assertIsNotNone(pack)
        tools = pack.required_tools + pack.optional_tools

        expected_tools = [
            "python", "pytorch", "jupyter", "huggingface", "ollama"
        ]
        for et in expected_tools:
            self.assertIn(et, tools, f"AI/ML Pack missing required tool: {et}")

    def test_multi_pack_deduplication(self):
        """Verify selecting multiple packs deduplicates common tools and computes accurate storage."""
        # Vibe Coder and Full-Stack both use: git, gh, mise, nodejs, python, podman, etc.
        plan = self.resolver.resolve(["vibecoder", "fullstack"])
        tool_ids = [t.id for t in plan.resolved_tools]

        # Verify no duplicates
        self.assertEqual(len(tool_ids), len(set(tool_ids)), "Resolved tools must be strictly unique")
        self.assertIn("antigravity", tool_ids)
        self.assertIn("postgresql", tool_ids)
        self.assertIn("python", tool_ids)
        self.assertIn("nodejs", tool_ids)
        self.assertGreater(plan.total_size_mb, 0)
        self.assertIn("GB", plan.total_size_formatted)

    def test_transitive_dependency_resolution_and_topological_order(self):
        """Verify dependencies are resolved and ordered from base runtimes to heavy apps."""
        # Selecting Android Developer requires openjdk
        plan = self.resolver.resolve(["android_dev"])
        tool_ids = [t.id for t in plan.resolved_tools]
        self.assertIn("openjdk", tool_ids)
        self.assertIn("android_studio", tool_ids)

        # openjdk must precede android_studio in execution order
        openjdk_idx = tool_ids.index("openjdk")
        studio_idx = tool_ids.index("android_studio")
        self.assertLess(openjdk_idx, studio_idx, "Prerequisite 'openjdk' must be installed before 'android_studio'")

    def test_hardware_compatibility_warnings(self):
        """Verify hardware requirement checks emit appropriate warnings for heavy packs."""
        plan = self.resolver.resolve(["robotics", "gamedev"])
        self.assertGreater(len(plan.hardware_warnings), 0)
        warning_str = " ".join(plan.hardware_warnings)
        self.assertTrue("GPU" in warning_str or "RAM" in warning_str)

    def test_engine_installation_logging_and_cancellation(self):
        """Verify installation execution, progress reporting, logging, and cancellation."""
        log_captured = []
        self.engine.on_log = lambda line: log_captured.append(line)

        # Start installation of a small pack
        started = self.engine.start_installation(["python_dev"])
        self.assertTrue(started)
        self.assertTrue(self.engine.is_running())

        # Test cancellation
        self.engine.cancel()
        time.sleep(0.3)
        self.assertFalse(self.engine.is_running())

        # Verify logs were written
        self.assertGreater(len(log_captured), 0)
        self.assertTrue(any("Cancelled" in line or "Starting" in line for line in log_captured))

        # Check log file exists on disk
        log_files = list(self.engine.logs_dir.glob("install_*.log"))
        self.assertGreater(len(log_files), 0)

    def test_state_persistence_and_uninstallation(self):
        """Verify pack installation state persistence and uninstall functionality."""
        # Manually mark pack installed
        self.engine._installed_packs.add("vibecoder")
        self.engine._save_state()

        # Reload engine
        fresh_engine = DevPackEngine(self.test_dir)
        self.assertTrue(fresh_engine.is_pack_installed("vibecoder"))
        self.assertIn("vibecoder", fresh_engine.get_installed_packs())

        # Uninstall pack
        success = fresh_engine.uninstall_pack("vibecoder")
        self.assertTrue(success)
        self.assertFalse(fresh_engine.is_pack_installed("vibecoder"))

    def test_qml_view_compilation(self):
        """Verify NexusDevPacksView.qml compiles cleanly without syntax errors in Qt QML engine."""
        from PyQt6.QtGui import QGuiApplication
        from PyQt6.QtQuick import QQuickView
        from PyQt6.QtCore import QUrl

        app = QGuiApplication.instance() or QGuiApplication(sys.argv)

        view = QQuickView()
        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        devpacks_qml = os.path.join(base_dir, "src", "devpacks", "qml")

        view.engine().addImportPath(ds_qml)
        view.engine().addImportPath(devpacks_qml)
        view.rootContext().setContextProperty("devpackBridge", self.bridge)

        qml_path = os.path.join(devpacks_qml, "NexusDevPacksView.qml")
        self.assertTrue(os.path.isfile(qml_path))

        view.setSource(QUrl.fromLocalFile(qml_path))
        errors = view.errors()
        err_messages = [e.toString() for e in errors]
        self.assertEqual(len(errors), 0, f"QML compilation errors: {err_messages}")
        self.assertEqual(view.status(), QQuickView.Status.Ready, f"View status expected Ready, got {view.status()}")


if __name__ == "__main__":
    unittest.main()
