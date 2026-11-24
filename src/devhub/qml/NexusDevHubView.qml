import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Item {
    id: hubRoot
    width: 1080
    height: 720

    // Active view: "dashboard" or "workspace"
    property string activeView: "dashboard"
    property var activeProject: null

    // Bridge instance or fallback mock data
    property var bridge: null

    // Project list model
    property var projectsList: [
        {
            id: "proj:nexus-os",
            name: "nexus-os",
            path: "d:/My own os",
            description: "Developer-first, AI-native Linux operating system",
            language: "Rust / Qt6",
            framework: "KDE Plasma 6 / Wayland",
            favorite: true,
            running: true,
            last_opened: "Just now",
            git: { branch: "main", dirty: false, last_commit: "feat(spotlight): universal launcher & FTS5 search" },
            tasks: [
                { id: "t1", title: "Implement Developer Hub", done: true },
                { id: "t2", title: "Connect Universal Spotlight", done: true },
                { id: "t3", title: "Hardware VRAM Watchdog", done: false }
            ],
            dev_commands: { build: "cargo build", test: "cargo test", run: "python tools/run_desktop.py" }
        },
        {
            id: "proj:ai-agent-core",
            name: "ai-agent-core",
            path: "~/Projects/ai-agent-core",
            description: "Autonomous coding agent orchestrator with local context injection",
            language: "Python",
            framework: "PyTorch / Transformers",
            favorite: true,
            running: false,
            last_opened: "1 hour ago",
            git: { branch: "feature/tool-calling", dirty: true, last_commit: "refactor: optimize token streaming buffer" },
            tasks: [
                { id: "t1", title: "Benchmark Ollama latency", done: true },
                { id: "t2", title: "Implement tool call parser", done: false }
            ],
            dev_commands: { run: "python main.py", test: "pytest" }
        },
        {
            id: "proj:robotics-nav2",
            name: "robotics-nav2",
            path: "~/Projects/robotics-nav2",
            description: "ROS 2 navigation and lidar odometry stack",
            language: "C++",
            framework: "ROS 2 Humble",
            favorite: false,
            running: false,
            last_opened: "Yesterday",
            git: { branch: "humble", dirty: false, last_commit: "fix: resolve lidar serial baud rate timing" },
            tasks: [
                { id: "t1", title: "Tune costmap parameters", done: false }
            ],
            dev_commands: { build: "colcon build", run: "ros2 run robotics-nav2 nav_node" }
        }
    ]

    Rectangle {
        anchors.fill: parent
        color: NexusTheme.background
    }

    // View: Dashboard
    ProjectDashboard {
        id: dashboardView
        anchors.fill: parent
        visible: hubRoot.activeView === "dashboard"
        projectsModel: hubRoot.projectsList
        bridge: hubRoot.bridge

        onOpenProjectRequested: function(proj) {
            hubRoot.activeProject = proj;
            hubRoot.activeView = "workspace";
        }
        onCreateNewRequested: {
            wizardModal.openWizard();
        }
    }

    // View: Workspace
    ProjectWorkspace {
        id: workspaceView
        anchors.fill: parent
        visible: hubRoot.activeView === "workspace"
        currentProject: hubRoot.activeProject
        bridge: hubRoot.bridge

        onBackToDashboardRequested: {
            hubRoot.activeView = "dashboard";
        }
    }

    // Project Creation Wizard Modal
    ProjectCreationWizard {
        id: wizardModal
        bridge: hubRoot.bridge
        onProjectCreatedSuccessfully: function(newProj) {
            var updated = [newProj].concat(hubRoot.projectsList);
            hubRoot.projectsList = updated;
            hubRoot.activeProject = newProj;
            hubRoot.activeView = "workspace";
        }
    }
}
