#!/usr/bin/env python3
"""
NEXUS OS — Universal Spotlight Standalone Launcher (PyQt6 / QML)
Runs the floating Spotlight HUD overlay backed by the real SQLite FTS5 search engine.
"""

import sys
import os
import json

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQuick import QQuickView

# Add src to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.spotlight.search_engine import get_engine

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("NEXUS Spotlight")
    app.setOrganizationName("NexusOS")
    app.setApplicationVersion("1.0.0")

    engine_core = get_engine()

    ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
    spotlight_qml = os.path.join(base_dir, "src", "spotlight", "qml")

    view = QQuickView()
    view.engine().addImportPath(ds_qml)
    view.engine().addImportPath(spotlight_qml)

    overlay_file = os.path.join(spotlight_qml, "NexusSpotlightOverlay.qml")
    if not os.path.isfile(overlay_file):
        print(f"Error: Missing Spotlight QML at {overlay_file}")
        sys.exit(1)

    view.setSource(QUrl.fromLocalFile(overlay_file))
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setTitle("NEXUS OS — Universal Spotlight")
    view.resize(800, 600)

    # Open by default in standalone mode
    root_obj = view.rootObject()
    if root_obj:
        root_obj.setProperty("openState", True)

        # Wire live Python search into QML refreshSearch
        def on_query(text, cat):
            results = engine_core.search(text, category_filter=cat, limit=10)
            root_obj.setProperty("resultsModel", results)

        # Connect initial results
        on_query("", "All")

    view.show()

    print("=================================================================")
    print(" NEXUS OS — Universal Spotlight Running                         ")
    print(" Shortcut: Win+Space / Alt+Space                                 ")
    print(" Search Categories: Apps, Files, Projects, AI Models, Commands,  ")
    print("                    System Settings, System Actions              ")
    print(" Navigation: Arrow Keys to navigate, Enter to launch,            ")
    print("             Tab to toggle Actions drawer, ESC to close          ")
    print("=================================================================")

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
