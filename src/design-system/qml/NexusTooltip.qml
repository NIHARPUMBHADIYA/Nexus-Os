import QtQuick

Rectangle {
    id: root

    property string text: "Tooltip"
    property bool visibleState: false

    width: label.implicitWidth + NexusTheme.space4
    height: 24
    radius: NexusTheme.radiusSmall
    color: NexusTheme.elevatedSurface
    border.color: NexusTheme.border
    border.width: 1

    opacity: visibleState ? 1 : 0
    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationFast }
    }

    Text {
        id: label
        anchors.centerIn: parent
        text: root.text
        font.pixelSize: 11
        font.family: NexusTheme.fontFamilyUI
        color: NexusTheme.primaryText
    }
}
