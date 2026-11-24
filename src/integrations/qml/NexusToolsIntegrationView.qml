import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Rectangle {
    id: root
    color: NexusTheme.background

    property string selectedCategory: "all" // "all", "editor", "terminal_agent", "extension"
    property string activeProfile: "local_coding"
    property string selectedFilter: "all" // "all", "installed", "configured", "ai_connected"
    property string searchQuery: ""
    property var activeModalTool: null
    property bool showInstallModal: false

    // Fallback data if bridge is not attached
    property var toolsData: (typeof toolsBridge !== "undefined" && toolsBridge.toolsList) ? toolsBridge.toolsList : [
        { "id": "antigravity", "name": "Google Antigravity", "category": "ide", "type": "AI-Native IDE & Agent CLI", "licensing": "Google Proprietary", "installed": true, "version": "1.0.0", "config_detected": true, "supports_ai_endpoint": true, "ai_endpoint_configured": true, "active_ai_provider": "nexus-aid (:11430)", "icon": "🚀", "install_methods": [{"command": "sudo dnf install google-antigravity"}], "description": "Google's developer-first agentic IDE with integrated terminal and workflow engines." },
        { "id": "vscode", "name": "Visual Studio Code", "category": "editor", "type": "Extensible Code Editor", "licensing": "Microsoft Proprietary", "installed": true, "version": "1.97.2", "config_detected": true, "supports_ai_endpoint": true, "ai_endpoint_configured": true, "active_ai_provider": "nexus-aid (:11430)", "icon": "🟦", "install_methods": [{"command": "sudo dnf install code"}], "description": "Extensible code editor supporting modern AI coding plugins." },
        { "id": "vscodium", "name": "VSCodium", "category": "editor", "type": "Free/Libre Open Source Editor", "licensing": "MIT (100% FLOSS)", "installed": false, "version": "Not installed", "config_detected": false, "supports_ai_endpoint": true, "ai_endpoint_configured": false, "active_ai_provider": "none", "icon": "🟩", "install_methods": [{"command": "sudo dnf install codium"}], "description": "Community-driven, telemetry-free open-source binaries of VS Code." },
        { "id": "cursor", "name": "Cursor", "category": "ide", "type": "AI-First Code Editor", "licensing": "Anysphere Proprietary", "installed": true, "version": "0.45.11", "config_detected": true, "supports_ai_endpoint": true, "ai_endpoint_configured": true, "active_ai_provider": "nexus-aid (:11430)", "icon": "⚡", "install_methods": [{"command": "Download AppImage from cursor.com"}], "description": "AI-native code editor with deep multi-file agentic code generation." },
        { "id": "windsurf", "name": "Windsurf", "category": "ide", "type": "Agentic AI IDE", "licensing": "Codeium Proprietary", "installed": false, "version": "Not installed", "config_detected": false, "supports_ai_endpoint": true, "ai_endpoint_configured": false, "active_ai_provider": "none", "icon": "🏄", "install_methods": [{"command": "sudo dnf install windsurf"}], "description": "Codeium's agentic IDE featuring collaborative Cascade AI workflows." },
        { "id": "zed", "name": "Zed Editor", "category": "editor", "type": "High-Performance Rust Editor", "licensing": "GPLv3 / Apache 2.0", "installed": true, "version": "0.174.0", "config_detected": true, "supports_ai_endpoint": true, "ai_endpoint_configured": true, "active_ai_provider": "nexus-aid (:11430)", "icon": "⚡", "install_methods": [{"command": "curl -f https://zed.dev/install.sh | sh"}], "description": "Ultra-fast GPU-accelerated code editor with native local and cloud LLM assistant integration." },
        { "id": "claude_code", "name": "Claude Code", "category": "terminal_agent", "type": "Terminal Coding Agent", "licensing": "Anthropic Proprietary", "installed": false, "version": "Not installed", "config_detected": false, "supports_ai_endpoint": true, "ai_endpoint_configured": false, "active_ai_provider": "none", "icon": "🤖", "install_methods": [{"command": "npm install -g @anthropic-ai/claude-code"}], "description": "Anthropic's research-grade agentic terminal CLI for codebase edits and test loops." },
        { "id": "aider", "name": "Aider Pair Programmer", "category": "terminal_agent", "type": "Git-Aware CLI AI Copilot", "licensing": "Apache 2.0", "installed": true, "version": "0.74.2", "config_detected": true, "supports_ai_endpoint": true, "ai_endpoint_configured": true, "active_ai_provider": "nexus-aid (:11430)", "icon": "🧑‍💻", "install_methods": [{"command": "pipx install aider-chat"}], "description": "Leaderboard-topping AI pair programming CLI with automatic Git commits." },
        { "id": "continue", "name": "Continue", "category": "extension", "type": "Open-Source AI Code Assistant", "licensing": "Apache 2.0", "installed": true, "version": "0.8.60", "config_detected": true, "supports_ai_endpoint": true, "ai_endpoint_configured": true, "active_ai_provider": "nexus-aid (:11430)", "icon": "⏩", "install_methods": [{"command": "code --install-extension Continue.continue"}], "description": "Connect any LLM to VS Code or JetBrains for tab autocomplete and conversational editing." }
    ]

    property var statsData: (typeof toolsBridge !== "undefined" && toolsBridge.stats) ? toolsBridge.stats : {
        "total": 15, "installed": 6, "configured": 6, "ai_connected": 6
    }

    property var profilesData: (typeof toolsBridge !== "undefined" && toolsBridge.profilesList) ? toolsBridge.profilesList : [
        { "id": "local_coding", "name": "Local Coding (Private & Offline)", "model": "nexus:default", "description": "Offline Qwen 2.5 Coder 7B running on local GPU. 100% private, zero token costs." },
        { "id": "free_cloud", "name": "Free Cloud Models (Groq / Gemini)", "model": "llama-3.3-70b-versatile", "description": "Legitimate free-tier models via Groq LPU (Llama 3.3 70B) or Google AI Studio." },
        { "id": "premium_cloud", "name": "Premium Cloud (Claude 3.7 / GPT-4o)", "model": "claude-3-7-sonnet", "description": "Frontier hybrid reasoning and agentic software engineering." },
        { "id": "reasoning", "name": "Deep Reasoning (DeepSeek R1 / o3-mini)", "model": "deepseek-r1:8b", "description": "Chain-of-thought mathematical proof and complex algorithmic verification." },
        { "id": "fast_coding", "name": "Fast Coding (Llama 3.2 3B / Low Latency)", "model": "nexus:fast", "description": "Sub-100ms completions for rapid iterative coding and scaffolding." }
    ]

    Connections {
        target: (typeof toolsBridge !== "undefined") ? toolsBridge : null
        function onToolsChanged() {
            root.toolsData = toolsBridge.toolsList;
        }
        function onStatsChanged() {
            root.statsData = toolsBridge.stats;
        }
    }

    Column {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 14

        // Header Strip
        Rectangle {
            width: parent.width
            height: 72
            radius: NexusTheme.radiusMedium
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                spacing: 16

                Text {
                    text: "🛠️"
                    font.pixelSize: 26
                    anchors.verticalCenter: parent.verticalCenter
                }

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 2

                    Text {
                        text: "AI CODING TOOLS & IDE INTEGRATION"
                        font.pixelSize: 15
                        font.bold: true
                        color: NexusTheme.primaryText
                    }
                    Text {
                        text: "Configure 15 modern AI tools to seamlessly use NEXUS OS AI Core, OmniRoute & Ollama"
                        font.pixelSize: 11
                        color: NexusTheme.secondaryText
                    }
                }

                Item { width: Math.max(10, root.width - 820); height: 1 }

                // Stat Counters
                Row {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 10

                    Rectangle {
                        height: 32
                        width: 90
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1
                        Column {
                            anchors.centerIn: parent
                            Text { text: "CATALOG"; font.pixelSize: 8; font.bold: true; color: NexusTheme.secondaryText }
                            Text { text: "" + root.statsData.total; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                        }
                    }

                    Rectangle {
                        height: 32
                        width: 90
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1
                        Column {
                            anchors.centerIn: parent
                            Text { text: "INSTALLED"; font.pixelSize: 8; font.bold: true; color: NexusTheme.secondaryText }
                            Text { text: "" + root.statsData.installed; font.pixelSize: 12; font.bold: true; color: NexusTheme.success }
                        }
                    }

                    Rectangle {
                        height: 32
                        width: 100
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1
                        Column {
                            anchors.centerIn: parent
                            Text { text: "AI ROUTED"; font.pixelSize: 8; font.bold: true; color: NexusTheme.secondaryText }
                            Text { text: "" + root.statsData.ai_connected; font.pixelSize: 12; font.bold: true; color: NexusTheme.accent }
                        }
                    }

                    // Rescan Button
                    Rectangle {
                        width: 32
                        height: 32
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1

                        Text {
                            anchors.centerIn: parent
                            text: "↻"
                            font.pixelSize: 16
                            color: NexusTheme.primaryText
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (typeof toolsBridge !== "undefined") {
                                    toolsBridge.scanTools();
                                }
                            }
                        }
                    }
                }
            }
        }

        // Active AI Profile Selection Bar
        Rectangle {
            width: parent.width
            height: 48
            radius: NexusTheme.radiusMedium
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.leftMargin: 16
                anchors.rightMargin: 16
                spacing: 12

                Text {
                    text: "Target AI Profile:"
                    font.pixelSize: 11
                    font.bold: true
                    color: NexusTheme.primaryText
                    anchors.verticalCenter: parent.verticalCenter
                }

                Repeater {
                    model: root.profilesData

                    delegate: Rectangle {
                        height: 28
                        width: Math.max(70, profileText.implicitWidth + 18)
                        radius: NexusTheme.radiusPill
                        color: root.activeProfile === modelData.id ? NexusTheme.accent : NexusTheme.secondaryBackground
                        border.color: root.activeProfile === modelData.id ? NexusTheme.accent : NexusTheme.border
                        border.width: 1
                        anchors.verticalCenter: parent.verticalCenter

                        Text {
                            id: profileText
                            anchors.centerIn: parent
                            text: modelData.name.split(" (")[0]
                            font.pixelSize: 11
                            font.bold: root.activeProfile === modelData.id
                            color: root.activeProfile === modelData.id ? "#FFFFFF" : NexusTheme.secondaryText
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.activeProfile = modelData.id
                        }
                    }
                }
            }
        }

        // Filter and Search Strip
        Row {
            width: parent.width
            spacing: 12

            Row {
                spacing: 6
                Repeater {
                    model: [
                        { "id": "all", "label": "All Tools" },
                        { "id": "installed", "label": "Installed Only" },
                        { "id": "ai_connected", "label": "AI Configured" }
                    ]
                    delegate: Rectangle {
                        height: 28
                        width: Math.max(60, fText.implicitWidth + 16)
                        radius: NexusTheme.radiusSmall
                        color: root.selectedFilter === modelData.id ? NexusTheme.surface : "transparent"
                        border.color: root.selectedFilter === modelData.id ? NexusTheme.accent : NexusTheme.border
                        border.width: 1

                        Text {
                            id: fText
                            anchors.centerIn: parent
                            text: modelData.label
                            font.pixelSize: 11
                            font.bold: root.selectedFilter === modelData.id
                            color: root.selectedFilter === modelData.id ? NexusTheme.accent : NexusTheme.secondaryText
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.selectedFilter = modelData.id
                        }
                    }
                }
            }

            Item { width: Math.max(10, root.width - 640); height: 1 }

            // Search Box
            Rectangle {
                width: 220
                height: 28
                radius: NexusTheme.radiusSmall
                color: NexusTheme.surface
                border.color: NexusTheme.border
                border.width: 1

                TextInput {
                    id: searchField
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    verticalAlignment: TextInput.AlignVCenter
                    font.pixelSize: 11
                    color: NexusTheme.primaryText
                    clip: true

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: "Search 15 tools..."
                        font.pixelSize: 11
                        color: NexusTheme.secondaryText
                        visible: !searchField.text
                    }

                    onTextChanged: root.searchQuery = searchField.text
                }
            }
        }

        // Tools List Container
        Rectangle {
            width: parent.width
            height: root.height - 230
            radius: NexusTheme.radiusMedium
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1
            clip: true

            ScrollView {
                anchors.fill: parent
                anchors.margins: 14
                clip: true

                Column {
                    width: parent.width - 16
                    spacing: 8

                    Repeater {
                        model: {
                            var filtered = [];
                            for (var i = 0; i < root.toolsData.length; i++) {
                                var t = root.toolsData[i];
                                if (root.selectedFilter === "installed" && !t.installed) continue;
                                if (root.selectedFilter === "ai_connected" && !t.ai_endpoint_configured) continue;
                                if (root.searchQuery) {
                                    var str = (t.name + " " + t.id + " " + t.type + " " + t.description).toLowerCase();
                                    if (str.indexOf(root.searchQuery.toLowerCase()) === -1) continue;
                                }
                                filtered.push(t);
                            }
                            return filtered;
                        }

                        delegate: Rectangle {
                            width: parent.width
                            height: 76
                            radius: NexusTheme.radiusSmall
                            color: NexusTheme.secondaryBackground
                            border.color: modelData.ai_endpoint_configured ? NexusTheme.accent : (modelData.installed ? NexusTheme.success : NexusTheme.border)
                            border.width: 1

                            Row {
                                anchors.fill: parent
                                anchors.leftMargin: 16
                                anchors.rightMargin: 16
                                spacing: 14

                                Text {
                                    text: modelData.icon || "💻"
                                    font.pixelSize: 24
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                Column {
                                    anchors.verticalCenter: parent.verticalCenter
                                    spacing: 3
                                    width: Math.max(220, parent.width - 500)

                                    Row {
                                        spacing: 8
                                        Text {
                                            text: modelData.name
                                            font.pixelSize: 13
                                            font.bold: true
                                            color: NexusTheme.primaryText
                                        }

                                        Rectangle {
                                            height: 16
                                            width: licLabel.implicitWidth + 8
                                            radius: NexusTheme.radiusPill
                                            color: NexusTheme.surface
                                            border.color: NexusTheme.border
                                            border.width: 1
                                            anchors.verticalCenter: parent.verticalCenter
                                            Text {
                                                id: licLabel
                                                anchors.centerIn: parent
                                                text: modelData.licensing.split(" ")[0].toUpperCase()
                                                font.pixelSize: 9
                                                font.bold: true
                                                color: NexusTheme.secondaryText
                                            }
                                        }

                                        Rectangle {
                                            height: 16
                                            width: instLabel.implicitWidth + 8
                                            radius: NexusTheme.radiusPill
                                            color: modelData.installed ? NexusTheme.successSubtle : NexusTheme.secondaryBackground
                                            border.color: modelData.installed ? NexusTheme.success : NexusTheme.border
                                            border.width: 1
                                            anchors.verticalCenter: parent.verticalCenter
                                            Text {
                                                id: instLabel
                                                anchors.centerIn: parent
                                                text: modelData.installed ? "INSTALLED" : "NOT INSTALLED"
                                                font.pixelSize: 9
                                                font.bold: true
                                                color: modelData.installed ? NexusTheme.success : NexusTheme.secondaryText
                                            }
                                        }
                                    }

                                    Text {
                                        text: modelData.description
                                        font.pixelSize: 11
                                        color: NexusTheme.secondaryText
                                        elide: Text.ElideRight
                                        width: parent.width
                                    }

                                    Text {
                                        text: "Version: " + modelData.version + " • AI Status: " + (modelData.ai_endpoint_configured ? ("Routed to " + modelData.active_ai_provider) : "Default / Unconfigured")
                                        font.pixelSize: 10
                                        font.family: NexusTheme.fontFamilyMono
                                        color: modelData.ai_endpoint_configured ? NexusTheme.accent : NexusTheme.secondaryText
                                    }
                                }

                                Item { width: 10; height: 1 }

                                // Action Buttons
                                Row {
                                    anchors.verticalCenter: parent.verticalCenter
                                    spacing: 8

                                    // Configure AI Endpoint Button
                                    Rectangle {
                                        width: 120
                                        height: 30
                                        radius: NexusTheme.radiusSmall
                                        color: modelData.supports_ai_endpoint ? NexusTheme.accentSubtle : NexusTheme.surface
                                        border.color: modelData.supports_ai_endpoint ? NexusTheme.accent : NexusTheme.border
                                        border.width: 1
                                        visible: modelData.supports_ai_endpoint

                                        Text {
                                            anchors.centerIn: parent
                                            text: modelData.ai_endpoint_configured ? "Re-configure AI" : "Inject AI Profile"
                                            font.pixelSize: 10
                                            font.bold: true
                                            color: modelData.supports_ai_endpoint ? NexusTheme.accent : NexusTheme.secondaryText
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                if (typeof toolsBridge !== "undefined") {
                                                    toolsBridge.applyProfile(modelData.id, root.activeProfile);
                                                }
                                            }
                                        }
                                    }

                                    // Launch Button
                                    Rectangle {
                                        width: 70
                                        height: 30
                                        radius: NexusTheme.radiusSmall
                                        color: NexusTheme.surface
                                        border.color: NexusTheme.border
                                        border.width: 1
                                        visible: modelData.installed

                                        Text {
                                            anchors.centerIn: parent
                                            text: "Launch"
                                            font.pixelSize: 11
                                            font.bold: true
                                            color: NexusTheme.primaryText
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                if (typeof toolsBridge !== "undefined") {
                                                    toolsBridge.launchTool(modelData.id, "");
                                                }
                                            }
                                        }
                                    }

                                    // Install Info Button (for uninstalled tools)
                                    Rectangle {
                                        width: 80
                                        height: 30
                                        radius: NexusTheme.radiusSmall
                                        color: NexusTheme.surface
                                        border.color: NexusTheme.border
                                        border.width: 1
                                        visible: !modelData.installed

                                        Text {
                                            anchors.centerIn: parent
                                            text: "Install Info"
                                            font.pixelSize: 11
                                            color: NexusTheme.primaryText
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                root.activeModalTool = modelData;
                                                root.showInstallModal = true;
                                            }
                                        }
                                    }

                                    // Desktop Shortcut Button
                                    Rectangle {
                                        width: 30
                                        height: 30
                                        radius: NexusTheme.radiusSmall
                                        color: NexusTheme.surface
                                        border.color: NexusTheme.border
                                        border.width: 1
                                        visible: modelData.installed

                                        Text {
                                            anchors.centerIn: parent
                                            text: "📌"
                                            font.pixelSize: 13
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                if (typeof toolsBridge !== "undefined") {
                                                    toolsBridge.createDesktopShortcut(modelData.id);
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

    // Modal Dialog: Installation Instructions
    Rectangle {
        anchors.fill: parent
        color: "#80000000"
        visible: root.showInstallModal

        Rectangle {
            anchors.centerIn: parent
            width: 520
            height: 320
            radius: NexusTheme.radiusLarge
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            Column {
                anchors.fill: parent
                anchors.margins: 24
                spacing: 14

                Row {
                    width: parent.width
                    Text {
                        text: "Installation Workflow: " + (root.activeModalTool ? root.activeModalTool.name : "")
                        font.pixelSize: 14
                        font.bold: true
                        color: NexusTheme.primaryText
                    }
                    Item { width: Math.max(10, parent.width - 380); height: 1 }
                    Text {
                        text: "✕"
                        font.pixelSize: 16
                        color: NexusTheme.secondaryText
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.showInstallModal = false
                        }
                    }
                }

                Text {
                    text: "License: " + (root.activeModalTool ? root.activeModalTool.licensing : "")
                    font.pixelSize: 11
                    color: NexusTheme.secondaryText
                }

                Text {
                    text: "Verified Installation Commands:"
                    font.pixelSize: 12
                    font.bold: true
                    color: NexusTheme.primaryText
                }

                Rectangle {
                    width: parent.width
                    height: 100
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1

                    ScrollView {
                        anchors.fill: parent
                        anchors.margins: 10
                        Text {
                            text: {
                                if (!root.activeModalTool || !root.activeModalTool.install_methods) return "No method specified.";
                                var out = "";
                                for (var i = 0; i < root.activeModalTool.install_methods.length; i++) {
                                    out += "# " + (root.activeModalTool.install_methods[i].type || "Install").toUpperCase() + ":\n" + root.activeModalTool.install_methods[i].command + "\n\n";
                                }
                                return out;
                            }
                            font.family: NexusTheme.fontFamilyMono
                            font.pixelSize: 11
                            color: NexusTheme.accent
                            wrapMode: Text.Wrap
                        }
                    }
                }

                Text {
                    text: "🛡️ Safety Notice: NEXUS OS respects software licensing. Proprietary binaries are installed directly through official repositories rather than bundled unauthorized redistribution."
                    font.pixelSize: 10
                    color: NexusTheme.secondaryText
                    wrapMode: Text.Wrap
                    width: parent.width
                }
            }
        }
    }
}
