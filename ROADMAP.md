# NEXUS OS Development Roadmap

> **Engineering Horizon:** 2026 – 2027  
> **Methodology:** Modular Subsystems, Test-Driven Verification, Continuous Executability  

---

## 1. Phasing Strategy

Building an operating system is an iterative engineering process. Attempting to build an entire OS as a monolithic image from day one leads to unmaintainable bugs and unverified components.

NEXUS OS follows an **inside-out architectural progression**:
1. Build and verify the core daemons and graphical components as **standalone user-space binaries** on standard Linux.
2. Integrate them seamlessly into the **KDE Plasma 6 Wayland desktop**.
3. Package the complete environment into **Fedora-native RPMs and OCI bootc container images**.
4. Generate the final bootable **NEXUS OS live ISO**.

---

## 2. Milestone Breakdown

```
+-------------------------------------------------------------------------+
| MILESTONE 0: Architecture & Foundation (Current Phase)                  |
| - Architectural blueprint & IPC interface definition                    |
| - Design system token definitions & asset specifications                |
| - Initial directory layout, tooling, and verification harness           |
+-------------------------------------------------------------------------+
                                    │
+-----------------------------------▼-------------------------------------+
| MILESTONE 1: User-Space Core Subsystems (Standalone Linux)              |
| - nexus-searchd & nexus-spotlight: Fast Tantivy indexer & Layer-shell UI|
| - nexus-aid: Unified /v1 HTTP proxy, Ollama lifecycle, VRAM monitor     |
| - nexus-devhub: Project scanner, language detector, Qt6 prototype UI    |
| - Verification: Can be launched and tested on any existing Linux distro |
+-------------------------------------------------------------------------+
                                    │
+-----------------------------------▼-------------------------------------+
| MILESTONE 2: Desktop Shell & KDE Plasma 6 Customization                 |
| - nexus-aether-theme: Plasma 6 Look-and-Feel package & SVG icons        |
| - KWin 6 rounded corner shaders & dual-pass blur effects                |
| - nexus-dock: Floating Wayland layer-shell dock with auto-dodge         |
| - Global shortcut daemon: Win+Space binding via xdg-desktop-portal      |
+-------------------------------------------------------------------------+
                                    │
+-----------------------------------▼-------------------------------------+
| MILESTONE 3: Developer Ecosystem & Toolchain Isolation                  |
| - mise-en-place & Podman deep integration into DevHub                   |
| - Project creation wizards (Rust, Go, Python, Node, Flutter, ROS 2)     |
| - First-Run Setup Engine for proprietary IDEs (Cursor, VS Code, etc.)   |
| - Project-specific AI context grounding & embedding generator           |
+-------------------------------------------------------------------------+
                                    │
+-----------------------------------▼-------------------------------------+
| MILESTONE 4: OS Image Pipeline & Fedora Base Packaging                  |
| - RPM spec files for nexus-core, nexus-desktop, nexus-aid               |
| - Fedora bootc / rpm-ostree container-first immutable OS definition    |
| - Anaconda Kickstart file & Lorax live ISO build script                 |
| - SELinux targeted security policy modules                              |
+-------------------------------------------------------------------------+
                                    │
+-----------------------------------▼-------------------------------------+
| MILESTONE 5: Polishing, Hardware Hardening, & Public Release            |
| - NVIDIA CUDA / AMD ROCm auto-detection and driver installer            |
| - Power & thermal profile optimization for developer laptops            |
| - Full automated end-to-end integration test suite                      |
| - Public Alpha release & Community Documentation                        |
+-------------------------------------------------------------------------+
```

---

## 3. Milestone Details & Verification Gates

### Milestone 0: Architecture & Foundation (CURRENT)
- [x] Analyze vision and define core pillars.
- [x] Define layered system architecture and IPC boundaries (`ARCHITECTURE.md`).
- [x] Author technical stack selection and trade-off analysis (`TECH_STACK.md`).
- [x] Specify design tokens, typography, and geometry (`DESIGN_SYSTEM.md`).
- [x] Establish security, secret management, and threat model (`SECURITY.md`).
- [x] Define AI agent collaboration rules (`AGENTS.md`) and contribution guide (`CONTRIBUTING.md`).
- [x] Initialize project directory structure and verification tooling.
- **Verification Gate**: Architecture review and approval; all specification documents in place.

---

### Milestone 1: User-Space Core Subsystems (Target: Q1)
- [ ] **Nexus Search Engine & Spotlight HUD**:
  - Implement `nexus-searchd` in Rust using `tantivy` and `zbus`.
  - Build application (`.desktop`), file, and project indexing plugins.
  - Implement `nexus-spotlight` overlay using Wayland layer-shell.
- [ ] **Nexus AI Core Daemon (`nexus-aid`)**:
  - Implement OpenAI-compatible `/v1` reverse proxy server in Rust (`axum`).
  - Implement local Ollama process lifecycle manager and inactivity unloader.
  - Implement GPU/VRAM hardware monitor (NVML / ROCm / Sysfs).
  - Implement FreeDesktop Secret Service client for provider API keys.
- [ ] **Nexus Developer Hub (`nexus-devhub`)**:
  - Build project directory crawler with polyglot project type detection.
  - Implement Qt6/QML desktop GUI adhering to Aether design tokens.
- **Verification Gate**: Subsystems compile and run on standard Fedora/Ubuntu/Arch desktop without root privileges.

---

### Milestone 2: Desktop Shell & KDE Plasma 6 Customization (Target: Q2)
- [ ] Implement Aether Plasma 6 desktop theme, widget styles, and color schemes.
- [ ] Configure and test KWin 6 rounded corner shaders and window decorations.
- [ ] Implement `nexus-dock`: Wayland floating dock with active running indicators and smart dodge.
- [ ] Unify global shortcuts: `Win + Space` for Spotlight, `Win + D` for DevHub, `Win + T` for Terminal.
- [ ] Implement Nexus Control Center module (KCM) for AI model and developer settings.
- **Verification Gate**: A standard KDE Plasma 6 session can load the Nexus Aether theme and display uniform rounded corners with the floating dock.

---

### Milestone 3: Developer Toolchains & Environment Virtualization (Target: Q3)
- [ ] Integrate `mise` into DevHub for one-click runtime switching (Node, Rust, Go, Python).
- [ ] Integrate rootless `podman` and `distrobox` for sandbox container creation.
- [ ] Implement Project Creation Wizard with curated templates for modern stacks.
- [ ] Build the First-Run Setup Wizard: Declarative installer for third-party proprietary tools (Cursor, Windsurf, VS Code, Slack) respecting upstream licensing.
- [ ] Implement local project vector context generator (`nexus-contextd`).
- **Verification Gate**: A developer can create a new project, launch it in an isolated container, and prompt an AI coding agent via the local proxy.

---

### Milestone 4: OS Image Pipeline & Packaging (Target: Q4)
- [ ] Author RPM spec files for all Nexus components.
- [ ] Build Fedora `bootc` Containerfile for transactional, immutable operating system deployment.
- [ ] Create Kickstart configuration for traditional bootable live ISO (`livemedia-creator`).
- [ ] Author SELinux policy files for `nexus-aid` and `nexus-searchd`.
- [ ] Customize Calamares / Anaconda installer with Nexus branding and OEM setup.
- **Verification Gate**: Successful bootable ISO generated via CI that installs onto bare metal / QEMU-KVM.

---

### Milestone 5: Hardware Hardening & Public Alpha (Target: Q1 Next Cycle)
- [ ] Auto-detection and seamless driver configuration for NVIDIA (proprietary) and AMD/Intel (open-source) GPUs.
- [ ] Laptop battery optimization and thermal throttling integration via `power-profiles-daemon`.
- [ ] Security audit and penetration testing of local proxy and D-Bus interfaces.
- [ ] Public developer release (ISO downloads, documentation portal, community forum).
- **Verification Gate**: Full battery life benchmark, zero crash reports on standard test hardware, successful public installation test.
