#!/usr/bin/env python3
"""
NEXUS OS - Desktop Shell Test Suite
Validates compilation, loading, and runtime state of all desktop shell components,
window manager methods, dock operations, and embedded applications.
"""

import unittest
import os
import sys

# Headless offscreen platform and Basic QtQuickControls style for testing
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, QQmlComponent

SHELL_COMPONENTS = [
    "NexusDesktop.qml",
    "NexusTopPanel.qml",
    "NexusDock.qml",
    "NexusWindow.qml",
    "NexusWindowManager.qml",
    "NexusLauncher.qml",
    "NexusQuickSettings.qml",
    "NexusNotificationCenter.qml",
    "NexusContextMenu.qml",
    "NexusWallpaperPicker.qml"
]

APP_COMPONENTS = [
    "apps/TerminalApp.qml",
    "apps/DevHubApp.qml",
    "apps/AICoreApp.qml",
    "apps/SettingsApp.qml",
    "apps/EditorApp.qml"
]

class TestDesktopShell(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.ds_qml = os.path.join(cls.base_dir, "src", "design-system", "qml")
        cls.shell_qml = os.path.join(cls.base_dir, "src", "desktop", "shell")

        if not QGuiApplication.instance():
            cls.app = QGuiApplication(sys.argv)
        else:
            cls.app = QGuiApplication.instance()

    def test_shell_components_compile_and_load(self):
        engine = QQmlApplicationEngine()
        engine.addImportPath(self.ds_qml)
        engine.addImportPath(self.shell_qml)

        for comp in SHELL_COMPONENTS:
            file_path = os.path.join(self.shell_qml, comp)
            self.assertTrue(os.path.isfile(file_path), f"File missing: {file_path}")

            component = QQmlComponent(engine, QUrl.fromLocalFile(file_path))
            if component.isError():
                errors = [e.toString() for e in component.errors()]
                self.fail(f"Component {comp} failed to compile: {errors}")

            obj = component.create()
            self.assertIsNotNone(obj, f"Component {comp} created None object")

    def test_app_components_compile_and_load(self):
        engine = QQmlApplicationEngine()
        engine.addImportPath(self.ds_qml)
        engine.addImportPath(self.shell_qml)

        for app_comp in APP_COMPONENTS:
            file_path = os.path.join(self.shell_qml, app_comp)
            self.assertTrue(os.path.isfile(file_path), f"File missing: {file_path}")

            component = QQmlComponent(engine, QUrl.fromLocalFile(file_path))
            if component.isError():
                errors = [e.toString() for e in component.errors()]
                self.fail(f"App Component {app_comp} failed to compile: {errors}")

            obj = component.create()
            self.assertIsNotNone(obj, f"App Component {app_comp} created None object")

    def test_window_manager_logic(self):
        engine = QQmlApplicationEngine()
        engine.addImportPath(self.ds_qml)
        engine.addImportPath(self.shell_qml)

        wm_file = os.path.join(self.shell_qml, "NexusWindowManager.qml")
        component = QQmlComponent(engine, QUrl.fromLocalFile(wm_file))
        wm = component.create()
        self.assertIsNotNone(wm)

        # 1. Test opening windows
        win_id_1 = wm.openApp("terminal", "Terminal", "⌨", 600, 400)
        self.assertTrue(win_id_1.startswith("win-"))
        windows_list = wm.property("windows").toVariant()
        self.assertEqual(len(windows_list), 1)
        self.assertEqual(wm.property("activeWindowId"), win_id_1)
        self.assertTrue(wm.isAppRunning("terminal"))
        self.assertFalse(wm.isAppRunning("devhub"))

        # 2. Test opening second window
        win_id_2 = wm.openApp("devhub", "Developer Hub", "📁", 700, 500)
        windows_list = wm.property("windows").toVariant()
        self.assertEqual(len(windows_list), 2)
        self.assertEqual(wm.property("activeWindowId"), win_id_2)

        # 3. Test minimize and restore
        wm.minimizeWindow(win_id_2)
        self.assertEqual(wm.property("activeWindowId"), "")

        wm.restoreWindow(win_id_2)
        self.assertEqual(wm.property("activeWindowId"), win_id_2)

        # 4. Test workspace switching
        self.assertEqual(wm.property("currentWorkspace"), 0)
        wm.switchWorkspace(1)
        self.assertEqual(wm.property("currentWorkspace"), 1)

        # 5. Test notifications
        wm.addNotification("info", "Test Alert", "Verification successful")
        notifs = wm.property("notifications").toVariant()
        self.assertGreaterEqual(len(notifs), 1)

        # 6. Test closing window
        wm.closeWindow(win_id_1)
        windows_list = wm.property("windows").toVariant()
        self.assertEqual(len(windows_list), 1)

if __name__ == "__main__":
    unittest.main()
