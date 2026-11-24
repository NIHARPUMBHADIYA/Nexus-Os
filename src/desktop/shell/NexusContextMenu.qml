import QtQuick
import QtQuick.Controls

Menu {
    id: contextMenuRoot

    property var windowManager: null
    signal changeWallpaperRequested()

    MenuItem {
        text: "🖼 Change Wallpaper..."
        onTriggered: contextMenuRoot.changeWallpaperRequested()
    }

    MenuItem {
        text: NexusTheme.isDark ? "☀️ Switch to Light Mode" : "🌙 Switch to Dark Mode"
        onTriggered: {
            if (NexusTheme.isDark) {
                NexusTheme.setTheme("paper-light");
            } else {
                NexusTheme.setTheme("midnight");
            }
        }
    }

    MenuSeparator {}

    MenuItem {
        text: "⌨ Open Terminal"
        onTriggered: if (windowManager) windowManager.openApp("terminal", "Nexus Terminal", "⌨")
    }

    MenuItem {
        text: "📁 Open Developer Hub"
        onTriggered: if (windowManager) windowManager.openApp("devhub", "Developer Hub", "📁")
    }

    MenuItem {
        text: "🤖 Open AI Core"
        onTriggered: if (windowManager) windowManager.openApp("aicore", "Nexus AI Core", "🤖")
    }

    MenuSeparator {}

    MenuItem {
        text: "⚙ System Settings..."
        onTriggered: if (windowManager) windowManager.openApp("settings", "System Settings", "⚙")
    }
}
