import QtQuick

Item {
    id: root

    property string iconText: "⚙"
    property string tooltipText: ""
    property int size: 36
    property string variant: "default" // "default", "accent", "danger", "subtle"
    property bool active: false
    property bool disabled: false

    signal clicked()

    implicitWidth: size
    implicitHeight: size

    Rectangle {
        id: bg
        anchors.fill: parent
        radius: NexusTheme.radiusSmall
        color: {
            if (root.disabled) return "transparent";
            if (root.active) return NexusTheme.accentSubtle;
            if (mouseArea.pressed) return NexusTheme.isDark ? "#282E47" : "#E2E8F0";
            if (mouseArea.containsMouse) return NexusTheme.isDark ? "#1F2439" : "#F1F5F9";
            return "transparent";
        }
        border.color: root.active ? NexusTheme.accent : "transparent"
        border.width: root.active ? 1 : 0

        Behavior on color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }

        Text {
            anchors.centerIn: parent
            text: root.iconText
            font.pixelSize: Math.round(root.size * 0.45)
            font.family: NexusTheme.fontFamilyUI
            color: {
                if (root.disabled) return NexusTheme.tertiaryText;
                if (root.active) return NexusTheme.accent;
                if (root.variant === "accent") return NexusTheme.accent;
                if (root.variant === "danger") return NexusTheme.error;
                return mouseArea.containsMouse ? NexusTheme.primaryText : NexusTheme.secondaryText;
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: !root.disabled
        cursorShape: root.disabled ? Qt.ArrowCursor : Qt.PointingHandCursor
        enabled: !root.disabled

        onClicked: root.clicked()
    }

    // Built-in compact tooltip
    Rectangle {
        id: tooltipBox
        visible: mouseArea.containsMouse && root.tooltipText !== ""
        anchors.bottom: parent.top
        anchors.bottomMargin: NexusTheme.space2
        anchors.horizontalCenter: parent.horizontalCenter
        width: tooltipLabel.implicitWidth + NexusTheme.space4
        height: 24
        radius: NexusTheme.radiusSmall
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1
        z: 999

        Text {
            id: tooltipLabel
            anchors.centerIn: parent
            text: root.tooltipText
            font.pixelSize: 11
            font.family: NexusTheme.fontFamilyUI
            color: NexusTheme.primaryText
        }
    }
}
