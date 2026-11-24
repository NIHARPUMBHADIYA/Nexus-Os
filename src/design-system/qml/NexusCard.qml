import QtQuick

Item {
    id: root

    default property alias contentData: contentContainer.data
    property string title: ""
    property string subtitle: ""
    property bool interactive: false
    property bool elevated: false
    property int radiusValue: NexusTheme.radiusMedium
    property int cardPadding: NexusTheme.space5
    property string accentHeaderColor: ""

    signal clicked()

    implicitWidth: 320
    implicitHeight: mainCol.implicitHeight + cardPadding * 2 + (accentHeaderColor !== "" ? 3 : 0)

    Rectangle {
        id: bgCard
        anchors.fill: parent
        radius: root.radiusValue
        color: {
            if (root.interactive && mouseArea.pressed) return Qt.darker(NexusTheme.surface, 1.08);
            if (root.interactive && mouseArea.containsMouse) return Qt.lighter(NexusTheme.surface, 1.12);
            return root.elevated ? NexusTheme.elevatedSurface : NexusTheme.surface;
        }
        border.color: (root.interactive && mouseArea.containsMouse) ? NexusTheme.accent : NexusTheme.border
        border.width: 1

        Behavior on color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }
        Behavior on border.color {
            ColorAnimation { duration: NexusTheme.durationFast }
        }

        // Optional top accent strip
        Rectangle {
            visible: root.accentHeaderColor !== ""
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: 3
            radius: root.radiusValue
            color: root.accentHeaderColor
        }

        Column {
            id: mainCol
            anchors.fill: parent
            anchors.margins: root.cardPadding
            anchors.topMargin: root.cardPadding + (root.accentHeaderColor !== "" ? 4 : 0)
            spacing: NexusTheme.space3

            // Card Header
            Column {
                visible: root.title !== ""
                width: parent.width
                spacing: 2

                Text {
                    text: root.title
                    font.pixelSize: 15
                    font.bold: true
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.primaryText
                }

                Text {
                    visible: root.subtitle !== ""
                    text: root.subtitle
                    font.pixelSize: 12
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.secondaryText
                }
            }

            // Card Body Container
            Item {
                id: contentContainer
                width: parent.width
                implicitHeight: childrenRect.height
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        enabled: root.interactive
        hoverEnabled: root.interactive
        cursorShape: root.interactive ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: root.clicked()
    }
}
