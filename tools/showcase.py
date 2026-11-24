#!/usr/bin/env python3
"""
NEXUS OS - Design System Showcase Launcher (PyQt6 / QML)
Runs the native desktop preview of all components, themes, and design tokens.
"""

import sys
import os

# Enforce clean, custom styled controls
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtQml import QQmlApplicationEngine

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Design System")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    engine = QQmlApplicationEngine()

    # Add the design system QML directory to import paths
    qml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "design-system", "qml"))
    engine.addImportPath(qml_dir)

    qml_file = os.path.join(qml_dir, "NexusShowcase.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Could not locate QML file at {qml_file}")
        sys.exit(1)

    # Wrap the item in a QuickView or ApplicationWindow if needed
    from PyQt6.QtQuick import QQuickView
    view = QQuickView()
    view.engine().addImportPath(qml_dir)
    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Design System Showcase & Theme Studio")
    view.resize(1200, 800)
    view.show()

    print("==========================================================")
    print(" NEXUS OS — Design System Showcase Running (PyQt6/QML)     ")
    print(" Themes: Midnight, Nord, Dracula, Catppuccin, Tokyo Night, ")
    print("         Terminal Green, Paper Light, AMOLED, Deep Space   ")
    print("==========================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
