import QtQuick
import QtQuick.Controls

Item {
    id: dockRoot

    property var windowManager: null
    signal launcherTriggered()

    // Dock pinned & dynamic applications model
    property var dockApps: [
        { appType: "launcher", title: "App Launcher", icon: "🚀", pinned: true },
        { appType: "terminal", title: "Terminal", icon: "⌨", pinned: true },
        { appType: "editor", title: "Code Editor", icon: "💻", pinned: true },
        { appType: "devhub", title: "Developer Hub", icon: "📁", pinned: true },
        { appType: "aicore", title: "Nexus AI Core", icon: "🤖", pinned: true },
        { appType: "settings", title: "System Settings", icon: "⚙", pinned: true }
    ]

    height: 68
    implicitWidth: dockCard.width

    // Floating Glassmorphism Container
    Rectangle {
        id: dockCard
        height: 60
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        width: dockRow.implicitWidth + 24
        radius: NexusTheme.radiusXL
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1
        z: 9500

        Row {
            id: dockRow
            anchors.centerIn: parent
            spacing: 8

            Repeater {
                model: dockRoot.dockApps

                delegate: Item {
                    id: dockItem
                    width: 48
                    height: 52

                    readonly property bool running: windowManager ? windowManager.isAppRunning(modelData.appType) : false

                    Column {
                        anchors.centerIn: parent
                        spacing: 2

                        // Icon box with hover lift
                        Item {
                            width: 42
                            height: 42
                            anchors.horizontalCenter: parent.horizontalCenter

                            y: itemMouse.containsMouse ? -6 : 0
                            scale: itemMouse.containsMouse ? 1.12 : 1.0

                            Behavior on y {
                                NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
                            }
                            Behavior on scale {
                                NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
                            }

                            Rectangle {
                                anchors.fill: parent
                                radius: 12
                                color: itemMouse.containsMouse ? NexusTheme.surface : "transparent"
                                border.color: itemMouse.containsMouse ? NexusTheme.border : "transparent"
                                border.width: 1

                                Text {
                                    anchors.centerIn: parent
                                    text: modelData.icon
                                    font.pixelSize: 22
                                }
                            }
                        }

                        // Running indicator dot
                        Rectangle {
                            width: 4
                            height: 4
                            radius: 2
                            anchors.horizontalCenter: parent.horizontalCenter
                            color: dockItem.running ? NexusTheme.accent : "transparent"
                        }
                    }

                    // Tooltip
                    Rectangle {
                        visible: itemMouse.containsMouse
                        anchors.bottom: parent.top
                        anchors.bottomMargin: 8
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: tooltipText.implicitWidth + 14
                        height: 24
                        radius: 6
                        color: NexusTheme.elevatedSurface
                        border.color: NexusTheme.border
                        border.width: 1
                        z: 9999

                        Text {
                            id: tooltipText
                            anchors.centerIn: parent
                            text: modelData.title
                            font.pixelSize: 11
                            font.bold: true
                            font.family: NexusTheme.fontFamilyUI
                            color: NexusTheme.primaryText
                        }
                    }

                    MouseArea {
                        id: itemMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        cursorShape: Qt.PointingHandCursor

                        onClicked: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                if (modelData.appType === "launcher") {
                                    dockRoot.launcherTriggered();
                                } else if (windowManager) {
                                    windowManager.openApp(modelData.appType, modelData.title, modelData.icon);
                                }
                            } else if (mouse.button === Qt.RightButton) {
                                dockContextMenu.targetApp = modelData;
                                dockContextMenu.popup();
                            }
                        }
                    }
                }
            }
        }
    }

    // Dock Item Right-Click Context Menu
    Menu {
        id: dockContextMenu
        property var targetApp: null

        MenuItem {
            text: "Open " + (dockContextMenu.targetApp ? dockContextMenu.targetApp.title : "")
            onTriggered: {
                if (windowManager && dockContextMenu.targetApp) {
                    windowManager.openApp(dockContextMenu.targetApp.appType, dockContextMenu.targetApp.title, dockContextMenu.targetApp.icon);
                }
            }
        }
        MenuItem {
            text: (dockContextMenu.targetApp && dockContextMenu.targetApp.pinned) ? "Unpin from Dock" : "Pin to Dock"
            onTriggered: {
                // In production, toggles pinned state in settings
            }
        }
        MenuSeparator {}
        MenuItem {
            text: "Quit Application"
            enabled: dockContextMenu.targetApp && windowManager && windowManager.isAppRunning(dockContextMenu.targetApp.appType)
            onTriggered: {
                if (windowManager && dockContextMenu.targetApp) {
                    for (var i = 0; i < windowManager.windows.length; i++) {
                        if (windowManager.windows[i].appType === dockContextMenu.targetApp.appType) {
                            windowManager.closeWindow(windowManager.windows[i].id);
                        }
                    }
                }
            }
        }
    }
}
