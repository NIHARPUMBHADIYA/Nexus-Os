import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Item {
    id: dashboardRoot

    property var projectsModel: []
    property var bridge: null
    property string searchQuery: ""
    property string activeTab: "all" // "all", "favorites", "running"

    signal openProjectRequested(var project)
    signal createNewRequested()

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 1. DevHub Top Header Bar
        Rectangle {
            Layout.fillWidth: true
            height: 52
            color: NexusTheme.secondaryBackground
            border.color: NexusTheme.border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                spacing: 16

                Row {
                    spacing: 8
                    Layout.alignment: Qt.AlignVCenter
                    Text { text: "📁"; font.pixelSize: 18 }
                    Text {
                        text: "NEXUS Developer Hub"
                        font.pixelSize: 15
                        font.bold: true
                        font.family: NexusTheme.fontFamilyUI
                        color: NexusTheme.primaryText
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                // Project Search Field
                Rectangle {
                    Layout.preferredWidth: 280
                    height: 34
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.surface
                    border.color: searchInput.activeFocus ? NexusTheme.borderFocus : NexusTheme.border
                    border.width: 1
                    Layout.alignment: Qt.AlignVCenter

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        spacing: 8

                        Text { text: "🔍"; font.pixelSize: 12; color: NexusTheme.secondaryText; anchors.verticalCenter: parent.verticalCenter }
                        TextInput {
                            id: searchInput
                            width: parent.width - 32
                            font.pixelSize: 12
                            font.family: NexusTheme.fontFamilyUI
                            color: NexusTheme.primaryText
                            selectByMouse: true
                            anchors.verticalCenter: parent.verticalCenter

                            Text {
                                anchors.fill: parent
                                verticalAlignment: Text.AlignVCenter
                                text: "Search projects (Ctrl+F)..."
                                color: NexusTheme.tertiaryText
                                font.pixelSize: 12
                                visible: searchInput.text === ""
                            }
                            onTextChanged: dashboardRoot.searchQuery = text.toLowerCase()
                        }
                    }
                }

                Item { Layout.fillWidth: true }

                // Create New Project Button
                NexusButton {
                    text: "+ New Project"
                    variant: "primary"
                    size: "sm"
                    onClicked: dashboardRoot.createNewRequested()
                }
            }
        }

        // 2. Main Scrollable Dashboard Content
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            Column {
                width: dashboardRoot.width - 48
                anchors.horizontalCenter: parent.horizontalCenter
                topPadding: 24
                bottomPadding: 32
                spacing: 24

                // Environment Status Summary Bar (Podman, Ollama, mise, Git)
                Rectangle {
                    width: parent.width
                    height: 56
                    radius: NexusTheme.radiusMedium
                    color: NexusTheme.surface
                    border.color: NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 18
                        anchors.rightMargin: 18
                        spacing: 28

                        Row {
                            spacing: 8
                            anchors.verticalCenter: parent.verticalCenter
                            Text { text: "🐳"; font.pixelSize: 15 }
                            Column {
                                spacing: 2
                                Text { text: "Podman (Rootless)"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText }
                                Text { text: "Ready • OCI Runtime"; font.pixelSize: 10; color: NexusTheme.success }
                            }
                        }

                        Rectangle { width: 1; height: 24; color: NexusTheme.border; anchors.verticalCenter: parent.verticalCenter }

                        Row {
                            spacing: 8
                            anchors.verticalCenter: parent.verticalCenter
                            Text { text: "🤖"; font.pixelSize: 15 }
                            Column {
                                spacing: 2
                                Text { text: "AI Core (Ollama)"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText }
                                Text { text: ":11430/v1 • qwen2.5-coder"; font.pixelSize: 10; color: NexusTheme.accent }
                            }
                        }

                        Rectangle { width: 1; height: 24; color: NexusTheme.border; anchors.verticalCenter: parent.verticalCenter }

                        Row {
                            spacing: 8
                            anchors.verticalCenter: parent.verticalCenter
                            Text { text: "⚡"; font.pixelSize: 15 }
                            Column {
                                spacing: 2
                                Text { text: "mise Toolchain"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText }
                                Text { text: "Rust, Node, Python"; font.pixelSize: 10; color: NexusTheme.secondaryText }
                            }
                        }

                        Rectangle { width: 1; height: 24; color: NexusTheme.border; anchors.verticalCenter: parent.verticalCenter }

                        Row {
                            spacing: 8
                            anchors.verticalCenter: parent.verticalCenter
                            Text { text: "🌿"; font.pixelSize: 15 }
                            Column {
                                spacing: 2
                                Text { text: "Git Version Control"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText }
                                Text { text: "All branches clean"; font.pixelSize: 10; color: NexusTheme.success }
                            }
                        }
                    }
                }

                // Filter Tabs: All, Favorites, Running
                Row {
                    spacing: 8
                    NexusTabs {
                        variant: "segmented"
                        model: ["All Projects", "★ Favorites", "● Running Sessions"]
                        currentIndex: dashboardRoot.activeTab === "favorites" ? 1 : (dashboardRoot.activeTab === "running" ? 2 : 0)
                        onTabSelected: function(index, label) {
                            if (index === 0) dashboardRoot.activeTab = "all";
                            else if (index === 1) dashboardRoot.activeTab = "favorites";
                            else if (index === 2) dashboardRoot.activeTab = "running";
                        }
                    }
                }

                // Project Cards Grid
                Column {
                    width: parent.width
                    spacing: 12

                    Repeater {
                        model: {
                            var list = dashboardRoot.projectsModel;
                            var filtered = [];
                            for (var i = 0; i < list.length; i++) {
                                var p = list[i];
                                if (dashboardRoot.activeTab === "favorites" && !p.favorite) continue;
                                if (dashboardRoot.activeTab === "running" && !p.running) continue;
                                if (dashboardRoot.searchQuery !== "" &&
                                    p.name.toLowerCase().indexOf(dashboardRoot.searchQuery) === -1 &&
                                    p.description.toLowerCase().indexOf(dashboardRoot.searchQuery) === -1 &&
                                    p.language.toLowerCase().indexOf(dashboardRoot.searchQuery) === -1) {
                                    continue;
                                }
                                filtered.push(p);
                            }
                            return filtered;
                        }

                        delegate: Rectangle {
                            id: projCard
                            width: parent.width
                            implicitHeight: cardCol.implicitHeight + 32
                            radius: NexusTheme.radiusMedium
                            color: cardMouse.containsMouse ? NexusTheme.elevatedSurface : NexusTheme.surface
                            border.color: cardMouse.containsMouse ? NexusTheme.accent : NexusTheme.border
                            border.width: 1

                            Behavior on color { ColorAnimation { duration: NexusTheme.durationFast } }

                            Column {
                                id: cardCol
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 10

                                // Top row: Title, Favorite star, Language badge, Running pill
                                Row {
                                    width: parent.width

                                    Row {
                                        spacing: 8
                                        anchors.verticalCenter: parent.verticalCenter

                                        // Favorite toggle button
                                        Text {
                                            text: modelData.favorite ? "★" : "☆"
                                            font.pixelSize: 16
                                            color: modelData.favorite ? "#F59E0B" : NexusTheme.tertiaryText
                                            anchors.verticalCenter: parent.verticalCenter

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    if (dashboardRoot.bridge) {
                                                        dashboardRoot.bridge.toggleFavorite(modelData.id);
                                                    }
                                                    modelData.favorite = !modelData.favorite;
                                                }
                                            }
                                        }

                                        Text {
                                            text: modelData.name
                                            font.pixelSize: 16
                                            font.bold: true
                                            font.family: NexusTheme.fontFamilyUI
                                            color: NexusTheme.primaryText
                                            anchors.verticalCenter: parent.verticalCenter
                                        }

                                        // Running indicator
                                        NexusBadge {
                                            visible: modelData.running === true
                                            text: "Running"
                                            status: "success"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                    }

                                    Item { Layout.fillWidth: true; width: 100; height: 1 }

                                    // Action buttons
                                    Row {
                                        spacing: 8
                                        anchors.verticalCenter: parent.verticalCenter

                                        NexusButton {
                                            text: "Open Workspace"
                                            variant: "primary"
                                            size: "sm"
                                            onClicked: dashboardRoot.openProjectRequested(modelData)
                                        }

                                        NexusButton {
                                            text: "Cursor / VS Code"
                                            variant: "outline"
                                            size: "sm"
                                            onClicked: {
                                                if (dashboardRoot.bridge) {
                                                    dashboardRoot.bridge.launchExternalIDE("cursor", modelData.path);
                                                }
                                            }
                                        }
                                    }
                                }

                                // Middle row: Description & Path
                                Text {
                                    text: modelData.description
                                    font.pixelSize: 13
                                    color: NexusTheme.secondaryText
                                }

                                // Bottom row: Git status, Language, Tasks pill, Last opened
                                Row {
                                    spacing: 16

                                    Row {
                                        spacing: 6
                                        anchors.verticalCenter: parent.verticalCenter
                                        Text { text: "🌿"; font.pixelSize: 12 }
                                        Text {
                                            text: modelData.git ? (modelData.git.branch + (modelData.git.dirty ? " (Uncommitted)" : " (Clean)")) : "main"
                                            font.pixelSize: 11
                                            font.family: NexusTheme.fontFamilyMono
                                            color: modelData.git && modelData.git.dirty ? NexusTheme.warning : NexusTheme.secondaryText
                                        }
                                    }

                                    Row {
                                        spacing: 6
                                        anchors.verticalCenter: parent.verticalCenter
                                        Text { text: "⚙"; font.pixelSize: 12 }
                                        Text {
                                            text: modelData.language + (modelData.framework ? " • " + modelData.framework : "")
                                            font.pixelSize: 11
                                            font.family: NexusTheme.fontFamilyMono
                                            color: NexusTheme.tertiaryText
                                        }
                                    }

                                    Row {
                                        spacing: 6
                                        anchors.verticalCenter: parent.verticalCenter
                                        Text { text: "✓"; font.pixelSize: 12 }
                                        Text {
                                            text: (modelData.tasks ? modelData.tasks.filter(t => t.done).length + "/" + modelData.tasks.length + " tasks" : "Tasks ready")
                                            font.pixelSize: 11
                                            color: NexusTheme.secondaryText
                                        }
                                    }

                                    Item { width: 20; height: 1 }

                                    Text {
                                        text: "Opened " + (modelData.last_opened || "recently")
                                        font.pixelSize: 11
                                        color: NexusTheme.tertiaryText
                                        anchors.verticalCenter: parent.verticalCenter
                                    }
                                }
                            }

                            MouseArea {
                                id: cardMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                propagateComposedEvents: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: function(mouse) {
                                    dashboardRoot.openProjectRequested(modelData);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
