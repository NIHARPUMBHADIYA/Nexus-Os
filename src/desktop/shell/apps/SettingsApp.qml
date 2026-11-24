import QtQuick
import QtQuick.Controls
import "../../../design-system/qml"
import "../../../settings/qml"

Rectangle {
    id: settingsRoot
    color: NexusTheme.background

    NexusSettingsView {
        anchors.fill: parent
    }
}
