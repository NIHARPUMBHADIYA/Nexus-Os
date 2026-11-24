import QtQuick
import QtQuick.Controls

Item {
    id: root

    property string title: "Dialog Title"
    property string message: ""
    property bool visibleState: false
    property string primaryActionText: "Confirm"
    property string cancelActionText: "Cancel"
    property bool showCancel: true

    default property alias bodyContent: bodyContainer.data

    signal confirmed()
    signal cancelled()

    anchors.fill: parent
    visible: opacity > 0
    opacity: visibleState ? 1 : 0

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationNormal }
    }

    // Modal backdrop scrim
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, NexusTheme.isDark ? 0.65 : 0.45)

        MouseArea {
            anchors.fill: parent
            onClicked: root.cancelled()
        }
    }

    // Centered Dialog Window
    Rectangle {
        id: dialogFrame
        width: Math.min(parent.width - 48, 480)
        implicitHeight: dialogLayout.implicitHeight + NexusTheme.space6 * 2
        anchors.centerIn: parent
        radius: NexusTheme.radiusLarge
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        scale: root.visibleState ? 1 : 0.94
        Behavior on scale {
            NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
        }

        Column {
            id: dialogLayout
            anchors.fill: parent
            anchors.margins: NexusTheme.space6
            spacing: NexusTheme.space4

            // Header
            Row {
                width: parent.width
                spacing: NexusTheme.space3

                Text {
                    width: parent.width - 32
                    text: root.title
                    font.pixelSize: 17
                    font.bold: true
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.primaryText
                    anchors.verticalCenter: parent.verticalCenter
                }

                // Close button
                Item {
                    width: 28
                    height: 28
                    Rectangle {
                        anchors.fill: parent
                        radius: 8
                        color: closeMouse.containsMouse ? NexusTheme.surface : "transparent"
                        Text {
                            anchors.centerIn: parent
                            text: "✕"
                            font.pixelSize: 12
                            color: NexusTheme.secondaryText
                        }
                    }
                    MouseArea {
                        id: closeMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.cancelled()
                    }
                }
            }

            // Optional message or custom body
            Text {
                visible: root.message !== ""
                width: parent.width
                text: root.message
                font.pixelSize: 13
                font.family: NexusTheme.fontFamilyUI
                color: NexusTheme.secondaryText
                wrapMode: Text.Wrap
            }

            Item {
                id: bodyContainer
                width: parent.width
                implicitHeight: childrenRect.height
            }

            // Action Buttons
            Row {
                anchors.right: parent.right
                spacing: NexusTheme.space3

                NexusButton {
                    visible: root.showCancel
                    text: root.cancelActionText
                    variant: "outline"
                    size: "md"
                    onClicked: root.cancelled()
                }

                NexusButton {
                    text: root.primaryActionText
                    variant: "primary"
                    size: "md"
                    onClicked: root.confirmed()
                }
            }
        }
    }
}
