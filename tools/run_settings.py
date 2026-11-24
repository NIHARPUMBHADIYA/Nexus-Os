#!/usr/bin/env python3
"""
NEXUS OS — Settings Application Standalone Runner
Launches the full 21-category settings interface with live search, storage analysis,
shortcut conflict editor, and system daemon integration.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.settings.settings_bridge import SettingsBridge


def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Settings")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("2026.1")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    settings_qml = os.path.join(base_dir, "src", "settings", "qml")

    bridge = SettingsBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(settings_qml)
    view.rootContext().setContextProperty("settingsBridge", bridge)

    qml_file = os.path.join(settings_qml, "NexusSettingsView.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Missing Settings QML at {qml_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — System Settings")
    view.resize(1180, 780)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — Settings Application Running                        ")
    print(" Categories: 21 (Appearance, Desktop, Dock, Keyboard, Spotlight, ")
    print("                 Display, Network, Bluetooth, Sound, Storage... )")
    print(" Zero-Telemetry: Strictly Enforced                              ")
    print(" Close the window to exit.                                       ")
    print("=================================================================")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
