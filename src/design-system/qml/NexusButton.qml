import QtQuick
import QtQuick.Controls

Item {
    id: root

    property string text: ""
    property string variant: "primary" // "primary", "secondary", "subtle", "outline", "danger", "ghost"
    property string size: "md" // "sm", "md", "lg"
    property string radiusMode: "rounded" // "rounded", "pill"
    property bool loading: false
    property bool disabled: false
    property string iconText: ""

    signal clicked()

    implicitWidth: Math.max(contentRow.implicitWidth + horizontalPadding * 2, minWidth)
    implicitHeight: btnHeight

    readonly property int minWidth: size === "sm" ? 64 : (size === "lg" ? 96 : 80)
    readonly property int btnHeight: size === "sm" ? 30 : (size === "lg" ? 44 : 36)
    readonly property int horizontalPadding: size === "sm" ? NexusTheme.space3 : (size === "lg" ? NexusTheme.space6 : NexusTheme.space4)
    readonly property int fontSize: size === "sm" ? 12 : (size === "lg" ? 14 : 13)

    readonly property int cornerRadius: radiusMode === "pill" ? NexusTheme.radiusPill : (size === "sm" ? 8 : NexusTheme.radiusSmall)

    // Compute background color based on variant and hover/press states
    function getBgColor() {
        if (disabled) return NexusTheme.isDark ? "#1C2030" : "#E2E8F0";
        if (variant === "primary") {
            if (mouseArea.pressed) return Qt.darker(NexusTheme.accent, 1.15);
            if (mouseArea.containsMouse) return NexusTheme.accentHover;
            return NexusTheme.accent;
        } else if (variant === "secondary") {
            if (mouseArea.pressed) return Qt.darker(NexusTheme.surface, 1.1);
            if (mouseArea.containsMouse) return Qt.lighter(NexusTheme.surface, 1.15);
            return NexusTheme.surface;
        } else if (variant === "subtle") {
            if (mouseArea.pressed) return Qt.darker(NexusTheme.accentSubtle, 1.2);
            if (mouseArea.containsMouse) return Qt.lighter(NexusTheme.accentSubtle, 1.15);
            return NexusTheme.accentSubtle;
        } else if (variant === "danger") {
            if (mouseArea.pressed) return Qt.darker(NexusTheme.error, 1.15);
            if (mouseArea.containsMouse) return Qt.lighter(NexusTheme.error, 1.1);
            return NexusTheme.error;
        } else if (variant === "outline" || variant === "ghost") {
            if (mouseArea.pressed) return NexusTheme.isDark ? "#282E47" : "#CBD5E1";
            if (mouseArea.containsMouse) return NexusTheme.isDark ? "#1F2439" : "#F1F5F9";
            return "transparent";
        }
        return NexusTheme.surface;
    }

    // Compute text color
    function getTextColor() {
        if (disabled) return NexusTheme.tertiaryText;
        if (variant === "primary" || variant === "danger") return "#FFFFFF";
        if (variant === "subtle") return NexusTheme.accent;
        return NexusTheme.primaryText;
    }

    // Background rectangle
    Rectangle {
        id: bgRect
        anchors.fill: parent
        radius: root.cornerRadius
        color: root.getBgColor()
        border.color: (root.variant === "outline") ? (mouseArea.containsMouse ? NexusTheme.accent : NexusTheme.border) : "transparent"
        border.width: (root.variant === "outline") ? 1 : 0

        Behavior on color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }
        Behavior on border.color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }
    }

    // Content: icon, text, and loading indicator
    Row {
        id: contentRow
        anchors.centerIn: parent
        spacing: NexusTheme.space2

        Text {
            visible: root.iconText !== "" && !root.loading
            text: root.iconText
            font.pixelSize: root.fontSize + 2
            color: root.getTextColor()
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            visible: !root.loading && root.text !== ""
            text: root.text
            font.pixelSize: root.fontSize
            font.bold: root.variant === "primary" || root.size === "lg"
            font.family: NexusTheme.fontFamilyUI
            color: root.getTextColor()
            anchors.verticalCenter: parent.verticalCenter
        }

        // Loading spinner
        Item {
            visible: root.loading
            width: root.fontSize + 2
            height: root.fontSize + 2
            anchors.verticalCenter: parent.verticalCenter

            Rectangle {
                anchors.fill: parent
                radius: width / 2
                color: "transparent"
                border.color: root.getTextColor()
                border.width: 2
            }
            RotationAnimation on rotation {
                loops: Animation.Infinite
                from: 0
                to: 360
                duration: 900
                running: root.loading && !NexusTheme.reducedMotion
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: !root.disabled && !root.loading
        cursorShape: (root.disabled || root.loading) ? Qt.ArrowCursor : Qt.PointingHandCursor
        enabled: !root.disabled && !root.loading

        onClicked: root.clicked()
    }
}
