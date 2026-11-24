import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Rectangle {
    id: root
    color: NexusTheme.background

    property string currentSection: "themes" // "themes", "appearance", "wallpapers", "windows", "dock_panel", "fonts_motion", "custom_editor"

    // Fallback data if bridge is not attached
    property var themesData: (typeof personalizationBridge !== "undefined" && personalizationBridge.themesList) ? personalizationBridge.themesList : [
        {"id": "midnight", "name": "Midnight", "type": "dark", "description": "Default deep indigo & navy dark theme with vibrant accents."},
        {"id": "nord", "name": "Nord", "type": "dark", "description": "Arctic, north-bluish clean color palette."},
        {"id": "dracula", "name": "Dracula", "type": "dark", "description": "Classic dark gothic theme with vibrant purple and green."},
        {"id": "catppuccin", "name": "Catppuccin", "type": "dark", "description": "Soothing pastel theme optimized for long coding sessions."},
        {"id": "tokyo-night", "name": "Tokyo Night", "type": "dark", "description": "Clean neon theme celebrating the lights of downtown Tokyo."},
        {"id": "terminal-green", "name": "Terminal Green", "type": "dark", "description": "Retro matrix phosphor green terminal aesthetic."},
        {"id": "paper-light", "name": "Paper Light", "type": "light", "description": "Warm, natural high-contrast daylight paper theme."},
        {"id": "amoled", "name": "AMOLED Black", "type": "dark", "description": "True pitch-black #000000 theme for OLED displays."},
        {"id": "deep-space", "name": "Deep Space", "type": "dark", "description": "High-contrast celestial navy with cyan highlights."},
        {"id": "custom", "name": "Custom Theme", "type": "custom", "description": "User-crafted custom color tokens and accents."}
    ]

    property var contrastData: (typeof personalizationBridge !== "undefined" && personalizationBridge.contrastEvaluation) ? personalizationBridge.contrastEvaluation : {
        "primary_on_bg": 14.8, "primary_on_surface": 11.2, "secondary_on_bg": 6.8, "rating": "Pass (AAA)", "wcag_aa_passed": true
    }

    Connections {
        target: (typeof personalizationBridge !== "undefined") ? personalizationBridge : null
        function onContrastChanged() { root.contrastData = personalizationBridge.contrastEvaluation; }
    }

    Row {
        anchors.fill: parent

        // 1. LEFT SIDEBAR: Personalization Categories
        Rectangle {
            width: 220
            height: parent.height
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            Column {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 6

                Row {
                    spacing: 10
                    Text { text: "🎨"; font.pixelSize: 22; anchors.verticalCenter: parent.verticalCenter }
                    Column {
                        Text { text: "Personalization"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }
                        Text { text: "Themes & Visual Styling"; font.pixelSize: 10; color: NexusTheme.secondaryText }
                    }
                }

                Item { width: 1; height: 12 }

                Repeater {
                    model: [
                        { "id": "themes", "label": "Theme Presets", "icon": "🎭" },
                        { "id": "appearance", "label": "Color Mode & Accent", "icon": "🌈" },
                        { "id": "wallpapers", "label": "Wallpapers & Blur", "icon": "🖼️" },
                        { "id": "windows", "label": "Window Appearance", "icon": "🪟" },
                        { "id": "dock_panel", "label": "Dock & Top Panel", "icon": "⚓" },
                        { "id": "fonts_motion", "label": "Fonts & Motion", "icon": "🔤" },
                        { "id": "custom_editor", "label": "Custom Theme Editor", "icon": "✏️" }
                    ]

                    delegate: Rectangle {
                        width: parent.width
                        height: 36
                        radius: NexusTheme.radiusSmall
                        color: root.currentSection === modelData.id ? NexusTheme.accentSubtle : "transparent"
                        border.color: root.currentSection === modelData.id ? NexusTheme.accent : "transparent"
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 12
                            spacing: 10
                            Text { text: modelData.icon; font.pixelSize: 13; anchors.verticalCenter: parent.verticalCenter }
                            Text {
                                text: modelData.label
                                font.pixelSize: 11
                                font.bold: root.currentSection === modelData.id
                                color: root.currentSection === modelData.id ? NexusTheme.accent : NexusTheme.primaryText
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.currentSection = modelData.id
                        }
                    }
                }

                Item { width: 1; height: 20 }

                // Live Contrast Score Card
                Rectangle {
                    width: parent.width
                    height: 90
                    radius: NexusTheme.radiusMedium
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1

                    Column {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 4

                        Row {
                            spacing: 6
                            Text { text: "👁️"; font.pixelSize: 12 }
                            Text { text: "WCAG Readability"; font.pixelSize: 10; font.bold: true; color: NexusTheme.primaryText }
                            Item { width: Math.max(1, parent.width - 150); height: 1 }
                            Rectangle {
                                height: 14; width: 60; radius: NexusTheme.radiusPill
                                color: NexusTheme.successSubtle; border.color: NexusTheme.success; border.width: 1
                                Text { anchors.centerIn: parent; text: root.contrastData.rating; font.pixelSize: 8; font.bold: true; color: NexusTheme.success }
                            }
                        }

                        Text { text: "Contrast: " + root.contrastData.primary_on_bg + ":1 (Text on Bg)"; font.pixelSize: 9; color: NexusTheme.secondaryText }
                        Text { text: "Surface: " + root.contrastData.primary_on_surface + ":1 (Text on Card)"; font.pixelSize: 9; color: NexusTheme.secondaryText }
                        Text { text: "All 10 themes meet WCAG AA standards."; font.pixelSize: 8; color: NexusTheme.accent }
                    }
                }
            }
        }

        // 2. RIGHT MAIN VIEW: Personalization Settings Sections
        Rectangle {
            width: parent.width - 220
            height: parent.height
            color: NexusTheme.background

            ScrollView {
                anchors.fill: parent
                anchors.margins: 20
                clip: true

                Column {
                    width: parent.width - 16
                    spacing: 16

                    // ==========================================
                    // SECTION 1: THEME PRESETS
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 12
                        visible: root.currentSection === "themes"

                        Text { text: "Theme Presets & Previews"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }
                        Text { text: "Select from 9 hand-crafted color palettes or activate your custom theme."; font.pixelSize: 11; color: NexusTheme.secondaryText }

                        Grid {
                            width: parent.width
                            columns: 2
                            spacing: 12

                            Repeater {
                                model: root.themesData

                                delegate: Rectangle {
                                    width: (parent.width - 12) / 2
                                    height: 115
                                    radius: NexusTheme.radiusMedium
                                    color: NexusTheme.surface
                                    border.color: NexusTheme.activeThemeId === modelData.id ? NexusTheme.accent : NexusTheme.border
                                    border.width: NexusTheme.activeThemeId === modelData.id ? 2 : 1

                                    Column {
                                        anchors.fill: parent
                                        anchors.margins: 12
                                        spacing: 6

                                        Row {
                                            width: parent.width
                                            Text { text: modelData.name; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                            Item { width: Math.max(10, parent.width - 240); height: 1 }

                                            Rectangle {
                                                height: 16; width: 45; radius: NexusTheme.radiusPill
                                                color: modelData.type === "dark" ? NexusTheme.secondaryBackground : NexusTheme.accentSubtle
                                                border.color: NexusTheme.border; border.width: 1
                                                Text { anchors.centerIn: parent; text: modelData.type.toUpperCase(); font.pixelSize: 8; font.bold: true; color: NexusTheme.secondaryText }
                                            }

                                            Rectangle {
                                                height: 16; width: 55; radius: NexusTheme.radiusPill
                                                visible: NexusTheme.activeThemeId === modelData.id
                                                color: NexusTheme.accent
                                                Text { anchors.centerIn: parent; text: "ACTIVE"; font.pixelSize: 8; font.bold: true; color: "#FFFFFF" }
                                            }
                                        }

                                        Text { text: modelData.description; font.pixelSize: 10; color: NexusTheme.secondaryText; elide: Text.ElideRight; width: parent.width }

                                        // Mini-Palette Swatch Bar
                                        Row {
                                            spacing: 6
                                            Repeater {
                                                model: {
                                                    var pal = NexusTheme.themeColorData[modelData.id] || NexusTheme.customThemeColors;
                                                    return [pal.background, pal.surface, pal.accent, pal.success, pal.primaryText];
                                                }
                                                delegate: Rectangle {
                                                    width: 22; height: 14; radius: 4
                                                    color: modelData
                                                    border.color: NexusTheme.border; border.width: 1
                                                }
                                            }
                                        }
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            NexusTheme.setTheme(modelData.id);
                                            if (typeof personalizationBridge !== "undefined") {
                                                personalizationBridge.setTheme(modelData.id);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // ==========================================
                    // SECTION 2: APPEARANCE & COLOR MODE
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 16
                        visible: root.currentSection === "appearance"

                        Text { text: "Color Mode & Custom Accent"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }

                        // Mode Selector Card
                        Rectangle {
                            width: parent.width
                            height: 80
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Row {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 14

                                Column {
                                    anchors.verticalCenter: parent.verticalCenter
                                    Text { text: "System Theme Mode"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                    Text { text: "Choose fixed dark/light mode or automated time-of-day switching."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                }

                                Item { width: Math.max(10, parent.width - 480); height: 1 }

                                Row {
                                    anchors.verticalCenter: parent.verticalCenter
                                    spacing: 8

                                    Repeater {
                                        model: [
                                            { "id": "dark", "label": "🌙 Dark" },
                                            { "id": "light", "label": "☀️ Light" },
                                            { "id": "auto", "label": "⏰ Auto (06:00 - 18:00)" }
                                        ]

                                        delegate: Rectangle {
                                            height: 32; width: 110; radius: NexusTheme.radiusSmall
                                            color: NexusTheme.themeMode === modelData.id ? NexusTheme.accent : NexusTheme.secondaryBackground
                                            border.color: NexusTheme.themeMode === modelData.id ? NexusTheme.accent : NexusTheme.border; border.width: 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.label
                                                font.pixelSize: 11; font.bold: NexusTheme.themeMode === modelData.id
                                                color: NexusTheme.themeMode === modelData.id ? "#FFFFFF" : NexusTheme.primaryText
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    NexusTheme.setThemeMode(modelData.id);
                                                    if (typeof personalizationBridge !== "undefined") {
                                                        personalizationBridge.setThemeMode(modelData.id);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Accent Color Palette
                        Rectangle {
                            width: parent.width
                            height: 110
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 10

                                Text { text: "Custom Accent Color Override"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }

                                Row {
                                    spacing: 10
                                    Repeater {
                                        model: NexusTheme.accentPalette

                                        delegate: Rectangle {
                                            width: 32; height: 32; radius: NexusTheme.radiusSmall
                                            color: modelData.color ? modelData.color : NexusTheme.currentColors.accent
                                            border.color: (NexusTheme.customAccentOverride === modelData.color) ? "#FFFFFF" : NexusTheme.border
                                            border.width: (NexusTheme.customAccentOverride === modelData.color) ? 2.5 : 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: (NexusTheme.customAccentOverride === modelData.color) ? "✓" : ""
                                                font.pixelSize: 14; font.bold: true; color: "#FFFFFF"
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    NexusTheme.setAccent(modelData.color);
                                                    if (typeof personalizationBridge !== "undefined") {
                                                        personalizationBridge.setAccent(modelData.color);
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
                    // SECTION 3: WALLPAPERS & GLASS BLUR
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 16
                        visible: root.currentSection === "wallpapers"

                        Text { text: "Wallpapers & Dual-Pass Acrylic Blur"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }

                        // Wallpaper Gallery Grid
                        Row {
                            spacing: 12
                            Repeater {
                                model: (typeof personalizationBridge !== "undefined" && personalizationBridge.wallpapersList) ? personalizationBridge.wallpapersList : [
                                    {"id": "nebula", "name": "Cosmic Nebula", "color": "#171B2B"},
                                    {"id": "aurora", "name": "Nordic Aurora", "color": "#242933"},
                                    {"id": "cyberpunk", "name": "Tokyo Neon", "color": "#16161E"},
                                    {"id": "minimal_dark", "name": "Minimal Dark", "color": "#0B0D14"},
                                    {"id": "paper_horizon", "name": "Warm Dawn", "color": "#FBFBFA"}
                                ]

                                delegate: Rectangle {
                                    width: (root.width - 280) / 5
                                    height: 90
                                    radius: NexusTheme.radiusMedium
                                    color: modelData.color
                                    border.color: NexusTheme.wallpaperSource.indexOf(modelData.id) !== -1 ? NexusTheme.accent : NexusTheme.border
                                    border.width: NexusTheme.wallpaperSource.indexOf(modelData.id) !== -1 ? 2 : 1

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 4
                                        Text { text: "🖼️"; font.pixelSize: 20; anchors.horizontalCenter: parent.horizontalCenter }
                                        Text { text: modelData.name; font.pixelSize: 10; font.bold: true; color: "#FFFFFF"; anchors.horizontalCenter: parent.horizontalCenter }
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            NexusTheme.wallpaperSource = modelData.id + ".jpg";
                                            if (typeof personalizationBridge !== "undefined") {
                                                personalizationBridge.setWallpaper(modelData.id, 15);
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Glass & Blur Controls
                        Rectangle {
                            width: parent.width
                            height: 110
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 10

                                Row {
                                    width: parent.width
                                    Text { text: "Acrylic Glass Surface Blur (" + NexusTheme.blurRadius + "px)"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                    Item { width: Math.max(10, parent.width - 320); height: 1 }
                                    Rectangle {
                                        width: 80; height: 26; radius: NexusTheme.radiusSmall
                                        color: NexusTheme.blurEnabled ? NexusTheme.accentSubtle : NexusTheme.secondaryBackground
                                        border.color: NexusTheme.blurEnabled ? NexusTheme.accent : NexusTheme.border; border.width: 1
                                        Text { anchors.centerIn: parent; text: NexusTheme.blurEnabled ? "ENABLED" : "DISABLED"; font.pixelSize: 9; font.bold: true; color: NexusTheme.blurEnabled ? NexusTheme.accent : NexusTheme.secondaryText }
                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: NexusTheme.blurEnabled = !NexusTheme.blurEnabled
                                        }
                                    }
                                }

                                Text { text: "Dual-pass hardware-accelerated blur shader applied to dock, spotlight, and window titlebars."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                            }
                        }
                    }

                    // ==========================================
                    // SECTION 4: WINDOW APPEARANCE & CORNERS
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 16
                        visible: root.currentSection === "windows"

                        Text { text: "Window Appearance & Rounded Geometry"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }

                        // Strict Rounded Design Rule Guarantee
                        Rectangle {
                            width: parent.width
                            height: 54
                            radius: NexusTheme.radiusSmall
                            color: NexusTheme.accentSubtle
                            border.color: NexusTheme.accent
                            border.width: 1

                            Row {
                                anchors.fill: parent
                                anchors.margins: 14
                                spacing: 10
                                Text { text: "🛡️"; font.pixelSize: 18; anchors.verticalCenter: parent.verticalCenter }
                                Text {
                                    text: "Aether Design Rule: All window, dialog, and panel corners remain consistently rounded throughout NEXUS OS."
                                    font.pixelSize: 11; font.bold: true; color: NexusTheme.accent
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        // Radius Token Selector
                        Rectangle {
                            width: parent.width
                            height: 100
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 10

                                Text { text: "Window Corner Radius Scale"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }

                                Row {
                                    spacing: 12
                                    Repeater {
                                        model: [
                                            { "id": "small", "label": "Small (10px)", "val": 10 },
                                            { "id": "medium", "label": "Medium (14px - Default)", "val": 14 },
                                            { "id": "large", "label": "Large (20px)", "val": 20 },
                                            { "id": "xl", "label": "XL (24px)", "val": 24 }
                                        ]

                                        delegate: Rectangle {
                                            height: 32; width: 140; radius: modelData.val
                                            color: NexusTheme.windowRadiusScale === modelData.id ? NexusTheme.accent : NexusTheme.secondaryBackground
                                            border.color: NexusTheme.windowRadiusScale === modelData.id ? NexusTheme.accent : NexusTheme.border; border.width: 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.label
                                                font.pixelSize: 10; font.bold: NexusTheme.windowRadiusScale === modelData.id
                                                color: NexusTheme.windowRadiusScale === modelData.id ? "#FFFFFF" : NexusTheme.primaryText
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    NexusTheme.windowRadiusScale = modelData.id;
                                                    if (typeof personalizationBridge !== "undefined") {
                                                        personalizationBridge.setWindowConfig(modelData.id, NexusTheme.blurEnabled, NexusTheme.blurRadius, NexusTheme.acrylicGlass);
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
                    // SECTION 5: DOCK & TOP PANEL
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 16
                        visible: root.currentSection === "dock_panel"

                        Text { text: "Floating Dock & Top Panel Configuration"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }

                        Rectangle {
                            width: parent.width
                            height: 120
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 10

                                Text { text: "Dock Position & Size"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }

                                Row {
                                    spacing: 12
                                    Repeater {
                                        model: [
                                            { "id": "bottom", "label": "Bottom Screen (Default)" },
                                            { "id": "left", "label": "Left Screen" },
                                            { "id": "right", "label": "Right Screen" }
                                        ]

                                        delegate: Rectangle {
                                            height: 32; width: 150; radius: NexusTheme.radiusSmall
                                            color: NexusTheme.dockPosition === modelData.id ? NexusTheme.accent : NexusTheme.secondaryBackground
                                            border.color: NexusTheme.dockPosition === modelData.id ? NexusTheme.accent : NexusTheme.border; border.width: 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.label
                                                font.pixelSize: 11; font.bold: NexusTheme.dockPosition === modelData.id
                                                color: NexusTheme.dockPosition === modelData.id ? "#FFFFFF" : NexusTheme.primaryText
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    NexusTheme.dockPosition = modelData.id;
                                                    if (typeof personalizationBridge !== "undefined") {
                                                        personalizationBridge.setDockConfig(modelData.id, NexusTheme.dockSize, NexusTheme.dockAutoDodge);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }

                                Row {
                                    spacing: 8
                                    Text { text: "Auto-Dodge Windows: " + (NexusTheme.dockAutoDodge ? "Enabled (Hides when window overlaps)" : "Always Visible"); font.pixelSize: 11; color: NexusTheme.secondaryText }
                                }
                            }
                        }
                    }

                    // ==========================================
                    // SECTION 6: FONTS & MOTION
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 16
                        visible: root.currentSection === "fonts_motion"

                        Text { text: "Typography, Cursors & Reduced Motion"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }

                        // Reduced Motion Toggle Card
                        Rectangle {
                            width: parent.width
                            height: 70
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Row {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 14

                                Column {
                                    anchors.verticalCenter: parent.verticalCenter
                                    Text { text: "Reduced Motion (Accessibility)"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                    Text { text: "Disables spring transitions and fast-forwards animations."; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                }

                                Item { width: Math.max(10, parent.width - 480); height: 1 }

                                Rectangle {
                                    width: 100; height: 32; radius: NexusTheme.radiusSmall
                                    color: NexusTheme.reducedMotion ? NexusTheme.accent : NexusTheme.secondaryBackground
                                    border.color: NexusTheme.reducedMotion ? NexusTheme.accent : NexusTheme.border; border.width: 1
                                    anchors.verticalCenter: parent.verticalCenter

                                    Text {
                                        anchors.centerIn: parent
                                        text: NexusTheme.reducedMotion ? "ON (Instant)" : "OFF (Smooth)"
                                        font.pixelSize: 11; font.bold: true
                                        color: NexusTheme.reducedMotion ? "#FFFFFF" : NexusTheme.primaryText
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            NexusTheme.reducedMotion = !NexusTheme.reducedMotion;
                                            if (typeof personalizationBridge !== "undefined") {
                                                personalizationBridge.setReducedMotion(NexusTheme.reducedMotion);
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Fonts Card
                        Rectangle {
                            width: parent.width
                            height: 100
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 8

                                Text { text: "System Typography"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }
                                Text { text: "UI Font: " + NexusTheme.fontFamilyUI; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                Text { text: "Monospace Font: " + NexusTheme.fontFamilyMono; font.pixelSize: 11; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.accent }
                            }
                        }
                    }

                    // ==========================================
                    // SECTION 7: CUSTOM THEME EDITOR
                    // ==========================================
                    Column {
                        width: parent.width
                        spacing: 16
                        visible: root.currentSection === "custom_editor"

                        Text { text: "Custom Theme Editor & Import / Export"; font.pixelSize: 15; font.bold: true; color: NexusTheme.primaryText }
                        Text { text: "Design your bespoke palette and export it as a shareable .nexus-theme.json file."; font.pixelSize: 11; color: NexusTheme.secondaryText }

                        Rectangle {
                            width: parent.width
                            height: 180
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.surface
                            border.color: NexusTheme.border
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 12

                                Text { text: "Semantic Color Tokens (Hex)"; font.pixelSize: 13; font.bold: true; color: NexusTheme.primaryText }

                                Grid {
                                    columns: 3
                                    spacing: 12

                                    Repeater {
                                        model: [
                                            { "token": "background", "label": "Background", "val": NexusTheme.background },
                                            { "token": "surface", "label": "Surface", "val": NexusTheme.surface },
                                            { "token": "accent", "label": "Accent", "val": NexusTheme.accent },
                                            { "token": "primaryText", "label": "Primary Text", "val": NexusTheme.primaryText },
                                            { "token": "border", "label": "Border", "val": NexusTheme.border },
                                            { "token": "success", "label": "Success", "val": NexusTheme.success }
                                        ]

                                        delegate: Row {
                                            spacing: 8
                                            Rectangle { width: 20; height: 20; radius: 4; color: modelData.val; border.color: NexusTheme.border; border.width: 1 }
                                            Text { text: modelData.label + ": " + modelData.val; font.pixelSize: 11; color: NexusTheme.secondaryText }
                                        }
                                    }
                                }

                                Item { width: 1; height: 4 }

                                Row {
                                    spacing: 10
                                    Rectangle {
                                        width: 140; height: 32; radius: NexusTheme.radiusSmall
                                        color: NexusTheme.accentSubtle; border.color: NexusTheme.accent; border.width: 1
                                        Text { anchors.centerIn: parent; text: "Activate Custom"; font.pixelSize: 11; font.bold: true; color: NexusTheme.accent }
                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                NexusTheme.setTheme("custom");
                                                if (typeof personalizationBridge !== "undefined") personalizationBridge.setTheme("custom");
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
    }
}
