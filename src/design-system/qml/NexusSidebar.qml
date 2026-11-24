import QtQuick

Rectangle {
    id: root

    property var items: [] // e.g. [{ "id": "projects", "icon": "📁", "label": "Projects", "badge": "12" }]
    property int activeIndex: 0
    property string headerTitle: "NEXUS"

    signal itemSelected(int index, string id, string label)

    implicitWidth: 220
    color: NexusTheme.secondaryBackground
    border.color: NexusTheme.border
    border.width: 1

    Column {
        anchors.fill: parent
        anchors.margins: NexusTheme.space3
        spacing: NexusTheme.space4

        // Sidebar Header
        Row {
            anchors.left: parent.left
            anchors.leftMargin: NexusTheme.space2
            spacing: NexusTheme.space2

            Rectangle {
                width: 8
                height: 8
                radius: 4
                color: NexusTheme.accent
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.headerTitle
                font.pixelSize: 12
                font.bold: true
                font.family: NexusTheme.fontFamilyUI
                color: NexusTheme.secondaryText
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        // Navigation list
        Column {
            width: parent.width
            spacing: 2

            Repeater {
                model: root.items

                delegate: Item {
                    id: navItem
                    readonly property bool isCurrent: root.activeIndex === index
                    width: parent.width
                    height: 36

                    Rectangle {
                        anchors.fill: parent
                        radius: NexusTheme.radiusSmall
                        color: navItem.isCurrent ? NexusTheme.accentSubtle : (itemMouse.containsMouse ? NexusTheme.surface : "transparent")

                        Behavior on color {
                            ColorAnimation { duration: NexusTheme.durationFast }
                        }

                        // Left active indicator pill
                        Rectangle {
                            visible: navItem.isCurrent
                            anchors.left: parent.left
                            anchors.leftMargin: 2
                            anchors.verticalCenter: parent.verticalCenter
                            width: 3
                            height: 18
                            radius: 1.5
                            color: NexusTheme.accent
                        }

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: NexusTheme.space4
                            anchors.rightMargin: NexusTheme.space3
                            spacing: NexusTheme.space3

                            Text {
                                text: modelData.icon || "•"
                                font.pixelSize: 14
                                anchors.verticalCenter: parent.verticalCenter
                                color: navItem.isCurrent ? NexusTheme.accent : NexusTheme.secondaryText
                            }

                            Text {
                                text: modelData.label || ""
                                font.pixelSize: 13
                                font.family: NexusTheme.fontFamilyUI
                                font.bold: navItem.isCurrent
                                anchors.verticalCenter: parent.verticalCenter
                                color: navItem.isCurrent ? NexusTheme.primaryText : NexusTheme.secondaryText
                            }

                            // Spacer
                            Item {
                                width: Math.max(0, parent.width - 40 - (modelData.label ? modelData.label.length * 8 : 40) - (modelData.badge ? 30 : 0))
                                height: 1
                            }

                            // Optional Badge
                            Rectangle {
                                visible: modelData.badge !== undefined && modelData.badge !== ""
                                width: badgeText.implicitWidth + 8
                                height: 18
                                radius: 9
                                color: navItem.isCurrent ? NexusTheme.accent : NexusTheme.surface
                                border.color: NexusTheme.border
                                border.width: 1
                                anchors.verticalCenter: parent.verticalCenter

                                Text {
                                    id: badgeText
                                    anchors.centerIn: parent
                                    text: modelData.badge || ""
                                    font.pixelSize: 10
                                    font.bold: true
                                    color: navItem.isCurrent ? "#FFFFFF" : NexusTheme.secondaryText
                                }
                            }
                        }

                        MouseArea {
                            id: itemMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                root.activeIndex = index;
                                root.itemSelected(index, modelData.id || "", modelData.label || "");
                            }
                        }
                    }
                }
            }
        }
    }
}
