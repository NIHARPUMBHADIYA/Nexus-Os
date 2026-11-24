import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Rectangle {
    id: root
    color: NexusTheme.background

    property string currentTab: "models" // "models", "services", "hardware", "providers", "free_tiers"
    property string selectedCategory: "all"
    property string searchQuery: ""
    property bool localOnly: false

    // Fallback data if bridge is not attached
    property var hardwareData: (typeof aiCoreBridge !== "undefined" && aiCoreBridge.hardwareStatus) ? aiCoreBridge.hardwareStatus : {
        "ram": { "total_gb": 16.0, "used_gb": 6.2, "free_gb": 9.8, "percent": 38.8 },
        "vram": { "name": "NVIDIA RTX 4070", "total_gb": 8.0, "used_gb": 4.5, "free_gb": 3.5, "percent": 56.2, "headroom_mb": 2048 },
        "safe_headroom_mb": 2048,
        "idle_timeout_minutes": 15,
        "active_models": ["qwen2.5-coder:7b", "nomic-embed-text"]
    }

    property var servicesData: (typeof aiCoreBridge !== "undefined" && aiCoreBridge.servicesList) ? aiCoreBridge.servicesList : [
        { "id": "omniroute", "name": "OmniRoute AI Gateway", "role": "Multi-Provider Dynamic Router", "endpoint": "http://127.0.0.1:20128/v1", "installed": true, "running": true, "latency_ms": 4.2, "version": "1.0.4", "icon": "🔀" },
        { "id": "ollama", "name": "Ollama Local Engine", "role": "Offline Local Model Server", "endpoint": "http://127.0.0.1:11434", "installed": true, "running": true, "latency_ms": 2.1, "version": "0.5.8", "icon": "🦙" }
    ]

    property var modelsData: (typeof aiCoreBridge !== "undefined" && aiCoreBridge.modelsList) ? aiCoreBridge.modelsList : [
        { "id": "qwen2.5-coder:7b", "name": "Qwen 2.5 Coder 7B", "provider": "Ollama (Local)", "category": "coding", "is_local": true, "ram_required_gb": 4.7, "vram_mb": 4200, "size_str": "4.7 GB", "context_size": "32k", "installed": true, "loaded": true, "description": "Premier open-weight coding model with 92+ languages and FIM support." },
        { "id": "deepseek-r1:8b", "name": "DeepSeek R1 Distill 8B", "provider": "Ollama (Local)", "category": "reasoning", "is_local": true, "ram_required_gb": 4.9, "vram_mb": 4500, "size_str": "4.9 GB", "context_size": "32k", "installed": true, "loaded": false, "description": "Chain-of-thought mathematical logic and algorithmic verification." },
        { "id": "llama3.2:3b", "name": "Llama 3.2 3B", "provider": "Ollama (Local)", "category": "general", "is_local": true, "ram_required_gb": 2.0, "vram_mb": 1800, "size_str": "2.0 GB", "context_size": "128k", "installed": true, "loaded": false, "description": "Snappy general assistant with 128k context and high efficiency." },
        { "id": "nomic-embed-text", "name": "Nomic Embed Text v1.5", "provider": "Ollama (Local)", "category": "embeddings", "is_local": true, "ram_required_gb": 0.3, "vram_mb": 300, "size_str": "274 MB", "context_size": "8k", "installed": true, "loaded": true, "description": "Embedding model for Spotlight and Developer Hub project semantic indexing." },
        { "id": "claude-3-7-sonnet", "name": "Claude 3.7 Sonnet", "provider": "Anthropic Cloud", "category": "coding", "is_local": false, "ram_required_gb": 0.0, "vram_mb": 0, "size_str": "Cloud API", "context_size": "200k", "installed": true, "loaded": false, "description": "Frontier hybrid reasoning and agentic software engineering." }
    ]

    property var providersData: (typeof aiCoreBridge !== "undefined" && aiCoreBridge.providersList) ? aiCoreBridge.providersList : [
        { "id": "ollama", "name": "Ollama (Local)", "category": "local", "is_configured": true, "masked_key": "None required", "description": "Local offline execution engine for open-weights models." },
        { "id": "omniroute", "name": "OmniRoute Gateway", "category": "router", "is_configured": true, "masked_key": "Local proxy", "description": "Multi-provider AI routing gateway and token compressor." },
        { "id": "groq", "name": "Groq Cloud (Free Tier)", "category": "cloud", "is_configured": true, "masked_key": "gsk...4e19", "description": "Ultra-low latency LPU inference with generous free quota." },
        { "id": "gemini", "name": "Google Gemini", "category": "cloud", "is_configured": true, "masked_key": "AIza...8b21", "description": "Multimodal flagship reasoning and code analysis." },
        { "id": "openai", "name": "OpenAI", "category": "cloud", "is_configured": false, "masked_key": "", "description": "GPT-4o and o3 reasoning models." }
    ]

    property var freeTiersData: (typeof aiCoreBridge !== "undefined" && aiCoreBridge.freeTiersList) ? aiCoreBridge.freeTiersList : [
        { "id": "ollama_local", "provider": "Ollama (Local)", "name": "Local Hardware Execution", "tier_type": "100% Free & Offline", "limits": "Unlimited requests, zero telemetry, private to your workstation.", "requirements": "Requires local GPU or CPU RAM.", "models": ["qwen2.5-coder:7b", "llama3.2:3b", "deepseek-r1:8b"], "url": "https://ollama.com", "requires_api_key": false },
        { "id": "groq_free", "provider": "Groq Cloud", "name": "LPU Inference Free Tier", "tier_type": "Free Developer Tier", "limits": "30 Requests/min, 14,400 Tokens/min, 500k Tokens/day.", "requirements": "Requires a free account and API key from console.groq.com.", "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"], "url": "https://console.groq.com", "requires_api_key": true },
        { "id": "gemini_free", "provider": "Google AI Studio", "name": "Gemini Developer Tier", "tier_type": "Free Tier (Rate-Limited)", "limits": "15 Requests/min, 1,500 Requests/day for Flash models.", "requirements": "Requires a free Google account and API key from aistudio.google.com.", "models": ["gemini-2.0-flash", "gemini-1.5-flash"], "url": "https://aistudio.google.com", "requires_api_key": true }
    ]

    Connections {
        target: (typeof aiCoreBridge !== "undefined") ? aiCoreBridge : null
        function onHardwareChanged() { root.hardwareData = aiCoreBridge.hardwareStatus; }
        function onServicesChanged() { root.servicesData = aiCoreBridge.servicesList; }
        function onModelsChanged() { root.modelsData = aiCoreBridge.modelsList; }
        function onProvidersChanged() { root.providersData = aiCoreBridge.providersList; }
    }

    Column {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        // Header & Status Strip
        Rectangle {
            width: parent.width
            height: 68
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
                    text: "⚡"
                    font.pixelSize: 24
                    anchors.verticalCenter: parent.verticalCenter
                }

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 2

                    Text {
                        text: "NEXUS AI CORE"
                        font.pixelSize: 15
                        font.bold: true
                        color: NexusTheme.primaryText
                    }
                    Text {
                        text: "System-wide Local AI Multiplexer, Hardware Governor & Provider Registry"
                        font.pixelSize: 11
                        color: NexusTheme.secondaryText
                    }
                }

                Item { width: Math.max(10, root.width - 660); height: 1 }

                // Proxy status pill
                Rectangle {
                    height: 28
                    width: 210
                    radius: NexusTheme.radiusPill
                    color: NexusTheme.successSubtle
                    border.color: NexusTheme.success
                    border.width: 1
                    anchors.verticalCenter: parent.verticalCenter

                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Rectangle {
                            width: 8; height: 8; radius: 4
                            color: NexusTheme.success
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        Text {
                            text: "PROXY :11430/v1 ONLINE"
                            font.pixelSize: 10
                            font.bold: true
                            font.family: NexusTheme.fontFamilyMono
                            color: NexusTheme.success
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

                // Refresh Button
                Rectangle {
                    width: 32
                    height: 32
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1
                    anchors.verticalCenter: parent.verticalCenter

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
                            if (typeof aiCoreBridge !== "undefined") {
                                aiCoreBridge.refreshAll();
                            }
                        }
                    }
                }
            }
        }

        // Navigation Tabs Strip
        Row {
            spacing: 8

            Repeater {
                model: [
                    { "id": "models", "label": "Model Center", "icon": "🧠" },
                    { "id": "services", "label": "Services & Daemons", "icon": "⚙️" },
                    { "id": "hardware", "label": "Hardware Watchdog", "icon": "📊" },
                    { "id": "providers", "label": "Providers & Keys", "icon": "🔑" },
                    { "id": "free_tiers", "label": "Free Tiers", "icon": "🎁" }
                ]

                delegate: Rectangle {
                    height: 34
                    width: 150
                    radius: NexusTheme.radiusSmall
                    color: root.currentTab === modelData.id ? NexusTheme.surface : "transparent"
                    border.color: root.currentTab === modelData.id ? NexusTheme.accent : NexusTheme.border
                    border.width: root.currentTab === modelData.id ? 1.5 : 1

                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Text { text: modelData.icon; font.pixelSize: 13 }
                        Text {
                            text: modelData.label
                            font.pixelSize: 12
                            font.bold: root.currentTab === modelData.id
                            color: root.currentTab === modelData.id ? NexusTheme.accent : NexusTheme.secondaryText
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.currentTab = modelData.id
                    }
                }
            }
        }

        // Content Area Container
        Rectangle {
            width: parent.width
            height: root.height - 180
            radius: NexusTheme.radiusMedium
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1
            clip: true

            // ==========================================
            // TAB 1: MODEL CENTER
            // ==========================================
            Column {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                visible: root.currentTab === "models"

                // Category Chips and Search
                Row {
                    width: parent.width
                    spacing: 12

                    // Category Selector
                    Row {
                        spacing: 6
                        Repeater {
                            model: ["all", "coding", "reasoning", "general", "vision", "embeddings", "lightweight", "large"]
                            delegate: Rectangle {
                                height: 28
                                width: Math.max(50, catText.implicitWidth + 16)
                                radius: NexusTheme.radiusPill
                                color: root.selectedCategory === modelData ? NexusTheme.accent : NexusTheme.secondaryBackground
                                border.color: root.selectedCategory === modelData ? NexusTheme.accent : NexusTheme.border
                                border.width: 1

                                Text {
                                    id: catText
                                    anchors.centerIn: parent
                                    text: modelData.charAt(0).toUpperCase() + modelData.slice(1)
                                    font.pixelSize: 11
                                    font.bold: root.selectedCategory === modelData
                                    color: root.selectedCategory === modelData ? "#FFFFFF" : NexusTheme.secondaryText
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        root.selectedCategory = modelData;
                                        if (typeof aiCoreBridge !== "undefined") {
                                            aiCoreBridge.filterModels(root.selectedCategory, searchInput.text, root.localOnly);
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Item { width: Math.max(10, parent.width - 800); height: 1 }

                    // Search Input
                    Rectangle {
                        width: 220
                        height: 28
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1

                        TextInput {
                            id: searchInput
                            anchors.fill: parent
                            anchors.leftMargin: 10
                            anchors.rightMargin: 10
                            verticalAlignment: TextInput.AlignVCenter
                            font.pixelSize: 11
                            color: NexusTheme.primaryText
                            clip: true

                            Text {
                                anchors.verticalCenter: parent.verticalCenter
                                text: "Search models..."
                                font.pixelSize: 11
                                color: NexusTheme.secondaryText
                                visible: !searchInput.text
                            }

                            onTextChanged: {
                                if (typeof aiCoreBridge !== "undefined") {
                                    aiCoreBridge.filterModels(root.selectedCategory, searchInput.text, root.localOnly);
                                }
                            }
                        }
                    }
                }

                // Models List ScrollView
                ScrollView {
                    width: parent.width
                    height: parent.height - 50
                    clip: true

                    Column {
                        width: parent.width - 16
                        spacing: 8

                        Repeater {
                            model: root.modelsData

                            delegate: Rectangle {
                                width: parent.width
                                height: 72
                                radius: NexusTheme.radiusSmall
                                color: modelData.loaded ? NexusTheme.accentSubtle : NexusTheme.secondaryBackground
                                border.color: modelData.loaded ? NexusTheme.accent : NexusTheme.border
                                border.width: 1

                                Row {
                                    anchors.fill: parent
                                    anchors.leftMargin: 16
                                    anchors.rightMargin: 16
                                    spacing: 14

                                    Text {
                                        text: modelData.category === "coding" ? "💻" : (modelData.category === "reasoning" ? "🧠" : (modelData.category === "vision" ? "👁️" : "🤖"))
                                        font.pixelSize: 22
                                        anchors.verticalCenter: parent.verticalCenter
                                    }

                                    Column {
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: 3
                                        width: Math.max(200, parent.width - 450)

                                        Row {
                                            spacing: 8
                                            Text {
                                                text: modelData.name
                                                font.pixelSize: 13
                                                font.bold: true
                                                font.family: NexusTheme.fontFamilyMono
                                                color: NexusTheme.primaryText
                                            }
                                            Rectangle {
                                                height: 16
                                                width: catTag.implicitWidth + 8
                                                radius: NexusTheme.radiusPill
                                                color: NexusTheme.surface
                                                border.color: NexusTheme.border
                                                border.width: 1
                                                anchors.verticalCenter: parent.verticalCenter
                                                Text {
                                                    id: catTag
                                                    anchors.centerIn: parent
                                                    text: modelData.category.toUpperCase()
                                                    font.pixelSize: 9
                                                    font.bold: true
                                                    color: NexusTheme.accent
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
                                            text: modelData.provider + " • Size: " + modelData.size_str + " • Context: " + modelData.context_size + (modelData.is_local ? " • Req RAM: " + modelData.ram_required_gb + " GB" : "")
                                            font.pixelSize: 10
                                            color: NexusTheme.secondaryText
                                        }
                                    }

                                    Item { width: 10; height: 1 }

                                    // Status and Actions
                                    Row {
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: 8

                                        // VRAM Status Pill
                                        Rectangle {
                                            height: 24
                                            width: 110
                                            radius: NexusTheme.radiusSmall
                                            color: modelData.loaded ? NexusTheme.accent : NexusTheme.surface
                                            border.color: modelData.loaded ? NexusTheme.accent : NexusTheme.border
                                            border.width: 1
                                            anchors.verticalCenter: parent.verticalCenter

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.loaded ? "Active in VRAM" : (modelData.installed ? "Installed" : "Available")
                                                font.pixelSize: 10
                                                font.bold: true
                                                color: modelData.loaded ? "#FFFFFF" : NexusTheme.secondaryText
                                            }
                                        }

                                        // Load / Unload Button
                                        Rectangle {
                                            width: 80
                                            height: 28
                                            radius: NexusTheme.radiusSmall
                                            color: modelData.loaded ? NexusTheme.errorSubtle : NexusTheme.accentSubtle
                                            border.color: modelData.loaded ? NexusTheme.error : NexusTheme.accent
                                            border.width: 1
                                            anchors.verticalCenter: parent.verticalCenter
                                            visible: modelData.is_local && modelData.installed

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.loaded ? "Unload" : "Load"
                                                font.pixelSize: 11
                                                font.bold: true
                                                color: modelData.loaded ? NexusTheme.error : NexusTheme.accent
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    if (typeof aiCoreBridge !== "undefined") {
                                                        if (modelData.loaded) {
                                                            aiCoreBridge.unloadModel(modelData.id);
                                                        } else {
                                                            aiCoreBridge.loadModel(modelData.id);
                                                        }
                                                    }
                                                }
                                            }
                                        }

                                        // Pull / Download Button
                                        Rectangle {
                                            width: 70
                                            height: 28
                                            radius: NexusTheme.radiusSmall
                                            color: NexusTheme.accentSubtle
                                            border.color: NexusTheme.accent
                                            border.width: 1
                                            anchors.verticalCenter: parent.verticalCenter
                                            visible: modelData.is_local && !modelData.installed

                                            Text {
                                                anchors.centerIn: parent
                                                text: "Pull"
                                                font.pixelSize: 11
                                                font.bold: true
                                                color: NexusTheme.accent
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    if (typeof aiCoreBridge !== "undefined") {
                                                        aiCoreBridge.pullModel(modelData.id);
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

            // ==========================================
            // TAB 2: SERVICES & DAEMONS
            // ==========================================
            Column {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 16
                visible: root.currentTab === "services"

                Text {
                    text: "Background AI System Services"
                    font.pixelSize: 15
                    font.bold: true
                    color: NexusTheme.primaryText
                }

                Repeater {
                    model: root.servicesData

                    delegate: Rectangle {
                        width: parent.width
                        height: 90
                        radius: NexusTheme.radiusMedium
                        color: NexusTheme.secondaryBackground
                        border.color: modelData.running ? NexusTheme.success : NexusTheme.border
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 20
                            anchors.rightMargin: 20
                            spacing: 16

                            Text {
                                text: modelData.icon
                                font.pixelSize: 32
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 4
                                width: Math.max(300, parent.width - 480)

                                Row {
                                    spacing: 10
                                    Text {
                                        text: modelData.name
                                        font.pixelSize: 14
                                        font.bold: true
                                        color: NexusTheme.primaryText
                                    }
                                    Rectangle {
                                        height: 18
                                        width: 70
                                        radius: NexusTheme.radiusPill
                                        color: modelData.running ? NexusTheme.successSubtle : NexusTheme.errorSubtle
                                        border.color: modelData.running ? NexusTheme.success : NexusTheme.error
                                        border.width: 1
                                        Text {
                                            anchors.centerIn: parent
                                            text: modelData.running ? "RUNNING" : "STOPPED"
                                            font.pixelSize: 9
                                            font.bold: true
                                            color: modelData.running ? NexusTheme.success : NexusTheme.error
                                        }
                                    }
                                }

                                Text {
                                    text: modelData.role + " • Endpoint: " + modelData.endpoint
                                    font.pixelSize: 11
                                    font.family: NexusTheme.fontFamilyMono
                                    color: NexusTheme.secondaryText
                                }

                                Text {
                                    text: "Installed: " + (modelData.installed ? "Yes (v" + modelData.version + ")" : "Not detected — run: " + modelData.install_command) + " • Latency: " + modelData.latency_ms + "ms"
                                    font.pixelSize: 10
                                    color: NexusTheme.secondaryText
                                }
                            }

                            Item { width: 10; height: 1 }

                            // Action buttons
                            Row {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 10

                                Rectangle {
                                    width: 70
                                    height: 32
                                    radius: NexusTheme.radiusSmall
                                    color: modelData.running ? NexusTheme.errorSubtle : NexusTheme.successSubtle
                                    border.color: modelData.running ? NexusTheme.error : NexusTheme.success
                                    border.width: 1

                                    Text {
                                        anchors.centerIn: parent
                                        text: modelData.running ? "Stop" : "Start"
                                        font.pixelSize: 11
                                        font.bold: true
                                        color: modelData.running ? NexusTheme.error : NexusTheme.success
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            if (typeof aiCoreBridge !== "undefined") {
                                                if (modelData.running) {
                                                    aiCoreBridge.stopService(modelData.id);
                                                } else {
                                                    aiCoreBridge.startService(modelData.id);
                                                }
                                            }
                                        }
                                    }
                                }

                                Rectangle {
                                    width: 70
                                    height: 32
                                    radius: NexusTheme.radiusSmall
                                    color: NexusTheme.surface
                                    border.color: NexusTheme.border
                                    border.width: 1

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Restart"
                                        font.pixelSize: 11
                                        color: NexusTheme.primaryText
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            if (typeof aiCoreBridge !== "undefined") {
                                                aiCoreBridge.restartService(modelData.id);
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
            // TAB 3: HARDWARE WATCHDOG
            // ==========================================
            Column {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 20
                visible: root.currentTab === "hardware"

                Text {
                    text: "Hardware Watchdog & VRAM Allocation Governor"
                    font.pixelSize: 15
                    font.bold: true
                    color: NexusTheme.primaryText
                }

                // GPU VRAM Meter Card
                Rectangle {
                    width: parent.width
                    height: 120
                    radius: NexusTheme.radiusMedium
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1

                    Column {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 10

                        Row {
                            width: parent.width
                            Text {
                                text: "GPU VRAM: " + (root.hardwareData.vram ? root.hardwareData.vram.name : "GPU") + " (" + (root.hardwareData.vram ? root.hardwareData.vram.total_gb : 8) + " GB Total)"
                                font.pixelSize: 13
                                font.bold: true
                                color: NexusTheme.primaryText
                            }
                            Item { width: Math.max(10, parent.width - 550); height: 1 }
                            Text {
                                text: (root.hardwareData.vram ? root.hardwareData.vram.used_gb : 4.5) + " GB in use (" + (root.hardwareData.vram ? root.hardwareData.vram.percent : 56.2) + "%)"
                                font.pixelSize: 12
                                color: NexusTheme.accent
                            }
                        }

                        // Progress Bar
                        Rectangle {
                            width: parent.width
                            height: 14
                            radius: 7
                            color: NexusTheme.surface
                            clip: true

                            Rectangle {
                                width: parent.width * ((root.hardwareData.vram ? root.hardwareData.vram.percent : 56.2) / 100.0)
                                height: parent.height
                                radius: 7
                                color: NexusTheme.accent
                            }
                        }

                        Text {
                            text: "🛡️ Compositor Headroom: " + (root.hardwareData.safe_headroom_mb || 2048) + " MB reserved strictly for Wayland KWin desktop compositing."
                            font.pixelSize: 11
                            color: NexusTheme.success
                        }
                    }
                }

                // System RAM Meter Card
                Rectangle {
                    width: parent.width
                    height: 100
                    radius: NexusTheme.radiusMedium
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1

                    Column {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 10

                        Row {
                            width: parent.width
                            Text {
                                text: "System RAM: " + (root.hardwareData.ram ? root.hardwareData.ram.total_gb : 16) + " GB Total"
                                font.pixelSize: 13
                                font.bold: true
                                color: NexusTheme.primaryText
                            }
                            Item { width: Math.max(10, parent.width - 450); height: 1 }
                            Text {
                                text: (root.hardwareData.ram ? root.hardwareData.ram.used_gb : 6.2) + " GB in use (" + (root.hardwareData.ram ? root.hardwareData.ram.percent : 38.8) + "%)"
                                font.pixelSize: 12
                                color: NexusTheme.accent
                            }
                        }

                        Rectangle {
                            width: parent.width
                            height: 14
                            radius: 7
                            color: NexusTheme.surface
                            clip: true

                            Rectangle {
                                width: parent.width * ((root.hardwareData.ram ? root.hardwareData.ram.percent : 38.8) / 100.0)
                                height: parent.height
                                radius: 7
                                color: NexusTheme.accent
                            }
                        }
                    }
                }

                // Idle unallocation policy
                Rectangle {
                    width: parent.width
                    height: 50
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 16
                        spacing: 12
                        Text { text: "⏱️"; font.pixelSize: 18; anchors.verticalCenter: parent.verticalCenter }
                        Text {
                            text: "Idle Model Unallocation Policy: Inactive models automatically unallocated after " + (root.hardwareData.idle_timeout_minutes || 15) + " minutes to free VRAM."
                            font.pixelSize: 11
                            color: NexusTheme.secondaryText
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }

            // ==========================================
            // TAB 4: PROVIDERS & CREDENTIALS
            // ==========================================
            Column {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 14
                visible: root.currentTab === "providers"

                Text {
                    text: "AI Provider Integrations & Secure Key Vault"
                    font.pixelSize: 15
                    font.bold: true
                    color: NexusTheme.primaryText
                }

                ScrollView {
                    width: parent.width
                    height: parent.height - 40
                    clip: true

                    Column {
                        width: parent.width - 16
                        spacing: 8

                        Repeater {
                            model: root.providersData

                            delegate: Rectangle {
                                width: parent.width
                                height: 60
                                radius: NexusTheme.radiusSmall
                                color: NexusTheme.secondaryBackground
                                border.color: NexusTheme.border
                                border.width: 1

                                Row {
                                    anchors.fill: parent
                                    anchors.leftMargin: 16
                                    anchors.rightMargin: 16
                                    spacing: 16

                                    Column {
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: 2
                                        width: 250

                                        Text {
                                            text: modelData.name
                                            font.pixelSize: 13
                                            font.bold: true
                                            color: NexusTheme.primaryText
                                        }
                                        Text {
                                            text: modelData.description
                                            font.pixelSize: 10
                                            color: NexusTheme.secondaryText
                                            elide: Text.ElideRight
                                            width: parent.width
                                        }
                                    }

                                    Text {
                                        text: "Status: " + (modelData.is_configured ? "Configured" : "Unconfigured") + (modelData.masked_key ? " (" + modelData.masked_key + ")" : "")
                                        font.pixelSize: 11
                                        font.family: NexusTheme.fontFamilyMono
                                        color: modelData.is_configured ? NexusTheme.success : NexusTheme.warning
                                        anchors.verticalCenter: parent.verticalCenter
                                    }

                                    Item { width: Math.max(10, parent.width - 550); height: 1 }

                                    Rectangle {
                                        width: 90
                                        height: 28
                                        radius: NexusTheme.radiusSmall
                                        color: NexusTheme.surface
                                        border.color: NexusTheme.border
                                        border.width: 1
                                        anchors.verticalCenter: parent.verticalCenter

                                        Text {
                                            anchors.centerIn: parent
                                            text: "Test API"
                                            font.pixelSize: 11
                                            color: NexusTheme.primaryText
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                if (typeof aiCoreBridge !== "undefined") {
                                                    aiCoreBridge.testProvider(modelData.id);
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
            // TAB 5: FREE TIERS DISCLOSURE
            // ==========================================
            Column {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 14
                visible: root.currentTab === "free_tiers"

                Text {
                    text: "Legitimate Free AI Tiers & Usage Limits"
                    font.pixelSize: 15
                    font.bold: true
                    color: NexusTheme.primaryText
                }

                ScrollView {
                    width: parent.width
                    height: parent.height - 40
                    clip: true

                    Column {
                        width: parent.width - 16
                        spacing: 10

                        Repeater {
                            model: root.freeTiersData

                            delegate: Rectangle {
                                width: parent.width
                                height: 90
                                radius: NexusTheme.radiusSmall
                                color: NexusTheme.secondaryBackground
                                border.color: NexusTheme.border
                                border.width: 1

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: 14
                                    spacing: 4

                                    Row {
                                        spacing: 10
                                        Text {
                                            text: modelData.name + " (" + modelData.provider + ")"
                                            font.pixelSize: 13
                                            font.bold: true
                                            color: NexusTheme.primaryText
                                        }
                                        Rectangle {
                                            height: 16
                                            width: tierLabel.implicitWidth + 8
                                            radius: NexusTheme.radiusPill
                                            color: NexusTheme.successSubtle
                                            border.color: NexusTheme.success
                                            border.width: 1
                                            Text {
                                                id: tierLabel
                                                anchors.centerIn: parent
                                                text: modelData.tier_type.toUpperCase()
                                                font.pixelSize: 9
                                                font.bold: true
                                                color: NexusTheme.success
                                            }
                                        }
                                    }

                                    Text {
                                        text: "Limits: " + modelData.limits
                                        font.pixelSize: 11
                                        color: NexusTheme.accent
                                    }

                                    Text {
                                        text: "Requirements: " + modelData.requirements + " • Portal: " + modelData.url
                                        font.pixelSize: 10
                                        color: NexusTheme.secondaryText
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
