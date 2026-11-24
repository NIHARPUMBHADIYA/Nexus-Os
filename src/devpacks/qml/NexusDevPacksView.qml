import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Rectangle {
    id: root
    color: NexusTheme.background

    readonly property bool hasBridge: typeof devpackBridge !== "undefined" && devpackBridge !== null

    // Fallback packs list if previewing without bridge
    property var packsData: (hasBridge && devpackBridge.packsList) ? devpackBridge.packsList : [
        {
            "id": "vibecoder", "name": "Vibe Coder", "icon": "✨",
            "tagline": "AI-native prompt-driven development and instant iteration",
            "description": "Antigravity, Cursor, Ollama local model execution, OmniRoute integration, and rapid prototyping tools.",
            "programming_languages": ["TypeScript", "Python 3.13", "HTML/CSS"],
            "frameworks": ["Next.js", "FastAPI", "Tailwind CSS"],
            "editors": ["Google Antigravity", "Cursor"],
            "estimated_storage_mb": 3900,
            "is_installed": false,
            "is_selected": true,
            "hardware": {"min_ram_gb": 8, "gpu_required": false, "notes": "GPU recommended"}
        }
    ]

    property bool showDetailModal: false
    property bool showLogsDrawer: false
    property bool includeOptional: false
    property bool rollbackOnFailure: true

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        // ==========================================
        // 1. TOP HEADER & MULTI-PACK SUMMARY TOOLBAR
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            height: 90
            radius: NexusTheme.radiusLarge
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                spacing: 16

                Rectangle {
                    width: 52
                    height: 52
                    radius: NexusTheme.radiusMedium
                    color: NexusTheme.elevatedSurface
                    border.color: NexusTheme.accent
                    border.width: 1
                    Text {
                        anchors.centerIn: parent
                        text: "📦"
                        font.pixelSize: 28
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2
                    RowLayout {
                        spacing: 8
                        Text {
                            text: "NEXUS Developer Packs"
                            font.pixelSize: 20
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        NexusBadge {
                            text: "15 Curated Packs"
                            variant: "primary"
                        }
                    }
                    Text {
                        text: "Install complete, production-grade development environments in a single click with zero dependency conflicts."
                        font.pixelSize: 12
                        color: NexusTheme.secondaryText
                    }
                }

                // Batch controls
                RowLayout {
                    spacing: 8
                    NexusButton {
                        text: "Select All"
                        variant: "ghost"
                        size: "small"
                        onClicked: if (hasBridge) devpackBridge.selectAll()
                    }
                    NexusButton {
                        text: "Clear"
                        variant: "ghost"
                        size: "small"
                        onClicked: if (hasBridge) devpackBridge.clearSelection()
                    }
                }
            }
        }

        // ==========================================
        // 2. PLAN SUMMARY & INSTALLATION ACTION BAR
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            height: 64
            radius: NexusTheme.radiusMedium
            color: NexusTheme.elevatedSurface
            border.color: NexusTheme.border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 16
                anchors.rightMargin: 16
                spacing: 14

                // Selection count pill
                Rectangle {
                    width: 140
                    height: 36
                    radius: NexusTheme.radiusPill
                    color: NexusTheme.surface
                    border.color: NexusTheme.accent
                    border.width: 1

                    RowLayout {
                        anchors.centerIn: parent
                        spacing: 6
                        Text { text: "✓"; font.pixelSize: 12; color: NexusTheme.accent; font.bold: true }
                        Text {
                            text: (hasBridge ? devpackBridge.selectedPackIds.length : 1) + " Packs Selected"
                            font.pixelSize: 12
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                    }
                }

                // Storage and tool count metrics
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2
                    RowLayout {
                        spacing: 10
                        Text {
                            text: "Total Download & Install: " + (hasBridge ? devpackBridge.resolutionPlan.total_size_formatted : "3.9 GB")
                            font.pixelSize: 12
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        Text {
                            text: "• " + (hasBridge ? devpackBridge.resolutionPlan.tools_count : 11) + " unique tools (deduplicated)"
                            font.pixelSize: 11
                            color: NexusTheme.secondaryText
                        }
                    }
                    Text {
                        text: "Free Disk Space: " + (hasBridge ? Math.round(devpackBridge.resolutionPlan.free_disk_mb / 1024) : 142) + " GB available (Sufficient)"
                        font.pixelSize: 11
                        color: NexusTheme.success
                    }
                }

                // Optional Tools Checkbox / Toggle
                RowLayout {
                    spacing: 6
                    NexusToggle {
                        checked: root.includeOptional
                        onToggled: {
                            root.includeOptional = checked;
                        }
                    }
                    Text {
                        text: "Include Optional Tools"
                        font.pixelSize: 11
                        color: NexusTheme.primaryText
                    }
                }

                // Primary Install / Cancel Button
                NexusButton {
                    text: (hasBridge && devpackBridge.isRunning) ? "Cancel Installation" : "Install Selected Packs"
                    variant: (hasBridge && devpackBridge.isRunning) ? "danger" : "primary"
                    size: "medium"
                    enabled: hasBridge ? (devpackBridge.selectedPackIds.length > 0 || devpackBridge.isRunning) : true
                    onClicked: {
                        if (hasBridge) {
                            if (devpackBridge.isRunning) {
                                devpackBridge.cancelInstallation();
                            } else {
                                devpackBridge.startInstallation(root.includeOptional, root.rollbackOnFailure);
                            }
                        }
                    }
                }
            }
        }

        // ==========================================
        // 3. LIVE INSTALLATION PROGRESS BANNER
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            height: root.showLogsDrawer ? 240 : 76
            radius: NexusTheme.radiusMedium
            color: NexusTheme.surface
            border.color: (hasBridge && devpackBridge.isRunning) ? NexusTheme.accent : NexusTheme.border
            border.width: (hasBridge && devpackBridge.isRunning) ? 2 : 1
            visible: hasBridge ? (devpackBridge.isRunning || devpackBridge.progress > 0) : false

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10
                    Text {
                        text: (hasBridge && devpackBridge.isRunning) ? "⏳" : "✓"
                        font.pixelSize: 16
                    }
                    Text {
                        text: hasBridge ? devpackBridge.statusMessage : "Installing packages..."
                        font.pixelSize: 13
                        font.bold: true
                        color: NexusTheme.primaryText
                        Layout.fillWidth: true
                    }
                    Text {
                        text: (hasBridge ? devpackBridge.progress : 0) + "%"
                        font.pixelSize: 13
                        font.bold: true
                        color: NexusTheme.accent
                    }
                    NexusButton {
                        text: root.showLogsDrawer ? "Hide Logs" : "View Live Logs"
                        variant: "outline"
                        size: "small"
                        onClicked: root.showLogsDrawer = !root.showLogsDrawer
                    }
                }

                // Progress Bar
                NexusProgress {
                    Layout.fillWidth: true
                    value: hasBridge ? devpackBridge.progress : 0
                }

                // Live Log Terminal Drawer
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    radius: NexusTheme.radiusSmall
                    color: "#080A10"
                    border.color: NexusTheme.border
                    border.width: 1
                    visible: root.showLogsDrawer

                    ScrollView {
                        anchors.fill: parent
                        anchors.margins: 8
                        clip: true

                        ColumnLayout {
                            width: parent.width - 10
                            spacing: 3

                            Repeater {
                                model: hasBridge ? devpackBridge.logLines : []
                                delegate: Text {
                                    text: modelData
                                    font.family: NexusTheme.fontMono
                                    font.pixelSize: 11
                                    color: modelData.indexOf("ERROR") !== -1 ? NexusTheme.error :
                                           modelData.indexOf("SUCCESS") !== -1 ? NexusTheme.success :
                                           modelData.indexOf("WARN") !== -1 ? NexusTheme.warning : "#CBD5E1"
                                    wrapMode: Text.WrapAnywhere
                                    Layout.fillWidth: true
                                }
                            }
                        }
                    }
                }
            }
        }

        // ==========================================
        // 4. HARDWARE WARNINGS BANNER (If any)
        // ==========================================
        Rectangle {
            Layout.fillWidth: true
            height: 40
            radius: NexusTheme.radiusMedium
            color: Qt.rgba(245/255, 158/255, 11/255, 0.15)
            border.color: NexusTheme.warning
            border.width: 1
            visible: hasBridge && devpackBridge.resolutionPlan.hardware_warnings.length > 0

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 14
                anchors.rightMargin: 14
                spacing: 8

                Text { text: "⚠️"; font.pixelSize: 14 }
                Text {
                    text: hasBridge ? devpackBridge.resolutionPlan.hardware_warnings.join(" • ") : ""
                    font.pixelSize: 11
                    color: NexusTheme.warning
                    Layout.fillWidth: true
                    elide: Text.ElideRight
                }
            }
        }

        // ==========================================
        // 5. PACKS GRID (All 15 Developer Packs)
        // ==========================================
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            GridLayout {
                width: parent.width - 10
                columns: parent.width > 1200 ? 3 : (parent.width > 800 ? 2 : 1)
                rowSpacing: 14
                columnSpacing: 14

                Repeater {
                    model: hasBridge ? devpackBridge.packsList : root.packsData
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        height: 240
                        radius: NexusTheme.radiusLarge
                        color: NexusTheme.surface
                        border.color: modelData.is_selected ? NexusTheme.accent : NexusTheme.border
                        border.width: modelData.is_selected ? 2 : 1

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (hasBridge) devpackBridge.togglePackSelection(modelData.id);
                            }
                        }

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 14
                            spacing: 8

                            // Header row: Icon, Name, and Selection / Installed Badge
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 10

                                Rectangle {
                                    width: 44
                                    height: 44
                                    radius: NexusTheme.radiusMedium
                                    color: NexusTheme.elevatedSurface
                                    border.color: NexusTheme.border
                                    border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: modelData.icon
                                        font.pixelSize: 22
                                    }
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 2
                                    Text {
                                        text: modelData.name
                                        font.pixelSize: 15
                                        font.bold: true
                                        color: NexusTheme.primaryText
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        text: modelData.tagline
                                        font.pixelSize: 11
                                        color: NexusTheme.secondaryText
                                        elide: Text.ElideRight
                                        Layout.fillWidth: true
                                    }
                                }

                                // Selection indicator / checkmark
                                Rectangle {
                                    width: 24
                                    height: 24
                                    radius: NexusTheme.radiusSmall
                                    color: modelData.is_selected ? NexusTheme.accent : "transparent"
                                    border.color: modelData.is_selected ? NexusTheme.accent : NexusTheme.border
                                    border.width: 1.5

                                    Text {
                                        anchors.centerIn: parent
                                        text: "✓"
                                        color: "#FFFFFF"
                                        font.pixelSize: 12
                                        font.bold: true
                                        visible: modelData.is_selected
                                    }
                                }
                            }

                            // Description
                            Text {
                                text: modelData.description
                                font.pixelSize: 11
                                color: NexusTheme.secondaryText
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                                maximumLineCount: 2
                                elide: Text.ElideRight
                            }

                            // Tags / Badges: Languages & Frameworks
                            Flow {
                                Layout.fillWidth: true
                                spacing: 4
                                Repeater {
                                    model: modelData.programming_languages.slice(0, 3)
                                    delegate: NexusBadge {
                                        text: modelData
                                        variant: "info"
                                    }
                                }
                                Repeater {
                                    model: modelData.frameworks.slice(0, 2)
                                    delegate: NexusBadge {
                                        text: modelData
                                        variant: "secondary"
                                    }
                                }
                            }

                            Item { Layout.fillHeight: true }

                            // Card Footer: Storage, Status Badge, and Inspect Details Button
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8

                                NexusBadge {
                                    text: "~" + (modelData.estimated_storage_mb / 1024).toFixed(1) + " GB"
                                    variant: "outline"
                                }

                                NexusBadge {
                                    text: "Installed"
                                    variant: "success"
                                    visible: Boolean(modelData.is_installed)
                                }

                                Item { Layout.fillWidth: true }

                                NexusButton {
                                    text: "Inspect Pack"
                                    variant: "ghost"
                                    size: "small"
                                    onClicked: {
                                        if (hasBridge) devpackBridge.inspectPack(modelData.id);
                                        root.showDetailModal = true;
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
    // 6. PACK DETAIL INSPECTION MODAL DRAWER
    // ==========================================
    Rectangle {
        id: detailModalOverlay
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0.7)
        visible: root.showDetailModal

        MouseArea {
            anchors.fill: parent
            onClicked: root.showDetailModal = false
        }

        Rectangle {
            width: Math.min(680, parent.width - 40)
            height: Math.min(640, parent.height - 40)
            anchors.centerIn: parent
            radius: NexusTheme.radiusLarge
            color: NexusTheme.surface
            border.color: NexusTheme.accent
            border.width: 1

            MouseArea { anchors.fill: parent } // Prevent click-through

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 22
                spacing: 14

                // Modal Header
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    Text {
                        text: hasBridge ? devpackBridge.activePackDetail.icon : "📦"
                        font.pixelSize: 32
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 2
                        Text {
                            text: hasBridge ? devpackBridge.activePackDetail.name : "Pack Detail"
                            font.pixelSize: 18
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        Text {
                            text: hasBridge ? devpackBridge.activePackDetail.tagline : ""
                            font.pixelSize: 12
                            color: NexusTheme.secondaryText
                        }
                    }
                    NexusIconButton {
                        iconText: "✕"
                        size: 28
                        onClicked: root.showDetailModal = false
                    }
                }

                Rectangle { Layout.fillWidth: true; height: 1; color: NexusTheme.border }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    ColumnLayout {
                        width: parent.width - 10
                        spacing: 14

                        Text {
                            text: "Overview"
                            font.pixelSize: 13
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        Text {
                            text: hasBridge ? devpackBridge.activePackDetail.description : ""
                            font.pixelSize: 12
                            color: NexusTheme.secondaryText
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }

                        Text {
                            text: "Languages & Frameworks"
                            font.pixelSize: 13
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        Flow {
                            Layout.fillWidth: true
                            spacing: 6
                            Repeater {
                                model: hasBridge ? devpackBridge.activePackDetail.programming_languages : []
                                delegate: NexusBadge { text: modelData; variant: "primary" }
                            }
                            Repeater {
                                model: hasBridge ? devpackBridge.activePackDetail.frameworks : []
                                delegate: NexusBadge { text: modelData; variant: "secondary" }
                            }
                        }

                        Text {
                            text: "Included Editors & IDEs"
                            font.pixelSize: 13
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        Flow {
                            Layout.fillWidth: true
                            spacing: 6
                            Repeater {
                                model: hasBridge ? devpackBridge.activePackDetail.editors : []
                                delegate: NexusBadge { text: modelData; variant: "info" }
                            }
                        }

                        Text {
                            text: "Hardware Requirements"
                            font.pixelSize: 13
                            font.bold: true
                            color: NexusTheme.primaryText
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            height: 60
                            radius: NexusTheme.radiusMedium
                            color: NexusTheme.elevatedSurface
                            border.color: NexusTheme.border
                            border.width: 1

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 12
                                spacing: 14
                                ColumnLayout {
                                    Text { text: "Min RAM: " + (hasBridge ? devpackBridge.activePackDetail.hardware.min_ram_gb : 8) + " GB"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText }
                                    Text { text: "Recommended: " + (hasBridge ? devpackBridge.activePackDetail.hardware.recommended_ram_gb : 16) + " GB"; font.pixelSize: 10; color: NexusTheme.secondaryText }
                                }
                                Rectangle { width: 1; height: parent.height; color: NexusTheme.border }
                                ColumnLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Notes: " + (hasBridge ? devpackBridge.activePackDetail.hardware.notes : ""); font.pixelSize: 10; color: NexusTheme.secondaryText; elide: Text.ElideRight; Layout.fillWidth: true }
                                }
                            }
                        }
                    }
                }

                // Modal Footer
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    Item { Layout.fillWidth: true }
                    NexusButton {
                        text: (hasBridge && devpackBridge.activePackDetail.is_selected) ? "Remove from Selection" : "Add to Selection"
                        variant: (hasBridge && devpackBridge.activePackDetail.is_selected) ? "secondary" : "primary"
                        onClicked: {
                            if (hasBridge) devpackBridge.togglePackSelection(devpackBridge.activePackDetail.id);
                            root.showDetailModal = false;
                        }
                    }
                    NexusButton {
                        text: "Close"
                        variant: "ghost"
                        onClicked: root.showDetailModal = false
                    }
                }
            }
        }
    }
}
