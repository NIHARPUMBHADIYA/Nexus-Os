import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Rectangle {
    id: root
    color: NexusTheme.background

    // Check if bridge is provided; otherwise use local state
    readonly property bool hasBridge: typeof settingsBridge !== "undefined" && settingsBridge !== null
    property string activeCategory: hasBridge ? settingsBridge.activeCategoryId : "appearance"
    property string searchFilter: ""

    // Local state for shortcut editing modal
    property bool editingShortcut: false
    property string editingShortcutId: ""
    property string editingShortcutName: ""
    property string editingShortcutKey: ""
    property string shortcutConflictMsg: ""

    // Indexing exclusion input
    property string newExclusionInput: ""

    Connections {
        target: hasBridge ? settingsBridge : null
        function onActiveCategoryChanged() {
            root.activeCategory = settingsBridge.activeCategoryId;
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // ==========================================
        // LEFT SIDEBAR: 21 Categories in 7 Groups
        // ==========================================
        Rectangle {
            Layout.preferredWidth: 260
            Layout.fillHeight: true
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 10

                // Header & Live Search Bar
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Text {
                        text: "⚙️"
                        font.pixelSize: 22
                    }
                    Text {
                        text: "Settings"
                        font.pixelSize: 18
                        font.bold: true
                        color: NexusTheme.primaryText
                        Layout.fillWidth: true
                    }
                    NexusButton {
                        text: "Reset"
                        variant: "ghost"
                        size: "small"
                        onClicked: {
                            if (hasBridge) settingsBridge.resetToDefaults();
                        }
                    }
                }

                // Search field
                Rectangle {
                    Layout.fillWidth: true
                    height: 36
                    radius: NexusTheme.radiusMedium
                    color: NexusTheme.elevatedSurface
                    border.color: searchField.activeFocus ? NexusTheme.accent : NexusTheme.border
                    border.width: 1

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        spacing: 6

                        Text {
                            text: "🔍"
                            font.pixelSize: 12
                            color: NexusTheme.secondaryText
                        }

                        TextInput {
                            id: searchField
                            Layout.fillWidth: true
                            color: NexusTheme.primaryText
                            font.pixelSize: 12
                            clip: true
                            selectByMouse: true
                            onTextChanged: {
                                root.searchFilter = text;
                                if (hasBridge) settingsBridge.search(text);
                            }

                            Text {
                                text: "Search settings..."
                                color: NexusTheme.secondaryText
                                visible: !searchField.text && !searchField.activeFocus
                                font.pixelSize: 12
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }

                        NexusIconButton {
                            iconText: "✕"
                            size: 24
                            visible: searchField.text.length > 0
                            onClicked: {
                                searchField.text = "";
                                root.searchFilter = "";
                                if (hasBridge) settingsBridge.search("");
                            }
                        }
                    }
                }

                // Scrollable Category Navigation List
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    ColumnLayout {
                        width: parent.width - 10
                        spacing: 12

                        // When searching, show search hits
                        Repeater {
                            model: (root.searchFilter.length > 0 && hasBridge) ? settingsBridge.searchResults : []
                            delegate: Rectangle {
                                Layout.fillWidth: true
                                height: 44
                                radius: NexusTheme.radiusMedium
                                color: searchArea.containsMouse ? NexusTheme.elevatedSurface : "transparent"
                                border.color: NexusTheme.border
                                border.width: 1

                                MouseArea {
                                    id: searchArea
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        if (modelData.category_id) {
                                            root.activeCategory = modelData.category_id;
                                            if (hasBridge) settingsBridge.setActiveCategory(modelData.category_id);
                                        }
                                    }
                                }

                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: 8
                                    anchors.rightMargin: 8
                                    spacing: 8
                                    Text { text: modelData.icon || "🔍"; font.pixelSize: 14 }
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 1
                                        Text {
                                            text: modelData.title
                                            font.pixelSize: 12
                                            font.bold: true
                                            color: NexusTheme.primaryText
                                            elide: Text.ElideRight
                                            Layout.fillWidth: true
                                        }
                                        Text {
                                            text: modelData.subtitle
                                            font.pixelSize: 10
                                            color: NexusTheme.secondaryText
                                            elide: Text.ElideRight
                                            Layout.fillWidth: true
                                        }
                                    }
                                }
                            }
                        }

                        // Normal Mode: Show 7 Groups and 21 Categories
                        Repeater {
                            model: (root.searchFilter.length === 0 && hasBridge) ? settingsBridge.groupsList : [
                                {"id": "personalization", "name": "Personalization"},
                                {"id": "hardware", "name": "Hardware & Input"},
                                {"id": "connectivity", "name": "Connectivity"},
                                {"id": "system", "name": "System & Search"},
                                {"id": "development", "name": "Apps & Development"},
                                {"id": "ai", "name": "AI & Intelligence"},
                                {"id": "security", "name": "Security & Maintenance"}
                            ]
                            delegate: ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 4
                                visible: root.searchFilter.length === 0

                                // Group Header
                                Text {
                                    text: modelData.name.toUpperCase()
                                    font.pixelSize: 10
                                    font.bold: true
                                    color: NexusTheme.secondaryText
                                    leftPadding: 6
                                    topPadding: 4
                                    bottomPadding: 2
                                }

                                // Categories within this group
                                Repeater {
                                    model: hasBridge ? settingsBridge.categoriesList : []
                                    delegate: Rectangle {
                                        readonly property bool inThisGroup: modelData.group === parent.parent.modelData.id
                                        visible: inThisGroup
                                        Layout.fillWidth: true
                                        height: inThisGroup ? 34 : 0
                                        radius: NexusTheme.radiusMedium
                                        color: (root.activeCategory === modelData.id) ? 
                                                NexusTheme.elevatedSurface : (catArea.containsMouse ? NexusTheme.elevatedSurface : "transparent")
                                        border.color: (root.activeCategory === modelData.id) ? NexusTheme.accent : "transparent"
                                        border.width: 1

                                        MouseArea {
                                            id: catArea
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                root.activeCategory = modelData.id;
                                                if (hasBridge) settingsBridge.setActiveCategory(modelData.id);
                                            }
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.leftMargin: 8
                                            anchors.rightMargin: 8
                                            spacing: 8

                                            Text {
                                                text: modelData.icon
                                                font.pixelSize: 14
                                                Layout.alignment: Qt.AlignVCenter
                                            }

                                            Text {
                                                text: modelData.name
                                                font.pixelSize: 12
                                                color: (root.activeCategory === modelData.id) ? NexusTheme.primaryText : NexusTheme.secondaryText
                                                font.bold: root.activeCategory === modelData.id
                                                Layout.fillWidth: true
                                                Layout.alignment: Qt.AlignVCenter
                                                elide: Text.ElideRight
                                            }

                                            Rectangle {
                                                width: 6
                                                height: 6
                                                radius: NexusTheme.radiusPill
                                                color: NexusTheme.accent
                                                visible: root.activeCategory === modelData.id
                                                Layout.alignment: Qt.AlignVCenter
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // ==========================================
        // RIGHT MAIN CONTENT: Dynamic Category Panels
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: NexusTheme.background

            ScrollView {
                anchors.fill: parent
                clip: true

                ColumnLayout {
                    width: parent.width - 40
                    anchors.horizontalCenter: parent.horizontalCenter
                    spacing: 18

                    Item { height: 10; width: 1 }

                    // Category Title & Subtitle Banner
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12

                        Rectangle {
                            width: 44
                            height: 44
                            radius: NexusTheme.radiusLarge
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1
                            Text {
                                anchors.centerIn: parent
                                text: hasBridge ? settingsBridge.activeCategory.icon : "⚙️"
                                font.pixelSize: 22
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2
                            Text {
                                text: hasBridge ? settingsBridge.activeCategory.name : "Category"
                                font.pixelSize: 20
                                font.bold: true
                                color: NexusTheme.primaryText
                            }
                            Text {
                                text: "Manage and configure your " + (hasBridge ? settingsBridge.activeCategory.name : "") + " preferences."
                                font.pixelSize: 12
                                color: NexusTheme.secondaryText
                            }
                        }

                        NexusButton {
                            text: "Reset Category"
                            variant: "outline"
                            size: "small"
                            onClicked: {
                                if (hasBridge) settingsBridge.resetCategory(root.activeCategory);
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 1. APPEARANCE PANEL
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "appearance"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Color Theme & Mode"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    spacing: 12
                                    NexusButton {
                                        text: "Midnight (Default)"
                                        variant: (hasBridge && settingsBridge.allSettings["appearance.theme"] === "midnight") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("appearance.theme", "midnight")
                                    }
                                    NexusButton {
                                        text: "Nord"
                                        variant: (hasBridge && settingsBridge.allSettings["appearance.theme"] === "nord") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("appearance.theme", "nord")
                                    }
                                    NexusButton {
                                        text: "Tokyo Night"
                                        variant: (hasBridge && settingsBridge.allSettings["appearance.theme"] === "tokyo-night") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("appearance.theme", "tokyo-night")
                                    }
                                    NexusButton {
                                        text: "AMOLED Black"
                                        variant: (hasBridge && settingsBridge.allSettings["appearance.theme"] === "amoled") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("appearance.theme", "amoled")
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Dark Mode"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? (settingsBridge.allSettings["appearance.mode"] === "dark") : true
                                        onToggled: {
                                            if (hasBridge) settingsBridge.setSetting("appearance.mode", checked ? "dark" : "light")
                                        }
                                    }
                                }
                            }
                        }

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Window & Interface Styling"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "Compositor Blur & Vibrancy"; font.pixelSize: 13; color: NexusTheme.primaryText }
                                        Text { text: "Enable frosted glass blur effect under Wayland"; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["appearance.blur_enabled"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("appearance.blur_enabled", checked)
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "Reduced Motion"; font.pixelSize: 13; color: NexusTheme.primaryText }
                                        Text { text: "Minimize UI animations for performance and accessibility"; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["appearance.reduced_motion"]) : false
                                        onToggled: if (hasBridge) settingsBridge.setSetting("appearance.reduced_motion", checked)
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 2. DESKTOP & 3. DOCK PANELS
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "desktop"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Wallpaper Selection"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    spacing: 12
                                    NexusButton {
                                        text: "Cosmic Nebula"
                                        variant: (hasBridge && settingsBridge.allSettings["desktop.wallpaper"] === "nebula") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("desktop.wallpaper", "nebula")
                                    }
                                    NexusButton {
                                        text: "Nordic Aurora"
                                        variant: (hasBridge && settingsBridge.allSettings["desktop.wallpaper"] === "aurora") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("desktop.wallpaper", "aurora")
                                    }
                                    NexusButton {
                                        text: "Tokyo Neon"
                                        variant: (hasBridge && settingsBridge.allSettings["desktop.wallpaper"] === "cyberpunk") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("desktop.wallpaper", "cyberpunk")
                                    }
                                    NexusButton {
                                        text: "Minimal Obsidian"
                                        variant: (hasBridge && settingsBridge.allSettings["desktop.wallpaper"] === "minimal_dark") ? "primary" : "secondary"
                                        onClicked: if (hasBridge) settingsBridge.setSetting("desktop.wallpaper", "minimal_dark")
                                    }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "dock"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Dock Configuration"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Position"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    RowLayout {
                                        spacing: 6
                                        NexusButton {
                                            text: "Bottom"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["dock.position"] === "bottom") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("dock.position", "bottom")
                                        }
                                        NexusButton {
                                            text: "Left"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["dock.position"] === "left") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("dock.position", "left")
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Auto-dodge Maximized Windows"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["dock.auto_dodge"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("dock.auto_dodge", checked)
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 4. KEYBOARD & SHORTCUTS PANEL (With Editor & Conflict Detection)
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "keyboard"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 10
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Keyboard Shortcuts Editor"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Conflict Detection Active"; variant: "success" }
                                }
                                Text { text: "Customize system and developer shortcuts. Conflicts with reserved keys are prevented."; font.pixelSize: 11; color: NexusTheme.secondaryText }

                                // Shortcuts list
                                Repeater {
                                    model: hasBridge ? settingsBridge.shortcutsList : []
                                    delegate: Rectangle {
                                        Layout.fillWidth: true
                                        height: 48
                                        radius: NexusTheme.radiusMedium
                                        color: NexusTheme.elevatedSurface
                                        border.color: NexusTheme.border
                                        border.width: 1

                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.leftMargin: 12
                                            anchors.rightMargin: 12
                                            spacing: 10

                                            ColumnLayout {
                                                Layout.fillWidth: true
                                                spacing: 2
                                                Text { text: modelData.name; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                                Text { text: modelData.description; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                            }

                                            NexusBadge {
                                                text: modelData.category
                                                variant: "info"
                                            }

                                            Rectangle {
                                                width: 110
                                                height: 30
                                                radius: NexusTheme.radiusMedium
                                                color: NexusTheme.surface
                                                border.color: NexusTheme.accent
                                                border.width: 1

                                                Text {
                                                    anchors.centerIn: parent
                                                    text: modelData.key
                                                    font.pixelSize: 12
                                                    font.bold: true
                                                    color: NexusTheme.primaryText
                                                }
                                            }

                                            NexusButton {
                                                text: "Edit"
                                                size: "small"
                                                variant: "outline"
                                                onClicked: {
                                                    root.editingShortcutId = modelData.id;
                                                    root.editingShortcutName = modelData.name;
                                                    root.editingShortcutKey = modelData.key;
                                                    root.shortcutConflictMsg = "";
                                                    root.editingShortcut = true;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Inline Modal for editing shortcut
                        Rectangle {
                            Layout.fillWidth: true
                            implicitHeight: shortcutCol.implicitHeight + 24
                            visible: root.editingShortcut
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.accent
                            border.width: 2

                            ColumnLayout {
                                id: shortcutCol
                                anchors.fill: parent
                                anchors.margins: 12
                                spacing: 12
                                Text { text: "Edit Shortcut: " + root.editingShortcutName; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 10
                                    NexusInput {
                                        id: shortcutInput
                                        Layout.fillWidth: true
                                        text: root.editingShortcutKey
                                        placeholderText: "e.g. Meta+Space or Ctrl+Alt+K"
                                        onTextChanged: {
                                            root.editingShortcutKey = text;
                                            if (hasBridge && text.length > 0) {
                                                var conf = settingsBridge.checkShortcutConflict(text, root.editingShortcutId);
                                                root.shortcutConflictMsg = conf.has_conflict ? conf.description : "";
                                            }
                                        }
                                    }
                                    NexusButton {
                                        text: "Save"
                                        variant: "primary"
                                        enabled: root.shortcutConflictMsg.length === 0 && root.editingShortcutKey.length > 0
                                        onClicked: {
                                            if (hasBridge) {
                                                var res = settingsBridge.updateShortcut(root.editingShortcutId, root.editingShortcutKey);
                                                if (res.success) {
                                                    root.editingShortcut = false;
                                                } else {
                                                    root.shortcutConflictMsg = res.error;
                                                }
                                            }
                                        }
                                    }
                                    NexusButton {
                                        text: "Cancel"
                                        variant: "secondary"
                                        onClicked: root.editingShortcut = false
                                    }
                                }

                                Text {
                                    text: "⚠️ " + root.shortcutConflictMsg
                                    color: NexusTheme.error
                                    font.pixelSize: 12
                                    font.bold: true
                                    visible: root.shortcutConflictMsg.length > 0
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 5. DISPLAY & 6. SOUND & 7. NETWORK & 8. BLUETOOTH
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "display"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Display Resolution & Scaling"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Primary Output: 2560x1440 @ 165Hz (eDP-1 / Wayland)"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Wayland Native"; variant: "success" }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "UI Scale Factor: " + (hasBridge ? settingsBridge.allSettings["display.scale_factor"] : 1.0) + "x"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusButton { text: "100%"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("display.scale_factor", 1.0) }
                                    NexusButton { text: "125%"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("display.scale_factor", 1.25) }
                                    NexusButton { text: "150%"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("display.scale_factor", 1.5) }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "sound"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "PipeWire Audio Control"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Output: PipeWire Low-Latency Audio Server"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "PipeWire Active"; variant: "success" }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Master Volume: " + (hasBridge ? settingsBridge.allSettings["sound.master_volume"] : 75) + "%"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusButton { text: "Mute"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("sound.master_volume", 0) }
                                    NexusButton { text: "50%"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("sound.master_volume", 50) }
                                    NexusButton { text: "100%"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("sound.master_volume", 100) }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "network"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Network & Interfaces"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Wi-Fi (wlan0): Connected to 'NexusSecure-5G'"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "192.168.1.140"; variant: "info" }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Loopback Interface (lo): Active & Protected for Local AI Daemons"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "127.0.0.1 Only"; variant: "success" }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "bluetooth"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Bluetooth Devices"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Intel AX211 Bluetooth 5.3 Controller"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Powered On"; variant: "success" }
                                }
                                Text { text: "Paired: Keychron K2 Mechanical Keyboard, Sony WH-1000XM5"; font.pixelSize: 11; color: NexusTheme.secondaryText }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 9. SPOTLIGHT & 10. INDEXING PANELS
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "spotlight"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Universal Spotlight Configuration"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Max Search Results Displayed: " + (hasBridge ? settingsBridge.allSettings["spotlight.max_results"] : 10); font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusButton { text: "5"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("spotlight.max_results", 5) }
                                    NexusButton { text: "10"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("spotlight.max_results", 10) }
                                    NexusButton { text: "20"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("spotlight.max_results", 20) }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Enable Terminal & Shell Commands Search"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["spotlight.enable_commands"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("spotlight.enable_commands", checked)
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Enable AI Model Queries in Search Bar"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["spotlight.enable_ai"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("spotlight.enable_ai", checked)
                                    }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "indexing"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Code & File Indexing Exclusions"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "SQLite FTS5 Active"; variant: "success" }
                                }
                                Text { text: "Exclude sensitive directories, secrets, and large build artifacts from Spotlight search."; font.pixelSize: 11; color: NexusTheme.secondaryText }

                                // Add exclusion input
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 8
                                    NexusInput {
                                        id: newExclusionBox
                                        Layout.fillWidth: true
                                        placeholderText: "e.g. ~/.secrets or **/build or ~/Documents/Private"
                                        text: root.newExclusionInput
                                        onTextChanged: root.newExclusionInput = text
                                    }
                                    NexusButton {
                                        text: "Add Exclusion"
                                        variant: "primary"
                                        size: "medium"
                                        enabled: root.newExclusionInput.length > 0
                                        onClicked: {
                                            if (hasBridge && root.newExclusionInput.length > 0) {
                                                settingsBridge.addIndexingExclusion(root.newExclusionInput);
                                                newExclusionBox.text = "";
                                                root.newExclusionInput = "";
                                            }
                                        }
                                    }
                                }

                                // List exclusions
                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 6
                                    Repeater {
                                        model: hasBridge ? settingsBridge.indexingExclusions : []
                                        delegate: Rectangle {
                                            Layout.fillWidth: true
                                            height: 36
                                            radius: NexusTheme.radiusMedium
                                            color: NexusTheme.elevatedSurface
                                            border.color: NexusTheme.border
                                            border.width: 1

                                            RowLayout {
                                                anchors.fill: parent
                                                anchors.leftMargin: 12
                                                anchors.rightMargin: 12
                                                spacing: 10
                                                Text { text: "🚫"; font.pixelSize: 12 }
                                                Text {
                                                    text: modelData
                                                    font.pixelSize: 12
                                                    font.family: NexusTheme.fontMono
                                                    color: NexusTheme.primaryText
                                                    Layout.fillWidth: true
                                                }
                                                NexusIconButton {
                                                    iconText: "🗑️"
                                                    size: 28
                                                    onClicked: {
                                                        if (hasBridge) settingsBridge.removeIndexingExclusion(modelData);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 11. NOTIFICATIONS & 12. STORAGE
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "notifications"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Notification Banners & Alerts"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Do Not Disturb (DND)"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["notifications.dnd"]) : false
                                        onToggled: if (hasBridge) settingsBridge.setSetting("notifications.dnd", checked)
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Banner Timeout"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    RowLayout {
                                        spacing: 6
                                        NexusButton { text: "3s"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("notifications.timeout_secs", 3) }
                                        NexusButton { text: "5s"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("notifications.timeout_secs", 5) }
                                        NexusButton { text: "10s"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("notifications.timeout_secs", 10) }
                                    }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "storage"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 14
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Storage Breakdown & Drive Capacity"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusButton {
                                        text: "Refresh Stats"
                                        size: "small"
                                        variant: "outline"
                                        onClicked: if (hasBridge) settingsBridge.refreshStorage()
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text {
                                        text: (hasBridge ? settingsBridge.storageData.used_formatted : "0 GB") + " used of " + (hasBridge ? settingsBridge.storageData.total_formatted : "0 GB") + " (" + (hasBridge ? settingsBridge.storageData.free_formatted : "0 GB") + " free)"
                                        font.pixelSize: 12
                                        color: NexusTheme.secondaryText
                                    }
                                }

                                // Visual Storage Bar
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 18
                                    radius: NexusTheme.radiusPill
                                    color: NexusTheme.elevatedSurface
                                    clip: true

                                    Row {
                                        anchors.fill: parent
                                        Repeater {
                                            model: (hasBridge && settingsBridge.storageData.breakdown) ? settingsBridge.storageData.breakdown : []
                                            delegate: Rectangle {
                                                readonly property real fraction: hasBridge ? (modelData.size_bytes / settingsBridge.storageData.total_bytes) : 0.2
                                                width: parent.width * fraction
                                                height: parent.height
                                                color: modelData.color
                                            }
                                        }
                                    }
                                }

                                // Storage category breakdown rows
                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 8
                                    Repeater {
                                        model: (hasBridge && settingsBridge.storageData.breakdown) ? settingsBridge.storageData.breakdown : []
                                        delegate: RowLayout {
                                            Layout.fillWidth: true
                                            spacing: 10

                                            Rectangle {
                                                width: 12
                                                height: 12
                                                radius: NexusTheme.radiusPill
                                                color: modelData.color
                                            }

                                            Text {
                                                text: modelData.name
                                                font.pixelSize: 12
                                                color: NexusTheme.primaryText
                                                Layout.fillWidth: true
                                            }

                                            Text {
                                                text: modelData.formatted
                                                font.pixelSize: 12
                                                font.bold: true
                                                color: NexusTheme.secondaryText
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 13. APPLICATIONS & 14. DEVELOPER ENVIRONMENT
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "applications"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Default Applications"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Web Browser: Chromium / Firefox (Wayland)"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "System Default"; variant: "info" }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Terminal Emulator: NEXUS Terminal (GPU accelerated)"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Native"; variant: "success" }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "File Manager: Dolphin / NEXUS Files"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Native"; variant: "info" }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "developer"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Developer Toolchains & Preferences"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Default Code Editor / IDE"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    RowLayout {
                                        spacing: 6
                                        NexusButton {
                                            text: "Cursor"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["developer.default_ide"] === "cursor") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("developer.default_ide", "cursor")
                                        }
                                        NexusButton {
                                            text: "VS Code"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["developer.default_ide"] === "vscode") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("developer.default_ide", "vscode")
                                        }
                                        NexusButton {
                                            text: "Zed"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["developer.default_ide"] === "zed") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("developer.default_ide", "zed")
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Container Engine: Podman (Rootless, Daemonless)"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Podman (Active)"; variant: "success" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "mise Polyglot Version Manager Integration"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["developer.mise_enabled"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("developer.mise_enabled", checked)
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 15. AI CORE & 16. MODELS PANELS
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "aicore"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "NEXUS AI Core Configuration (`nexus-aid`)"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Loopback Proxy Port: 11430 (OpenAI Compatible)"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "127.0.0.1:11430"; variant: "success" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "OmniRoute Unified Model Router Port: 20128"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "127.0.0.1:20128"; variant: "info" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Ollama Local Inference Port: 11434"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "127.0.0.1:11434"; variant: "info" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Autostart OmniRoute on Boot"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["aicore.autostart_omniroute"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("aicore.autostart_omniroute", checked)
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Autostart Ollama on Boot"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusToggle {
                                        checked: hasBridge ? Boolean(settingsBridge.allSettings["aicore.autostart_ollama"]) : true
                                        onToggled: if (hasBridge) settingsBridge.setSetting("aicore.autostart_ollama", checked)
                                    }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "models"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Local Model Management & VRAM Governor"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "Wayland Compositor Safety Headroom: " + (hasBridge ? settingsBridge.allSettings["aicore.vram_headroom_mb"] : 2048) + " MB"; font.pixelSize: 13; color: NexusTheme.primaryText }
                                        Text { text: "Guarantees dedicated VRAM for desktop rendering so large LLMs never freeze the desktop."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusBadge { text: "Governor Enforced"; variant: "success" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Idle Model Unload Timeout: " + (hasBridge ? settingsBridge.allSettings["aicore.idle_timeout_minutes"] : 15) + " minutes"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    RowLayout {
                                        spacing: 6
                                        NexusButton { text: "10m"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("aicore.idle_timeout_minutes", 10) }
                                        NexusButton { text: "15m"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("aicore.idle_timeout_minutes", 15) }
                                        NexusButton { text: "30m"; size: "small"; onClicked: if (hasBridge) settingsBridge.setSetting("aicore.idle_timeout_minutes", 30) }
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 17. SYSTEM SERVICES
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "services"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "System Daemons & Background Services"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusButton {
                                        text: "Refresh Services"
                                        size: "small"
                                        variant: "outline"
                                        onClicked: if (hasBridge) settingsBridge.refreshServices()
                                    }
                                }

                                Repeater {
                                    model: hasBridge ? settingsBridge.servicesList : []
                                    delegate: Rectangle {
                                        Layout.fillWidth: true
                                        height: 52
                                        radius: NexusTheme.radiusMedium
                                        color: NexusTheme.elevatedSurface
                                        border.color: NexusTheme.border
                                        border.width: 1

                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.leftMargin: 12
                                            anchors.rightMargin: 12
                                            spacing: 12

                                            Text { text: "⚙️"; font.pixelSize: 16 }

                                            ColumnLayout {
                                                Layout.fillWidth: true
                                                spacing: 2
                                                Text { text: modelData.name + " (" + modelData.id + ")"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                                Text { text: modelData.description; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                            }

                                            NexusBadge {
                                                text: modelData.status_label
                                                variant: modelData.is_running ? "success" : "warning"
                                            }

                                            NexusToggle {
                                                checked: modelData.autostart
                                                onToggled: {
                                                    if (hasBridge) settingsBridge.toggleServiceAutostart(modelData.id, checked);
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 18. SECURITY & 19. PRIVACY PANELS
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "security"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "Security & Access Control"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "Polkit Privilege Separation"; font.pixelSize: 13; color: NexusTheme.primaryText }
                                        Text { text: "Rootless desktop operation enforced. Root password required only for package installation."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusBadge { text: "Enforced"; variant: "success" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "Local Loopback Isolation"; font.pixelSize: 13; color: NexusTheme.primaryText }
                                        Text { text: "All AI daemons strictly refuse external WAN connections and bind to 127.0.0.1."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusBadge { text: "Strict (127.0.0.1)"; variant: "success" }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "privacy"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 14
                                Text { text: "Privacy & Zero-Telemetry Policy"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "Operating System Telemetry"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                        Text { text: "NEXUS OS does not track keystrokes, queries, files, or usage metrics. Zero remote telemetry."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusBadge { text: "Permanently Disabled"; variant: "success" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Text { text: "API Credential Vault"; font.pixelSize: 13; color: NexusTheme.primaryText }
                                        Text { text: "AES-256-GCM hardware/software encrypted local secret storage (~/.config/nexus/vault.enc)"; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                    }
                                    NexusBadge { text: "AES-256 Encrypted"; variant: "success" }
                                }
                            }
                        }
                    }

                    // ----------------------------------------------------
                    // 20. UPDATES & 21. ABOUT NEXUS OS PANELS
                    // ----------------------------------------------------
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        visible: root.activeCategory === "updates"

                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 12
                                Text { text: "System Updates & Release Channels"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Current Version: 2026.1 (Stable Release)"; font.pixelSize: 12; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    NexusBadge { text: "Up to Date"; variant: "success" }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Release Channel"; font.pixelSize: 13; color: NexusTheme.primaryText; Layout.fillWidth: true }
                                    RowLayout {
                                        spacing: 6
                                        NexusButton {
                                            text: "Stable"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["updates.channel"] === "stable") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("updates.channel", "stable")
                                        }
                                        NexusButton {
                                            text: "Dev Preview"
                                            size: "small"
                                            variant: (hasBridge && settingsBridge.allSettings["updates.channel"] === "preview") ? "primary" : "secondary"
                                            onClicked: if (hasBridge) settingsBridge.setSetting("updates.channel", "preview")
                                        }
                                    }
                                }

                                NexusButton {
                                    text: "Check for System Updates (DNF)"
                                    variant: "primary"
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 14
                        visible: root.activeCategory === "about"

                        // Hero card
                        NexusCard {
                            Layout.fillWidth: true
                            RowLayout {
                                width: parent.width
                                spacing: 18

                                Rectangle {
                                    width: 64
                                    height: 64
                                    radius: NexusTheme.radiusLarge
                                    color: NexusTheme.accent
                                    Text {
                                        anchors.centerIn: parent
                                        text: "N"
                                        font.pixelSize: 36
                                        font.bold: true
                                        color: "#FFFFFF"
                                    }
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 4
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.os_name : "NEXUS OS"; font.pixelSize: 22; font.bold: true; color: NexusTheme.primaryText }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.os_version : "2026.1"; font.pixelSize: 13; color: NexusTheme.secondaryText }
                                    Text { text: "Developer-First, AI-Native Linux Operating System"; font.pixelSize: 11; color: NexusTheme.accent }
                                }

                                NexusBadge {
                                    text: "Fedora + KDE Native"; variant: "primary"
                                }
                            }
                        }

                        // Specs card
                        NexusCard {
                            Layout.fillWidth: true
                            ColumnLayout {
                                width: parent.width
                                spacing: 10
                                Text { text: "Hardware & Operating System Specifications"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Base Distribution"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.os_base : "Fedora Linux 41"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Desktop Environment"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.desktop_shell : "NEXUS Aether Desktop"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Kernel"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.kernel : "Linux 6.12"; font.pixelSize: 12; font.family: NexusTheme.fontMono; color: NexusTheme.primaryText }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "CPU Cores"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: (hasBridge ? settingsBridge.aboutInfo.cpu_cores : "8") + " logical cores"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Memory (RAM)"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.ram_total : "16.0 GB RAM"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Graphics / GPU"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.gpu : "NVIDIA GPU"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Architecture"; font.pixelSize: 12; color: NexusTheme.secondaryText; Layout.preferredWidth: 160 }
                                    Text { text: hasBridge ? settingsBridge.aboutInfo.architecture : "x86_64"; font.pixelSize: 12; font.family: NexusTheme.fontMono; color: NexusTheme.primaryText }
                                }
                            }
                        }
                    }

                    Item { height: 20; width: 1 }
                }
            }
        }
    }
}
