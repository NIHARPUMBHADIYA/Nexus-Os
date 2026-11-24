pragma Singleton
import QtQuick

QtObject {
    id: theme

    // Corner Radii Tokens
    readonly property int radiusSmall: 10
    readonly property int radiusMedium: 14
    readonly property int radiusLarge: 20
    readonly property int radiusXL: 24
    readonly property int radiusXXL: 28
    readonly property int radiusPill: 9999

    // Spacing Tokens
    readonly property int space1: 2
    readonly property int space2: 4
    readonly property int space3: 8
    readonly property int space4: 12
    readonly property int space5: 16
    readonly property int space6: 20
    readonly property int space7: 24
    readonly property int space8: 32
    readonly property int space9: 40
    readonly property int space10: 48
    readonly property int space12: 64

    // Motion & Animation Tokens
    property bool reducedMotion: false
    readonly property int durationFast: reducedMotion ? 0 : 120
    readonly property int durationNormal: reducedMotion ? 0 : 180
    readonly property int durationSlow: reducedMotion ? 0 : 280

    // Typography Fonts
    readonly property string fontFamilyUI: "Inter, 'Segoe UI', system-ui, sans-serif"
    readonly property string fontFamilyMono: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"

    // Active Theme State
    property string activeThemeId: "midnight"
    property string customAccentOverride: ""
    property string themeMode: "dark" // "dark", "light", "auto"
    property real fontScale: 1.0
    property string fontUI: "Inter, 'Segoe UI', system-ui, sans-serif"
    property string fontMono: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"
    property string dockPosition: "bottom" // "bottom", "left", "right"
    property string dockSize: "medium"     // "small", "medium", "large"
    property bool dockAutoDodge: true
    property real panelOpacity: 0.85
    property string panelClockFormat: "24h"
    property string windowRadiusScale: "medium" // "small", "medium", "large", "xl"
    property bool blurEnabled: true
    property int blurRadius: 20
    property bool acrylicGlass: true
    property string iconTheme: "aether-default"
    property string cursorTheme: "aether-glow"
    property string wallpaperSource: "nebula.jpg"

    // Custom Theme Token Overrides
    property var customThemeColors: {
        "background": "#0D1117",
        "secondaryBackground": "#161B22",
        "surface": "#21262D",
        "elevatedSurface": "#30363D",
        "border": "#30363D",
        "borderFocus": "#58A6FF",
        "primaryText": "#F0F6FC",
        "secondaryText": "#8B949E",
        "tertiaryText": "#6E7681",
        "accent": "#58A6FF",
        "accentHover": "#388BFD",
        "accentSubtle": "#1F3554",
        "success": "#3FB950",
        "successSubtle": "#0F3327",
        "warning": "#D29922",
        "warningSubtle": "#3B2B11",
        "error": "#F85149",
        "errorSubtle": "#3E1B1B",
        "info": "#58A6FF",
        "infoSubtle": "#123046",
        "isDark": true
    }

    // Available themes list
    readonly property var availableThemes: [
        { "id": "midnight", "name": "Midnight", "type": "dark" },
        { "id": "nord", "name": "Nord", "type": "dark" },
        { "id": "dracula", "name": "Dracula", "type": "dark" },
        { "id": "catppuccin", "name": "Catppuccin", "type": "dark" },
        { "id": "tokyo-night", "name": "Tokyo Night", "type": "dark" },
        { "id": "terminal-green", "name": "Terminal Green", "type": "dark" },
        { "id": "paper-light", "name": "Paper Light", "type": "light" },
        { "id": "amoled", "name": "AMOLED", "type": "dark" },
        { "id": "deep-space", "name": "Deep Space", "type": "dark" },
        { "id": "custom", "name": "Custom", "type": "custom" }
    ]

    // Curated accent palette
    readonly property var accentPalette: [
        { "name": "Default (Theme)", "color": "" },
        { "name": "Indigo", "color": "#6366F1" },
        { "name": "Emerald", "color": "#10B981" },
        { "name": "Amber", "color": "#F59E0B" },
        { "name": "Crimson", "color": "#EF4444" },
        { "name": "Cyan", "color": "#06B6D4" },
        { "name": "Violet", "color": "#8B5CF6" },
        { "name": "Rose", "color": "#F43F5E" },
        { "name": "Sky", "color": "#0284C7" }
    ]

    // Built-in theme color definitions
    readonly property var themeColorData: {
        "midnight": {
            "background": "#0B0D14",
            "secondaryBackground": "#10131E",
            "surface": "#171B2B",
            "elevatedSurface": "#1F2439",
            "border": "#282E47",
            "borderFocus": "#6366F1",
            "primaryText": "#F3F4F6",
            "secondaryText": "#94A3B8",
            "tertiaryText": "#64748B",
            "accent": "#6366F1",
            "accentHover": "#4F46E5",
            "accentSubtle": "#22274A",
            "success": "#10B981",
            "successSubtle": "#0F3327",
            "warning": "#F59E0B",
            "warningSubtle": "#3B2B11",
            "error": "#EF4444",
            "errorSubtle": "#3E1B1B",
            "info": "#38BDF8",
            "infoSubtle": "#123046",
            "isDark": true
        },
        "nord": {
            "background": "#242933",
            "secondaryBackground": "#2E3440",
            "surface": "#3B4252",
            "elevatedSurface": "#434C5E",
            "border": "#4C566A",
            "borderFocus": "#88C0D0",
            "primaryText": "#ECEFF4",
            "secondaryText": "#D8DEE9",
            "tertiaryText": "#939BAA",
            "accent": "#88C0D0",
            "accentHover": "#81A1C1",
            "accentSubtle": "#2B4049",
            "success": "#A3BE8C",
            "successSubtle": "#31442E",
            "warning": "#EBCB8B",
            "warningSubtle": "#4D422C",
            "error": "#BF616A",
            "errorSubtle": "#48262B",
            "info": "#81A1C1",
            "infoSubtle": "#283C4D",
            "isDark": true
        },
        "dracula": {
            "background": "#1E1F29",
            "secondaryBackground": "#282A36",
            "surface": "#343746",
            "elevatedSurface": "#44475A",
            "border": "#555870",
            "borderFocus": "#BD93F9",
            "primaryText": "#F8F8F2",
            "secondaryText": "#A2ABCC",
            "tertiaryText": "#6272A4",
            "accent": "#BD93F9",
            "accentHover": "#A777E3",
            "accentSubtle": "#3A2B52",
            "success": "#50FA7B",
            "successSubtle": "#1B4728",
            "warning": "#FFB86C",
            "warningSubtle": "#4A3521",
            "error": "#FF5555",
            "errorSubtle": "#4A1C1C",
            "info": "#8BE9FD",
            "infoSubtle": "#21444E",
            "isDark": true
        },
        "catppuccin": {
            "background": "#181825",
            "secondaryBackground": "#1E1E2E",
            "surface": "#313244",
            "elevatedSurface": "#45475A",
            "border": "#585B70",
            "borderFocus": "#CBA6F7",
            "primaryText": "#CDD6F4",
            "secondaryText": "#A6ADC8",
            "tertiaryText": "#7F849C",
            "accent": "#CBA6F7",
            "accentHover": "#B48EED",
            "accentSubtle": "#392C4E",
            "success": "#A6E3A1",
            "successSubtle": "#274229",
            "warning": "#F9E2AF",
            "warningSubtle": "#473F28",
            "error": "#F38BA8",
            "errorSubtle": "#492631",
            "info": "#89DCEB",
            "infoSubtle": "#224147",
            "isDark": true
        },
        "tokyo-night": {
            "background": "#16161E",
            "secondaryBackground": "#1A1B26",
            "surface": "#24283B",
            "elevatedSurface": "#2F354A",
            "border": "#3B4261",
            "borderFocus": "#7AA2F7",
            "primaryText": "#C0CAF5",
            "secondaryText": "#9AA5CE",
            "tertiaryText": "#565F89",
            "accent": "#7AA2F7",
            "accentHover": "#5E89E8",
            "accentSubtle": "#223157",
            "success": "#9ECE6A",
            "successSubtle": "#2B401F",
            "warning": "#E0AF68",
            "warningSubtle": "#47341D",
            "error": "#F7768E",
            "errorSubtle": "#4A202A",
            "info": "#7DCFFF",
            "infoSubtle": "#213D52",
            "isDark": true
        },
        "terminal-green": {
            "background": "#050B06",
            "secondaryBackground": "#0A140C",
            "surface": "#0F1E12",
            "elevatedSurface": "#172E1C",
            "border": "#1E3B24",
            "borderFocus": "#22C55E",
            "primaryText": "#4ADE80",
            "secondaryText": "#22C55E",
            "tertiaryText": "#15803D",
            "accent": "#22C55E",
            "accentHover": "#16A34A",
            "accentSubtle": "#0F2E16",
            "success": "#4ADE80",
            "successSubtle": "#0F3818",
            "warning": "#FACC15",
            "warningSubtle": "#3B3308",
            "error": "#F87171",
            "errorSubtle": "#3B1515",
            "info": "#2DD4BF",
            "infoSubtle": "#0D332D",
            "isDark": true
        },
        "paper-light": {
            "background": "#FBFBFA",
            "secondaryBackground": "#F2F1EE",
            "surface": "#FFFFFF",
            "elevatedSurface": "#FFFFFF",
            "border": "#E5E4DE",
            "borderFocus": "#4F46E5",
            "primaryText": "#1C1917",
            "secondaryText": "#57534E",
            "tertiaryText": "#A8A29E",
            "accent": "#4F46E5",
            "accentHover": "#4338CA",
            "accentSubtle": "#EEF2FF",
            "success": "#16A34A",
            "successSubtle": "#F0FDF4",
            "warning": "#D97706",
            "warningSubtle": "#FFFBEB",
            "error": "#DC2626",
            "errorSubtle": "#FEF2F2",
            "info": "#0284C7",
            "infoSubtle": "#F0F9FF",
            "isDark": false
        },
        "amoled": {
            "background": "#000000",
            "secondaryBackground": "#080808",
            "surface": "#121212",
            "elevatedSurface": "#1C1C1C",
            "border": "#27272A",
            "borderFocus": "#6366F1",
            "primaryText": "#FFFFFF",
            "secondaryText": "#A1A1AA",
            "tertiaryText": "#71717A",
            "accent": "#6366F1",
            "accentHover": "#4F46E5",
            "accentSubtle": "#18182E",
            "success": "#22C55E",
            "successSubtle": "#0A2912",
            "warning": "#EAB308",
            "warningSubtle": "#2B2104",
            "error": "#EF4444",
            "errorSubtle": "#2E0E0E",
            "info": "#06B6D4",
            "infoSubtle": "#082329",
            "isDark": true
        },
        "deep-space": {
            "background": "#030712",
            "secondaryBackground": "#070F22",
            "surface": "#0D1938",
            "elevatedSurface": "#14244E",
            "border": "#1E3466",
            "borderFocus": "#0284C7",
            "primaryText": "#F0F9FF",
            "secondaryText": "#7DD3FC",
            "tertiaryText": "#38BDF8",
            "accent": "#0284C7",
            "accentHover": "#0369A1",
            "accentSubtle": "#0C2744",
            "success": "#34D399",
            "successSubtle": "#0D3325",
            "warning": "#FBBF24",
            "warningSubtle": "#362706",
            "error": "#FB7185",
            "errorSubtle": "#3B141C",
            "info": "#38BDF8",
            "infoSubtle": "#0D2E42",
            "isDark": true
        },
        "custom": customThemeColors
    }

    // Active color resolver
    readonly property var currentColors: themeColorData[activeThemeId] || themeColorData["midnight"]

    readonly property color background: currentColors.background
    readonly property color secondaryBackground: currentColors.secondaryBackground
    readonly property color surface: currentColors.surface
    readonly property color elevatedSurface: currentColors.elevatedSurface
    readonly property color border: currentColors.border
    readonly property color borderFocus: (customAccentOverride !== "") ? customAccentOverride : currentColors.borderFocus
    readonly property color primaryText: currentColors.primaryText
    readonly property color secondaryText: currentColors.secondaryText
    readonly property color tertiaryText: currentColors.tertiaryText

    readonly property color accent: (customAccentOverride !== "") ? customAccentOverride : currentColors.accent
    readonly property color accentHover: currentColors.accentHover
    readonly property color accentSubtle: currentColors.accentSubtle

    readonly property color success: currentColors.success
    readonly property color successSubtle: currentColors.successSubtle
    readonly property color warning: currentColors.warning
    readonly property color warningSubtle: currentColors.warningSubtle
    readonly property color error: currentColors.error
    readonly property color errorSubtle: currentColors.errorSubtle
    readonly property color info: currentColors.info
    readonly property color infoSubtle: currentColors.infoSubtle

    readonly property bool isDark: currentColors.isDark

    function setTheme(themeId) {
        if (themeColorData[themeId]) {
            activeThemeId = themeId;
        }
    }

    function setAccent(hexColor) {
        customAccentOverride = hexColor;
    }

    function setThemeMode(mode) {
        themeMode = mode;
        if (mode === "light") {
            setTheme("paper-light");
        } else if (mode === "dark") {
            if (activeThemeId === "paper-light") {
                setTheme("midnight");
            }
        }
    }

    function setCustomThemeColors(colorsObj) {
        customThemeColors = colorsObj;
        activeThemeId = "custom";
    }

    function getEffectiveWindowRadius() {
        if (windowRadiusScale === "small") return radiusSmall;
        if (windowRadiusScale === "large") return radiusLarge;
        if (windowRadiusScale === "xl") return radiusXL;
        return radiusMedium; // Default 14px
    }
}
