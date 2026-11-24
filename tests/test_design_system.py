#!/usr/bin/env python3
"""
NEXUS OS - Design System Test Suite
Tests tokens, theme schemas, color validations, and QML component instantiation.
"""

import unittest
import json
import os
import re
import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView
from PyQt6.QtQml import QQmlApplicationEngine, QQmlComponent

# Ensure headless QGuiApplication for testing
os.environ["QT_QPA_PLATFORM"] = "offscreen"

HEX_REGEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

REQUIRED_COLOR_KEYS = [
    "background",
    "secondaryBackground",
    "surface",
    "elevatedSurface",
    "border",
    "primaryText",
    "secondaryText",
    "accent",
    "success",
    "warning",
    "error",
    "info"
]

EXPECTED_THEMES = [
    "midnight",
    "nord",
    "dracula",
    "catppuccin",
    "tokyo-night",
    "terminal-green",
    "paper-light",
    "amoled",
    "deep-space"
]

QML_COMPONENTS = [
    "NexusButton.qml",
    "NexusIconButton.qml",
    "NexusInput.qml",
    "NexusSearchField.qml",
    "NexusCard.qml",
    "NexusDialog.qml",
    "NexusPopover.qml",
    "NexusMenu.qml",
    "NexusTooltip.qml",
    "NexusTabs.qml",
    "NexusToggle.qml",
    "NexusProgress.qml",
    "NexusNotification.qml",
    "NexusDockItem.qml",
    "NexusWindowHeader.qml",
    "NexusSidebar.qml",
    "NexusBadge.qml",
    "NexusShowcase.qml"
]

class TestDesignSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.ds_dir = os.path.join(cls.base_dir, "src", "design-system")
        cls.themes_dir = os.path.join(cls.ds_dir, "themes")
        cls.qml_dir = os.path.join(cls.ds_dir, "qml")

        if not QGuiApplication.instance():
            cls.app = QGuiApplication(sys.argv)
        else:
            cls.app = QGuiApplication.instance()

    def test_tokens_json_structure(self):
        tokens_path = os.path.join(self.ds_dir, "tokens.json")
        self.assertTrue(os.path.isfile(tokens_path), "tokens.json must exist")
        with open(tokens_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("radii", data)
        self.assertEqual(data["radii"]["small"], 10)
        self.assertEqual(data["radii"]["medium"], 14)
        self.assertEqual(data["radii"]["large"], 20)
        self.assertEqual(data["radii"]["xl"], 24)
        self.assertEqual(data["radii"]["xxl"], 28)
        self.assertEqual(data["radii"]["pill"], 9999)

        self.assertIn("spacing", data)
        self.assertIn("typography", data)
        self.assertIn("motion", data)
        self.assertIn("accents", data)

    def test_all_nine_themes_exist(self):
        for theme_id in EXPECTED_THEMES:
            theme_file = os.path.join(self.themes_dir, f"{theme_id}.json")
            self.assertTrue(os.path.isfile(theme_file), f"Theme file missing: {theme_id}.json")

            with open(theme_file, "r", encoding="utf-8") as f:
                theme_data = json.load(f)

            self.assertEqual(theme_data["id"], theme_id)
            self.assertIn("name", theme_data)
            self.assertIn("type", theme_data)
            self.assertIn(theme_data["type"], ["dark", "light"])
            self.assertIn("colors", theme_data)

            for key in REQUIRED_COLOR_KEYS:
                self.assertIn(key, theme_data["colors"], f"Theme {theme_id} missing color token: {key}")
                val = theme_data["colors"][key]
                self.assertTrue(HEX_REGEX.match(val), f"Color {key}={val} in theme {theme_id} is not valid hex")

    def test_qml_showcase_loads_cleanly(self):
        engine = QQmlApplicationEngine()
        engine.addImportPath(self.qml_dir)

        qml_path = os.path.join(self.qml_dir, "NexusShowcase.qml")
        component = QQmlComponent(engine, QUrl.fromLocalFile(qml_path))

        if component.isError():
            errors = [err.toString() for err in component.errors()]
            self.fail(f"Failed to load NexusShowcase.qml: {errors}")

        obj = component.create()
        self.assertIsNotNone(obj, "NexusShowcase instance should not be None")

    def test_individual_components_load(self):
        engine = QQmlApplicationEngine()
        engine.addImportPath(self.qml_dir)

        for comp_name in QML_COMPONENTS:
            qml_path = os.path.join(self.qml_dir, comp_name)
            component = QQmlComponent(engine, QUrl.fromLocalFile(qml_path))
            if component.isError():
                errors = [err.toString() for err in component.errors()]
                self.fail(f"Component {comp_name} failed to load: {errors}")
            obj = component.create()
            self.assertIsNotNone(obj, f"Component {comp_name} instantiated as None")

if __name__ == "__main__":
    unittest.main()
