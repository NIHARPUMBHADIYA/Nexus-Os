import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 1080
    height: 720
    title: qsTr("NEXUS Developer Hub")
    color: "#0F1117" // surface-base (Obsidian Core)

    header: ToolBar {
        background: Rectangle {
            color: "#161922" // surface-panel
            Rectangle {
                anchors.bottom: parent.bottom
                width: parent.width
                height: 1
                color: "#262B3D"
            }
        }
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            Label {
                text: "NEXUS Workspaces"
                font.bold: true
                font.pixelSize: 16
                color: "#F1F5F9"
            }
            Item { Layout.fillWidth: true }
            Button {
                text: "+ New Project"
                font.pixelSize: 13
                background: Rectangle {
                    color: "#6366F1" // Nexus Indigo
                    radius: 8 // radius-sm
                }
            }
        }
    }

    Item {
        anchors.fill: parent
        anchors.margins: 24

        ColumnLayout {
            anchors.fill: parent
            spacing: 16

            Label {
                text: "Active Projects"
                font.pixelSize: 20
                font.bold: true
                color: "#F1F5F9"
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 120
                color: "#1E2230" // surface-card
                radius: 12 // radius-md
                border.color: "#262B3D"
                border.width: 1

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 16

                    ColumnLayout {
                        spacing: 6
                        Label {
                            text: "nexus-core"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#F1F5F9"
                        }
                        Label {
                            text: "Rust • main • Clean working directory"
                            font.pixelSize: 13
                            color: "#94A3B8"
                        }
                    }

                    Item { Layout.fillWidth: true }

                    Button {
                        text: "Launch IDE"
                        background: Rectangle {
                            color: "#262B3D"
                            radius: 8
                        }
                    }
                }
            }

            Item { Layout.fillHeight: true }
        }
    }
}
