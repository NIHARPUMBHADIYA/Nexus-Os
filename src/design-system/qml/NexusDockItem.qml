import QtQuick

Item {
    id: root

    property string iconText: "💻"
    property string appName: "App"
    property bool isRunning: false
    property int badgeCount: 0

    signal clicked()

    implicitWidth: 52
    implicitHeight: 60

    Column {
        anchors.centerIn: parent
        spacing: 4

        // Icon Container with hover lift
        Item {
            id: iconBox
            width: 44
            height: 44
            anchors.horizontalCenter: parent.horizontalCenter

            scale: mouseArea.containsMouse ? 1.12 : 1.0
            y: mouseArea.containsMouse ? -4 : 0

            Behavior on scale {
                NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
            }
            Behavior on y {
                NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
            }

            Rectangle {
                anchors.fill: parent
                radius: 12
                color: mouseArea.containsMouse ? NexusTheme.elevatedSurface : NexusTheme.surface
                border.color: NexusTheme.border
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: root.iconText
                    font.pixelSize: 22
                }

                // Notification count badge
                Rectangle {
                    visible: root.badgeCount > 0
                    anchors.top: parent.top
                    anchors.right: parent.right
                    anchors.topMargin: -4
                    anchors.rightMargin: -4
                    width: 18
                    height: 18
                    radius: 9
                    color: NexusTheme.error

                    Text {
                        anchors.centerIn: parent
                        text: root.badgeCount > 99 ? "99+" : root.badgeCount
                        font.pixelSize: 9
                        font.bold: true
                        color: "#FFFFFF"
                    }
                }
            }
        }

        // Active running indicator dot
        Rectangle {
            width: 4
            height: 4
            radius: 2
            anchors.horizontalCenter: parent.horizontalCenter
            color: root.isRunning ? NexusTheme.accent : "transparent"

            Behavior on color {
                ColorAnimation { duration: NexusTheme.durationFast }
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }

    // Dock Tooltip
    Rectangle {
        visible: mouseArea.containsMouse
        anchors.bottom: parent.top
        anchors.bottomMargin: 8
        anchors.horizontalCenter: parent.horizontalCenter
        width: tooltipLabel.implicitWidth + 14
        height: 24
        radius: 6
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1
        z: 9999

        Text {
            id: tooltipLabel
            anchors.centerIn: parent
            text: root.appName
            font.pixelSize: 11
            font.bold: true
            font.family: NexusTheme.fontFamilyUI
            color: NexusTheme.primaryText
        }
    }
}
