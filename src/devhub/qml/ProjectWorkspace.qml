import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Item {
    id: workspaceRoot

    property var currentProject: null
    property var bridge: null

    // Modular panel visibility states
    property bool showFileExplorer: true
    property bool showRightPanel: true
    property bool showBottomPanel: true
    property string activeRightTab: "ai" // "ai", "browser", "git", "db", "docs"
    property string activeBottomTab: "terminal" // "terminal", "logs", "testing"

    // Active file in editor
    property string activeFileName: "main.rs"
    property string activeFileContent: "// NEXUS OS Active Project Workspace\n\nfn main() {\n    println!(\"Running inside NEXUS Developer Hub!\");\n}"

    signal backToDashboardRequested()

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 1. Top Workspace Navigation & Action Toolbar
        Rectangle {
            Layout.fillWidth: true
            height: 48
            color: NexusTheme.secondaryBackground
            border.color: NexusTheme.border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 16
                anchors.rightMargin: 16
                spacing: 12

                // Back Button
                NexusButton {
                    text: "← Workspaces"
                    variant: "subtle"
                    size: "sm"
                    onClicked: workspaceRoot.backToDashboardRequested()
                }

                Rectangle { width: 1; height: 20; color: NexusTheme.border; Layout.alignment: Qt.AlignVCenter }

                // Project Info
                Row {
                    spacing: 8
                    Layout.alignment: Qt.AlignVCenter
                    Text { text: "📁"; font.pixelSize: 14 }
                    Text {
                        text: workspaceRoot.currentProject ? workspaceRoot.currentProject.name : "Active Project"
                        font.pixelSize: 14
                        font.bold: true
                        color: NexusTheme.primaryText
                    }
                    NexusBadge {
                        text: workspaceRoot.currentProject ? (workspaceRoot.currentProject.git ? workspaceRoot.currentProject.git.branch : "main") : "main"
                        status: "info"
                    }
                }

                Item { Layout.fillWidth: true }

                // External IDE Launcher Trigger
                Row {
                    spacing: 6
                    Layout.alignment: Qt.AlignVCenter

                    NexusButton {
                        text: "Cursor"
                        variant: "outline"
                        size: "sm"
                        onClicked: {
                            if (workspaceRoot.bridge && workspaceRoot.currentProject) {
                                workspaceRoot.bridge.launchExternalIDE("cursor", workspaceRoot.currentProject.path);
                            }
                        }
                    }

                    NexusButton {
                        text: "VS Code"
                        variant: "outline"
                        size: "sm"
                        onClicked: {
                            if (workspaceRoot.bridge && workspaceRoot.currentProject) {
                                workspaceRoot.bridge.launchExternalIDE("vscode", workspaceRoot.currentProject.path);
                            }
                        }
                    }

                    NexusButton {
                        text: "Zed"
                        variant: "outline"
                        size: "sm"
                        onClicked: {
                            if (workspaceRoot.bridge && workspaceRoot.currentProject) {
                                workspaceRoot.bridge.launchExternalIDE("zed", workspaceRoot.currentProject.path);
                            }
                        }
                    }
                }

                Rectangle { width: 1; height: 20; color: NexusTheme.border; Layout.alignment: Qt.AlignVCenter }

                // Modular Panel Toggle Switches
                Row {
                    spacing: 4
                    Layout.alignment: Qt.AlignVCenter

                    NexusIconButton {
                        iconText: "📁"
                        tooltipText: "Toggle File Explorer"
                        active: workspaceRoot.showFileExplorer
                        size: 30
                        onClicked: workspaceRoot.showFileExplorer = !workspaceRoot.showFileExplorer
                    }

                    NexusIconButton {
                        iconText: "🤖"
                        tooltipText: "Toggle AI & Side Panel"
                        active: workspaceRoot.showRightPanel
                        size: 30
                        onClicked: workspaceRoot.showRightPanel = !workspaceRoot.showRightPanel
                    }

                    NexusIconButton {
                        iconText: "⌨"
                        tooltipText: "Toggle Terminal & Bottom Panel"
                        active: workspaceRoot.showBottomPanel
                        size: 30
                        onClicked: workspaceRoot.showBottomPanel = !workspaceRoot.showBottomPanel
                    }
                }
            }
        }

        // 2. Middle Main Area (Split: Files | Editor | Right Tool Panel)
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            // Left: File Explorer Panel
            Rectangle {
                visible: workspaceRoot.showFileExplorer
                Layout.preferredWidth: 210
                Layout.fillHeight: true
                color: NexusTheme.secondaryBackground
                border.color: NexusTheme.border
                border.width: 1

                Column {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 8

                    Text {
                        text: "PROJECT FILES"
                        font.pixelSize: 10
                        font.bold: true
                        font.family: NexusTheme.fontFamilyMono
                        color: NexusTheme.tertiaryText
                        leftPadding: 4
                    }

                    // Files List
                    Repeater {
                        model: [
                            { name: "main.rs", icon: "🦀" },
                            { name: "Cargo.toml", icon: "📦" },
                            { name: "README.md", icon: "📖" },
                            { name: ".nexus/project.json", icon: "⚙" },
                            { name: "tests/integration.rs", icon: "🧪" }
                        ]

                        delegate: Rectangle {
                            readonly property bool isFileCurrent: workspaceRoot.activeFileName === modelData.name
                            width: parent.width
                            height: 28
                            radius: 6
                            color: isFileCurrent ? NexusTheme.accentSubtle : (fMouse.containsMouse ? NexusTheme.surface : "transparent")

                            Row {
                                anchors.fill: parent
                                anchors.leftMargin: 8
                                spacing: 8

                                Text { text: modelData.icon; font.pixelSize: 12; anchors.verticalCenter: parent.verticalCenter }
                                Text {
                                    text: modelData.name
                                    font.pixelSize: 12
                                    font.family: NexusTheme.fontFamilyMono
                                    font.bold: isFileCurrent
                                    color: isFileCurrent ? NexusTheme.accent : NexusTheme.primaryText
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }

                            MouseArea {
                                id: fMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    workspaceRoot.activeFileName = modelData.name;
                                    if (modelData.name === "Cargo.toml") {
                                        workspaceRoot.activeFileContent = "[package]\nname = \"nexus-project\"\nversion = \"0.1.0\"\nedition = \"2021\"\n\n[dependencies]\ntokio = { version = \"1.40\", features = [\"full\"] }";
                                    } else if (modelData.name === "README.md") {
                                        workspaceRoot.activeFileContent = "# Project Documentation\n\nNEXUS OS developer-first environment.";
                                    } else {
                                        workspaceRoot.activeFileContent = "// Code for " + modelData.name + "\n\nfn main() {\n    println!(\"Hello from NEXUS!\");\n}";
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // Center: Code Editor Area
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: NexusTheme.isDark ? "#0D1117" : "#FFFFFF"

                Column {
                    anchors.fill: parent
                    spacing: 0

                    // Editor Tab Header
                    Rectangle {
                        width: parent.width
                        height: 34
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 8

                            Rectangle {
                                width: 140
                                height: 34
                                color: NexusTheme.isDark ? "#0D1117" : "#FFFFFF"
                                border.color: NexusTheme.border
                                border.width: 1

                                Row {
                                    anchors.centerIn: parent
                                    spacing: 6
                                    Text { text: "📄"; font.pixelSize: 11 }
                                    Text {
                                        text: workspaceRoot.activeFileName
                                        font.pixelSize: 11
                                        font.family: NexusTheme.fontFamilyMono
                                        color: NexusTheme.primaryText
                                    }
                                }
                            }
                        }
                    }

                    // Code Area with line numbers
                    Row {
                        width: parent.width
                        height: parent.height - 34

                        // Line Numbers
                        Rectangle {
                            width: 38
                            height: parent.height
                            color: NexusTheme.secondaryBackground

                            Column {
                                anchors.fill: parent
                                anchors.topMargin: 10
                                spacing: 4

                                Repeater {
                                    model: 18
                                    delegate: Text {
                                        text: (index + 1)
                                        font.pixelSize: 11
                                        font.family: NexusTheme.fontFamilyMono
                                        color: NexusTheme.tertiaryText
                                        anchors.right: parent.right
                                        anchors.rightMargin: 6
                                    }
                                }
                            }
                        }

                        // Code Text
                        Flickable {
                            width: parent.width - 38
                            height: parent.height
                            contentWidth: width
                            contentHeight: codeInput.implicitHeight + 20
                            clip: true

                            TextEdit {
                                id: codeInput
                                width: parent.width - 16
                                anchors.margins: 10
                                font.family: NexusTheme.fontFamilyMono
                                font.pixelSize: 12
                                color: NexusTheme.primaryText
                                text: workspaceRoot.activeFileContent
                                wrapMode: TextEdit.NoWrap
                                selectByMouse: true
                            }
                        }
                    }
                }
            }

            // Right Tool Panel (AI Assistant, Browser Preview, Git, DB, Docs)
            Rectangle {
                visible: workspaceRoot.showRightPanel
                Layout.preferredWidth: 320
                Layout.fillHeight: true
                color: NexusTheme.secondaryBackground
                border.color: NexusTheme.border
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0

                    // Right Panel Tabs
                    Rectangle {
                        Layout.fillWidth: true
                        height: 36
                        color: NexusTheme.surface
                        border.color: NexusTheme.border
                        border.width: 1

                        Row {
                            anchors.centerIn: parent
                            spacing: 4

                            Repeater {
                                model: [
                                    { id: "ai", label: "AI Copilot", icon: "🤖" },
                                    { id: "browser", label: "Preview", icon: "🌐" },
                                    { id: "git", label: "Git", icon: "🌿" },
                                    { id: "docs", label: "Docs", icon: "📖" }
                                ]

                                delegate: Rectangle {
                                    readonly property bool isTabSel: workspaceRoot.activeRightTab === modelData.id
                                    width: tabText.implicitWidth + 12
                                    height: 26
                                    radius: 6
                                    color: isTabSel ? NexusTheme.accentSubtle : "transparent"

                                    Text {
                                        id: tabText
                                        anchors.centerIn: parent
                                        text: modelData.icon + " " + modelData.label
                                        font.pixelSize: 10
                                        font.bold: isTabSel
                                        color: isTabSel ? NexusTheme.accent : NexusTheme.secondaryText
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: workspaceRoot.activeRightTab = modelData.id
                                    }
                                }
                            }
                        }
                    }

                    // Panel Content: AI Assistant
                    Item {
                        visible: workspaceRoot.activeRightTab === "ai"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 10

                            Text {
                                text: "AI Context: Local Ollama (qwen2.5-coder)"
                                font.pixelSize: 11
                                font.bold: true
                                color: NexusTheme.accent
                            }

                            Rectangle {
                                width: parent.width
                                height: 180
                                radius: 8
                                color: NexusTheme.surface
                                border.color: NexusTheme.border
                                border.width: 1
                                Column {
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    spacing: 4
                                    Text { text: "🤖 Nexus Copilot"; font.pixelSize: 11; font.bold: true; color: NexusTheme.accent }
                                    Text {
                                        text: "I have indexed this workspace. You can ask me to explain code, generate unit tests, or run refactorings."
                                        font.pixelSize: 11
                                        color: NexusTheme.secondaryText
                                        wrapMode: Text.Wrap
                                        width: parent.width
                                    }
                                }
                            }

                            // AI Input field
                            Rectangle {
                                width: parent.width
                                height: 34
                                radius: 6
                                color: NexusTheme.surface
                                border.color: NexusTheme.border
                                border.width: 1

                                TextInput {
                                    anchors.fill: parent
                                    anchors.leftMargin: 8
                                    anchors.rightMargin: 8
                                    font.pixelSize: 11
                                    color: NexusTheme.primaryText
                                    verticalAlignment: TextInput.AlignVCenter

                                    Text {
                                        anchors.fill: parent
                                        verticalAlignment: Text.AlignVCenter
                                        text: "Ask AI assistant..."
                                        color: NexusTheme.tertiaryText
                                        font.pixelSize: 11
                                        visible: parent.text === ""
                                    }
                                }
                            }
                        }
                    }

                    // Panel Content: Browser Preview
                    Item {
                        visible: workspaceRoot.activeRightTab === "browser"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Column {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 8

                            Rectangle {
                                width: parent.width
                                height: 28
                                radius: 4
                                color: NexusTheme.surface
                                Row {
                                    anchors.fill: parent
                                    anchors.leftMargin: 8
                                    spacing: 6
                                    Text { text: "🔒 http://localhost:3000"; font.pixelSize: 11; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.secondaryText; anchors.verticalCenter: parent.verticalCenter }
                                }
                            }

                            Rectangle {
                                width: parent.width
                                height: 200
                                radius: 6
                                color: NexusTheme.surface
                                Text {
                                    anchors.centerIn: parent
                                    text: "🌐 Live Web Preview\nPort 3000 Ready"
                                    font.pixelSize: 12
                                    color: NexusTheme.secondaryText
                                }
                            }
                        }
                    }

                    // Panel Content: Git
                    Item {
                        visible: workspaceRoot.activeRightTab === "git"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Column {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 8

                            Text { text: "Branch: main (Clean)"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                            Text { text: "No uncommitted changes detected."; font.pixelSize: 11; color: NexusTheme.success }
                            NexusButton { text: "Git Pull"; size: "sm"; variant: "outline" }
                        }
                    }

                    // Panel Content: Docs
                    Item {
                        visible: workspaceRoot.activeRightTab === "docs"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Column {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 6
                            Text { text: "README.md Preview"; font.pixelSize: 12; font.bold: true; color: NexusTheme.primaryText }
                            Text { text: "# " + (workspaceRoot.currentProject ? workspaceRoot.currentProject.name : "Project") + "\n\nDocumentation rendered dynamically."; font.pixelSize: 11; color: NexusTheme.secondaryText; wrapMode: Text.Wrap; width: parent.width }
                        }
                    }
                }
            }
        }

        // 3. Bottom Panel (Terminal, Logs, Testing)
        Rectangle {
            visible: workspaceRoot.showBottomPanel
            Layout.fillWidth: true
            Layout.preferredHeight: 180
            color: NexusTheme.secondaryBackground
            border.color: NexusTheme.border
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                // Bottom Panel Header / Tabs
                Rectangle {
                    Layout.fillWidth: true
                    height: 30
                    color: NexusTheme.surface
                    border.color: NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.left: parent.left
                        anchors.leftMargin: 12
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 8

                        Repeater {
                            model: [
                                { id: "terminal", label: "Terminal", icon: "⌨" },
                                { id: "logs", label: "Build Logs", icon: "📋" },
                                { id: "testing", label: "Test Runner", icon: "🧪" }
                            ]

                            delegate: Rectangle {
                                readonly property bool isBottomSel: workspaceRoot.activeBottomTab === modelData.id
                                width: bText.implicitWidth + 12
                                height: 22
                                radius: 4
                                color: isBottomSel ? NexusTheme.accentSubtle : "transparent"

                                Text {
                                    id: bText
                                    anchors.centerIn: parent
                                    text: modelData.icon + " " + modelData.label
                                    font.pixelSize: 11
                                    font.bold: isBottomSel
                                    color: isBottomSel ? NexusTheme.accent : NexusTheme.secondaryText
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: workspaceRoot.activeBottomTab = modelData.id
                                }
                            }
                        }
                    }
                }

                // Bottom Panel Viewport
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: NexusTheme.isDark ? "#0A0D14" : "#F8FAFC"

                    Column {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 4

                        Text {
                            text: "nexus@devhub:" + (workspaceRoot.currentProject ? workspaceRoot.currentProject.path : "~/Projects") + " (main) $"
                            font.pixelSize: 11
                            font.family: NexusTheme.fontFamilyMono
                            color: NexusTheme.accent
                        }

                        Text {
                            text: workspaceRoot.activeBottomTab === "testing" ? "running 4 tests\ntest tests::test_build ... ok\ntest tests::test_env ... ok\ntest result: ok. 4 passed; 0 failed." :
                                  (workspaceRoot.activeBottomTab === "logs" ? "[INFO] Podman rootless runtime initialized.\n[INFO] Ollama endpoint :11434 streaming." :
                                  "Type 'cargo run' or developer commands here.")
                            font.pixelSize: 11
                            font.family: NexusTheme.fontFamilyMono
                            color: NexusTheme.primaryText
                        }
                    }
                }
            }
        }
    }
}
