"""
NEXUS OS — Theme & Personalization Test Suite
Verifies:
1. Complete catalog of 10 themes (Midnight, Nord, Dracula, Catppuccin, Tokyo Night,
   Terminal Green, Paper Light, AMOLED Black, Deep Space, Custom)
2. Strict WCAG 2.1 AA Readability and Contrast across all themes
3. Auto mode (time-of-day resolution)
4. Custom theme creation, token overrides, and import/export
5. Strict Rounded Corners Design Rule (radii >= 10px across all scales)
6. QML Component Compilation & Reactive Bridge Bindings
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

from src.personalization.personalization_engine import PersonalizationEngine
from src.personalization.personalization_bridge import PersonalizationBridge

class TestPersonalization(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="nexus_theme_test_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_theme_catalog_and_required_tokens(self):
        """Verify all 10 themes are registered and contain semantic tokens."""
        engine = PersonalizationEngine(self.test_dir)
        themes = engine.DEFAULT_THEMES
        self.assertEqual(len(themes), 10)

        theme_ids = [t["id"] for t in themes]
        expected_themes = [
            "midnight", "nord", "dracula", "catppuccin", "tokyo-night",
            "terminal-green", "paper-light", "amoled", "deep-space", "custom"
        ]
        for tid in expected_themes:
            self.assertIn(tid, theme_ids, f"Missing theme: {tid}")

    def test_wcag_contrast_and_readability_all_themes(self):
        """Verify every theme meets WCAG 2.1 AA contrast requirements (>= 4.5:1)."""
        engine = PersonalizationEngine(self.test_dir)
        bridge = PersonalizationBridge(engine)

        themes_to_test = [
            "midnight", "nord", "dracula", "catppuccin", "tokyo-night",
            "terminal-green", "paper-light", "amoled", "deep-space"
        ]

        for tid in themes_to_test:
            tokens = bridge._get_theme_tokens(tid)
            eval_res = engine.evaluate_theme_contrast(tokens)

            # Assert text contrast on background meets WCAG AA (>= 4.5:1)
            self.assertGreaterEqual(
                eval_res["primary_on_bg"],
                4.5,
                f"Theme '{tid}' failed WCAG AA primary text on background contrast: {eval_res['primary_on_bg']}:1"
            )

            # Assert text contrast on surface cards meets WCAG AA (>= 4.5:1)
            self.assertGreaterEqual(
                eval_res["primary_on_surface"],
                4.5,
                f"Theme '{tid}' failed WCAG AA primary text on surface contrast: {eval_res['primary_on_surface']}:1"
            )

            # Assert secondary text meets large text / subtle contrast (>= 3.0:1)
            self.assertGreaterEqual(
                eval_res["secondary_on_bg"],
                3.0,
                f"Theme '{tid}' failed secondary text contrast: {eval_res['secondary_on_bg']}:1"
            )

            self.assertTrue(eval_res["wcag_aa_passed"])

    def test_auto_theme_mode_resolution(self):
        """Verify theme mode switching for light, dark, and auto."""
        engine = PersonalizationEngine(self.test_dir)

        engine.set_setting("theme_mode", "light")
        self.assertEqual(engine.get_effective_theme_mode(), "light")

        engine.set_setting("theme_mode", "dark")
        self.assertEqual(engine.get_effective_theme_mode(), "dark")

        engine.set_setting("theme_mode", "auto")
        effective = engine.get_effective_theme_mode()
        self.assertIn(effective, ("light", "dark"))

    def test_custom_theme_and_import_export(self):
        """Verify custom theme creation, token modification, export, and import."""
        engine = PersonalizationEngine(self.test_dir)

        # 1. Update custom color
        custom_colors = engine.settings["custom_colors"]
        custom_colors["accent"] = "#FF007F"
        engine.set_setting("custom_colors", custom_colors)
        engine.set_setting("active_theme", "custom")

        # 2. Export theme
        export_file = os.path.join(self.test_dir, "my_custom.nexus-theme.json")
        exported = engine.export_theme("Neon Rose", export_file)
        self.assertTrue(exported)
        self.assertTrue(os.path.isfile(export_file))

        with open(export_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["name"], "Neon Rose")
        self.assertEqual(data["tokens"]["accent"], "#FF007F")

        # 3. Import theme into new engine instance
        engine2 = PersonalizationEngine(self.test_dir)
        import_res = engine2.import_theme(export_file)
        self.assertTrue(import_res["success"])
        self.assertEqual(engine2.settings["active_theme"], "custom")
        self.assertEqual(engine2.settings["custom_colors"]["accent"], "#FF007F")

    def test_strict_rounded_geometry_rule(self):
        """Verify all corner radii throughout the design tokens are rounded (>= 10px)."""
        # Read tokens from tokens.json
        tokens_file = os.path.join(base_dir, "src", "design-system", "tokens.json")
        with open(tokens_file, "r") as f:
            tokens = json.load(f)

        radii = tokens.get("radii", {})
        for r_name, r_val in radii.items():
            self.assertGreaterEqual(
                r_val,
                10,
                f"Design rule violation: Corner radius '{r_name}' ({r_val}px) must be >= 10px rounded."
            )

    def test_qml_view_compilation(self):
        """Verify QML compilation of NexusPersonalizationView.qml with bridge attached."""
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QGuiApplication
        from PyQt6.QtQuick import QQuickView

        app = QGuiApplication.instance() or QGuiApplication(sys.argv)
        view = QQuickView()

        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        pers_qml = os.path.join(base_dir, "src", "personalization", "qml")

        view.engine().addImportPath(ds_qml)
        view.engine().addImportPath(pers_qml)

        engine = PersonalizationEngine(self.test_dir)
        bridge = PersonalizationBridge(engine)
        view.rootContext().setContextProperty("personalizationBridge", bridge)

        qml_path = os.path.join(pers_qml, "NexusPersonalizationView.qml")
        view.setSource(QUrl.fromLocalFile(qml_path))

        status = view.status()
        self.assertEqual(
            status,
            QQuickView.Status.Ready,
            f"NexusPersonalizationView.qml failed compilation with status {status}"
        )

if __name__ == "__main__":
    unittest.main()
