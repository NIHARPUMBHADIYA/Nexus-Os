# NEXUS OS — Release Notes: Version 2026.1 (Aether Edition)

> **Release Date**: November 23, 2026  
> **Codename**: Aether Workstation  
> **Target Base**: Fedora Linux 41 x86_64 (Linux 6.12+, Wayland, systemd, PipeWire)  
> **ISO Checksum**: `SHA256: c3e5cb3d8ae8afc1cf80724214e26c0db14bf97a0757ff7126fe573cb15f5273`  

---

## 1. Executive Summary

**NEXUS OS 2026.1** is the inaugural production release of the developer-first, AI-native operating system. Engineered on a solid Fedora Linux foundation with a polished, rounded KDE Frameworks 6 Wayland desktop, NEXUS OS bridges traditional systems programming, modern full-stack web engineering, and agentic AI-assisted development.

---

## 2. Key Subsystems & Feature Highlights

### 2.1. Aether Design System & Desktop Shell
- **Unified Rounded Aesthetics**: Consistent corner radii (`radiusSmall` 10px, `radiusMedium` 14px, `radiusLarge` 20px, `radiusPill` 9999px) applied across all windows, docks, panels, and dialogs.
- **10 Accessible Color Themes**: Midnight (Default), Nord, Dracula, Catppuccin, Tokyo Night, Terminal Green, Paper Light, AMOLED Black, Deep Space, and Custom Theme Editor — all verified against WCAG 2.1 AA contrast standards (>= 4.5:1).
- **Floating Aether Dock**: Auto-dodge window collision avoidance, running indicators, and context menus.
- **Top System Panel**: Real-time hardware telemetry, PipeWire audio, NetworkManager, Bluetooth, and Quick Settings.

### 2.2. Universal Spotlight Launcher (`Win + Space`)
- **SQLite FTS5 Indexed Search**: High-speed prefix and fuzzy search across 16 categories including Applications, Projects, Code Symbols, Packages, Services, and System Actions.
- **Actions Drawer & Safety Guards**: Destructive terminal actions (e.g. system reboots, service stops) require explicit secondary confirmation.

### 2.3. NEXUS AI Core (`nexus-aid`)
- **Loopback Proxy (`127.0.0.1:11430`)**: OpenAI-compatible API endpoint with anti-CSRF token verification and origin header validation.
- **OmniRoute & Ollama Integration**: Multi-model fallback routing and local GGUF model execution.
- **Compositor VRAM Safety Governor**: Enforces a dedicated 2048 MB VRAM headroom to prevent Wayland desktop UI freezing when large models are loaded.
- **Hardware-Backed AES-256-GCM Vault**: Encrypted credential storage at `~/.config/nexus/vault.enc`.

### 2.4. Developer Hub & Software Center
- **18 Polyglot Project Templates**: Python, C/C++, Rust, Go, React, Next.js, FastAPI, ROS 2, Flutter, Android, and AI/ML.
- **60+ Developer Software Packages**: Multi-backend installations across DNF, Flatpak, mise, and OCI containers.

### 2.5. 15 Curated Developer Packs
- One-click comprehensive environment installations: Full-Stack, AI/ML, Vibe Coder, Software Engineer, Python, C/C++, Android, Game Dev, Robotics, Embedded, Cybersecurity, DevOps, Cloud, Student, and Complete Developer.
- **Deduplicated Dependency Resolver**: Eliminates duplicate tool downloads across multiple selected packs.
- **Automated Rollback**: Restores previous state if an installation step fails.

### 2.6. Linux System Integration Abstraction Layer
- 20 native Linux subsystem providers covering kernel info, XDG desktop entries, safe argument execution, PipeWire audio, BlueZ Bluetooth, Podman containers, and process management.
- Environment compatibility detector identifying Fedora native, generic Linux, virtual machines, and development hosts with graceful degradation.

---

## 3. Known Issues & Workarounds

1. **NVIDIA Proprietary Driver Post-Installation**:
   - *Issue*: Some older NVIDIA legacy cards (Pascal or earlier) require `akmod-nvidia` compilation on first boot.
   - *Workaround*: In the bootloader menu, select **Troubleshooting - Basic Graphics** to boot with standard open-source Nouveau / simplefb, then install `akmod-nvidia` via Software Center.
2. **First-Boot Large AI Models**:
   - *Notice*: To prevent excessive bandwidth usage during ISO installation, AI models are not bundled into the ISO image. Users can pull models (e.g. `qwen2.5-coder:7b`, `llama3.2:3b`) via Settings > Models or `ollama run` after installation.
3. **Dual-Boot Windows BitLocker**:
   - *Notice*: When installing alongside Windows 11 with BitLocker enabled, ensure you have your BitLocker recovery key before modifying disk partition boundaries.

---

## 4. Verification & Testing Matrix

NEXUS OS 2026.1 has undergone rigorous verification across 13 dedicated test suites:

| Test Suite | Components Tested | Result |
|---|---|---|
| `test_iso_distribution.py` | ISO binary, El Torito BIOS/UEFI catalog, Kickstart, VM boot harness (13 stages) | **PASSED (100%)** |
| `test_system_integration.py` | 20 Linux subsystem providers, environment detector, hardware tiering | **PASSED (100%)** |
| `test_devpacks.py` | 15 Developer Packs, deduplicated resolver, live logs, rollback | **PASSED (100%)** |
| `test_settings_app.py` | 21 Settings categories, shortcut editor, storage analysis, zero telemetry | **PASSED (100%)** |
| `test_personalization.py` | 10 themes, WCAG 2.1 AA contrast, custom editor, token persistence | **PASSED (100%)** |
| `test_software_center.py` | 60+ packages, DNF/Flatpak/mise/container multi-backends | **PASSED (100%)** |
| `test_tool_integrations.py` | 15 AI tools, config adapters, backup engine, desktop shortcuts | **PASSED (100%)** |
| `test_aicore.py` | `nexus-aid` proxy, loopback isolation, VRAM governor, AES-256 vault | **PASSED (100%)** |
| `test_devhub.py` | 18 project templates, `.nexus/project.json`, modular panels | **PASSED (100%)** |
| `test_spotlight.py` | SQLite FTS5 search engine, 16 categories, actions drawer | **PASSED (100%)** |
| `test_desktop_shell.py` | Aether window manager, dock, panel, launcher, context menu | **PASSED (100%)** |
| `test_design_system.py` | 17 reusable QML components, token bindings, layout responsiveness | **PASSED (100%)** |
| `test_subsystems.py` | Architectural directory structure, Cargo workspace, documentation | **PASSED (100%)** |
