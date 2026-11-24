import QtQuick
import QtQuick.Controls
import "../../../design-system/qml"
import "../../../integrations/qml"

Rectangle {
    id: toolsAppRoot
    color: NexusTheme.background

    NexusToolsIntegrationView {
        anchors.fill: parent
    }
}
