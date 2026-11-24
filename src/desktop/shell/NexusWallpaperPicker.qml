import QtQuick
import QtQuick.Controls

Item {
    id: pickerRoot

    property bool openState: false
    property string activeWallpaper: "obsidian"

    signal wallpaperSelected(string wallpaperId)
    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: openState ? 1 : 0
    z: 99999

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationNormal }
    }

    readonly property var wallpapers: [
        { id: "obsidian", name: "Obsidian Void", c1: "#0B0D14", c2: "#161B2B" },
        { id: "nordic", name: "Nordic Aurora", c1: "#242933", c2: "#434C5E" },
        { id: "deepspace", name: "Deep Space Void", c1: "#030712", c2: "#0F172A" },
        { id: "phosphor", name: "Terminal Phosphor", c1: "#050B06", c2: "#0A1F0E" },
        { id: "ceramic", name: "Alpine Dawn", c1: "#F1F5F9", c2: "#CBD5E1" },
        { id: "tokyo", name: "Tokyo Neon", c1: "#16161E", c2: "#2A2E44" }
    ]

    MouseArea {
        anchors.fill: parent
        onClicked: pickerRoot.closeRequested()
    }

    Rectangle {
        width: Math.min(parent.width - 64, 560)
        implicitHeight: col.implicitHeight + 40
        anchors.centerIn: parent
        radius: NexusTheme.radiusLarge
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        Column {
            id: col
            anchors.fill: parent
            anchors.margins: 20
            spacing: 16

            Row {
                width: parent.width
                Text {
                    text: "Select Desktop Wallpaper"
                    font.pixelSize: 16
                    font.bold: true
                    color: NexusTheme.primaryText
                }
            }

            Grid {
                columns: 3
                spacing: 12
                width: parent.width

                Repeater {
                    model: pickerRoot.wallpapers

                    delegate: Rectangle {
                        readonly property bool isCurrent: pickerRoot.activeWallpaper === modelData.id
                        width: (col.width - 24) / 3
                        height: 90
                        radius: NexusTheme.radiusSmall
                        border.color: isCurrent ? NexusTheme.accent : NexusTheme.border
                        border.width: isCurrent ? 2 : 1
                        clip: true

                        // Wallpaper preview gradient
                        Rectangle {
                            anchors.fill: parent
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: modelData.c1 }
                                GradientStop { position: 1.0; color: modelData.c2 }
                            }

                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 26
                                color: Qt.rgba(0, 0, 0, 0.6)

                                Text {
                                    anchors.centerIn: parent
                                    text: modelData.name
                                    font.pixelSize: 11
                                    font.bold: true
                                    color: "#FFFFFF"
                                }
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                pickerRoot.activeWallpaper = modelData.id;
                                pickerRoot.wallpaperSelected(modelData.id);
                                pickerRoot.closeRequested();
                            }
                        }
                    }
                }
            }
        }
    }
}
