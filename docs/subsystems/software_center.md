# Subsystem: Developer Software Center (`nexus-software-center`)

## 1. Architectural Overview

The **NEXUS OS Developer Software Center** is the central graphical environment for discovering, installing, managing, updating, and removing developer tools, programming languages, runtimes, IDEs, and system utilities.

It features a **multi-backend installation engine** supporting native Fedora RPMs (DNF via Polkit/pkexec), user-space Flatpak packages from Flathub, Mise language toolchains, portable AppImages, and rootless OCI containers (Podman).

```
+=============================================================================+
|                 NEXUS DEVELOPER SOFTWARE CENTER UI                          |
|   +-----------------------+  +--------------------------------------------+ |
|   | 15 Category Sidebar   |  | Multi-Backend Software Grid & Detail Modal | |
|   | - AI Dev    - Cloud   |  | - Package Info    - Version Selector       | |
|   | - Editors   - Security|  | - Prereq Deps     - Live Progress Bar      | |
|   | - Languages - Robotics|  | - Fast Search     - Task Cancellation      | |
|   +-----------------------+  +--------------------------------------------+ |
+=============================================================================+
                                      │
                         (SoftwareCenterBridge)
                                      │
+=====================================▼=======================================+
|                   SOFTWARE CENTER CORE & CATALOG DB                         |
|   - 60+ Curated Developer Packages across 15 Categories                     |
|   - Real-time Binary & Package Presence Detection                           |
|   - User Favorites & Pinned Packages Persistence                            |
+=============================================================================+
                                      │
+=====================================▼=======================================+
|              MULTI-BACKEND INSTALLATION & SECURITY ENGINE                   |
|  +--------------------+  +--------------------+  +------------------------+ |
|  | DNF (Native RPM)   |  | Flatpak (Flathub)  |  | Mise Toolchains        | |
|  | - Polkit / pkexec  |  | - Rootless Sandbox |  | - User-Space Runtimes  | |
|  +--------------------+  +--------------------+  +------------------------+ |
|  +--------------------+  +--------------------+  +------------------------+ |
|  | AppImage Portable  |  | Podman Containers  |  | Vendor Packages        | |
|  | - ~/.local/bin     |  | - Rootless OCI     |  | - Verified Upstream    | |
|  +--------------------+  +--------------------+  +------------------------+ |
+=============================================================================+
```

---

## 2. The 15 Standard Categories

1. **AI Development**: Google Antigravity, Ollama, Cursor, Windsurf, Claude Code, OpenCode.
2. **IDEs and Editors**: Visual Studio Code, VSCodium, Zed Editor, Neovim, IntelliJ IDEA Community.
3. **Programming Languages**: Rust Toolchain (`rustup`), Python 3.13, Go, GCC & G++ (C/C++20), OpenJDK 21 LTS, Dart SDK.
4. **Web Development**: Node.js LTS, Bun Runtime & Bundler, TypeScript, React & Next.js tooling.
5. **Mobile Development**: Android Studio, Flutter SDK, Android SDK & ADB.
6. **AI and Machine Learning**: PyTorch, Hugging Face CLI, Nomic Embeddings, JupyterLab.
7. **Databases**: PostgreSQL Database Server, Redis In-Memory Store, SQLite, MariaDB.
8. **DevOps**: Podman Rootless Containers, Git & GitHub CLI, Docker-compatible tools, Ansible.
9. **Cloud**: Kubernetes CLI (`kubectl`), Terraform, AWS CLI, Google Cloud CLI.
10. **Cybersecurity**: Wireshark Network Analyzer, Nmap Network Scanner, Ghidra SRE, Burp Suite Community, OWASP ZAP.
11. **Robotics**: ROS 2 Jazzy Jalisco, Gazebo Physics Simulation, RViz 3D Visualizer.
12. **Embedded Systems**: Arduino IDE 2.x, PlatformIO Core (CLI), ESP-IDF.
13. **Game Development**: Godot Engine 4 (2D & 3D), Vulkan SDK.
14. **Design**: Blender 3D Suite, Inkscape Vector Graphics, GIMP, Figma Linux.
15. **Productivity**: DBeaver Community Database Manager, Obsidian Markdown Knowledge Base, Postman.

---

## 3. Multi-Backend Installation Architecture

NEXUS OS rejects the fragile pattern of executing random unverified curl-to-bash scripts. Instead, the installation engine orchestrates vetted backends:

| Backend | Scope | Privilege Level | Sandboxing | Typical Targets |
| :--- | :--- | :--- | :--- | :--- |
| **Native RPM (DNF)** | System-wide | Privileged via Polkit / `pkexec` | Base OS Level | Compilers, Kernel drivers, Wireshark, PostgreSQL |
| **Flatpak (Flathub)** | User-space | Unprivileged (Standard User) | Bubblewrap Sandbox | Godot, Blender, DBeaver, Zed, Arduino IDE |
| **Mise Toolchain** | User-space | Unprivileged | Isolated Per-User | Node.js, Python versions, Rust, Go, Dart |
| **AppImage** | User-space | Unprivileged | Portable Executable | Cursor, Windsurf, portable developer tools |
| **OCI Container (Podman)**| Containerized | Rootless User Namespaces | OCI Container Isolation | ROS 2 Jazzy Desktop, isolated microservice stacks |
| **Vendor Package** | Local/System | Documented / Verified | Vetted Source | Ollama, Bun |

---

## 4. Security & Authorization Architecture

1. **Privilege Separation**:
   - The GUI desktop shell and Software Center run strictly as standard unprivileged user processes.
   - Any operation modifying `/usr` or requiring system package manager modifications calls `pkexec dnf` or the system PackageKit D-Bus daemon, triggering the OS Polkit authentication dialog.
2. **Zero Shell Interpolation**:
   - Commands are dispatched as sanitized argument lists (`[binary, *args]`) without `sh -c` string concatenation, preventing command injection attacks.
3. **Verification Before Marking Installed**:
   - The engine never fakes success. A package is only marked as installed when its target binary is verified on `PATH` or its package reference is confirmed in the backend database.

---

## 5. Asynchronous Task Lifecycle

Installation and removal operations run in worker threads with real-time status reporting:
- `queued`: Task added to scheduling queue.
- `downloading`: Package payloads and dependencies being retrieved.
- `verifying`: Cryptographic checksums and GPG signatures checked.
- `installing`: Files unpacked and system hooks executed.
- `completed`: Verified binary detected on system PATH.
- `failed`: Non-zero exit code or missing post-install binary with captured error log.
- `cancelled`: User initiated task cancellation.

---

## 6. Verification and Testing

The subsystem is thoroughly tested in **`tests/test_software_center.py`**:
- 15/15 categories verified with complete package coverage.
- Multi-criteria search and fuzzy matching.
- Favorites persistence across restarts (`favorites.json`).
- Asynchronous installation task execution with progress tracking.
- Uninstallation state verification.
- Task cancellation mechanics.
- QML view compilation and reactive property binding.
