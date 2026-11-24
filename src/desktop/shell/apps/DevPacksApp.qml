import QtQuick
import QtQuick.Controls
import "../../../design-system/qml"
import "../../../devpacks/qml"

Rectangle {
    id: devPacksAppRoot
    color: NexusTheme.background

    NexusDevPacksView {
        anchors.fill: parent
    }
}
