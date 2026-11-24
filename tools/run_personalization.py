#!/usr/bin/env python3
"""
NEXUS OS — Theme and Personalization System Standalone Runner
Inspects, configures, and tests all 10 themes and personalization tokens.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.personalization.personalization_bridge import PersonalizationBridge

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Personalization")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    pers_qml = os.path.join(base_dir, "src", "personalization", "qml")

    bridge = PersonalizationBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(pers_qml)
    view.rootContext().setContextProperty("personalizationBridge", bridge)

    qml_file = os.path.join(pers_qml, "NexusPersonalizationView.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Missing Personalization QML at {qml_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Themes & Personalization")
    view.resize(1140, 740)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — Theme & Personalization System Running               ")
    print(" Themes: 10 (Midnight, Nord, Dracula, Catppuccin, Tokyo Night,   ")
    print("             Terminal Green, Paper Light, AMOLED, Deep Space,    ")
    print("             Custom Theme Editor)                                ")
    print(" WCAG 2.1 AA Contrast Verification: Active                       ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
