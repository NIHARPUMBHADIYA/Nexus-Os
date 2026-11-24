import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root

    property string title: "NEXUS OS"
    property bool showControls: true
    property string activeAppIcon: ""
    default property alias actionsContent: rightActions.data

    signal closeClicked()
    signal minimizeClicked()
    signal maximizeClicked()

    height: 46
    color: NexusTheme.secondaryBackground
    border.color: NexusTheme.border
    border.width: 1

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: NexusTheme.space5
        anchors.rightMargin: NexusTheme.space5
        spacing: NexusTheme.space4

        // Window Controls (Traffic Lights)
        Row {
            visible: root.showControls
            spacing: 8
            Layout.alignment: Qt.AlignVCenter

            // Close
            Rectangle {
                width: 12
                height: 12
                radius: 6
                color: closeHover.containsMouse ? "#EF4444" : "#4A2222"
                border.color: "#EF4444"
                border.width: 1

                MouseArea {
                    id: closeHover
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.closeClicked()
                }
            }

            // Minimize
            Rectangle {
                width: 12
                height: 12
                radius: 6
                color: minHover.containsMouse ? "#F59E0B" : "#4A3B1C"
                border.color: "#F59E0B"
                border.width: 1

                MouseArea {
                    id: minHover
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.minimizeClicked()
                }
            }

            // Maximize
            Rectangle {
                width: 12
                height: 12
                radius: 6
                color: maxHover.containsMouse ? "#10B981" : "#1C4A2E"
                border.color: "#10B981"
                border.width: 1

                MouseArea {
                    id: maxHover
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.maximizeClicked()
                }
            }
        }

        // Center Title & App Icon
        Row {
            Layout.alignment: Qt.AlignVCenter
            spacing: NexusTheme.space2

            Text {
                visible: root.activeAppIcon !== ""
                text: root.activeAppIcon
                font.pixelSize: 14
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.title
                font.pixelSize: 13
                font.bold: true
                font.family: NexusTheme.fontFamilyUI
                color: NexusTheme.primaryText
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Item { Layout.fillWidth: true }

        // Right Actions Slot
        Row {
            id: rightActions
            Layout.alignment: Qt.AlignVCenter
            spacing: NexusTheme.space2
        }
    }
}
