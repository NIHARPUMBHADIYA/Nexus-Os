import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Item {
    id: wizardRoot

    property bool openState: false
    property var bridge: null

    property string selectedTemplate: "rust"
    property string projectName: "my-nexus-service"
    property string projectLocation: "d:/My own os/projects"
    property bool initGit: true
    property bool enableAI: true
    property string selectedDevEnv: "Podman (Rootless Container)"
    property string activeCategory: "All"

    signal projectCreatedSuccessfully(var project)
    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: openState ? 1 : 0
    z: 999999

    Behavior on opacity {
        NumberAnimation { duration: NexusTheme.durationFast }
    }

    function openWizard() {
        openState = true;
    }

    // Backdrop Scrim
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, NexusTheme.isDark ? 0.7 : 0.5)

        MouseArea {
            anchors.fill: parent
            onClicked: wizardRoot.openState = false
        }
    }

    // Modal Card
    Rectangle {
        id: wizardCard
        width: Math.min(parent.width - 48, 860)
        implicitHeight: mainCol.implicitHeight + 40
        anchors.centerIn: parent
        radius: NexusTheme.radiusXL
        color: NexusTheme.elevatedSurface
        border.color: NexusTheme.border
        border.width: 1

        Column {
            id: mainCol
            anchors.fill: parent
            anchors.margins: 24
            spacing: 16

            // Header
            Row {
                width: parent.width
                spacing: 12

                Text { text: "⚡"; font.pixelSize: 22; anchors.verticalCenter: parent.verticalCenter }
                Column {
                    spacing: 2
                    Text {
                        text: "Project Creation Wizard"
                        font.pixelSize: 17
                        font.bold: true
                        font.family: NexusTheme.fontFamilyUI
                        color: NexusTheme.primaryText
                    }
                    Text {
                        text: "Scaffold a verified, containerized, AI-ready developer project."
                        font.pixelSize: 12
                        color: NexusTheme.secondaryText
                    }
                }
                Item { Layout.fillWidth: true; width: 100; height: 1 }
                NexusButton {
                    text: "✕"
                    variant: "ghost"
                    size: "sm"
                    onClicked: wizardRoot.openState = false
                }
            }

            // Step 1: Category Filter Pills
            Row {
                spacing: 6
                Repeater {
                    model: ["All", "Systems", "Frontend", "Backend & Scripting", "AI & ML", "Mobile", "Robotics", "Embedded"]
                    delegate: Rectangle {
                        readonly property bool isCurrent: wizardRoot.activeCategory === modelData
                        width: catLabel.implicitWidth + 14
                        height: 24
                        radius: NexusTheme.radiusPill
                        color: isCurrent ? NexusTheme.accent : (cMouse.containsMouse ? NexusTheme.surface : "transparent")
                        border.color: isCurrent ? NexusTheme.accent : NexusTheme.border
                        border.width: 1

                        Text {
                            id: catLabel
                            anchors.centerIn: parent
                            text: modelData
                            font.pixelSize: 11
                            font.bold: isCurrent
                            color: isCurrent ? "#FFFFFF" : NexusTheme.secondaryText
                        }

                        MouseArea {
                            id: cMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: wizardRoot.activeCategory = modelData
                        }
                    }
                }
            }

            // Step 2: 18 Project Templates Grid
            Grid {
                columns: 3
                spacing: 10
                width: parent.width

                Repeater {
                    model: [
                        { key: "rust", name: "Rust", desc: "Cargo binary with Tokio async runtime", cat: "Systems", icon: "🦀" },
                        { key: "python", name: "Python", desc: "Clean Python application with pytest", cat: "Backend & Scripting", icon: "🐍" },
                        { key: "c_cpp", name: "C / C++", desc: "Modern C++20 with CMake build", cat: "Systems", icon: "⚙" },
                        { key: "react", name: "React", desc: "React 19 with Vite & TypeScript", cat: "Frontend", icon: "⚛" },
                        { key: "nextjs", name: "Next.js", desc: "Next.js 15 App Router Fullstack", cat: "Frontend", icon: "▲" },
                        { key: "node_api", name: "Node.js API", desc: "Express / Fastify REST backend", cat: "Backend & Scripting", icon: "🟢" },
                        { key: "typescript", name: "TypeScript", desc: "Strict ESM library with tsconfig", cat: "Frontend", icon: "🔷" },
                        { key: "fastapi", name: "FastAPI", desc: "High-speed Python ASGI with Uvicorn", cat: "Backend & Scripting", icon: "⚡" },
                        { key: "flask", name: "Flask", desc: "Lightweight Python microservice", cat: "Backend & Scripting", icon: "🧪" },
                        { key: "django", name: "Django", desc: "Enterprise Python battery-included", cat: "Backend & Scripting", icon: "🎸" },
                        { key: "go", name: "Go", desc: "Go microservice with modules", cat: "Backend & Scripting", icon: "🐹" },
                        { key: "java", name: "Java", desc: "Maven / Spring Boot Java 21", cat: "Backend & Scripting", icon: "☕" },
                        { key: "ai_ml", name: "AI / ML", desc: "PyTorch & HuggingFace pipeline", cat: "AI & ML", icon: "🤖" },
                        { key: "ros2", name: "ROS 2", desc: "Robotics node with colcon build", cat: "Robotics", icon: "🦾" },
                        { key: "flutter", name: "Flutter", desc: "Cross-platform mobile & desktop", cat: "Mobile", icon: "💙" },
                        { key: "android", name: "Android", desc: "Kotlin with Jetpack Compose", cat: "Mobile", icon: "🤖" },
                        { key: "arduino", name: "Arduino", desc: "PlatformIO embedded C++ firmware", cat: "Embedded", icon: "🔌" },
                        { key: "empty", name: "Empty", desc: "Clean blank repository directory", cat: "Other", icon: "📄" }
                    ]

                    delegate: Rectangle {
                        readonly property bool isSelected: wizardRoot.selectedTemplate === modelData.key
                        visible: wizardRoot.activeCategory === "All" || wizardRoot.activeCategory === modelData.cat
                        width: (mainCol.width - 20) / 3
                        height: 54
                        radius: NexusTheme.radiusSmall
                        color: isSelected ? NexusTheme.accentSubtle : (tMouse.containsMouse ? NexusTheme.surface : NexusTheme.secondaryBackground)
                        border.color: isSelected ? NexusTheme.accent : NexusTheme.border
                        border.width: isSelected ? 1.5 : 1

                        Row {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 8

                            Text { text: modelData.icon; font.pixelSize: 20; anchors.verticalCenter: parent.verticalCenter }
                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 2
                                width: parent.width - 32

                                Text {
                                    text: modelData.name
                                    font.pixelSize: 12
                                    font.bold: true
                                    color: NexusTheme.primaryText
                                }
                                Text {
                                    text: modelData.desc
                                    font.pixelSize: 10
                                    color: NexusTheme.secondaryText
                                    elide: Text.ElideRight
                                    width: parent.width
                                }
                            }
                        }

                        MouseArea {
                            id: tMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                wizardRoot.selectedTemplate = modelData.key;
                                wizardRoot.projectName = "nexus-" + modelData.key + "-app";
                            }
                        }
                    }
                }
            }

            // Step 3: Project Configuration Details
            Rectangle {
                width: parent.width
                implicitHeight: configCol.implicitHeight + 20
                radius: NexusTheme.radiusMedium
                color: NexusTheme.secondaryBackground
                border.color: NexusTheme.border
                border.width: 1

                Column {
                    id: configCol
                    anchors.fill: parent
                    anchors.margins: 12
                    spacing: 12

                    Row {
                        width: parent.width
                        spacing: 16

                        Column {
                            spacing: 4
                            Text { text: "Project Name"; font.pixelSize: 11; font.bold: true; color: NexusTheme.secondaryText }
                            Rectangle {
                                width: 360
                                height: 32
                                radius: 6
                                color: NexusTheme.surface
                                border.color: NexusTheme.border
                                border.width: 1
                                TextInput {
                                    anchors.fill: parent
                                    anchors.leftMargin: 8
                                    anchors.rightMargin: 8
                                    font.pixelSize: 12
                                    font.family: NexusTheme.fontFamilyMono
                                    color: NexusTheme.primaryText
                                    text: wizardRoot.projectName
                                    onTextChanged: wizardRoot.projectName = text
                                    verticalAlignment: TextInput.AlignVCenter
                                }
                            }
                        }

                        Column {
                            spacing: 4
                            Text { text: "Development Environment"; font.pixelSize: 11; font.bold: true; color: NexusTheme.secondaryText }
                            Row {
                                spacing: 6
                                Repeater {
                                    model: ["Host (Native)", "Podman (Rootless Container)", "Distrobox"]
                                    delegate: Rectangle {
                                        readonly property bool isEnvSel: wizardRoot.selectedDevEnv === modelData
                                        width: envLabel.implicitWidth + 12
                                        height: 32
                                        radius: 6
                                        color: isEnvSel ? NexusTheme.accent : NexusTheme.surface
                                        border.color: isEnvSel ? NexusTheme.accent : NexusTheme.border
                                        border.width: 1

                                        Text {
                                            id: envLabel
                                            anchors.centerIn: parent
                                            text: modelData
                                            font.pixelSize: 11
                                            font.bold: isEnvSel
                                            color: isEnvSel ? "#FFFFFF" : NexusTheme.primaryText
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: wizardRoot.selectedDevEnv = modelData
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Toggles: Git & AI
                    Row {
                        spacing: 24

                        NexusToggle {
                            type: "checkbox"
                            label: "Initialize Git repository (main)"
                            checked: wizardRoot.initGit
                            onToggled: function(c) { wizardRoot.initGit = c; }
                        }

                        NexusToggle {
                            type: "checkbox"
                            label: "Inject local AI context & Ollama model rules"
                            checked: wizardRoot.enableAI
                            onToggled: function(c) { wizardRoot.enableAI = c; }
                        }
                    }
                }
            }

            // Step 4: Bottom Action Bar
            Row {
                anchors.right: parent.right
                spacing: 12

                NexusButton {
                    text: "Cancel"
                    variant: "outline"
                    onClicked: wizardRoot.openState = false
                }

                NexusButton {
                    text: "Create & Open Workspace"
                    variant: "primary"
                    onClicked: {
                        var newProj = {
                            id: "proj:" + wizardRoot.projectName.toLowerCase(),
                            name: wizardRoot.projectName,
                            path: wizardRoot.projectLocation + "/" + wizardRoot.projectName,
                            description: wizardRoot.selectedTemplate.toUpperCase() + " workspace created on NEXUS OS",
                            language: wizardRoot.selectedTemplate,
                            framework: wizardRoot.selectedDevEnv,
                            favorite: false,
                            running: true,
                            last_opened: "Just now",
                            git: { branch: "main", dirty: false, last_commit: "Initial commit" },
                            tasks: [
                                { id: "t1", title: "Verify environment and build", done: false }
                            ]
                        };

                        if (wizardRoot.bridge) {
                            try {
                                wizardRoot.bridge.createProject(
                                    wizardRoot.selectedTemplate,
                                    wizardRoot.projectName,
                                    wizardRoot.projectLocation,
                                    wizardRoot.initGit,
                                    wizardRoot.enableAI,
                                    wizardRoot.selectedDevEnv
                                );
                            } catch(e) {
                                console.log("Bridge creation fallback:", e);
                            }
                        }

                        wizardRoot.openState = false;
                        wizardRoot.projectCreatedSuccessfully(newProj);
                    }
                }
            }
        }
    }
}
