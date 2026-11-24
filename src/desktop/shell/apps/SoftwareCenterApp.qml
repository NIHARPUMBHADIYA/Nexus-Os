import QtQuick
import QtQuick.Controls
import "../../../design-system/qml"
import "../../../software_center/qml"

Rectangle {
    id: softwareCenterAppRoot
    color: NexusTheme.background

    NexusSoftwareCenterView {
        anchors.fill: parent
    }
}
