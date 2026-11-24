import QtQuick

Item {
    id: root

    property var model: ["Tab 1", "Tab 2", "Tab 3"]
    property int currentIndex: 0
    property string variant: "segmented" // "segmented", "pills", "underline"

    signal tabSelected(int index, string label)

    implicitWidth: tabRow.implicitWidth + (variant === "segmented" ? 8 : 0)
    implicitHeight: 38

    // Segmented background container
    Rectangle {
        visible: root.variant === "segmented"
        anchors.fill: parent
        radius: NexusTheme.radiusSmall
        color: NexusTheme.secondaryBackground
        border.color: NexusTheme.border
        border.width: 1
    }

    Row {
        id: tabRow
        anchors.centerIn: parent
        spacing: root.variant === "underline" ? NexusTheme.space4 : NexusTheme.space2

        Repeater {
            model: root.model

            delegate: Item {
                id: tabItem
                readonly property bool isSelected: root.currentIndex === index
                width: tabLabel.implicitWidth + (root.variant === "underline" ? NexusTheme.space3 : NexusTheme.space4)
                height: 32

                // Pill / Segmented active background
                Rectangle {
                    visible: root.variant !== "underline"
                    anchors.fill: parent
                    radius: root.variant === "pills" ? NexusTheme.radiusPill : 8
                    color: {
                        if (tabItem.isSelected) return root.variant === "segmented" ? NexusTheme.surface : NexusTheme.accent;
                        if (mouseArea.containsMouse) return NexusTheme.elevatedSurface;
                        return "transparent";
                    }
                    border.color: (root.variant === "segmented" && tabItem.isSelected) ? NexusTheme.border : "transparent"
                    border.width: 1

                    Behavior on color {
                        ColorAnimation { duration: NexusTheme.durationFast }
                    }
                }

                Text {
                    id: tabLabel
                    anchors.centerIn: parent
                    text: modelData
                    font.pixelSize: 13
                    font.bold: tabItem.isSelected
                    font.family: NexusTheme.fontFamilyUI
                    color: {
                        if (tabItem.isSelected) {
                            if (root.variant === "pills") return "#FFFFFF";
                            if (root.variant === "underline") return NexusTheme.accent;
                            return NexusTheme.primaryText;
                        }
                        return mouseArea.containsMouse ? NexusTheme.primaryText : NexusTheme.secondaryText;
                    }
                }

                // Underline active indicator
                Rectangle {
                    visible: root.variant === "underline" && tabItem.isSelected
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 2
                    radius: 1
                    color: NexusTheme.accent
                }

                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        root.currentIndex = index;
                        root.tabSelected(index, modelData);
                    }
                }
            }
        }
    }
}
