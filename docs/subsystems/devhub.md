# Subsystem: Nexus Developer Hub (`nexus-devhub`)

## 1. Architectural Overview

The **Nexus Developer Hub** (`nexus-devhub`) is the central control plane and unified workspace for software developers on NEXUS OS. It bridges system-level polyglot toolchains, containerized environments, local AI coding agents, and external IDEs into an intuitive, keyboard-friendly graphical interface adhering strictly to the **Aether Design System**.

Unlike web-based electronic dashboards, Developer Hub is built natively using **C++/Qt6 / QML** and **PyQt6**, delivering sub-millisecond response times, low memory overhead, and deep desktop shell integration.

```
+-----------------------------------------------------------------------------------+
|                            NEXUS DEVELOPER HUB UI                                  |
|   +-------------------+  +-------------------------+  +------------------------+  |
|   | Project Dashboard |  | Project Creation Wizard |  | Unified Workspace HUD  |  |
|   +-------------------+  +-------------------------+  +------------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                (PyQt6 Bridge)
                                         v
+-----------------------------------------------------------------------------------+
|                        DEVELOPER HUB CORE (hub_core.py)                           |
|  - Project Registry & Indexer       - 18 Polyglot Template Scaffolders            |
|  - .nexus/project.json Context      - .nexus/session.json State Restoration       |
|  - External IDE Process Launcher    - Spotlight Project Provider Adapter          |
+-----------------------------------------------------------------------------------+
       |                        |                           |
       v                        v                           v
+--------------+       +-------------------+       +-------------------------------+
| System Tools |       | External IDEs     |       | Nexus AI Core (`nexus-aid`)   |
| (git, mise)  |       | (Cursor, VS Code) |       | (Context, Prompt Injection)   |
+--------------+       +-------------------+       +-------------------------------+
```

---

## 2. Core Subsystem Features

### 2.1 Project Dashboard
- **Recent & Favorite Projects**: Quick access to active projects with last opened timestamps, language badges, and pinned favorites.
- **Real-Time Project Search**: Fast fuzzy filtering across project names, descriptions, and technology tags.
- **Status & Metrics**: Live visibility into Git branches, dirty working trees, pending tasks, and background service statuses.
- **One-Click Workspace Opening**: Smooth transition from dashboard view directly into the active multi-panel project workspace.

### 2.2 Project Creation Wizard (18 Polyglot Templates)
Developer Hub provides an interactive scaffolding wizard supporting 18 standardized project templates across modern stacks:

| ID | Template Name | Default Framework | Key Files Generated |
| :--- | :--- | :--- | :--- |
| `python` | Modern Python CLI | Standard Library / Pytest | `src/main.py`, `pyproject.toml`, `tests/` |
| `c_cpp` | Modern C++20 | CMake / GoogleTest | `src/main.cpp`, `CMakeLists.txt` |
| `react` | React SPA | Vite / TypeScript | `src/App.tsx`, `package.json`, `vite.config.ts` |
| `nextjs` | Next.js App Router | React 19 / Tailwind CSS | `app/page.tsx`, `app/layout.tsx`, `package.json` |
| `node_api` | Node.js Backend API | Express / REST | `src/server.js`, `package.json` |
| `typescript` | TypeScript Library | ES Modules / Vitest | `src/index.ts`, `tsconfig.json` |
| `flask` | Flask Web Service | Flask / Jinja2 | `app.py`, `requirements.txt` |
| `fastapi` | High-Perf FastAPI | FastAPI / Pydantic | `main.py`, `requirements.txt` |
| `django` | Full-Stack Django | Django 5.x / SQLite | `manage.py`, `requirements.txt` |
| `java` | Java Microservice | Gradle / JUnit 5 | `src/main/java/Main.java`, `build.gradle` |
| `rust` | Rust Systems App | Cargo / Tokio | `src/main.rs`, `Cargo.toml` |
| `go` | Go Cloud Service | Go Modules / Chi | `main.go`, `go.mod` |
| `flutter` | Flutter Multiplatform | Flutter SDK | `lib/main.dart`, `pubspec.yaml` |
| `android` | Android Native | Kotlin / Jetpack Compose | `app/src/main/kotlin/MainActivity.kt` |
| `arduino` | Embedded Microcontroller | Arduino C++ / PlatformIO | `src/main.cpp`, `platformio.ini` |
| `ros2` | ROS 2 Robotics Node | rclpy / ROS 2 Jazzy | `robot_node/node.py`, `setup.py` |
| `ai_ml` | AI/ML Pipeline | PyTorch / Transformers | `train.py`, `model.py`, `requirements.txt` |
| `empty` | Blank Project | Universal | `.nexus/project.json`, `README.md` |

### 2.3 Modular Project Workspace
The project workspace provides a unified, customizable environment containing modular panels:
1. **File Explorer**: Tree and flat list navigation of source files and subdirectories.
2. **Code Editor / Preview**: Embedded syntax-highlighted code editor with line numbers and save shortcuts.
3. **Embedded Terminal**: Interactive terminal shell emulator executing within the project's root directory.
4. **AI Assistant HUD**: Direct contextual conversational interface connected to `nexus-aid` (Ollama/OmniRoute) with automated project context injection.
5. **Browser / Web Preview**: Embedded lightweight webview for inspecting local dev servers (`http://localhost:3000`, `http://localhost:8000`).
6. **Git Inspector**: Live branch indicator, commit logs, changed file diff summary, and staged status.
7. **Build & Test Runner**: Quick action buttons for running project build scripts, test suites (`pytest`, `cargo test`, `npm test`), and dev servers.
8. **Live Logs**: Streaming stdout/stderr output from running background services and build processes.
9. **Database Inspector**: Table schema and SQL query scratchpad for local project databases (SQLite, PostgreSQL, Redis).
10. **Project Documentation**: In-line Markdown renderer for `README.md`, `ARCHITECTURE.md`, and project guides.

Each panel can be toggled, resized, or rearranged according to developer workflow preference.

---

## 3. Project Metadata & Session Architecture

### 3.1 Project Context Metadata (`.nexus/project.json`)
Every project managed by Developer Hub contains a `.nexus/` directory storing machine-readable and AI-indexable metadata:

```json
{
  "name": "nexus-web-service",
  "description": "High-throughput API gateway for Nexus OS services",
  "template": "fastapi",
  "language": "python",
  "framework": "fastapi",
  "created_at": 1740306000.0,
  "last_opened": 1740306120.0,
  "favorite": true,
  "git_repo": "git@github.com:nexus-os/nexus-web-service.git",
  "git_branch": "main",
  "dev_commands": {
    "run": "uvicorn main:app --reload --port 8000",
    "test": "pytest tests/ -v",
    "build": "docker build -t nexus-web-service ."
  },
  "tasks": [
    { "id": "task-1", "title": "Implement JWT auth middleware", "status": "pending" },
    { "id": "task-2", "title": "Add rate limiting headers", "status": "done" }
  ],
  "ai_context": {
    "system_prompt": "You are assisting on a high-concurrency FastAPI microservice. Favor async/await and Pydantic v2 schemas.",
    "model_override": "qwen2.5-coder:7b"
  }
}
```

### 3.2 Session Preservation & Restoration (`.nexus/session.json`)
When closing Developer Hub or switching between projects, the complete workspace state is serialized so developers can resume uninterrupted:

```json
{
  "opened_files": [
    "src/server.py",
    "src/config.py"
  ],
  "active_file": "src/server.py",
  "active_panel": "editor",
  "terminal_tabs": [
    { "id": "term-1", "title": "Dev Server", "last_command": "npm run dev" },
    { "id": "term-2", "title": "Git", "last_command": "git status" }
  ],
  "layout_state": {
    "sidebar_width": 240,
    "bottom_panel_height": 180,
    "active_bottom_tab": "terminal"
  },
  "running_services": [
    { "name": "Vite Dev Server", "pid": 4821, "port": 5173 }
  ],
  "saved_at": 1740306150.0
}
```

---

## 4. External IDE Process Integration

In alignment with NEXUS OS Operating Principles, Developer Hub does **not** simulate or mock external proprietary IDEs inside fake web frames. Instead, it provides robust, secure system process execution to launch real external editors and IDEs installed on the system:

- **Supported IDEs**: Cursor (`cursor`), VS Code (`code`), Zed (`zed`), Neovim (`nvim` via terminal emulator), PyCharm (`pycharm`), RustRover (`rustrover`), Antigravity IDE (`antigravity`).
- **Execution Safety**: Commands are executed via sanitized argument lists (`[binary_path, project_path]`) rather than raw shell string concatenation (`sh -c ...`).
- **Container / Distrobox Support**: External IDEs can be launched with containerized environment wrappers when specified in project settings.

---

## 5. Subsystem Integrations

### 5.1 Desktop Shell Integration
- Embedded inside the Desktop Window Manager as `DevHubApp.qml` (`src/desktop/shell/apps/DevHubApp.qml`).
- Accessible via the Desktop Floating Dock (dedicated Developer Hub icon with running indicator).
- Pinned to Desktop Application Launcher under the **Development** category.

### 5.2 Universal Spotlight Integration
- The `ProjectProvider` in `src/spotlight/search_engine.py` directly indexes projects registered in Developer Hub.
- Typing project names or tags in `Win+Space` immediately displays projects with direct actions:
  - *Open in Developer Hub*
  - *Open in VS Code / Cursor*
  - *Open Terminal Here*
  - *Reveal in File Manager*

---

## 6. Verification and Test Suite

The Developer Hub subsystem is thoroughly tested with automated unit and integration tests:
- **`tests/test_devhub.py`**:
  - `test_project_registry_and_persistence`: Verifies project registration, indexing, search, and JSON serialization.
  - `test_project_creation_wizard`: Tests scaffolding of all 18 project templates with directory structures and config files.
  - `test_session_restoration`: Tests saving and restoring active files, layout state, and workspace panels.
  - `test_external_ide_launch`: Validates safe parameter passing for IDE execution.
  - `test_qml_component_compilation`: Validates QML compilation and property bindings across all DevHub QML views.
