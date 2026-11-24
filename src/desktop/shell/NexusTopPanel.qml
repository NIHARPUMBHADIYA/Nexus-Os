import QtQuick
import QtQuick.Layouts

Rectangle {
    id: panelRoot

    property var windowManager: null
    property string activeAppName: "Desktop"

    signal launcherTriggered()
    signal quickSettingsTriggered()
    signal clockTriggered()
    signal notificationsTriggered()

    height: 38
    color: NexusTheme.secondaryBackground
    border.color: NexusTheme.border
    border.width: 1
    z: 9000

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 12

        // Left Section: OS Brand & Launcher Button
        Row {
            spacing: 8
            Layout.alignment: Qt.AlignVCenter

            // NEXUS OS Brand Pill
            Rectangle {
                width: brandRow.implicitWidth + 14
                height: 26
                radius: NexusTheme.radiusPill
                color: brandMouse.containsMouse ? NexusTheme.accentSubtle : "transparent"
                border.color: brandMouse.containsMouse ? NexusTheme.accent : "transparent"
                border.width: 1

                Row {
                    id: brandRow
                    anchors.centerIn: parent
                    spacing: 6

                    Text {
                        text: "💠"
                        font.pixelSize: 13
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: "NEXUS"
                        font.pixelSize: 12
                        font.bold: true
                        font.family: NexusTheme.fontFamilyUI
                        color: NexusTheme.primaryText
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                MouseArea {
                    id: brandMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: panelRoot.launcherTriggered()
                }
            }

            // Active Application Name Pill
            Text {
                text: panelRoot.activeAppName
                font.pixelSize: 12
                font.bold: true
                font.family: NexusTheme.fontFamilyUI
                color: NexusTheme.secondaryText
                anchors.verticalCenter: parent.verticalCenter
            }

            Rectangle {
                width: 1
                height: 16
                color: NexusTheme.border
                anchors.verticalCenter: parent.verticalCenter
            }

            // Workspace Switcher Pills
            Row {
                spacing: 4
                anchors.verticalCenter: parent.verticalCenter

                Repeater {
                    model: windowManager ? windowManager.workspaceNames : []

                    delegate: Rectangle {
                        readonly property bool isCurrent: windowManager && windowManager.currentWorkspace === index
                        width: wsLabel.implicitWidth + 14
                        height: 22
                        radius: NexusTheme.radiusPill
                        color: isCurrent ? NexusTheme.accent : (wsMouse.containsMouse ? NexusTheme.surface : "transparent")

                        Text {
                            id: wsLabel
                            anchors.centerIn: parent
                            text: (index + 1) + " " + modelData
                            font.pixelSize: 11
                            font.bold: isCurrent
                            font.family: NexusTheme.fontFamilyUI
                            color: isCurrent ? "#FFFFFF" : (wsMouse.containsMouse ? NexusTheme.primaryText : NexusTheme.secondaryText)
                        }

                        MouseArea {
                            id: wsMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: if (windowManager) windowManager.switchWorkspace(index)
                        }
                    }
                }
            }
        }

        Item { Layout.fillWidth: true }

        // Center Section: Clock and Date
        Rectangle {
            id: clockPill
            Layout.alignment: Qt.AlignVCenter
            width: clockRow.implicitWidth + 16
            height: 26
            radius: NexusTheme.radiusPill
            color: clockMouse.containsMouse ? NexusTheme.surface : "transparent"

            Row {
                id: clockRow
                anchors.centerIn: parent
                spacing: 6

                Text {
                    id: dateLabel
                    text: Qt.formatDateTime(new Date(), "ddd MMM d")
                    font.pixelSize: 12
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.secondaryText
                }

                Text {
                    id: timeLabel
                    text: Qt.formatDateTime(new Date(), "hh:mm")
                    font.pixelSize: 12
                    font.bold: true
                    font.family: NexusTheme.fontFamilyMono
                    color: NexusTheme.primaryText
                }
            }

            Timer {
                interval: 1000
                running: true
                repeat: true
                onTriggered: {
                    var now = new Date();
                    dateLabel.text = Qt.formatDateTime(now, "ddd MMM d");
                    timeLabel.text = Qt.formatDateTime(now, "hh:mm");
                }
            }

            MouseArea {
                id: clockMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: panelRoot.clockTriggered()
            }
        }

        Item { Layout.fillWidth: true }

        // Right Section: System Tray & Quick Settings
        Row {
            spacing: 6
            Layout.alignment: Qt.AlignVCenter

            // Hardware Status Pill (RAM / VRAM)
            Rectangle {
                width: hwRow.implicitWidth + 12
                height: 22
                radius: 4
                color: NexusTheme.surface
                border.color: NexusTheme.border
                border.width: 1
                anchors.verticalCenter: parent.verticalCenter

                Row {
                    id: hwRow
                    anchors.centerIn: parent
                    spacing: 4

                    Text {
                        text: "VRAM"
                        font.pixelSize: 9
                        font.bold: true
                        font.family: NexusTheme.fontFamilyMono
                        color: NexusTheme.secondaryText
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: "3.2 / 8 GB"
                        font.pixelSize: 10
                        font.bold: true
                        font.family: NexusTheme.fontFamilyMono
                        color: NexusTheme.accent
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }

            // Quick Status Icons (Wi-Fi, Bluetooth, Audio, Battery)
            Row {
                spacing: 2
                anchors.verticalCenter: parent.verticalCenter

                // Wi-Fi
                Rectangle {
                    width: 26
                    height: 24
                    radius: 4
                    color: wifiHover.containsMouse ? NexusTheme.surface : "transparent"
                    Text {
                        anchors.centerIn: parent
                        text: "📶"
                        font.pixelSize: 12
                    }
                    MouseArea { id: wifiHover; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: panelRoot.quickSettingsTriggered() }
                }

                // Volume
                Rectangle {
                    width: 26
                    height: 24
                    radius: 4
                    color: volHover.containsMouse ? NexusTheme.surface : "transparent"
                    Text {
                        anchors.centerIn: parent
                        text: "🔊"
                        font.pixelSize: 12
                    }
                    MouseArea { id: volHover; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: panelRoot.quickSettingsTriggered() }
                }

                // Battery
                Rectangle {
                    width: 32
                    height: 24
                    radius: 4
                    color: batHover.containsMouse ? NexusTheme.surface : "transparent"
                    Row {
                        anchors.centerIn: parent
                        spacing: 2
                        Text { text: "🔋"; font.pixelSize: 12 }
                    }
                    MouseArea { id: batHover; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: panelRoot.quickSettingsTriggered() }
                }

                // Notifications Bell with Badge
                Item {
                    width: 28
                    height: 24
                    anchors.verticalCenter: parent.verticalCenter

                    Rectangle {
                        anchors.fill: parent
                        radius: 4
                        color: notifHover.containsMouse ? NexusTheme.surface : "transparent"
                        Text {
                            anchors.centerIn: parent
                            text: "🔔"
                            font.pixelSize: 12
                        }
                    }

                    // Unread badge
                    Rectangle {
                        visible: windowManager && windowManager.notifications.length > 0
                        width: 8
                        height: 8
                        radius: 4
                        color: NexusTheme.accent
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.topMargin: 2
                        anchors.rightMargin: 2
                    }

                    MouseArea {
                        id: notifHover
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: panelRoot.notificationsTriggered()
                    }
                }
            }

            Rectangle {
                width: 1
                height: 16
                color: NexusTheme.border
                anchors.verticalCenter: parent.verticalCenter
            }

            // Quick Settings Trigger Pill
            Rectangle {
                width: qsRow.implicitWidth + 12
                height: 26
                radius: NexusTheme.radiusPill
                color: qsHover.containsMouse ? NexusTheme.accentSubtle : NexusTheme.surface
                border.color: qsHover.containsMouse ? NexusTheme.accent : NexusTheme.border
                border.width: 1
                anchors.verticalCenter: parent.verticalCenter

                Row {
                    id: qsRow
                    anchors.centerIn: parent
                    spacing: 4

                    Text { text: "⚙"; font.pixelSize: 12; anchors.verticalCenter: parent.verticalCenter }
                    Text { text: "Control"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText; anchors.verticalCenter: parent.verticalCenter }
                }

                MouseArea {
                    id: qsHover
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: panelRoot.quickSettingsTriggered()
                }
            }
        }
    }
}
