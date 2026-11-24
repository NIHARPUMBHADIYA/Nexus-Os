import QtQuick
import QtQuick.Controls

Item {
    id: root

    property alias text: textInput.text
    property string placeholderText: "Enter value..."
    property bool isPassword: false
    property string leadingIcon: ""
    property bool clearable: true
    property bool readOnly: false
    property string errorText: ""

    signal accepted()
    signal cleared()

    implicitWidth: 260
    implicitHeight: col.implicitHeight

    Column {
        id: col
        anchors.fill: parent
        spacing: NexusTheme.space1

        Rectangle {
            id: inputContainer
            width: parent.width
            height: 38
            radius: NexusTheme.radiusSmall
            color: NexusTheme.secondaryBackground
            border.color: {
                if (root.errorText !== "") return NexusTheme.error;
                if (textInput.activeFocus) return NexusTheme.borderFocus;
                return NexusTheme.border;
            }
            border.width: textInput.activeFocus || root.errorText !== "" ? 1.5 : 1

            Behavior on border.color {
                ColorAnimation { duration: NexusTheme.durationFast }
            }

            Row {
                anchors.fill: parent
                anchors.leftMargin: NexusTheme.space3
                anchors.rightMargin: NexusTheme.space3
                spacing: NexusTheme.space2

                Text {
                    id: iconLabel
                    visible: root.leadingIcon !== ""
                    text: root.leadingIcon
                    font.pixelSize: 14
                    anchors.verticalCenter: parent.verticalCenter
                    color: textInput.activeFocus ? NexusTheme.accent : NexusTheme.secondaryText
                }

                TextInput {
                    id: textInput
                    width: parent.width - (iconLabel.visible ? iconLabel.width + NexusTheme.space2 : 0) - (clearBtn.visible ? clearBtn.width + NexusTheme.space2 : 0)
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 13
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.primaryText
                    echoMode: root.isPassword ? TextInput.Password : TextInput.Normal
                    readOnly: root.readOnly
                    selectByMouse: true
                    selectionColor: NexusTheme.accentSubtle
                    selectedTextColor: NexusTheme.accent

                    Text {
                        anchors.fill: parent
                        verticalAlignment: Text.AlignVCenter
                        text: root.placeholderText
                        color: NexusTheme.tertiaryText
                        font.pixelSize: 13
                        font.family: NexusTheme.fontFamilyUI
                        visible: textInput.text === "" && !textInput.activeFocus
                    }

                    onAccepted: root.accepted()
                }

                // Clear button
                Item {
                    id: clearBtn
                    visible: root.clearable && textInput.text !== "" && !root.readOnly
                    width: 20
                    height: 20
                    anchors.verticalCenter: parent.verticalCenter

                    Rectangle {
                        anchors.fill: parent
                        radius: width / 2
                        color: clearMouse.containsMouse ? NexusTheme.elevatedSurface : "transparent"

                        Text {
                            anchors.centerIn: parent
                            text: "✕"
                            font.pixelSize: 10
                            color: NexusTheme.secondaryText
                        }
                    }

                    MouseArea {
                        id: clearMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            textInput.text = "";
                            root.cleared();
                        }
                    }
                }
            }
        }

        Text {
            visible: root.errorText !== ""
            text: root.errorText
            font.pixelSize: 11
            font.family: NexusTheme.fontFamilyUI
            color: NexusTheme.error
            leftPadding: NexusTheme.space2
        }
    }
}
