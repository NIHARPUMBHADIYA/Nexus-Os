#!/usr/bin/env python3
"""
NEXUS OS — AI Coding Tools Integrator Standalone Runner
Inspects, launches, and configures 15 modern AI tools with NEXUS AI Core.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.integrations.integrations_bridge import ToolsIntegrationBridge

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Tools Integrator")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    tools_qml = os.path.join(base_dir, "src", "integrations", "qml")

    bridge = ToolsIntegrationBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(tools_qml)
    view.rootContext().setContextProperty("toolsBridge", bridge)

    qml_file = os.path.join(tools_qml, "NexusToolsIntegrationView.qml")
    if not os.path.isfile(qml_file):
        print(f"Error: Missing Tools Integrator QML at {qml_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(qml_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — AI Coding Tools Integrator")
    view.resize(1140, 740)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — AI Coding Tools Integrator Running                   ")
    print(" Supported Tools: 15 (Antigravity, VS Code, Cursor, Zed, Aider,   ")
    print("                     Windsurf, Claude Code, Cline, Continue, etc)")
    print(" AI Profiles: Local Coding, Free Cloud, Premium, Reasoning, Fast ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
