import QtQuick

Item {
    id: root

    property var items: [] // e.g. [{ "text": "New Project", "icon": "📁", "shortcut": "Ctrl+N" }, { "separator": true }, { "text": "Settings", "icon": "⚙" }]
    signal itemTriggered(int index, string text)

    implicitWidth: 220
    implicitHeight: menuCol.implicitHeight + NexusTheme.space2 * 2

    Rectangle {
        anchors.fill: parent
        radius: NexusTheme.radiusMedium
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        Column {
            id: menuCol
            anchors.fill: parent
            anchors.margins: NexusTheme.space2
            spacing: 2

            Repeater {
                model: root.items

                delegate: Item {
                    width: menuCol.width
                    height: modelData.separator ? 9 : 32

                    // Separator line
                    Rectangle {
                        visible: modelData.separator === true
                        anchors.centerIn: parent
                        width: parent.width - NexusTheme.space2 * 2
                        height: 1
                        color: NexusTheme.border
                    }

                    // Menu Item
                    Rectangle {
                        id: itemBg
                        visible: !modelData.separator
                        anchors.fill: parent
                        radius: NexusTheme.radiusSmall
                        color: itemMouse.containsMouse ? NexusTheme.accentSubtle : "transparent"

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: NexusTheme.space3
                            anchors.rightMargin: NexusTheme.space3
                            spacing: NexusTheme.space3

                            Text {
                                text: modelData.icon || ""
                                font.pixelSize: 13
                                anchors.verticalCenter: parent.verticalCenter
                                color: itemMouse.containsMouse ? NexusTheme.accent : NexusTheme.secondaryText
                                visible: text !== ""
                            }

                            Text {
                                text: modelData.text || ""
                                font.pixelSize: 13
                                font.family: NexusTheme.fontFamilyUI
                                anchors.verticalCenter: parent.verticalCenter
                                color: itemMouse.containsMouse ? NexusTheme.primaryText : NexusTheme.primaryText
                            }

                            // Spacer
                            Item {
                                width: Math.max(0, parent.width - 50 - (modelData.text ? modelData.text.length * 8 : 40) - (modelData.shortcut ? 40 : 0))
                                height: 1
                            }

                            Text {
                                text: modelData.shortcut || ""
                                font.pixelSize: 11
                                font.family: NexusTheme.fontFamilyMono
                                anchors.verticalCenter: parent.verticalCenter
                                color: NexusTheme.tertiaryText
                                visible: text !== ""
                            }
                        }

                        MouseArea {
                            id: itemMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.itemTriggered(index, modelData.text)
                        }
                    }
                }
            }
        }
    }
}
