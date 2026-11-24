import QtQuick

Item {
    id: root

    property string variant: "info" // "info", "success", "warning", "error"
    property string title: "Notification"
    property string message: ""
    property bool dismissible: true
    property bool visibleState: true

    signal dismissed()

    implicitWidth: 360
    implicitHeight: notifCol.implicitHeight + NexusTheme.space4 * 2

    visible: opacity > 0
    opacity: visibleState ? 1 : 0

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationNormal }
    }

    // Helper functions for notification styling
    function getVariantColor() {
        if (variant === "success") return NexusTheme.success;
        if (variant === "warning") return NexusTheme.warning;
        if (variant === "error") return NexusTheme.error;
        return NexusTheme.info;
    }

    function getVariantSubtle() {
        if (variant === "success") return NexusTheme.successSubtle;
        if (variant === "warning") return NexusTheme.warningSubtle;
        if (variant === "error") return NexusTheme.errorSubtle;
        return NexusTheme.infoSubtle;
    }

    function getVariantIcon() {
        if (variant === "success") return "✓";
        if (variant === "warning") return "⚠";
        if (variant === "error") return "✕";
        return "ℹ";
    }

    Rectangle {
        anchors.fill: parent
        radius: NexusTheme.radiusMedium
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        // Left vertical indicator bar
        Rectangle {
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            width: 4
            radius: 2
            color: root.getVariantColor()
        }

        Row {
            id: notifCol
            anchors.fill: parent
            anchors.margins: NexusTheme.space4
            anchors.leftMargin: NexusTheme.space4 + 6
            spacing: NexusTheme.space3

            // Icon badge
            Rectangle {
                width: 28
                height: 28
                radius: 14
                color: root.getVariantSubtle()
                anchors.verticalCenter: parent.verticalCenter

                Text {
                    anchors.centerIn: parent
                    text: root.getVariantIcon()
                    font.pixelSize: 13
                    font.bold: true
                    color: root.getVariantColor()
                }
            }

            // Message text column
            Column {
                width: parent.width - 28 - (root.dismissible ? 28 : 0) - NexusTheme.space3 * 2
                anchors.verticalCenter: parent.verticalCenter
                spacing: 2

                Text {
                    text: root.title
                    font.pixelSize: 13
                    font.bold: true
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.primaryText
                }

                Text {
                    visible: root.message !== ""
                    text: root.message
                    font.pixelSize: 12
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.secondaryText
                    wrapMode: Text.Wrap
                    width: parent.width
                }
            }

            // Dismiss button
            Item {
                visible: root.dismissible
                width: 24
                height: 24
                anchors.verticalCenter: parent.verticalCenter

                Rectangle {
                    anchors.fill: parent
                    radius: 6
                    color: closeMouse.containsMouse ? NexusTheme.surface : "transparent"

                    Text {
                        anchors.centerIn: parent
                        text: "✕"
                        font.pixelSize: 11
                        color: NexusTheme.secondaryText
                    }
                }

                MouseArea {
                    id: closeMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        root.visibleState = false;
                        root.dismissed();
                    }
                }
            }
        }
    }
}
