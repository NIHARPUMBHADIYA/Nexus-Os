import QtQuick
import QtQuick.Controls

Item {
    id: root

    property alias text: searchInput.text
    property string placeholderText: "Search apps, files, commands (Win+Space)..."
    property string shortcutHint: "Ctrl+K"
    property bool clearable: true

    signal accepted()
    signal cleared()

    implicitWidth: 360
    implicitHeight: 42

    Rectangle {
        id: searchBox
        anchors.fill: parent
        radius: NexusTheme.radiusSmall
        color: NexusTheme.secondaryBackground
        border.color: searchInput.activeFocus ? NexusTheme.borderFocus : NexusTheme.border
        border.width: searchInput.activeFocus ? 1.5 : 1

        Behavior on border.color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }

        Row {
            anchors.fill: parent
            anchors.leftMargin: NexusTheme.space3
            anchors.rightMargin: NexusTheme.space3
            spacing: NexusTheme.space2

            Text {
                text: "🔍"
                font.pixelSize: 13
                anchors.verticalCenter: parent.verticalCenter
                color: searchInput.activeFocus ? NexusTheme.accent : NexusTheme.secondaryText
            }

            TextInput {
                id: searchInput
                width: parent.width - 24 - (clearItem.visible ? 24 : (shortcutBadge.visible ? shortcutBadge.width + NexusTheme.space2 : 0))
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 13
                font.family: NexusTheme.fontFamilyUI
                color: NexusTheme.primaryText
                selectByMouse: true
                selectionColor: NexusTheme.accentSubtle
                selectedTextColor: NexusTheme.accent

                Text {
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    text: root.placeholderText
                    color: NexusTheme.tertiaryText
                    font.pixelSize: 13
                    font.family: NexusTheme.fontFamilyUI
                    visible: searchInput.text === ""
                }

                onAccepted: root.accepted()
            }

            // Clear button
            Item {
                id: clearItem
                visible: root.clearable && searchInput.text !== ""
                width: 20
                height: 20
                anchors.verticalCenter: parent.verticalCenter

                Rectangle {
                    anchors.fill: parent
                    radius: width / 2
                    color: clearMouseArea.containsMouse ? NexusTheme.elevatedSurface : "transparent"

                    Text {
                        anchors.centerIn: parent
                        text: "✕"
                        font.pixelSize: 10
                        color: NexusTheme.secondaryText
                    }
                }

                MouseArea {
                    id: clearMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        searchInput.text = "";
                        root.cleared();
                    }
                }
            }

            // Keyboard shortcut badge
            Rectangle {
                id: shortcutBadge
                visible: !clearItem.visible && root.shortcutHint !== ""
                width: shortcutText.implicitWidth + NexusTheme.space2 * 2
                height: 20
                radius: 4
                color: NexusTheme.elevatedSurface
                border.color: NexusTheme.border
                border.width: 1
                anchors.verticalCenter: parent.verticalCenter

                Text {
                    id: shortcutText
                    anchors.centerIn: parent
                    text: root.shortcutHint
                    font.pixelSize: 10
                    font.family: NexusTheme.fontFamilyMono
                    color: NexusTheme.secondaryText
                }
            }
        }
    }
}
