import QtQuick
import QtQuick.Controls

Item {
    id: launcherRoot

    property bool openState: false
    property var windowManager: null
    property string searchQuery: ""

    signal appLaunched(string appType, string title, string icon)
    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: openState ? 1 : 0
    z: 99999

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationNormal }
    }

    // Apps catalog
    readonly property var allApps: [
        { appType: "terminal", title: "Nexus Terminal", icon: "⌨", desc: "Zsh / Bash with Starship prompt & AI command integration", category: "Developer Tools" },
        { appType: "editor", title: "Code Editor", icon: "💻", desc: "Lightweight developer editor with syntax highlighting", category: "Developer Tools" },
        { appType: "devhub", title: "Developer Hub", icon: "📁", desc: "Workspace orchestrator, container manager & git monitor", category: "Developer Tools" },
        { appType: "tools", title: "AI Tools Integrator", icon: "🛠️", desc: "Configure 15 modern AI tools & IDEs with NEXUS AI Core", category: "Developer Tools" },
        { appType: "aicore", title: "Nexus AI Core", icon: "🤖", desc: "Local Ollama models, VRAM governor & OpenAI /v1 proxy", category: "AI & ML" },
        { appType: "devpacks", title: "Developer Packs", icon: "📦", desc: "One-click curated environments: Full-Stack, AI/ML, Vibe Coder...", category: "Developer Tools" },
        { appType: "software_center", title: "Software Center", icon: "🛍️", desc: "Discover and install developer tools, languages, and IDEs", category: "System Utilities" },
        { appType: "settings", title: "System Settings", icon: "⚙", desc: "Appearance, display scaling, keyboard shortcuts, network", category: "System Utilities" }
    ]

    // Scrim backdrop
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, NexusTheme.isDark ? 0.65 : 0.45)

        MouseArea {
            anchors.fill: parent
            onClicked: launcherRoot.closeRequested()
        }
    }

    // Centered Launcher Overlay Card
    Rectangle {
        id: card
        width: Math.min(parent.width - 64, 680)
        implicitHeight: layoutCol.implicitHeight + 48
        anchors.centerIn: parent
        radius: NexusTheme.radiusXL
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        scale: launcherRoot.openState ? 1.0 : 0.95
        Behavior on scale {
            NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
        }

        Column {
            id: layoutCol
            anchors.fill: parent
            anchors.margins: 24
            spacing: 18

            // Header & Search Input
            Row {
                width: parent.width
                spacing: 12

                Text {
                    text: "🚀"
                    font.pixelSize: 22
                    anchors.verticalCenter: parent.verticalCenter
                }

                Rectangle {
                    width: parent.width - 34
                    height: 42
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.secondaryBackground
                    border.color: searchInput.activeFocus ? NexusTheme.borderFocus : NexusTheme.border
                    border.width: 1.5

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 12
                        spacing: 8

                        Text {
                            text: "🔍"
                            font.pixelSize: 13
                            anchors.verticalCenter: parent.verticalCenter
                            color: NexusTheme.secondaryText
                        }

                        TextInput {
                            id: searchInput
                            width: parent.width - 32
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 13
                            font.family: NexusTheme.fontFamilyUI
                            color: NexusTheme.primaryText
                            selectByMouse: true

                            Text {
                                anchors.fill: parent
                                verticalAlignment: Text.AlignVCenter
                                text: "Search applications, developer tools, models..."
                                color: NexusTheme.tertiaryText
                                font.pixelSize: 13
                                visible: searchInput.text === ""
                            }

                            onTextChanged: launcherRoot.searchQuery = text.toLowerCase()
                        }
                    }
                }
            }

            // Grid of Applications
            Grid {
                columns: 2
                spacing: 12
                width: parent.width

                Repeater {
                    model: {
                        if (launcherRoot.searchQuery === "") return launcherRoot.allApps;
                        var filtered = [];
                        for (var i = 0; i < launcherRoot.allApps.length; i++) {
                            var app = launcherRoot.allApps[i];
                            if (app.title.toLowerCase().indexOf(launcherRoot.searchQuery) !== -1 ||
                                app.desc.toLowerCase().indexOf(launcherRoot.searchQuery) !== -1 ||
                                app.category.toLowerCase().indexOf(launcherRoot.searchQuery) !== -1) {
                                filtered.push(app);
                            }
                        }
                        return filtered;
                    }

                    delegate: Rectangle {
                        width: (layoutCol.width - 12) / 2
                        height: 64
                        radius: NexusTheme.radiusMedium
                        color: appMouse.containsMouse ? NexusTheme.surface : NexusTheme.secondaryBackground
                        border.color: appMouse.containsMouse ? NexusTheme.accent : NexusTheme.border
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 14
                            anchors.rightMargin: 14
                            spacing: 12

                            Text {
                                text: modelData.icon
                                font.pixelSize: 24
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 2
                                width: parent.width - 44

                                Text {
                                    text: modelData.title
                                    font.pixelSize: 13
                                    font.bold: true
                                    font.family: NexusTheme.fontFamilyUI
                                    color: NexusTheme.primaryText
                                }

                                Text {
                                    text: modelData.desc
                                    font.pixelSize: 11
                                    font.family: NexusTheme.fontFamilyUI
                                    color: NexusTheme.secondaryText
                                    elide: Text.ElideRight
                                    width: parent.width
                                }
                            }
                        }

                        MouseArea {
                            id: appMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (windowManager) {
                                    windowManager.openApp(modelData.appType, modelData.title, modelData.icon);
                                }
                                launcherRoot.appLaunched(modelData.appType, modelData.title, modelData.icon);
                                launcherRoot.closeRequested();
                            }
                        }
                    }
                }
            }

            // Keyboard navigation hint footer
            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 8

                Text {
                    text: "Press ESC to close  •  Click any application to launch"
                    font.pixelSize: 11
                    font.family: NexusTheme.fontFamilyUI
                    color: NexusTheme.tertiaryText
                }
            }
        }
    }
}
