import QtQuick
import QtQuick.Controls

Item {
    id: notifCenterRoot

    property bool openState: false
    property var windowManager: null
    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: openState ? 1 : 0
    z: 95000

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationFast }
    }

    // Backdrop
    MouseArea {
        anchors.fill: parent
        onClicked: notifCenterRoot.closeRequested()
    }

    Rectangle {
        width: 360
        implicitHeight: Math.min(parent.height - 100, notifCol.implicitHeight + 32)
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: 46
        anchors.rightMargin: 16
        radius: NexusTheme.radiusLarge
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        Column {
            id: notifCol
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            // Header
            Row {
                width: parent.width

                Text {
                    text: "Notification Center"
                    font.pixelSize: 14
                    font.bold: true
                    color: NexusTheme.primaryText
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item { width: 100; height: 1 }

                Text {
                    text: "Clear All"
                    font.pixelSize: 11
                    color: NexusTheme.accent
                    anchors.verticalCenter: parent.verticalCenter
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: if (windowManager) windowManager.clearNotifications()
                    }
                }
            }

            // Notification Items List
            Repeater {
                model: windowManager ? windowManager.notifications : []

                delegate: Rectangle {
                    width: notifCol.width
                    implicitHeight: itemCol.implicitHeight + 16
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.surface
                    border.color: NexusTheme.border
                    border.width: 1

                    Column {
                        id: itemCol
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 4

                        Row {
                            width: parent.width
                            spacing: 6

                            Text {
                                text: modelData.title
                                font.pixelSize: 12
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            Item { width: 10; height: 1 }

                            Text {
                                text: modelData.time || ""
                                font.pixelSize: 10
                                color: NexusTheme.tertiaryText
                            }
                        }

                        Text {
                            text: modelData.message
                            font.pixelSize: 11
                            color: NexusTheme.secondaryText
                            wrapMode: Text.Wrap
                            width: parent.width
                        }
                    }
                }
            }

            Text {
                visible: !windowManager || windowManager.notifications.length === 0
                text: "No new notifications."
                font.pixelSize: 12
                color: NexusTheme.tertiaryText
                anchors.horizontalCenter: parent.horizontalCenter
                topPadding: 24
                bottomPadding: 24
            }
        }
    }
}
