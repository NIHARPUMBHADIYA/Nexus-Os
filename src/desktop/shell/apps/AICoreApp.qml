import QtQuick
import QtQuick.Controls
import "../../../design-system/qml"
import "../../../aicore/qml"

Rectangle {
    id: aicoreAppRoot
    color: NexusTheme.background

    NexusAICoreView {
        anchors.fill: parent
    }
}
