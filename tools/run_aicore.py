#!/usr/bin/env python3
"""
NEXUS OS — AI Core Standalone Launcher (PyQt6 / QML)
Runs the unified Model Center, Hardware Governor, and AI Service Manager.
"""

import sys
import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.aicore.aicore_bridge import AICoreBridge

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS AI Core")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    aicore_qml = os.path.join(base_dir, "src", "aicore", "qml")

    bridge = AICoreBridge()

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(aicore_qml)
    view.rootContext().setContextProperty("aiCoreBridge", bridge)

    aicore_file = os.path.join(aicore_qml, "NexusAICoreView.qml")
    if not os.path.isfile(aicore_file):
        print(f"Error: Missing AICore QML at {aicore_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(aicore_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — AI Core & Model Center")
    view.resize(1140, 740)
    view.show()

    print("=================================================================")
    print(" NEXUS OS — AI Core Running                                      ")
    print(" Local Proxy: http://127.0.0.1:11430/v1                          ")
    print(" Managed Services: OmniRoute (:20128) & Ollama (:11434)          ")
    print(" Model Center: Coding, Reasoning, Vision, Embeddings, Large      ")
    print(" Free Tiers: Groq LPU, Gemini Flash, OpenRouter Free             ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
