# NEXUS OS Technology Stack Specification

> **Document Version:** 1.0.0  
> **Target Platform:** x86_64 / AArch64  
> **Base Ecosystem:** Fedora Linux (Version 41+)  
> **Compositor / Display Server:** Wayland native (KWin 6)  

---

## 1. Architectural Stack Overview

NEXUS OS selects technologies based on four strict criteria:
1. **Performance & Low Latency**: Daemons and launchers must activate instantaneously with near-zero memory footprint.
2. **Reliability & Memory Safety**: Core background services must not suffer from memory leaks, buffer overflows, or unexpected crashes.
3. **Ecosystem Synergy**: Deep integration with modern Linux desktop standards (Wayland protocols, D-Bus, FreeDesktop specifications, systemd).
4. **Developer Familiarity**: Using modern, well-maintained languages and frameworks with vibrant open-source ecosystems.

---

## 2. Component Evaluation & Selection Matrix

| Subsystem | Primary Technology | Considered Alternatives | Justification & Decision Analysis |
| :--- | :--- | :--- | :--- |
| **Base Distribution** | **Fedora Linux (41+)** | Arch Linux, Debian, Ubuntu | **Selected: Fedora**. Provides cutting-edge kernel (6.12+), first-class Wayland support, SELinux security, modern package management (`dnf5`), and industry-standard container tooling (`bootc`, `podman`, `rpm-ostree`). |
| **Desktop Shell** | **KDE Plasma 6 (Wayland)** | GNOME 47, Hyprland, Cosmic Desktop | **Selected: KDE Plasma 6**. Mature Wayland compositor (KWin), high graphical performance, native Qt6 foundation, deeply modular, superior multi-monitor fractional scaling, and rich theming extensibility. |
| **Core Daemons (`nexus-aid`, `nexus-searchd`)** | **Rust** | Go, C++, Python | **Selected: Rust**. Uncompromising memory safety, zero-cost abstractions, single-binary distribution, sub-millisecond cold starts, and best-in-class async runtime (`tokio`). |
| **Universal Spotlight UI** | **Rust + Slint / Qt6 QML** | Electron, Tauri, GTK4 | **Selected: Qt6/QML (or Rust+Slint)**. Direct support for `wlr-layer-shell-unstable-v1` and `kde-layer-shell`, GPU-accelerated rendering, instant popup display (<16ms), and minimal RAM consumption (under 40MB vs 300MB+ for Electron). |
| **Developer Hub (`nexus-devhub`)** | **C++ / Qt 6 (QML + Kirigami)** | Electron, Flutter, Webview | **Selected: Qt 6 / Kirigami**. Seamless visual harmony with KDE Plasma 6, direct access to system D-Bus and C++ Linux APIs, native styling, responsive UI, and lightweight resource usage. |
| **Search Engine Core** | **Tantivy (Rust)** | SQLite FTS5, Bleve, Baloo | **Selected: Tantivy**. High-performance Lucene-like search engine in Rust with memory-mapped indices (`mmap`), instantaneous fuzzy matching, BM25 ranking, and zero GC pauses. |
| **Local AI Inference Engine** | **Ollama & OmniRoute / llama.cpp** | LocalAI, vLLM, text-generation-webui | **Selected: Ollama + OmniRoute**. Proven zero-setup local LLM runner, optimized GGUF quantization, dynamic GPU layer offloading (CUDA, ROCm, Vulkan, Metal), and lightweight background daemon footprint. |
| **AI Multiplexer / Proxy** | **Rust (`axum` + `reqwest`)** | Python FastAPI, Node.js Express | **Selected: Rust (Axum)**. High-concurrency async HTTP multiplexer, sub-millisecond request routing, rock-solid token streaming, and minimal memory usage (<15MB RAM). |
| **Toolchain Virtualization** | **mise-en-place (`mise`) & Podman** | asdf, Docker, Nix, Homebrew | **Selected: mise + Podman**. `mise` provides blazingly fast polyglot runtime management (Node, Rust, Python, Go, etc.) in Rust; `podman` provides rootless, daemonless OCI containers with full systemd integration. |
| **Secrets & Credential Store**| **FreeDesktop Secret Service (`org.freedesktop.secrets`)** | Plaintext config files, custom encryption | **Selected: FreeDesktop Secret Service via KWallet / Secret Service API**. Hardware-backed or master-password encrypted credential storage preventing plain-text credential leaks. |

---

## 3. Deep-Dive Stack Breakdown

### 3.1. Base Operating System Tier

- **Kernel**: Linux Kernel 6.12+ (standard Fedora kernel with zRAM enabled by default).
- **Init System**: `systemd` (leveraging systemd-homed, user units `systemctl --user`, and `systemd-oomd` out-of-memory prevention).
- **Audio & Media**: `PipeWire` + `WirePlumber` (low-latency audio routing, Wayland screen capture via `xdg-desktop-portal`).
- **Networking**: `NetworkManager` + `iwd` / `wpa_supplicant`.
- **Security Subsystem**: `SELinux` (Targeted policy, enforcing by default).

### 3.2. Desktop & Window Management Tier

- **Display Server Protocol**: Pure **Wayland** (Xwayland available for legacy compatibility).
- **Compositor**: **KWin 6** (KDE 6 Wayland Compositor).
- **Custom Shaders & Effects**:
  - `kwin-effect-rounded-corners`: Custom GLSL/Vulkan shader applying anti-aliased border radius to client buffers.
  - `kwin-effect-blur`: Dual-pass Gaussian blur with custom saturation boost for glassmorphism surfaces.
- **Dock & Panels**: Wayland layer-shell protocol integration via `gtk4-layer-shell` or native `QtWaylandClient`.

### 3.3. Development & Build Tools

- **Rust Subsystem**:
  - Compiler: `rustc` / `cargo` (Edition 2021/2024).
  - Crates:
    - Async Runtime: `tokio`
    - Web Framework / Proxy: `axum`, `tower`, `hyper`
    - D-Bus Integration: `zbus` (pure Rust D-Bus implementation)
    - Search: `tantivy`, `fuzzy-matcher`
    - System / Hardware: `sysinfo`, `nvml-wrapper`
    - Keyring: `keyring` (integrating with `libsecret`)
- **Qt6 Subsystem**:
  - Version: Qt 6.8+
  - Modules: `qtbase`, `qtdeclarative`, `qtwayland`, `kirigami`
  - Build System: `CMake 3.28+` / `Ninja`
- **Shell & Scripting**:
  - Default User Shell: `fish` or `zsh` with pre-configured developer prompts (`starship`), with `bash` as POSIX system shell.

### 3.4. AI Infrastructure Tier

- **Local Inference Engine**:
  - `ollama` (bundled as systemd user unit).
  - Model Repository: GGUF quantized models (Q4_K_M, Q5_K_M, Q8_0).
  - Default Starter Models:
    - Code Intelligence: `qwen2.5-coder:7b` (recommended default for 8GB+ VRAM) or `qwen2.5-coder:1.5b` (lightweight fallback for CPU/low VRAM).
    - General / Reasoning: `llama3.2:3b` or `deepseek-r1:8b`.
    - Embeddings: `nomic-embed-text` (for local project semantic search).
- **Hardware Acceleration Backends**:
  - NVIDIA: CUDA 12+, cuDNN, TensorRT.
  - AMD: ROCm / HIP 6.x.
  - Intel: oneAPI / Level Zero / Vulkan Compute.
  - CPU: AVX-512 / AVX2 fallback with OpenMP acceleration.

---

## 4. Packaging & OS Build Pipeline

1. **Host Image Build Pipeline**:
   - Primary: **Fedora bootc** (OCI-based bootable container image). This modern approach allows NEXUS OS to be versioned, tested, and distributed as a container image that is atomically deployed to metal via `bootc install`.
   - Secondary / Traditional: Fedora Kickstart + `Lorax` / `livemedia-creator` for classic ISO generation.
2. **Component Packaging**:
   - `rpm`: Core system daemons (`nexus-aid`, `nexus-searchd`, `nexus-spotlight`).
   - `flatpak`: Sandboxed GUI apps where appropriate.
   - Proprietary Developer Applications (Cursor, JetBrains, Windsurf, Claude Code): Installed via the Nexus First-Run Setup Engine using verified upstream sources.

---

## 5. Technical Risks & Mitigations

| Technical Risk | Impact | Architectural Mitigation |
| :--- | :--- | :--- |
| **VRAM Exhaustion by Local AI Models** | Compositor freeze or system crash if local LLM exhausts all GPU memory. | `nexus-aid` includes a proactive hardware watchdog that checks available VRAM before model load. Implements safe quantization fallbacks and CPU layer offloading. |
| **Wayland Window Focus & Shortcut Grabbing** | Spotlight popup fails to capture keyboard input cleanly under strict Wayland security rules. | Use standardized `kde-layer-shell` / `wlr-layer-shell` protocols with `ZWLR_LAYER_SURFACE_V1_KEYBOARD_INTERACTIVITY_EXCLUSIVE` and `org.freedesktop.portal.GlobalShortcuts`. |
| **Search Indexing Performance & Battery Drain** | Constant filesystem indexing degrades laptop battery life and disk I/O. | `nexus-searchd` utilizes Linux `inotify` (event-driven, zero polling), skips binary/build directories (`node_modules`, `target`, `.git`), and throttles indexing during battery operation via `UPower` D-Bus signals. |
| **Legal / Licensing Exposure** | Inability to bundle proprietary tools (e.g. Cursor, official VS Code, Slack, Discord) inside the public OS ISO. | NEXUS OS provides zero proprietary software on the base installation media. Instead, a declarative, user-consenting First-Run Setup downloads and verifies upstream binaries directly to the user's workstation. |
