#!/usr/bin/env python3
"""
NEXUS OS - Desktop Shell Executable Launcher (PyQt6 / QML)
Runs the complete NEXUS OS desktop environment with window manager, dock,
top panel, application launcher, workspaces, and system controls.
"""

import sys
import os

# Enforce clean, custom styled controls
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS OS Desktop Shell")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    shell_qml = os.path.join(base_dir, "src", "desktop", "shell")
    spotlight_qml = os.path.join(base_dir, "src", "spotlight", "qml")

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(shell_qml)
    view.engine().addImportPath(spotlight_qml)

    desktop_qml = os.path.join(shell_qml, "NexusDesktop.qml")
    if not os.path.isfile(desktop_qml):
        print(f"Error: Missing desktop QML file at {desktop_qml}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(desktop_qml))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Developer-First AI-Native Desktop Shell")
    view.resize(1280, 800)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — Desktop Shell Running (PyQt6/Wayland Native Preview) ")
    print(" Active Modules: WindowManager, Floating Dock, Top Panel,        ")
    print("                 Application Launcher, Notifications, Workspaces ")
    print(" Keyboard Shortcuts:                                             ")
    print("   Meta+Space : Application Launcher                             ")
    print("   Meta+T     : Terminal                                         ")
    print("   Meta+D     : Developer Hub                                    ")
    print("   Meta+S     : System Settings                                  ")
    print("   Ctrl+1..4  : Switch Workspace                                 ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
