#!/usr/bin/env python3
"""
NEXUS OS — Developer Hub Test Suite
Validates project templates, metadata creation, session restoration,
external IDE command generation, and QML component loading.
"""

import unittest
import os
import sys
import tempfile
import json
import shutil

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, QQmlComponent

from src.devhub.hub_core import DeveloperHubCore, DEFAULT_TEMPLATES
from src.devhub.hub_bridge import DeveloperHubBridge

EXPECTED_TEMPLATES = [
    "python", "c_cpp", "react", "nextjs", "node_api", "typescript",
    "flask", "fastapi", "django", "java", "rust", "go",
    "flutter", "android", "arduino", "ros2", "ai_ml", "empty"
]

DEVHUB_QML_COMPONENTS = [
    "NexusDevHubView.qml",
    "ProjectDashboard.qml",
    "ProjectCreationWizard.qml",
    "ProjectWorkspace.qml"
]

class TestDeveloperHub(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="nexus_devhub_test_")
        cls.hub = DeveloperHubCore(cls.temp_dir)

        if not QGuiApplication.instance():
            cls.app = QGuiApplication(sys.argv)
        else:
            cls.app = QGuiApplication.instance()

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(cls.temp_dir):
            try:
                shutil.rmtree(cls.temp_dir)
            except Exception:
                pass

    def test_all_eighteen_templates_exist(self):
        for t_key in EXPECTED_TEMPLATES:
            self.assertIn(t_key, DEFAULT_TEMPLATES, f"Template missing: {t_key}")
            tpl = DEFAULT_TEMPLATES[t_key]
            self.assertIn("name", tpl)
            self.assertIn("category", tpl)
            self.assertIn("language", tpl)
            self.assertIn("files", tpl)
            self.assertGreater(len(tpl["files"]), 0, f"Template {t_key} has no files")

    def test_project_creation_and_metadata(self):
        proj_dir = os.path.join(self.temp_dir, "workspaces")
        os.makedirs(proj_dir, exist_ok=True)

        res = self.hub.create_project(
            template_key="fastapi",
            name="test-fastapi-service",
            location_dir=proj_dir,
            enable_git=True,
            enable_ai=True,
            dev_env="Podman (Rootless Container)"
        )

        self.assertEqual(res["name"], "test-fastapi-service")
        target_path = res["path"]
        self.assertTrue(os.path.isdir(target_path))

        # Verify template files were created
        self.assertTrue(os.path.isfile(os.path.join(target_path, "main.py")))
        self.assertTrue(os.path.isfile(os.path.join(target_path, "requirements.txt")))

        # Verify .nexus/project.json metadata
        meta_file = os.path.join(target_path, ".nexus", "project.json")
        self.assertTrue(os.path.isfile(meta_file))
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.assertEqual(meta["template"], "fastapi")
        self.assertTrue(meta["ai_integration"]["enabled"])
        self.assertEqual(meta["dev_env"], "Podman (Rootless Container)")

    def test_session_saving_and_restoration(self):
        proj_path = os.path.join(self.temp_dir, "workspaces", "session-test")
        os.makedirs(proj_path, exist_ok=True)

        session_payload = {
            "opened_files": ["main.py", "test.py"],
            "active_file": "main.py",
            "terminal_history": ["python main.py", "pytest"],
            "running_services": [8000],
            "layout": "split_right"
        }

        self.hub.save_session(proj_path, session_payload)
        restored = self.hub.load_session(proj_path)

        self.assertEqual(restored["active_file"], "main.py")
        self.assertEqual(len(restored["opened_files"]), 2)
        self.assertEqual(restored["layout"], "split_right")

    def test_external_ide_integration_mapping(self):
        path = "/tmp/test"
        res_cursor = self.hub.launch_external_ide("cursor", path)
        self.assertIn("status", res_cursor)
        res_code = self.hub.launch_external_ide("vscode", path)
        self.assertIn("status", res_code)
        res_zed = self.hub.launch_external_ide("zed", path)
        self.assertIn("status", res_zed)

    def test_qml_devhub_components_compile_and_load(self):
        engine = QQmlApplicationEngine()
        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        devhub_qml = os.path.join(base_dir, "src", "devhub", "qml")

        engine.addImportPath(ds_qml)
        engine.addImportPath(devhub_qml)

        for comp_name in DEVHUB_QML_COMPONENTS:
            file_path = os.path.join(devhub_qml, comp_name)
            self.assertTrue(os.path.isfile(file_path), f"File missing: {file_path}")

            component = QQmlComponent(engine, QUrl.fromLocalFile(file_path))
            if component.isError():
                errors = [e.toString() for e in component.errors()]
                self.fail(f"DevHub component {comp_name} failed to compile: {errors}")

            obj = component.create()
            self.assertIsNotNone(obj, f"Component {comp_name} instantiated as None")

if __name__ == "__main__":
    unittest.main()
