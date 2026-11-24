import QtQuick

Item {
    id: root

    property string text: "Active"
    property string variant: "status" // "status", "count", "tag"
    property string status: "success" // "success", "warning", "error", "info", "neutral"
    property bool dot: true

    implicitWidth: badgeRow.implicitWidth + (variant === "count" ? 10 : 16)
    implicitHeight: variant === "count" ? 18 : 22

    function getStatusColor() {
        if (status === "success") return NexusTheme.success;
        if (status === "warning") return NexusTheme.warning;
        if (status === "error") return NexusTheme.error;
        if (status === "info") return NexusTheme.info;
        return NexusTheme.secondaryText;
    }

    function getStatusSubtle() {
        if (status === "success") return NexusTheme.successSubtle;
        if (status === "warning") return NexusTheme.warningSubtle;
        if (status === "error") return NexusTheme.errorSubtle;
        if (status === "info") return NexusTheme.infoSubtle;
        return NexusTheme.surface;
    }

    Rectangle {
        anchors.fill: parent
        radius: NexusTheme.radiusPill
        color: root.getStatusSubtle()
        border.color: Qt.rgba(root.getStatusColor().r, root.getStatusColor().g, root.getStatusColor().b, 0.3)
        border.width: 1

        Row {
            id: badgeRow
            anchors.centerIn: parent
            spacing: NexusTheme.space2

            // Status dot
            Rectangle {
                visible: root.dot && root.variant === "status"
                width: 6
                height: 6
                radius: 3
                color: root.getStatusColor()
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.text
                font.pixelSize: root.variant === "count" ? 10 : 11
                font.bold: true
                font.family: root.variant === "tag" ? NexusTheme.fontFamilyMono : NexusTheme.fontFamilyUI
                color: root.getStatusColor()
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}
