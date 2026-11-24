# NEXUS OS

> **The Developer-First, AI-Native Linux Operating System**  
> *Engineered for traditional programmers, AI-assisted developers, vibe coders, systems engineers, and robotics researchers.*

---

## 1. Executive Summary & Vision

**NEXUS OS** is a modern, developer-first, AI-native Linux operating system built on top of the rock-solid **Fedora Linux** ecosystem and the cutting-edge **KDE Plasma 6 (Wayland)** desktop platform.

Modern software engineering has transformed fundamentally. Developers no longer only edit local code files; they collaborate with autonomous coding agents, run local Large Language Models (LLMs), orchestrate containerized microservices, build for heterogeneous targets (Web, Embedded, Cloud, Robotics), and interact across disparate cloud model providers. Yet existing operating systems treat AI tools and modern developer workflows as disconnected third-party user-space add-ons.

**NEXUS OS bridges this divide.** It delivers an out-of-the-box, fully integrated development experience immediately after installation. It pairs a bespoke, minimal, rounded desktop environment with deep system-level developer tooling, a local-first Universal Spotlight engine, and a secure, hardware-aware AI subsystem.

---

## 2. Core Pillars

```
+-------------------------------------------------------------------------+
|                               NEXUS OS                                  |
+-------------------+---------------------------------+-------------------+
| 1. Complete Dev   | 2. AI-Native Development        | 3. Local AI       |
|    Ecosystem      |    Seamless Agent Integrations  |    Infrastructure |
+-------------------+---------------------------------+-------------------+
| 4. Universal      | 5. Project-Centric              | 6. Minimalist     |
|    Spotlight      |    Developer Hub                |    Modern Desktop |
+-------------------+---------------------------------+-------------------+
| 7. Security, Privacy, and User Sovereignty                              |
+-------------------------------------------------------------------------+
```

1. **Complete Development Ecosystem**: Ready on day one with modern toolchains, container engines (Podman/Docker), native runtimes, and developer utilities.
2. **AI-Native Environment**: First-class support for AI coding agents (Antigravity, Claude Code, Cursor, Windsurf, Aider, Codex, Gemini CLI) with shared context and zero configuration friction.
3. **Integrated Local AI Infrastructure**: Built-in orchestration for local models via Ollama and OmniRoute, featuring GPU/VRAM hardware awareness and a unified OpenAI-compatible routing proxy.
4. **Universal Spotlight (`Win + Space`)**: Sub-millisecond fuzzy search spanning apps, files, repositories, code definitions, settings, models, and system services.
5. **Project-Centric Workflow**: A dedicated Developer Hub that monitors, isolates, creates, and launches workspace environments with contextual AI grounding.
6. **Beautiful, Restrained Desktop**: Built on KDE Plasma 6 Wayland with strict design tokens—consistent corner radiuses, subtle elevation, restrained blur, and zero neon clutter.
7. **Security, Reliability, & User Sovereignty**: Principle of least privilege, hardware-isolated secrets via FreeDesktop Secret Service, SELinux enforcement, and zero silent telemetry.

---

## 3. High-Level Architecture

NEXUS OS is engineered in distinct, decoupled layers:

```
+--------------------------------------------------------------------------+
| USER APPLICATIONS & AGENTS                                               |
| Antigravity | Cursor | VS Code | Zed | Claude Code | Aider | Web Browsers|
+--------------------------------------------------------------------------+
| NEXUS USER-SPACE SUITE                                                   |
| - Nexus Spotlight (Layer-shell HUD, Tantivy/FTS5 search engine)          |
| - Nexus Developer Hub (Project orchestrator, dev environment manager)    |
| - Nexus AI Core (OmniRoute / Ollama orchestrator, unified /v1 proxy)     |
| - Nexus Settings (KCM integration & custom developer control panels)     |
+--------------------------------------------------------------------------+
| DESKTOP ENVIRONMENT                                                      |
| KDE Plasma 6 (Wayland) | KWin 6 (Rounded Corner Shaders) | Floating Dock |
| Nexus Aether Design Tokens (Qt 6 / Kirigami / SVG Assets)                |
+--------------------------------------------------------------------------+
| SYSTEM SERVICES & RUNTIMES                                               |
| systemd | D-Bus (Session/System) | PipeWire | WirePlumber | NetworkManager|
| Podman / Distrobox / Toolbx | mise-en-place | KSecretService             |
+--------------------------------------------------------------------------+
| BASE OPERATING SYSTEM & HARDWARE                                         |
| Fedora Linux (Kernel 6.12+, Mesa, Wayland, SELinux, rpm-ostree/bootc)   |
| Heterogeneous Accelerators (NVIDIA CUDA, AMD ROCm, Intel oneAPI, CPU)    |
+--------------------------------------------------------------------------+
```

---

## 4. Execution Model: Prototype vs. Production

To maintain rapid development velocity and ensure stability, NEXUS OS features a tiered deployment architecture:

| Component | Standard Linux (Prototype Phase) | Fedora Host Integration | Full OS Image (ISO / bootc) |
| :--- | :--- | :--- | :--- |
| **Nexus Spotlight** | Runs as Wayland layer-shell binary on any modern compositor | Native D-Bus service, desktop integration | Built-in default keybind (`Win+Space`) |
| **Nexus AI Core** | User-space daemon connecting to local Ollama / Cloud APIs | Systemd user unit, hardware device detection | Pre-pulled base coding models, auto-GPU provisioning |
| **Nexus Dev Hub** | Native Qt6/QML desktop application | Integrates with Fedora `podman`, `toolbox`, `mise` | Default workspace manager, pre-seeded templates |
| **Aether Design System**| Qt6 style plugin & QML theme pack | Full KDE Plasma 6 theme & KWin decoration | Custom desktop session, default Greetd/SDDM theme |
| **OS Distribution** | N/A (runs on host OS) | Layered packages on Fedora Kinoite / Workstation | Immutable bootc / rpm-ostree or Kickstart ISO |

---

## 5. Documentation Navigation

Detailed technical documentation is structured as follows:

- [ARCHITECTURE.md](file:///d:/My%20own%20os/ARCHITECTURE.md): Deep-dive systems engineering, IPC D-Bus specifications, service boundaries, and data flow.
- [TECH_STACK.md](file:///d:/My%20own%20os/TECH_STACK.md): Detailed component evaluation, language and framework choices, and trade-off analysis.
- [DESIGN_SYSTEM.md](file:///d:/My%20own%20os/DESIGN_SYSTEM.md): Complete specifications for UI geometry, radius system, color tokens, typography, and motion.
- [ROADMAP.md](file:///d:/My%20own%20os/ROADMAP.md): Five-stage engineering plan from standalone user-space binaries to bootable OS ISOs.
- [SECURITY.md](file:///d:/My%20own%20os/SECURITY.md): Threat modeling, local AI sandboxing, permission policies, and credential security.
- [AGENTS.md](file:///d:/My%20own%20os/AGENTS.md): Coding guidelines and system conventions for autonomous AI agents contributing to NEXUS OS.
- [CONTRIBUTING.md](file:///d:/My%20own%20os/CONTRIBUTING.md): Developer workflows, local build instructions, code standards, and PR processes.

---

## 6. Repository Layout

```
.
├── docs/                     # In-depth architectural & subsystem guides
├── src/
│   ├── aicore/               # Nexus AI Core service (Rust daemon, proxy, Ollama bridge)
│   ├── spotlight/            # Nexus Spotlight (Rust search indexer & Wayland UI)
│   ├── devhub/               # Nexus Developer Hub (Qt6 / QML workspace app)
│   ├── desktop/              # KDE Plasma 6 configs, KWin effects, themes, dock
│   └── settings/             # Nexus System & Developer Control Center
├── packaging/
│   ├── bootc/                # Containerfile for Fedora bootc immutable OS builds
│   ├── kickstart/            # Fedora Lorax/Kickstart specifications
│   ├── rpm/                  # RPM spec files for nexus core packages
│   └── flatpak/              # Flatpak manifests for isolated components
├── tools/                    # Developer setup, build scripts, verification harnesses
└── tests/                    # Integration and unit test suites
```

---

## 7. Licensing & Third-Party Software Distribution

NEXUS OS strictly respects open-source and proprietary software licensing:
- **Core Operating System & Nexus Subsystems**: Open-source under Apache-2.0 and GPL-3.0 licenses.
- **Redistribution Policy**: Only freely redistributable software is packaged into base OS media.
- **Proprietary IDEs & Tools** (e.g. Cursor, Windsurf, JetBrains, official VS Code binaries): Provided through a first-run declarative installer or Flathub integration that downloads packages directly from vendor distribution points upon user request.
