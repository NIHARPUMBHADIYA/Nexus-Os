#!/usr/bin/env python3
"""
NEXUS OS — First-Boot Setup & Local Account Creation Executable Launcher
Runs the initial account setup wizard. If setup has already been completed,
exits silently unless --force is specified.
"""

import os
import sys

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.setup.setup_bridge import SetupBridge


def main():
    force = "--force" in sys.argv
    marker = "/var/lib/nexus/setup_done"
    legacy_marker = "/etc/nexus/user_configured"

    if not force and (os.path.exists(marker) or os.path.exists(legacy_marker)):
        print("[NEXUS SETUP] Setup has already been completed. Exiting.")
        return 0

    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS OS Setup")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("2026.1")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    setup_qml = os.path.join(base_dir, "src", "setup")

    bridge = SetupBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(setup_qml)
    view.rootContext().setContextProperty("setupBridge", bridge)
    view.rootContext().setContextProperty("setupWindow", view)

    qml_file = os.path.join(setup_qml, "NexusSetupWizard.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Missing Setup QML at {qml_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Welcome & Account Setup")
    view.resize(680, 640)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — First-Boot Setup & Account Creation Wizard Running   ")
    print(" Complete account setup to proceed to the desktop.               ")
    print("=================================================================")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
