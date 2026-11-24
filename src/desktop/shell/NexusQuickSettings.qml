import QtQuick
import QtQuick.Controls

Item {
    id: quickSettingsRoot

    property bool openState: false
    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: openState ? 1 : 0
    z: 95000

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationFast }
    }

    // Dismiss scrim
    MouseArea {
        anchors.fill: parent
        onClicked: quickSettingsRoot.closeRequested()
    }

    // Popover Box anchored at top-right
    Rectangle {
        id: box
        width: 340
        implicitHeight: col.implicitHeight + 32
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: 46
        anchors.rightMargin: 16
        radius: NexusTheme.radiusLarge
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        Column {
            id: col
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16

            // Header
            Row {
                width: parent.width
                Text {
                    text: "Quick Controls"
                    font.pixelSize: 14
                    font.bold: true
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.primaryText
                }
            }

            // Grid of Toggle Tiles (Wi-Fi, Bluetooth, Dark Mode, DND)
            Grid {
                columns: 2
                spacing: 8
                width: parent.width

                // Dark / Light Theme Toggle
                Rectangle {
                    width: (col.width - 8) / 2
                    height: 52
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.isDark ? NexusTheme.accentSubtle : NexusTheme.surface
                    border.color: NexusTheme.isDark ? NexusTheme.accent : NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Text { text: NexusTheme.isDark ? "🌙" : "☀️"; font.pixelSize: 14 }
                        Text {
                            text: NexusTheme.isDark ? "Dark Mode" : "Light Mode"
                            font.pixelSize: 12
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            if (NexusTheme.isDark) {
                                NexusTheme.setTheme("paper-light");
                            } else {
                                NexusTheme.setTheme("midnight");
                            }
                        }
                    }
                }

                // Wi-Fi Tile
                Rectangle {
                    width: (col.width - 8) / 2
                    height: 52
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.accentSubtle
                    border.color: NexusTheme.accent
                    border.width: 1

                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Text { text: "📶"; font.pixelSize: 14 }
                        Text { text: "Wi-Fi 6"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                    }
                }

                // Bluetooth Tile
                Rectangle {
                    width: (col.width - 8) / 2
                    height: 52
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.surface
                    border.color: NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Text { text: "ᛒ"; font.pixelSize: 14 }
                        Text { text: "Bluetooth"; font.pixelSize: 12; font.bold: true; color: NexusTheme.secondaryText }
                    }
                }

                // Do Not Disturb
                Rectangle {
                    width: (col.width - 8) / 2
                    height: 52
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.surface
                    border.color: NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Text { text: "🔕"; font.pixelSize: 14 }
                        Text { text: "Focus Mode"; font.pixelSize: 12; font.bold: true; color: NexusTheme.secondaryText }
                    }
                }
            }

            // Audio Volume Slider
            Column {
                width: parent.width
                spacing: 6

                Row {
                    width: parent.width
                    Text { text: "🔊 Volume"; font.pixelSize: 12; color: NexusTheme.secondaryText }
                    Item { width: Math.max(0, parent.width - 120); height: 1 }
                    Text { text: "75%"; font.pixelSize: 11; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.primaryText }
                }

                Rectangle {
                    width: parent.width
                    height: 8
                    radius: 4
                    color: NexusTheme.secondaryBackground
                    clip: true

                    Rectangle {
                        width: parent.width * 0.75
                        height: parent.height
                        radius: 4
                        color: NexusTheme.accent
                    }
                }
            }

            // Display Brightness Slider
            Column {
                width: parent.width
                spacing: 6

                Row {
                    width: parent.width
                    Text { text: "🔆 Brightness"; font.pixelSize: 12; color: NexusTheme.secondaryText }
                    Item { width: Math.max(0, parent.width - 130); height: 1 }
                    Text { text: "90%"; font.pixelSize: 11; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.primaryText }
                }

                Rectangle {
                    width: parent.width
                    height: 8
                    radius: 4
                    color: NexusTheme.secondaryBackground
                    clip: true

                    Rectangle {
                        width: parent.width * 0.90
                        height: parent.height
                        radius: 4
                        color: NexusTheme.accent
                    }
                }
            }

            // Power Profile Selector
            Row {
                width: parent.width
                spacing: 6

                Repeater {
                    model: ["Power Saver", "Balanced", "Performance"]

                    delegate: Rectangle {
                        readonly property bool isSelected: index === 1
                        width: (col.width - 12) / 3
                        height: 28
                        radius: NexusTheme.radiusSmall
                        color: isSelected ? NexusTheme.accent : NexusTheme.secondaryBackground
                        border.color: isSelected ? NexusTheme.accent : NexusTheme.border
                        border.width: 1

                        Text {
                            anchors.centerIn: parent
                            text: modelData
                            font.pixelSize: 10
                            font.bold: isSelected
                            color: isSelected ? "#FFFFFF" : NexusTheme.secondaryText
                        }
                    }
                }
            }
        }
    }
}
