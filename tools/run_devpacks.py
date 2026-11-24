#!/usr/bin/env python3
"""
NEXUS OS — Developer Packs Standalone Runner (`tools/run_devpacks.py`)
Interactive one-click developer environment installer and package suite manager.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.devpacks.devpack_bridge import DevPackBridge
from src.devpacks.devpack_engine import DevPackEngine


def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Developer Packs")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("2026.1")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    devpacks_qml = os.path.join(base_dir, "src", "devpacks", "qml")

    engine = DevPackEngine()
    bridge = DevPackBridge(engine)

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(devpacks_qml)
    view.rootContext().setContextProperty("devpackBridge", bridge)

    qml_file = os.path.join(devpacks_qml, "NexusDevPacksView.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Missing DevPacks QML at {qml_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Developer Packs Installer")
    view.resize(1200, 780)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — Developer Packs Installer Running                   ")
    print(" Available Packs: 15 (Full-Stack, AI/ML, Vibe Coder, Robotics...)")
    print(" Deduplicated Multi-Pack Resolution Active                      ")
    print(" Close the window to exit.                                       ")
    print("=================================================================")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
