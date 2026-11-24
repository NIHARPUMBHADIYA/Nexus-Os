import QtQuick
import QtQuick.Controls

Item {
    id: windowRoot

    // Window data object
    property var windowData: ({})
    property var windowManager: null
    property rect desktopBounds: Qt.rect(0, 38, 1200, 700)

    default property alias contentData: windowBody.data

    readonly property bool isCurrent: windowData.isActive === true
    readonly property bool isMax: windowData.isMaximized === true

    // Positioning and dimensions
    x: isMax ? desktopBounds.x : windowData.x
    y: isMax ? desktopBounds.y : windowData.y
    width: isMax ? desktopBounds.width : windowData.width
    height: isMax ? desktopBounds.height : windowData.height
    z: windowData.zIndex || 1

    visible: !(windowData.isMinimized === true) && (windowData.workspace === (windowManager ? windowManager.currentWorkspace : 0))

    Behavior on x {
        enabled: !dragArea.drag.active && !NexusTheme.reducedMotion
        NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
    }
    Behavior on y {
        enabled: !dragArea.drag.active && !NexusTheme.reducedMotion
        NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
    }
    Behavior on width {
        enabled: !resizeArea.drag.active && !NexusTheme.reducedMotion
        NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
    }
    Behavior on height {
        enabled: !resizeArea.drag.active && !NexusTheme.reducedMotion
        NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
    }

    // Outer Window Frame
    Rectangle {
        id: frame
        anchors.fill: parent
        radius: isMax ? 0 : NexusTheme.radiusLarge
        color: NexusTheme.surface
        border.color: windowRoot.isCurrent ? NexusTheme.borderFocus : NexusTheme.border
        border.width: windowRoot.isCurrent ? 1.5 : 1
        clip: true

        Behavior on border.color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }

        Column {
            anchors.fill: parent
            spacing: 0

            // Window Titlebar Header
            Rectangle {
                id: titlebar
                width: parent.width
                height: 42
                color: windowRoot.isCurrent ? NexusTheme.secondaryBackground : Qt.darker(NexusTheme.secondaryBackground, 1.08)
                border.color: NexusTheme.border
                border.width: 1

                Row {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    spacing: 12

                    // macOS / KDE Traffic Light Controls
                    Row {
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 8

                        // Close (Red)
                        Rectangle {
                            width: 12
                            height: 12
                            radius: 6
                            color: closeMouse.containsMouse ? "#EF4444" : (windowRoot.isCurrent ? "#FF5F56" : "#6E3838")

                            Text {
                                anchors.centerIn: parent
                                visible: closeMouse.containsMouse
                                text: "✕"
                                font.pixelSize: 8
                                font.bold: true
                                color: "#4A0000"
                            }

                            MouseArea {
                                id: closeMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: if (windowManager) windowManager.closeWindow(windowData.id)
                            }
                        }

                        // Minimize (Amber)
                        Rectangle {
                            width: 12
                            height: 12
                            radius: 6
                            color: minMouse.containsMouse ? "#F59E0B" : (windowRoot.isCurrent ? "#FFBD2E" : "#6E5B28")

                            Text {
                                anchors.centerIn: parent
                                visible: minMouse.containsMouse
                                text: "−"
                                font.pixelSize: 9
                                font.bold: true
                                color: "#4A3300"
                            }

                            MouseArea {
                                id: minMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: if (windowManager) windowManager.minimizeWindow(windowData.id)
                            }
                        }

                        // Maximize / Restore (Green)
                        Rectangle {
                            width: 12
                            height: 12
                            radius: 6
                            color: maxMouse.containsMouse ? "#10B981" : (windowRoot.isCurrent ? "#27C93F" : "#285E33")

                            Text {
                                anchors.centerIn: parent
                                visible: maxMouse.containsMouse
                                text: windowRoot.isMax ? "▫" : "+"
                                font.pixelSize: 9
                                font.bold: true
                                color: "#003A0C"
                            }

                            MouseArea {
                                id: maxMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (windowManager) {
                                        if (windowRoot.isMax) {
                                            windowManager.restoreWindow(windowData.id);
                                        } else {
                                            windowManager.maximizeWindow(windowData.id);
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Window Title & App Icon
                    Row {
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 8

                        Text {
                            text: windowData.icon || "💻"
                            font.pixelSize: 14
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Text {
                            text: windowData.title || "Window"
                            font.pixelSize: 12
                            font.bold: true
                            font.family: NexusTheme.fontFamilyUI
                            color: windowRoot.isCurrent ? NexusTheme.primaryText : NexusTheme.secondaryText
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

                // Titlebar Drag Area
                MouseArea {
                    id: dragArea
                    anchors.fill: parent
                    anchors.leftMargin: 80
                    anchors.rightMargin: 40

                    drag.target: isMax ? null : windowRoot
                    drag.minimumX: desktopBounds.x - windowRoot.width + 100
                    drag.maximumX: desktopBounds.x + desktopBounds.width - 100
                    drag.minimumY: desktopBounds.y
                    drag.maximumY: desktopBounds.y + desktopBounds.height - 42

                    onPressed: {
                        if (windowManager) windowManager.focusWindow(windowData.id);
                    }

                    onDoubleClicked: {
                        if (windowManager) {
                            if (windowRoot.isMax) {
                                windowManager.restoreWindow(windowData.id);
                            } else {
                                windowManager.maximizeWindow(windowData.id);
                            }
                        }
                    }

                    onReleased: {
                        if (windowManager) {
                            // Check for window snapping triggers
                            if (windowRoot.y <= desktopBounds.y + 4) {
                                // Snap Maximize
                                windowManager.maximizeWindow(windowData.id);
                            } else if (windowRoot.x <= desktopBounds.x + 4) {
                                // Snap Left Half
                                windowManager.updateWindowGeometry(
                                    windowData.id,
                                    desktopBounds.x,
                                    desktopBounds.y,
                                    Math.floor(desktopBounds.width / 2),
                                    desktopBounds.height
                                );
                            } else if (windowRoot.x + windowRoot.width >= desktopBounds.x + desktopBounds.width - 4) {
                                // Snap Right Half
                                windowManager.updateWindowGeometry(
                                    windowData.id,
                                    desktopBounds.x + Math.floor(desktopBounds.width / 2),
                                    desktopBounds.y,
                                    Math.floor(desktopBounds.width / 2),
                                    desktopBounds.height
                                );
                            } else {
                                windowManager.updateWindowGeometry(
                                    windowData.id,
                                    windowRoot.x,
                                    windowRoot.y,
                                    windowRoot.width,
                                    windowRoot.height
                                );
                            }
                        }
                    }
                }
            }

            // Window Body / Content Viewport
            Item {
                id: windowBody
                width: parent.width
                height: parent.height - 42
                clip: true
            }
        }

        // Bottom-Right Corner Resize Grip
        Item {
            id: resizeHandle
            visible: !windowRoot.isMax
            width: 18
            height: 18
            anchors.bottom: parent.bottom
            anchors.right: parent.right

            Text {
                anchors.centerIn: parent
                text: "⌟"
                font.pixelSize: 13
                color: resizeMouse.containsMouse ? NexusTheme.accent : NexusTheme.tertiaryText
            }

            MouseArea {
                id: resizeArea
                anchors.fill: parent
                cursorShape: Qt.SizeFDiagCursor

                property int startX: 0
                property int startY: 0
                property int startW: 0
                property int startH: 0

                onPressed: function(mouse) {
                    if (windowManager) windowManager.focusWindow(windowData.id);
                    startX = mouse.x;
                    startY = mouse.y;
                    startW = windowRoot.width;
                    startH = windowRoot.height;
                }

                onPositionChanged: function(mouse) {
                    var newW = Math.max(480, startW + (mouse.x - startX));
                    var newH = Math.max(320, startH + (mouse.y - startY));
                    windowRoot.width = newW;
                    windowRoot.height = newH;
                }

                onReleased: {
                    if (windowManager) {
                        windowManager.updateWindowGeometry(
                            windowData.id,
                            windowRoot.x,
                            windowRoot.y,
                            windowRoot.width,
                            windowRoot.height
                        );
                    }
                }
            }
        }
    }

    // Direct click on window brings it to focus
    MouseArea {
        anchors.fill: parent
        propagateComposedEvents: true
        z: -1
        onPressed: function(mouse) {
            if (windowManager) windowManager.focusWindow(windowData.id);
            mouse.accepted = false;
        }
    }
}
