import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "apps"
import "../../spotlight/qml"

Item {
    id: desktopRoot
    width: 1280
    height: 800
    focus: true

    // Wallpaper configuration
    property string activeWallpaper: "obsidian"

    // Window Manager state instance
    NexusWindowManager {
        id: winManager
    }

    // Wallpaper Background Canvas
    Rectangle {
        id: wallpaperBg
        anchors.fill: parent

        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: {
                    if (desktopRoot.activeWallpaper === "nordic") return "#242933";
                    if (desktopRoot.activeWallpaper === "deepspace") return "#030712";
                    if (desktopRoot.activeWallpaper === "phosphor") return "#050B06";
                    if (desktopRoot.activeWallpaper === "ceramic") return "#F1F5F9";
                    if (desktopRoot.activeWallpaper === "tokyo") return "#16161E";
                    return NexusTheme.isDark ? "#0B0D14" : "#F8FAFC"; // obsidian
                }
            }
            GradientStop {
                position: 1.0
                color: {
                    if (desktopRoot.activeWallpaper === "nordic") return "#434C5E";
                    if (desktopRoot.activeWallpaper === "deepspace") return "#0F172A";
                    if (desktopRoot.activeWallpaper === "phosphor") return "#0A1F0E";
                    if (desktopRoot.activeWallpaper === "ceramic") return "#CBD5E1";
                    if (desktopRoot.activeWallpaper === "tokyo") return "#2A2E44";
                    return NexusTheme.isDark ? "#171B2B" : "#E2E8F0";
                }
            }
        }

        // Subtle geometric mesh lines / grid
        Canvas {
            anchors.fill: parent
            opacity: NexusTheme.isDark ? 0.08 : 0.04
            onPaint: {
                var ctx = getContext("2d");
                ctx.clearRect(0, 0, width, height);
                ctx.strokeStyle = "#FFFFFF";
                ctx.lineWidth = 1;
                var step = 48;
                for (var x = 0; x < width; x += step) {
                    ctx.beginPath();
                    ctx.moveTo(x, 0);
                    ctx.lineTo(x, height);
                    ctx.stroke();
                }
                for (var y = 0; y < height; y += step) {
                    ctx.beginPath();
                    ctx.moveTo(0, y);
                    ctx.lineTo(width, y);
                    ctx.stroke();
                }
            }
        }

        // Right-Click Context Menu Trigger on empty desktop
        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.RightButton
            onClicked: {
                desktopContextMenu.popup();
            }
        }
    }

    // Top System Panel
    NexusTopPanel {
        id: topPanel
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        windowManager: winManager
        activeAppName: {
            for (var i = 0; i < winManager.windows.length; i++) {
                if (winManager.windows[i].id === winManager.activeWindowId) {
                    return winManager.windows[i].title;
                }
            }
            return "Desktop";
        }

        onLauncherTriggered: appLauncher.openState = !appLauncher.openState
        onQuickSettingsTriggered: quickSettings.openState = !quickSettings.openState
        onNotificationsTriggered: notifCenter.openState = !notifCenter.openState
        onClockTriggered: notifCenter.openState = !notifCenter.openState
    }

    // Desktop Windows Viewport Layer
    Item {
        id: windowLayer
        anchors.top: topPanel.bottom
        anchors.bottom: bottomDock.top
        anchors.left: parent.left
        anchors.right: parent.right

        readonly property rect availableBounds: Qt.rect(0, 0, width, height)

        Repeater {
            model: winManager.windows

            delegate: NexusWindow {
                windowData: modelData
                windowManager: winManager
                desktopBounds: windowLayer.availableBounds

                // Dynamically instantiate the proper application based on appType
                Loader {
                    anchors.fill: parent
                    sourceComponent: {
                        if (modelData.appType === "terminal") return terminalComp;
                        if (modelData.appType === "devhub") return devhubComp;
                        if (modelData.appType === "tools") return toolsComp;
                        if (modelData.appType === "aicore") return aicoreComp;
                        if (modelData.appType === "software_center") return scComp;
                        if (modelData.appType === "settings") return settingsComp;
                        if (modelData.appType === "editor") return editorComp;
                        if (modelData.appType === "devpacks") return devpacksComp;
                        return terminalComp;
                    }
                }
            }
        }
    }

    // Floating Bottom Dock
    NexusDock {
        id: bottomDock
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 14
        anchors.horizontalCenter: parent.horizontalCenter
        windowManager: winManager
        onLauncherTriggered: appLauncher.openState = !appLauncher.openState
    }

    // Application Components for Loader
    Component { id: terminalComp; TerminalApp {} }
    Component { id: devhubComp; DevHubApp {} }
    Component { id: scComp; SoftwareCenterApp {} }
    Component { id: toolsComp; ToolsApp {} }
    Component { id: aicoreComp; AICoreApp {} }
    Component { id: settingsComp; SettingsApp {} }
    Component { id: editorComp; EditorApp {} }
    Component { id: devpacksComp; DevPacksApp {} }

    // Overlays: Universal Spotlight HUD (Win+Space)
    NexusSpotlightOverlay {
        id: spotlightOverlay
        onCloseRequested: spotlightOverlay.openState = false
        onResultSelected: function(item, actionId) {
            spotlightOverlay.openState = false;
            var iid = item.id || "";
            if (iid === "app:terminal" || actionId === "terminal_here") {
                winManager.openApp("terminal", "Nexus Terminal", "⌨");
            } else if (iid === "app:devhub") {
                winManager.openApp("devhub", "Developer Hub", "📁");
            } else if (iid === "app:editor" || actionId === "open_ide") {
                winManager.openApp("editor", "Code Editor", "💻");
            } else if (iid === "app:aicore" || actionId === "prompt") {
                winManager.openApp("aicore", "Nexus AI Core", "🤖");
            } else if (iid === "app:settings") {
                winManager.openApp("settings", "System Settings", "⚙");
            } else if (iid === "sys:theme_toggle") {
                if (NexusTheme.isDark) {
                    NexusTheme.setTheme("paper-light");
                } else {
                    NexusTheme.setTheme("midnight");
                }
            } else if (iid.indexOf("sys:") === 0) {
                winManager.addNotification("info", "System Action", "Executed " + item.title);
            } else {
                winManager.addNotification("success", "Launched", item.title);
            }
        }
    }

    // Overlays: Launcher
    NexusLauncher {
        id: appLauncher
        windowManager: winManager
        onCloseRequested: appLauncher.openState = false
    }

    // Overlays: Quick Settings Popover
    NexusQuickSettings {
        id: quickSettings
        onCloseRequested: quickSettings.openState = false
    }

    // Overlays: Notification Center Popover
    NexusNotificationCenter {
        id: notifCenter
        windowManager: winManager
        onCloseRequested: notifCenter.openState = false
    }

    // Overlays: Wallpaper Picker Dialog
    NexusWallpaperPicker {
        id: wallpaperPicker
        activeWallpaper: desktopRoot.activeWallpaper
        onWallpaperSelected: function(wId) {
            desktopRoot.activeWallpaper = wId;
        }
        onCloseRequested: wallpaperPicker.openState = false
    }

    // Desktop Context Menu
    NexusContextMenu {
        id: desktopContextMenu
        windowManager: winManager
        onChangeWallpaperRequested: wallpaperPicker.openState = true
    }

    // Global Desktop Keyboard Shortcuts (Win+Space triggers Universal Spotlight)
    Shortcut {
        sequence: "Meta+Space"
        onActivated: spotlightOverlay.openState = !spotlightOverlay.openState
    }
    Shortcut {
        sequence: "Alt+Space"
        onActivated: spotlightOverlay.openState = !spotlightOverlay.openState
    }
    Shortcut {
        sequence: "Meta+T"
        onActivated: winManager.openApp("terminal", "Nexus Terminal", "⌨")
    }
    Shortcut {
        sequence: "Ctrl+Alt+T"
        onActivated: winManager.openApp("terminal", "Nexus Terminal", "⌨")
    }
    Shortcut {
        sequence: "Meta+D"
        onActivated: winManager.openApp("devhub", "Developer Hub", "📁")
    }
    Shortcut {
        sequence: "Meta+S"
        onActivated: winManager.openApp("settings", "System Settings", "⚙")
    }
    Shortcut {
        sequence: "Ctrl+1"
        onActivated: winManager.switchWorkspace(0)
    }
    Shortcut {
        sequence: "Ctrl+2"
        onActivated: winManager.switchWorkspace(1)
    }
    Shortcut {
        sequence: "Ctrl+3"
        onActivated: winManager.switchWorkspace(2)
    }
    Shortcut {
        sequence: "Ctrl+4"
        onActivated: winManager.switchWorkspace(3)
    }
    Shortcut {
        sequence: "Escape"
        onActivated: {
            spotlightOverlay.openState = false;
            appLauncher.openState = false;
            quickSettings.openState = false;
            notifCenter.openState = false;
            wallpaperPicker.openState = false;
        }
    }

    // Open default initial developer apps on launch
    Component.onCompleted: {
        winManager.openApp("devhub", "Developer Hub", "📁", 760, 480);
        winManager.openApp("terminal", "Nexus Terminal", "⌨", 680, 420);
    }
}
