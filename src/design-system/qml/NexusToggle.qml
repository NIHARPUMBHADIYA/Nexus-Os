import QtQuick

Item {
    id: root

    property string type: "switch" // "switch", "checkbox", "radio"
    property bool checked: false
    property string label: ""
    property bool disabled: false

    signal toggled(bool state)

    implicitWidth: row.implicitWidth
    implicitHeight: 28

    Row {
        id: row
        anchors.verticalCenter: parent.verticalCenter
        spacing: NexusTheme.space3

        // Switch Variant
        Item {
            visible: root.type === "switch"
            width: 44
            height: 24
            anchors.verticalCenter: parent.verticalCenter

            Rectangle {
                id: switchTrack
                anchors.fill: parent
                radius: 12
                color: root.checked ? NexusTheme.accent : (root.disabled ? NexusTheme.border : (NexusTheme.isDark ? "#282E47" : "#CBD5E1"))

                Behavior on color {
                    ColorAnimation { duration: NexusTheme.durationFast }
                }

                Rectangle {
                    id: switchThumb
                    width: 20
                    height: 20
                    radius: 10
                    anchors.verticalCenter: parent.verticalCenter
                    x: root.checked ? parent.width - width - 2 : 2
                    color: "#FFFFFF"

                    Behavior on x {
                        NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
                    }
                }
            }
        }

        // Checkbox Variant
        Rectangle {
            visible: root.type === "checkbox"
            width: 20
            height: 20
            radius: 6
            anchors.verticalCenter: parent.verticalCenter
            color: root.checked ? NexusTheme.accent : NexusTheme.secondaryBackground
            border.color: root.checked ? NexusTheme.accent : NexusTheme.border
            border.width: 1.5

            Text {
                anchors.centerIn: parent
                visible: root.checked
                text: "✓"
                font.pixelSize: 12
                font.bold: true
                color: "#FFFFFF"
            }
        }

        // Radio Variant
        Rectangle {
            visible: root.type === "radio"
            width: 20
            height: 20
            radius: 10
            anchors.verticalCenter: parent.verticalCenter
            color: NexusTheme.secondaryBackground
            border.color: root.checked ? NexusTheme.accent : NexusTheme.border
            border.width: 1.5

            Rectangle {
                visible: root.checked
                width: 10
                height: 10
                radius: 5
                anchors.centerIn: parent
                color: NexusTheme.accent
            }
        }

        // Label
        Text {
            visible: root.label !== ""
            text: root.label
            font.pixelSize: 13
            font.family: NexusTheme.fontFamilyUI
            color: root.disabled ? NexusTheme.tertiaryText : NexusTheme.primaryText
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    MouseArea {
        anchors.fill: parent
        enabled: !root.disabled
        cursorShape: root.disabled ? Qt.ArrowCursor : Qt.PointingHandCursor
        onClicked: {
            root.checked = !root.checked;
            root.toggled(root.checked);
        }
    }
}
