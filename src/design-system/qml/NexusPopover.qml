import QtQuick

Item {
    id: root

    property bool open: false
    default property alias contentData: popoverContent.data

    implicitWidth: 240
    implicitHeight: popoverFrame.implicitHeight

    visible: opacity > 0
    opacity: open ? 1 : 0

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationFast }
    }

    Rectangle {
        id: popoverFrame
        anchors.fill: parent
        radius: NexusTheme.radiusMedium
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        Item {
            id: popoverContent
            anchors.fill: parent
            anchors.margins: NexusTheme.space4
        }
    }
}
