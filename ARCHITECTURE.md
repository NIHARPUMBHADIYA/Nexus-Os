# NEXUS OS Architecture Specification

> **Status:** Draft / Proposed  
> **Target Release:** NEXUS OS 1.0 (Based on Fedora 41+ / KDE Plasma 6)  
> **Author:** NEXUS OS Systems Engineering Team  

---

## 1. System Philosophy & Architectural Overview

NEXUS OS is designed to address a critical friction in modern computing: modern software development is fractured across decoupled tools, containerized services, terminal emulators, disparate model APIs, and uncoordinated local runtimes. 

NEXUS OS treats **AI execution**, **developer project context**, and **fast fuzzy discovery** as primary operating system primitives rather than external applications.

```
+=============================================================================+
|                          USER PRESENTATION LAYER                            |
|  +--------------------+  +----------------------+  +---------------------+  |
|  |  Nexus Spotlight   |  | Nexus Developer Hub  |  |  Nexus Control Hub  |  |
|  |  (Wayland Overlay) |  | (Project Manager UI) |  |   (System & AI)     |  |
|  +--------------------+  +----------------------+  +---------------------+  |
|  +-----------------------------------------------------------------------+  |
|  |             KDE Plasma 6 Desktop Shell (Wayland Native)               |  |
|  |   - Floating Dock  - KWin Rounded Corners  - Aether Design Tokens    |  |
|  +-----------------------------------------------------------------------+  |
+=============================================================================+
                                      │ IPC (D-Bus / Unix Sockets / HTTP /v1)
+=====================================▼=======================================+
|                         NEXUS CORE SYSTEM DAEMONS                           |
|  +------------------------------------+ +--------------------------------+  |
|  |           nexus-aid                | |         nexus-searchd          |  |
|  |  - Unified /v1 Proxy Multiplexer   | |  - Tantivy / SQLite FTS5 Core  |  |
|  |  - Ollama & OmniRoute Lifecycle   | |  - Inotify File/Project Indexer|  |
|  |  - GPU/VRAM Hardware Watchdog      | |  - Application & Symbol Index  |  |
|  |  - FreeDesktop Secret Service Mgr  | |  - D-Bus Search Provider API   |  |
|  +------------------------------------+ +--------------------------------+  |
|  +-----------------------------------------------------------------------+  |
|  |                          nexus-projectd                               |  |
|  |  - Git & Repo Scanner   - Devcontainer & Toolchain (mise) Orchestrator |  |
|  |  - Project AI Grounding Context Extractor                             |  |
|  +-----------------------------------------------------------------------+  |
+=============================================================================+
                                      │ System Interfaces
+=====================================▼=======================================+
|                      BASE OS & CONTAINER RUNTIMES                           |
|  - Systemd (User & System units)      - PipeWire / WirePlumber Audio        |
|  - Podman / Distrobox Rootless OCI    - NetworkManager / BlueZ              |
|  - Wayland Compositor (KWin 6)        - SELinux Security Policies           |
+=============================================================================+
                                      │ Kernel & Hardware
+=====================================▼=======================================+
|                   LINUX KERNEL 6.12+ (Fedora Base)                          |
|  - DRM / KMS Graphics Drivers         - cgroups v2 / systemd-oomd           |
|  - Hardware Accelerators: NVIDIA CUDA / AMD ROCm / Intel oneAPI / NPU       |
+=============================================================================+
```

---

## 2. Core Subsystems Specification

### 2.1. Nexus Spotlight (`nexus-spotlight` & `nexus-searchd`)

Nexus Spotlight is the universal command HUD of NEXUS OS, bound to `Meta+Space` (or `Win+Space`). It provides an instantaneous, sub-millisecond, keyboard-first modal overlay that unifies search across the entire workstation.

#### Architecture:
1. **Frontend (`nexus-spotlight`)**:
   - Built with **Rust + Slint** or **C++/Qt6 + QML** utilizing the `wlr-layer-shell` or `kde-layer-shell` Wayland protocol.
   - Operates in the overlay layer (`ZWLR_LAYER_SHELL_V1_LAYER_OVERLAY`) with exclusive keyboard focus grab on invocation.
   - Guaranteed launch latency under 16ms (60 FPS frame time).
2. **Backend Daemon (`nexus-searchd`)**:
   - Background user service (`nexus-searchd.service`).
   - Search Core: Embedded **Tantivy** search engine (or SQLite FTS5) with zero-cost memory mapping (`mmap`).
   - Plugin Architecture:
     - `app`: Scans `/usr/share/applications` and `~/.local/share/applications` (`.desktop` spec).
     - `project`: Discovers local Git repositories, package roots (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`).
     - `file`: Live inotify-driven fast path matching inside user home directory, respecting `.gitignore` and `.nexusignore`.
     - `cmd`: Safely executes shell commands with non-destructive parsing.
     - `model`: Queries local AI models currently loaded in memory via `nexus-aid`.
     - `system`: Directly toggles system settings, power profiles, Bluetooth devices, and systemd user services.

#### D-Bus Interface:
```xml
<interface name="org.nexus.Spotlight">
    <method name="Toggle"/>
    <method name="ShowWithQuery">
        <arg name="query" type="s" direction="in"/>
    </method>
    <method name="Hide"/>
    <signal name="VisibilityChanged">
        <arg name="visible" type="b"/>
    </signal>
</interface>

<interface name="org.nexus.Search">
    <method name="Query">
        <arg name="term" type="s" direction="in"/>
        <arg name="categories" type="as" direction="in"/>
        <arg name="limit" type="u" direction="in"/>
        <arg name="results" type="aa{sv}" direction="out"/>
    </method>
</interface>
```

---

### 2.2. Nexus AI Core (`nexus-aid`)

NEXUS OS features a native local AI subsystem engineered to remove the friction of running local models while managing system stability.

#### Key Functions:
1. **Unified AI Multiplexer (`localhost:11430/v1`)**:
   - An OpenAI-compatible HTTP reverse proxy and router.
   - Any tool (Cursor, VS Code, Claude Code, Aider, custom scripts) can simply point to `http://localhost:11430/v1` with an optional local token.
   - Routes requests based on model identifier:
     - Local models (`nexus:qwen2.5-coder:7b`, `llama3.2`, etc.) are transparently routed to local **Ollama** or **OmniRoute** backends.
     - Cloud models (`claude-3-5-sonnet`, `gemini-1.5-pro`, `gpt-4o`) are routed to cloud providers using credentials stored securely in the system keyring.
2. **Ollama & Local Backend Lifecycle Orchestration**:
   - Manages Ollama (`localhost:11434`) as an on-demand systemd user unit.
   - Prevents constant memory leaks: automatically transitions idle local models out of VRAM after a configurable inactivity timeout (default: 15 minutes).
3. **GPU / VRAM Watchdog & Hardware Awareness**:
   - Interfaces directly with `nvml` (NVIDIA), `rocm-smi` (AMD), or `/sys/class/drm` (Intel/standard DRM).
   - Monitors available VRAM and system memory before loading models.
   - If a requested model exceeds safe VRAM thresholds (which could freeze the Wayland desktop compositor), `nexus-aid` automatically prevents Out-Of-Memory (OOM) crashes by enforcing safe quantization or offloading CPU layers.
4. **Credential Security**:
   - Integrates with `org.freedesktop.secrets` (KDE KWallet / Secret Service).
   - Never writes plain-text API keys to disk files or shell history.

---

### 2.3. Nexus Developer Hub (`nexus-devhub` & `nexus-projectd`)

The Developer Hub is a project-centric dashboard that organizes workspaces, development tools, and context.

#### Subsystem Components:
1. **Project Scanner (`nexus-projectd`)**:
   - Traverses developer directories (`~/Projects`, `~/dev`, `~/src`, or custom paths).
   - Detects toolchains: Node.js/Bun/Deno, Rust, Go, Python, C/C++, Java, Flutter, Docker/Podman compose, ROS 2 (Robotics).
   - Reads project metadata (git branch, dirty state, last commit, open issues, ports).
2. **Environment & Toolchain Isolation**:
   - Direct integration with **mise-en-place** (`mise`) for declarative local language versions.
   - Direct integration with **Podman** and **Distrobox/Toolbx**: Allows developers to launch isolated development containers with a single click, keeping the host OS pristine.
3. **Project AI Grounding Context**:
   - Indexes local project structure, `README.md`, docstrings, and symbol tables into a local lightweight vector index.
   - Supplies this contextual metadata to local coding agents on demand via `nexus-aid`'s context endpoint.
4. **GUI Dashboard (`nexus-devhub`)**:
   - Built in **Qt6 / QML (Kirigami)** adhering strictly to the Aether Design System.
   - One-click launch into the user's preferred IDE (Antigravity, Cursor, VS Code, Zed, Neovim).
   - Integrated terminal drawer, live port inspector, and local container monitor.

---

### 2.4. Desktop Shell & Window Management (KDE Plasma 6 + KWin)

Rather than building a fragile desktop environment from scratch, NEXUS OS leverages the mature, robust, hardware-accelerated **KDE Plasma 6** Wayland stack, customized with bespoke Nexus components.

#### Desktop Enhancements:
1. **Floating Dock (`nexus-dock`)**:
   - A minimalist, Wayland layer-shell floating dock positioned at the bottom of the display.
   - Supports active running indicators, pinned developer applications, drag-and-drop, and project workspace quick-switching.
2. **Window Management & Rounded Corners**:
   - Customized **KWin 6** window decoration and shader effects.
   - Enforces uniform rounded corners across all client windows (Wayland SSD and CSD) with clean anti-aliasing and drop-shadows.
   - Restrained background blur: custom KWin dual-pass Gaussian blur filter with controlled saturation.
3. **Theme & Tokens ("Aether")**:
   - Global KDE Plasma 6 Look-and-Feel package (`nexus-aether-theme`).
   - SVG icons, unified Qt6/QML style plugin, custom SDDM login theme.
   - Dedicated dark mode ("Obsidian") and light mode ("Alabaster") with adaptive accent color switching.

---

## 3. Execution Environments Breakdown

To ensure transparency and rapid iterative progress, we clearly distinguish between runtime tiers:

### 3.1. What is Prototype Functionality (Stand-Alone Binaries)
These components are implemented and testable immediately as standalone user-space binaries on **any modern Linux distribution** (Fedora, Arch, Ubuntu, Debian):
- `nexus-searchd` and `nexus-spotlight` UI overlay.
- `nexus-aid` proxy multiplexer and Ollama integration daemon.
- `nexus-devhub` project scanner and GUI dashboard.
- Design token preview widgets and Qt6/QML style prototypes.
- Mock CLI test harnesses for VRAM monitoring and model routing.

### 3.2. What Can Run on Ordinary Linux
- The entire developer suite can run on an existing Linux desktop running Wayland:
  - Running `nexus-spotlight` via Wayland layer-shell.
  - Running `nexus-aid` as a user systemd service (`systemctl --user`).
  - Running `nexus-devhub` to manage local Git repositories and Podman containers.
  - Using local Ollama and cloud AI models through `http://localhost:11430/v1`.

### 3.3. What Requires Fedora Integration
These capabilities depend on the specific Fedora package ecosystem:
- Native packaging via RPM specs (`nexus-desktop.spec`, `nexus-core.spec`).
- Integration with Fedora's `dnf5` and `rpm-ostree` package managers.
- Fedora-specific hardware acceleration packages (Mesa, NVIDIA akmods, ROCm libraries).
- System-level SELinux policies (`nexus-aid.te`, `nexus-spotlight.te`) tailored for Fedora's targeted policy.
- Anaconda / Lorax / Kiwi kickstart files for building the bootable ISO.

### 3.4. What Requires Privileged Access
NEXUS OS enforces strict privilege separation. The vast majority of components run strictly as the unprivileged user. Only the following require elevated privileges:
- OS Installation and initial disk partitioning (`root` / Anaconda installer).
- Low-level system package updates via `dnf5` or `rpm-ostree` (handled through standard `polkit` authentication dialogs).
- System-wide hardware power profile configuration (`power-profiles-daemon` via D-Bus).
- Systemd system units (e.g. system-level container daemon or hardware drivers).

*Note: The AI daemon (`nexus-aid`), Spotlight (`nexus-spotlight`), and DevHub (`nexus-devhub`) NEVER run as root.*

### 3.5. What Must Be Implemented Later (Phase 4 & 5)
- Fully automated ISO image generation pipeline (Fedora bootc / Lorax CI image builder).
- Custom SDDM / Greetd login greeter with biometric authentication support.
- Kernel-level custom boot splashes (Plymouth theme).
- Advanced robotics/ROS 2 pre-seeded hardware bridge profiles.

---

## 4. Inter-Process Communication (IPC) Architecture

The NEXUS OS subsystems interact over clean, standardized protocols:

```
+-------------------------------------------------------------------------+
|                              SESSION BUS                                |
|                        (org.freedesktop.DBus)                           |
+-------------------------------------------------------------------------+
       ▲                               ▲                        ▲
       │ D-Bus                         │ D-Bus                  │ D-Bus
+──────▼───────────────+   +───────────▼────────────+   +───────▼─────────+
| nexus-spotlight      |   | nexus-devhub           |   | nexus-settings  |
+──────────────────────+   +────────────────────────+   +─────────────────+
       ▲                               ▲                        ▲
       │ Unix Domain Socket            │ HTTP /v1               │ D-Bus
+──────▼───────────────────────────────▼────────────────────────▼─────────+
| nexus-aid (AI Multiplexer & Core Daemon)                                |
|   - Local OpenAI Proxy: http://localhost:11430/v1                       |
|   - IPC Socket: /run/user/$UID/nexus/aid.sock                           |
+─────────────────────────────────────────────────────────────────────────+
       ▲                               ▲
       │ HTTP / API                    │ Native C/Driver APIs
+──────▼───────────────+   +───────────▼────────────+
| Ollama Daemon        |   | NVML / ROCm / Sysfs    |
| (localhost:11434)    |   | (Hardware Watchdog)    |
+──────────────────────+   +────────────────────────+
```

1. **D-Bus Session Bus**: Used for desktop-level IPC, notifications, global shortcut triggers, and settings synchronization.
2. **Unix Domain Sockets (`/run/user/$UID/nexus/`)**: Used for high-throughput, low-latency communication between daemons and GUI overlays.
3. **HTTP REST (`localhost:11430/v1`)**: Used for universal compatibility with any AI client library or coding agent expecting an OpenAI-compatible endpoint.

---

## 5. Security Architecture & Boundary Verification

NEXUS OS adheres to the following non-negotiable security principles:
1. **No Silent Command Execution**: When Spotlight offers command execution, destructive commands require explicit user acknowledgement.
2. **Zero Plaintext Secrets**: API keys for external AI providers (Anthropic, OpenAI, Gemini) are stored in the system keyring via `libsecret` / FreeDesktop Secret Service.
3. **Model Containment**: Local model downloads and weights are isolated in `~/.local/share/nexus/models` or standard Ollama paths. Model files are integrity-checked (SHA-256) before loading.
4. **SELinux Enforcing**: On the production Fedora base, all daemons run under tailored SELinux domains preventing unauthorized filesystem escalation.
