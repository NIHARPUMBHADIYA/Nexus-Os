#!/usr/bin/env python3
"""
NEXUS OS — Developer Software Center Standalone Runner
Discovers, installs, updates, and manages developer software packages.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.software_center.software_center_bridge import SoftwareCenterBridge

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Software Center")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    sc_qml = os.path.join(base_dir, "src", "software_center", "qml")

    bridge = SoftwareCenterBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(sc_qml)
    view.rootContext().setContextProperty("softwareCenterBridge", bridge)

    qml_file = os.path.join(sc_qml, "NexusSoftwareCenterView.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Missing Software Center QML at {qml_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Developer Software Center")
    view.resize(1140, 740)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — Developer Software Center Running                    ")
    print(" Categories: 15 (AI, Editors, Languages, Web, Mobile, Databases, ")
    print("                 DevOps, Cloud, Security, Robotics, GameDev)     ")
    print(" Backends: DNF Native RPM, Flatpak Flathub, Mise, OCI Containers ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
