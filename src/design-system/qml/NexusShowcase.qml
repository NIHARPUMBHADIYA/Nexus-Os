import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    width: 1200
    height: 800

    property string activeSection: "overview"

    // Background Canvas
    Rectangle {
        anchors.fill: parent
        color: NexusTheme.background

        Behavior on color {
            ColorAnimation { duration: NexusTheme.durationNormal }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Window Header with controls, title, theme picker, accent picker, and reduced-motion switch
        NexusWindowHeader {
            Layout.fillWidth: true
            title: "NEXUS OS — Design System Showcase & Theme Studio"
            activeAppIcon: "💎"

            Row {
                spacing: NexusTheme.space3
                anchors.verticalCenter: parent.verticalCenter

                // Reduced Motion Switch
                NexusToggle {
                    type: "switch"
                    label: "Reduced Motion"
                    checked: NexusTheme.reducedMotion
                    onToggled: function(val) { NexusTheme.reducedMotion = val; }
                    anchors.verticalCenter: parent.verticalCenter
                }

                Rectangle {
                    width: 1
                    height: 20
                    color: NexusTheme.border
                    anchors.verticalCenter: parent.verticalCenter
                }

                // Curated Accent Pickers
                Row {
                    spacing: 4
                    anchors.verticalCenter: parent.verticalCenter

                    Repeater {
                        model: [
                            { name: "Indigo", color: "#6366F1" },
                            { name: "Emerald", color: "#10B981" },
                            { name: "Amber", color: "#F59E0B" },
                            { name: "Crimson", color: "#EF4444" },
                            { name: "Cyan", color: "#06B6D4" },
                            { name: "Violet", color: "#8B5CF6" },
                            { name: "Rose", color: "#F43F5E" }
                        ]

                        delegate: Rectangle {
                            width: 16
                            height: 16
                            radius: 8
                            color: modelData.color
                            border.color: NexusTheme.accent === modelData.color ? "#FFFFFF" : "transparent"
                            border.width: 1.5

                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: NexusTheme.setAccent(modelData.color)
                            }
                        }
                    }
                }

                Rectangle {
                    width: 1
                    height: 20
                    color: NexusTheme.border
                    anchors.verticalCenter: parent.verticalCenter
                }

                // Active Theme Display Pill
                NexusBadge {
                    text: NexusTheme.activeThemeId.toUpperCase()
                    status: "info"
                    variant: "tag"
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }

        // Sub-Header Theme Selector Bar
        Rectangle {
            Layout.fillWidth: true
            height: 48
            color: NexusTheme.secondaryBackground
            border.color: NexusTheme.border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: NexusTheme.space5
                anchors.rightMargin: NexusTheme.space5
                spacing: NexusTheme.space3

                Text {
                    text: "THEMES:"
                    font.pixelSize: 11
                    font.bold: true
                    font.family: NexusTheme.fontFamilyMono
                    color: NexusTheme.tertiaryText
                    Layout.alignment: Qt.AlignVCenter
                }

                // Horizontal Theme Switcher Pills
                Row {
                    spacing: 6
                    Layout.alignment: Qt.AlignVCenter

                    Repeater {
                        model: NexusTheme.availableThemes

                        delegate: Rectangle {
                            readonly property bool isCurrent: NexusTheme.activeThemeId === modelData.id
                            width: themeText.implicitWidth + 16
                            height: 28
                            radius: NexusTheme.radiusPill
                            color: isCurrent ? NexusTheme.accent : (mouseArea.containsMouse ? NexusTheme.surface : "transparent")
                            border.color: isCurrent ? NexusTheme.accent : NexusTheme.border
                            border.width: 1

                            Text {
                                id: themeText
                                anchors.centerIn: parent
                                text: modelData.name
                                font.pixelSize: 12
                                font.bold: isCurrent
                                font.family: NexusTheme.fontFamilyUI
                                color: isCurrent ? "#FFFFFF" : (mouseArea.containsMouse ? NexusTheme.primaryText : NexusTheme.secondaryText)
                            }

                            MouseArea {
                                id: mouseArea
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: NexusTheme.setTheme(modelData.id)
                            }
                        }
                    }
                }

                Item { Layout.fillWidth: true }
            }
        }

        // Main Content Area with Left Sidebar and Right Showcase Views
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            // Left Navigation Sidebar
            NexusSidebar {
                Layout.preferredWidth: 230
                Layout.fillHeight: true
                headerTitle: "SHOWCASE SECTIONS"
                items: [
                    { id: "overview", icon: "✨", label: "Tokens & Palette", badge: "" },
                    { id: "buttons", icon: "🔘", label: "Buttons & Actions", badge: "6" },
                    { id: "inputs", icon: "📝", label: "Inputs & Search", badge: "" },
                    { id: "cards", icon: "🗂️", label: "Cards & Modals", badge: "" },
                    { id: "navigation", icon: "🧭", label: "Tabs & Menus", badge: "" },
                    { id: "feedback", icon: "🔔", label: "Feedback & Status", badge: "4" },
                    { id: "dock", icon: "🚀", label: "Dock & Windows", badge: "" }
                ]

                onItemSelected: function(index, id, label) {
                    root.activeSection = id;
                }
            }

            // Right Main Panel
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: NexusTheme.background

                Flickable {
                    id: flickable
                    anchors.fill: parent
                    contentWidth: width
                    contentHeight: contentCol.implicitHeight + 64
                    clip: true

                    Column {
                        id: contentCol
                        width: parent.width - 64
                        anchors.horizontalCenter: parent.horizontalCenter
                        topPadding: 28
                        spacing: 24

                        // SECTION 1: OVERVIEW & TOKENS
                        Column {
                            visible: root.activeSection === "overview"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Design Tokens & Semantic Colors"
                                font.pixelSize: 22
                                font.bold: true
                                font.family: NexusTheme.fontFamilyUI
                                color: NexusTheme.primaryText
                            }

                            Text {
                                text: "Every surface, border, and control in NEXUS OS consumes strict semantic tokens. Switch themes above to preview live palette adaptations."
                                font.pixelSize: 13
                                font.family: NexusTheme.fontFamilyUI
                                color: NexusTheme.secondaryText
                            }

                            // Palette Grid
                            Grid {
                                columns: 4
                                spacing: 12
                                width: parent.width

                                Repeater {
                                    model: [
                                        { label: "Background", color: NexusTheme.background, text: NexusTheme.primaryText },
                                        { label: "Secondary Bg", color: NexusTheme.secondaryBackground, text: NexusTheme.primaryText },
                                        { label: "Surface", color: NexusTheme.surface, text: NexusTheme.primaryText },
                                        { label: "Elevated Surface", color: NexusTheme.elevatedSurface, text: NexusTheme.primaryText },
                                        { label: "Accent Color", color: NexusTheme.accent, text: "#FFFFFF" },
                                        { label: "Success Token", color: NexusTheme.success, text: "#FFFFFF" },
                                        { label: "Warning Token", color: NexusTheme.warning, text: "#FFFFFF" },
                                        { label: "Error Token", color: NexusTheme.error, text: "#FFFFFF" }
                                    ]

                                    delegate: Rectangle {
                                        width: (contentCol.width - 36) / 4
                                        height: 72
                                        radius: NexusTheme.radiusMedium
                                        color: modelData.color
                                        border.color: NexusTheme.border
                                        border.width: 1

                                        Column {
                                            anchors.centerIn: parent
                                            spacing: 4
                                            Text {
                                                text: modelData.label
                                                font.pixelSize: 12
                                                font.bold: true
                                                font.family: NexusTheme.fontFamilyUI
                                                color: modelData.text
                                                anchors.horizontalCenter: parent.horizontalCenter
                                            }
                                            Text {
                                                text: modelData.color
                                                font.pixelSize: 11
                                                font.family: NexusTheme.fontFamilyMono
                                                color: Qt.rgba(modelData.text.r, modelData.text.g, modelData.text.b, 0.75)
                                                anchors.horizontalCenter: parent.horizontalCenter
                                            }
                                        }
                                    }
                                }
                            }

                            // Corner Radius Scale
                            NexusCard {
                                width: parent.width
                                title: "Consistent Corner Radii System"
                                subtitle: "Harmonious geometry applied systematically across every UI component."

                                Row {
                                    spacing: 16
                                    topPadding: 8

                                    Repeater {
                                        model: [
                                            { name: "Small", radius: NexusTheme.radiusSmall, val: "10px" },
                                            { name: "Medium", radius: NexusTheme.radiusMedium, val: "14px" },
                                            { name: "Large", radius: NexusTheme.radiusLarge, val: "20px" },
                                            { name: "XL", radius: NexusTheme.radiusXL, val: "24px" },
                                            { name: "XXL", radius: NexusTheme.radiusXXL, val: "28px" },
                                            { name: "Pill", radius: NexusTheme.radiusPill, val: "9999px" }
                                        ]

                                        delegate: Column {
                                            spacing: 6
                                            Rectangle {
                                                width: 80
                                                height: 52
                                                radius: modelData.radius
                                                color: NexusTheme.secondaryBackground
                                                border.color: NexusTheme.accent
                                                border.width: 1.5

                                                Text {
                                                    anchors.centerIn: parent
                                                    text: modelData.val
                                                    font.pixelSize: 11
                                                    font.family: NexusTheme.fontFamilyMono
                                                    color: NexusTheme.accent
                                                }
                                            }
                                            Text {
                                                text: modelData.name
                                                font.pixelSize: 11
                                                color: NexusTheme.secondaryText
                                                anchors.horizontalCenter: parent.horizontalCenter
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // SECTION 2: BUTTONS & ACTIONS
                        Column {
                            visible: root.activeSection === "buttons"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Buttons & Action Controls"
                                font.pixelSize: 22
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            NexusCard {
                                width: parent.width
                                title: "Button Variants"
                                subtitle: "Primary, secondary, subtle, outline, danger, and ghost variations."

                                Row {
                                    spacing: 12
                                    topPadding: 8

                                    NexusButton { text: "Primary Action"; variant: "primary" }
                                    NexusButton { text: "Secondary"; variant: "secondary" }
                                    NexusButton { text: "Subtle Accent"; variant: "subtle" }
                                    NexusButton { text: "Outline"; variant: "outline" }
                                    NexusButton { text: "Destructive"; variant: "danger" }
                                    NexusButton { text: "Ghost"; variant: "ghost" }
                                }
                            }

                            NexusCard {
                                width: parent.width
                                title: "Sizes, Shapes & Loading States"

                                Row {
                                    spacing: 12
                                    topPadding: 8

                                    NexusButton { text: "Small"; size: "sm"; variant: "primary" }
                                    NexusButton { text: "Medium"; size: "md"; variant: "primary" }
                                    NexusButton { text: "Large Action"; size: "lg"; variant: "primary" }
                                    NexusButton { text: "Pill Button"; radiusMode: "pill"; variant: "primary" }
                                    NexusButton { text: "Loading..."; loading: true; variant: "primary" }
                                    NexusButton { text: "Disabled"; disabled: true; variant: "primary" }
                                }
                            }

                            NexusCard {
                                width: parent.width
                                title: "Icon Buttons"
                                subtitle: "Compact icon actions with built-in tooltips and hover feedback."

                                Row {
                                    spacing: 16
                                    topPadding: 8

                                    NexusIconButton { iconText: "⚙"; tooltipText: "Settings" }
                                    NexusIconButton { iconText: "🔍"; tooltipText: "Search Spotlight" }
                                    NexusIconButton { iconText: "📁"; tooltipText: "File Manager" }
                                    NexusIconButton { iconText: "⚡"; variant: "accent"; active: true; tooltipText: "AI Engine Active" }
                                    NexusIconButton { iconText: "🗑"; variant: "danger"; tooltipText: "Delete Environment" }
                                }
                            }
                        }

                        // SECTION 3: INPUTS & SEARCH
                        Column {
                            visible: root.activeSection === "inputs"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Form Inputs & Search Fields"
                                font.pixelSize: 22
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            NexusCard {
                                width: parent.width
                                title: "Universal Spotlight Search Field"
                                subtitle: "Optimized for fast keyboard input, category filters, and shortcut cues."

                                Column {
                                    spacing: 12
                                    topPadding: 8

                                    NexusSearchField {
                                        placeholderText: "Search projects, files, commands, AI models (Win+Space)..."
                                        shortcutHint: "Win+Space"
                                    }
                                }
                            }

                            NexusCard {
                                width: parent.width
                                title: "Text Inputs & Validations"

                                Row {
                                    spacing: 16
                                    topPadding: 8

                                    NexusInput {
                                        placeholderText: "Project name..."
                                        leadingIcon: "📦"
                                    }

                                    NexusInput {
                                        placeholderText: "API Token / Key..."
                                        isPassword: true
                                        leadingIcon: "🔑"
                                    }

                                    NexusInput {
                                        placeholderText: "Validation error..."
                                        text: "invalid-branch-name"
                                        errorText: "Git branch contains illegal characters"
                                    }
                                }
                            }
                        }

                        // SECTION 4: CARDS & MODALS
                        Column {
                            visible: root.activeSection === "cards"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Cards, Surfaces & Dialogs"
                                font.pixelSize: 22
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            Row {
                                spacing: 16

                                NexusCard {
                                    width: (contentCol.width - 16) / 2
                                    title: "Interactive Workspace Card"
                                    subtitle: "Hover over this card to preview elevation transitions."
                                    interactive: true
                                    accentHeaderColor: NexusTheme.accent

                                    Column {
                                        spacing: 6
                                        Text {
                                            text: "Rust • main • Clean working directory"
                                            font.pixelSize: 12
                                            font.family: NexusTheme.fontFamilyMono
                                            color: NexusTheme.secondaryText
                                        }
                                        NexusBadge { text: "Container Running"; status: "success" }
                                    }
                                }

                                NexusCard {
                                    width: (contentCol.width - 16) / 2
                                    title: "Modal Dialog Trigger"
                                    subtitle: "Test full-screen backdrop blur and action dispatch."

                                    NexusButton {
                                        text: "Open Sample Modal Dialog"
                                        variant: "primary"
                                        onClicked: sampleDialog.visibleState = true
                                    }
                                }
                            }
                        }

                        // SECTION 5: NAVIGATION & TABS
                        Column {
                            visible: root.activeSection === "navigation"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Tabs, Menus & Navigation Controls"
                                font.pixelSize: 22
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            NexusCard {
                                width: parent.width
                                title: "Tab Variants"
                                subtitle: "Segmented controls, pill tabs, and underline indicators."

                                Column {
                                    spacing: 16
                                    topPadding: 8

                                    NexusTabs {
                                        variant: "segmented"
                                        model: ["Source Code", "Git Graph", "Containers", "Logs"]
                                    }

                                    NexusTabs {
                                        variant: "pills"
                                        model: ["All Models", "Local (Ollama)", "Cloud (API)", "Fine-Tuning"]
                                    }

                                    NexusTabs {
                                        variant: "underline"
                                        model: ["Overview", "Dependencies", "Environment", "Security Audit"]
                                    }
                                }
                            }

                            NexusCard {
                                width: parent.width
                                title: "Dropdown & Context Menus"
                                subtitle: "Keyboard-friendly menus with separators and shortcut hints."

                                NexusMenu {
                                    items: [
                                        { text: "Create New Workspace", icon: "📁", shortcut: "Ctrl+N" },
                                        { text: "Open in Cursor / VS Code", icon: "💻", shortcut: "Ctrl+O" },
                                        { separator: true },
                                        { text: "Spawn Local Model Session", icon: "🤖", shortcut: "Ctrl+M" },
                                        { text: "Delete Workspace", icon: "🗑", shortcut: "Del" }
                                    ]
                                }
                            }
                        }

                        // SECTION 6: FEEDBACK & STATUS
                        Column {
                            visible: root.activeSection === "feedback"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Notifications, Progress & Status Indicators"
                                font.pixelSize: 22
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            NexusCard {
                                width: parent.width
                                title: "Notifications / Toasts"
                                subtitle: "Semantic alerts with dismiss capability and status cues."

                                Column {
                                    spacing: 12
                                    topPadding: 8

                                    NexusNotification {
                                        variant: "info"
                                        title: "AI Model Downloading"
                                        message: "Downloading qwen2.5-coder:7b into local Ollama storage (4.2GB)."
                                    }

                                    NexusNotification {
                                        variant: "success"
                                        title: "Build Succeeded"
                                        message: "Cargo workspace built with 0 warnings in 3.42s."
                                    }

                                    NexusNotification {
                                        variant: "warning"
                                        title: "High VRAM Utilization"
                                        message: "VRAM at 88%. Background model unload will trigger in 10 minutes."
                                    }

                                    NexusNotification {
                                        variant: "error"
                                        title: "Container Port Collision"
                                        message: "Port 5432 is already bound by host PostgreSQL service."
                                    }
                                }
                            }

                            NexusCard {
                                width: parent.width
                                title: "Progress Indicators"
                                subtitle: "Linear bars (determinate/indeterminate) and circular spinners."

                                Row {
                                    spacing: 24
                                    topPadding: 8

                                    Column {
                                        spacing: 12
                                        Text { text: "Determinate (70%):"; color: NexusTheme.secondaryText; font.pixelSize: 12 }
                                        NexusProgress { variant: "linear"; value: 0.7 }

                                        Text { text: "Indeterminate Wave:"; color: NexusTheme.secondaryText; font.pixelSize: 12 }
                                        NexusProgress { variant: "linear"; indeterminate: true }
                                    }

                                    Column {
                                        spacing: 12
                                        Text { text: "Circular Spinner:"; color: NexusTheme.secondaryText; font.pixelSize: 12 }
                                        NexusProgress { variant: "spinner"; spinnerSize: 36 }
                                    }
                                }
                            }

                            NexusCard {
                                width: parent.width
                                title: "Status Badges & Tags"

                                Row {
                                    spacing: 12
                                    topPadding: 8

                                    NexusBadge { text: "Running"; status: "success" }
                                    NexusBadge { text: "Compiling"; status: "warning" }
                                    NexusBadge { text: "Failed"; status: "error" }
                                    NexusBadge { text: "Ollama Active"; status: "info" }
                                    NexusBadge { text: "v1.84.0"; variant: "tag"; status: "neutral" }
                                    NexusBadge { text: "12"; variant: "count"; status: "warning" }
                                }
                            }
                        }

                        // SECTION 7: DOCK & WINDOWS
                        Column {
                            visible: root.activeSection === "dock"
                            width: parent.width
                            spacing: 16

                            Text {
                                text: "Desktop Shell: Floating Dock & Window Components"
                                font.pixelSize: 22
                                font.bold: true
                                color: NexusTheme.primaryText
                            }

                            NexusCard {
                                width: parent.width
                                title: "Floating Dock Simulator"
                                subtitle: "Hover over application icons to observe physics-based lift, badges, and running state indicators."

                                Rectangle {
                                    width: dockRow.implicitWidth + 32
                                    height: 72
                                    radius: NexusTheme.radiusXL
                                    color: NexusTheme.elevatedSurface
                                    border.color: NexusTheme.border
                                    border.width: 1
                                    anchors.horizontalCenter: parent.horizontalCenter

                                    Row {
                                        id: dockRow
                                        anchors.centerIn: parent
                                        spacing: 12

                                        NexusDockItem { iconText: "🚀"; appName: "App Launcher"; isRunning: true }
                                        NexusDockItem { iconText: "💻"; appName: "Cursor IDE"; isRunning: true; badgeCount: 2 }
                                        NexusDockItem { iconText: "⌨"; appName: "Terminal"; isRunning: true }
                                        NexusDockItem { iconText: "📁"; appName: "Developer Hub"; isRunning: false }
                                        NexusDockItem { iconText: "🌐"; appName: "Browser"; isRunning: false }
                                        NexusDockItem { iconText: "🤖"; appName: "AI Core Manager"; isRunning: true; badgeCount: 1 }
                                        NexusDockItem { iconText: "⚙"; appName: "System Settings"; isRunning: false }
                                    }
                                }
                            }
                        }

                        Item { height: 32 }
                    }
                }
            }
        }
    }

    // Sample Modal Dialog
    NexusDialog {
        id: sampleDialog
        title: "Create Isolated Development Container"
        message: "This will provision a rootless Podman container environment with Rust, Node.js, and Python pre-installed. The host OS filesystem remains pristine."
        primaryActionText: "Provision Container"
        cancelActionText: "Cancel"

        onConfirmed: sampleDialog.visibleState = false
        onCancelled: sampleDialog.visibleState = false
    }
}
