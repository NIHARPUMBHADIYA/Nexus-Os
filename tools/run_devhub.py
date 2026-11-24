#!/usr/bin/env python3
"""
NEXUS OS — Developer Hub Standalone Launcher (PyQt6 / QML)
Runs the central project dashboard, creation wizard, and workspace environment.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.devhub.hub_bridge import DeveloperHubBridge

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Developer Hub")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    devhub_qml = os.path.join(base_dir, "src", "devhub", "qml")

    bridge = DeveloperHubBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(devhub_qml)
    view.rootContext().setContextProperty("devHubBridge", bridge)

    hub_file = os.path.join(devhub_qml, "NexusDevHubView.qml")
    if not os.path.isfile(hub_file):
        print(f"Error: Missing DevHub QML at {hub_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(hub_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Developer Hub")
    view.resize(1140, 740)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — Developer Hub Running                                ")
    print(" Templates Supported: 18 (Python, Rust, C++, React, Next.js,     ")
    print("                         ROS 2, AI/ML, Flutter, Android, etc.)   ")
    print(" Modular Panels: File Explorer, Code Editor, Terminal, AI Copilot,")
    print("                 Browser Preview, Git, Logs, Testing, Database   ")
    print(" External IDE Integrations: Cursor, VS Code, Zed                 ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
