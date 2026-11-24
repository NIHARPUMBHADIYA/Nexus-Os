import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Item {
    id: spotlightRoot

    property bool openState: false
    property string activeCategory: "All"
    property int selectedIndex: 0
    property bool actionDrawerOpen: false
    property var resultsModel: []

    // Confirmation modal state
    property bool showConfirmDialog: false
    property string confirmActionId: ""
    property string confirmWarningMessage: ""
    property var confirmItemData: null

    signal resultSelected(var item, string actionId)
    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: openState ? 1 : 0
    z: 999999

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationFast }
    }

    // Backdrop Scrim
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, NexusTheme.isDark ? 0.65 : 0.45)

        MouseArea {
            anchors.fill: parent
            onClicked: spotlightRoot.closeRequested()
        }
    }

    // Master Centered HUD Card
    Rectangle {
        id: hudCard
        width: Math.min(parent.width - 48, 680)
        implicitHeight: mainLayout.implicitHeight + 24
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: Math.floor(parent.height * 0.16)
        radius: NexusTheme.radiusXL
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1
        clip: true

        scale: spotlightRoot.openState ? 1.0 : 0.96
        Behavior on scale {
            NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
        }

        Column {
            id: mainLayout
            anchors.fill: parent
            anchors.margins: 14
            spacing: 10

            // 1. Search Input Bar
            Rectangle {
                width: parent.width
                height: 52
                radius: NexusTheme.radiusMedium
                color: NexusTheme.secondaryBackground
                border.color: searchInput.activeFocus ? NexusTheme.borderFocus : NexusTheme.border
                border.width: 1.5

                Row {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    spacing: 12

                    Text {
                        text: "🔍"
                        font.pixelSize: 16
                        anchors.verticalCenter: parent.verticalCenter
                        color: searchInput.activeFocus ? NexusTheme.accent : NexusTheme.secondaryText
                    }

                    TextInput {
                        id: searchInput
                        width: parent.width - 150
                        font.pixelSize: 15
                        font.family: NexusTheme.fontFamilyUI
                        color: NexusTheme.primaryText
                        selectByMouse: true
                        anchors.verticalCenter: parent.verticalCenter
                        focus: spotlightRoot.openState

                        Text {
                            anchors.fill: parent
                            verticalAlignment: Text.AlignVCenter
                            text: "Search apps, files, projects, models (Win+Space)..."
                            color: NexusTheme.tertiaryText
                            font.pixelSize: 15
                            font.family: NexusTheme.fontFamilyUI
                            visible: searchInput.text === ""
                        }

                        onTextChanged: {
                            spotlightRoot.selectedIndex = 0;
                            spotlightRoot.refreshSearch();
                        }

                        Keys.onDownPressed: {
                            if (spotlightRoot.resultsModel.length > 0) {
                                spotlightRoot.selectedIndex = (spotlightRoot.selectedIndex + 1) % spotlightRoot.resultsModel.length;
                            }
                        }
                        Keys.onUpPressed: {
                            if (spotlightRoot.resultsModel.length > 0) {
                                spotlightRoot.selectedIndex = (spotlightRoot.selectedIndex - 1 + spotlightRoot.resultsModel.length) % spotlightRoot.resultsModel.length;
                            }
                        }
                        Keys.onReturnPressed: {
                            spotlightRoot.triggerDefaultAction();
                        }
                        Keys.onTabPressed: {
                            spotlightRoot.actionDrawerOpen = !spotlightRoot.actionDrawerOpen;
                        }
                        Keys.onRightPressed: {
                            spotlightRoot.actionDrawerOpen = true;
                        }
                        Keys.onLeftPressed: {
                            spotlightRoot.actionDrawerOpen = false;
                        }
                        Keys.onEscapePressed: {
                            if (spotlightRoot.actionDrawerOpen) {
                                spotlightRoot.actionDrawerOpen = false;
                            } else {
                                spotlightRoot.closeRequested();
                            }
                        }
                    }

                    // Key navigation hint pill
                    Rectangle {
                        width: 86
                        height: 22
                        radius: 4
                        color: NexusTheme.surface
                        border.color: NexusTheme.border
                        border.width: 1
                        anchors.verticalCenter: parent.verticalCenter

                        Text {
                            anchors.centerIn: parent
                            text: "TAB: Actions"
                            font.pixelSize: 10
                            font.family: NexusTheme.fontFamilyMono
                            color: NexusTheme.secondaryText
                        }
                    }
                }
            }

            // 2. Category Filter Pills
            Row {
                spacing: 6
                anchors.left: parent.left
                anchors.leftMargin: 4

                Repeater {
                    model: ["All", "Applications", "Projects", "Files", "AI Models", "Commands", "System Actions"]

                    delegate: Rectangle {
                        readonly property bool isCurrent: spotlightRoot.activeCategory === modelData
                        width: catText.implicitWidth + 14
                        height: 24
                        radius: NexusTheme.radiusPill
                        color: isCurrent ? NexusTheme.accent : (catMouse.containsMouse ? NexusTheme.surface : "transparent")
                        border.color: isCurrent ? NexusTheme.accent : NexusTheme.border
                        border.width: 1

                        Text {
                            id: catText
                            anchors.centerIn: parent
                            text: modelData
                            font.pixelSize: 11
                            font.bold: isCurrent
                            color: isCurrent ? "#FFFFFF" : NexusTheme.secondaryText
                        }

                        MouseArea {
                            id: catMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                spotlightRoot.activeCategory = modelData;
                                spotlightRoot.refreshSearch();
                            }
                        }
                    }
                }
            }

            // 3. Results List with Integrated Action Drawer
            Row {
                width: parent.width
                spacing: 12

                // Main Results List
                ListView {
                    id: resultsList
                    width: spotlightRoot.actionDrawerOpen ? parent.width - 230 : parent.width
                    height: Math.min(360, count * 52)
                    model: spotlightRoot.resultsModel
                    currentIndex: spotlightRoot.selectedIndex
                    clip: true
                    spacing: 4

                    Behavior on width {
                        NumberAnimation { duration: NexusTheme.durationFast; easing.type: Easing.OutQuad }
                    }

                    delegate: Rectangle {
                        id: resultRow
                        readonly property bool isSelected: spotlightRoot.selectedIndex === index
                        width: resultsList.width
                        height: 48
                        radius: NexusTheme.radiusSmall
                        color: isSelected ? NexusTheme.accentSubtle : (rowMouse.containsMouse ? NexusTheme.surface : "transparent")
                        border.color: isSelected ? NexusTheme.accent : "transparent"
                        border.width: isSelected ? 1 : 0

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 12
                            anchors.rightMargin: 12
                            spacing: 12

                            // Left selection indicator
                            Rectangle {
                                width: 3
                                height: 20
                                radius: 1.5
                                color: resultRow.isSelected ? NexusTheme.accent : "transparent"
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            // Icon
                            Text {
                                text: modelData.icon || "•"
                                font.pixelSize: 18
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            // Title & Description
                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 2
                                width: parent.width - 150

                                Text {
                                    text: modelData.title || ""
                                    font.pixelSize: 13
                                    font.bold: true
                                    font.family: NexusTheme.fontFamilyUI
                                    color: resultRow.isSelected ? NexusTheme.primaryText : NexusTheme.primaryText
                                    elide: Text.ElideRight
                                    width: parent.width
                                }

                                Text {
                                    text: modelData.description || ""
                                    font.pixelSize: 11
                                    font.family: NexusTheme.fontFamilyUI
                                    color: NexusTheme.secondaryText
                                    elide: Text.ElideRight
                                    width: parent.width
                                }
                            }

                            Item { width: 10; height: 1 }

                            // Category Tag Badge
                            Rectangle {
                                width: catBadgeLabel.implicitWidth + 10
                                height: 20
                                radius: NexusTheme.radiusPill
                                color: NexusTheme.surface
                                border.color: NexusTheme.border
                                border.width: 1
                                anchors.verticalCenter: parent.verticalCenter

                                Text {
                                    id: catBadgeLabel
                                    anchors.centerIn: parent
                                    text: modelData.category || ""
                                    font.pixelSize: 10
                                    color: NexusTheme.secondaryText
                                }
                            }
                        }

                        MouseArea {
                            id: rowMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                spotlightRoot.selectedIndex = index;
                                spotlightRoot.triggerDefaultAction();
                            }
                        }
                    }
                }

                // Action Drawer Panel
                Rectangle {
                    visible: spotlightRoot.actionDrawerOpen && currentItemActions.length > 0
                    width: 218
                    height: resultsList.height
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.surface
                    border.color: NexusTheme.border
                    border.width: 1

                    Column {
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 4

                        Text {
                            text: "ACTIONS"
                            font.pixelSize: 10
                            font.bold: true
                            font.family: NexusTheme.fontFamilyMono
                            color: NexusTheme.tertiaryText
                            leftPadding: 6
                            topPadding: 4
                        }

                        Repeater {
                            model: spotlightRoot.currentItemActions

                            delegate: Rectangle {
                                width: parent.width
                                height: 32
                                radius: 6
                                color: actMouse.containsMouse ? NexusTheme.accentSubtle : "transparent"

                                Row {
                                    anchors.fill: parent
                                    anchors.leftMargin: 8
                                    anchors.rightMargin: 8
                                    spacing: 8

                                    Text {
                                        text: modelData.title || ""
                                        font.pixelSize: 12
                                        color: modelData.destructive ? NexusTheme.error : (actMouse.containsMouse ? NexusTheme.accent : NexusTheme.primaryText)
                                        anchors.verticalCenter: parent.verticalCenter
                                    }

                                    Item { Layout.fillWidth: true; width: 10; height: 1 }

                                    Text {
                                        text: modelData.shortcut || ""
                                        font.pixelSize: 10
                                        font.family: NexusTheme.fontFamilyMono
                                        color: NexusTheme.tertiaryText
                                        anchors.verticalCenter: parent.verticalCenter
                                    }
                                }

                                MouseArea {
                                    id: actMouse
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        spotlightRoot.triggerAction(modelData);
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // 4. Keyboard Navigation Footer
            Row {
                width: parent.width
                spacing: 16

                Text {
                    text: (spotlightRoot.resultsModel.length) + " items found"
                    font.pixelSize: 11
                    font.family: NexusTheme.fontFamilyMono
                    color: NexusTheme.tertiaryText
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item { Layout.fillWidth: true; width: 200; height: 1 }

                Text {
                    text: "↑↓ Navigate  •  ↵ Launch  •  TAB Actions  •  ESC Close"
                    font.pixelSize: 11
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.secondaryText
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }
    }

    // Current selected item actions helper
    readonly property var currentItemActions: {
        if (resultsModel.length > 0 && selectedIndex >= 0 && selectedIndex < resultsModel.length) {
            return resultsModel[selectedIndex].actions || [];
        }
        return [];
    }

    // Destructive Confirmation Modal
    Rectangle {
        id: confirmDialog
        visible: spotlightRoot.showConfirmDialog
        width: 440
        implicitHeight: confirmCol.implicitHeight + 36
        anchors.centerIn: parent
        radius: NexusTheme.radiusLarge
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.error
        border.width: 1.5
        z: 9999999

        Column {
            id: confirmCol
            anchors.fill: parent
            anchors.margins: 18
            spacing: 12

            Row {
                spacing: 8
                Text { text: "⚠️"; font.pixelSize: 18 }
                Text { text: "Confirm Action"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }
            }

            Text {
                text: spotlightRoot.confirmWarningMessage
                font.pixelSize: 13
                color: NexusTheme.secondaryText
                wrapMode: Text.Wrap
                width: parent.width
            }

            Row {
                anchors.right: parent.right
                spacing: 8

                NexusButton {
                    text: "Cancel"
                    variant: "outline"
                    size: "sm"
                    onClicked: spotlightRoot.showConfirmDialog = false
                }

                NexusButton {
                    text: "Confirm & Execute"
                    variant: "danger"
                    size: "sm"
                    onClicked: {
                        spotlightRoot.showConfirmDialog = false;
                        if (spotlightRoot.confirmItemData) {
                            spotlightRoot.resultSelected(spotlightRoot.confirmItemData, spotlightRoot.confirmActionId);
                            spotlightRoot.closeRequested();
                        }
                    }
                }
            }
        }
    }

    function triggerDefaultAction() {
        if (resultsModel.length > 0 && selectedIndex >= 0 && selectedIndex < resultsModel.length) {
            var item = resultsModel[selectedIndex];
            var actions = item.actions || [];
            if (actions.length > 0) {
                triggerAction(actions[0]);
            }
        }
    }

    function triggerAction(action) {
        if (resultsModel.length > 0 && selectedIndex >= 0 && selectedIndex < resultsModel.length) {
            var item = resultsModel[selectedIndex];
            if (action.destructive) {
                spotlightRoot.confirmActionId = action.id;
                spotlightRoot.confirmWarningMessage = action.warning || "This action is destructive. Are you sure?";
                spotlightRoot.confirmItemData = item;
                spotlightRoot.showConfirmDialog = true;
            } else {
                spotlightRoot.resultSelected(item, action.id);
                spotlightRoot.closeRequested();
            }
        }
    }

    function refreshSearch() {
        // Populated dynamically by bridge or native engine
    }

    // Default sample results if bridge is not attached
    Component.onCompleted: {
        resultsModel = [
            { id: "app:terminal", title: "Nexus Terminal", description: "Default Zsh / Starship terminal emulator", category: "Applications", icon: "⌨", actions: [{ id: "open", title: "Launch Terminal" }] },
            { id: "proj:nexus-os", title: "nexus-os", description: "Rust / Qt6 • main (clean) • d:/My own os", category: "Projects", icon: "📁", actions: [{ id: "open_ide", title: "Open in Editor" }, { id: "terminal_here", title: "Terminal Here" }] },
            { id: "model:qwen", title: "qwen2.5-coder:7b", description: "Code Intelligence • Loaded in VRAM (4.2GB)", category: "AI Models", icon: "🤖", actions: [{ id: "prompt", title: "Spawn AI Session" }] },
            { id: "cmd:cargo_build", title: "> cargo build", description: "Compile active workspace packages", category: "Commands", icon: "⚡", actions: [{ id: "run", title: "Execute Command" }] },
            { id: "sys:theme_toggle", title: "Toggle Dark / Light Theme", description: "Switch between Obsidian dark and Paper light", category: "System Actions", icon: "🌓", actions: [{ id: "toggle_theme", title: "Switch Theme" }] }
        ];
    }
}
