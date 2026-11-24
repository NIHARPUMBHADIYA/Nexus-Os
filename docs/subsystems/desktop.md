# Subsystem: NEXUS OS Desktop Shell & Window Management

## 1. Overview & Architecture

The **NEXUS OS Desktop Shell** (`src/desktop/shell/`) provides a clean, refined, developer-focused desktop operating system environment built on **KDE Plasma 6 (Wayland)** architecture, implemented in modular Qt6 / QML, and strictly adhering to the **Aether Design System** (`DESIGN_SYSTEM.md`).

```
+=============================================================================+
|                      NEXUS TOP SYSTEM PANEL (38px)                          |
| [💠 NEXUS] [Active App] [1 Code] [2 AI] [3 DevOps] [4 Web] | [Clock] | [Tray] |
+=============================================================================+
|                                                                             |
|   +---------------------------------------------------------------------+   |
|   |  NexusWindow: Draggable, Resizable, Snappable (radius-lg: 20px)     |   |
|   |  - Header: [✕][−][+] Traffic Lights • Title • Actions               |   |
|   |  - Body: TerminalApp / DevHubApp / AICoreApp / SettingsApp / Editor |   |
|   +---------------------------------------------------------------------+   |
|                                                                             |
|              +-----------------------------------------------+              |
|              |         NEXUS FLOATING BOTTOM DOCK            |              |
|              | [🚀]  [⌨]  [💻]  [📁]  [🤖]  [⚙]              |              |
|              |        •    •     •                           |              |
|              +-----------------------------------------------+              |
+=============================================================================+
```

---

## 2. Implemented Subsystems & Features

### 2.1. Desktop Wallpaper & Canvas
- Procedural geometric vector mesh overlay on top of ambient multi-stop gradients.
- Six curated wallpapers: **Obsidian Void**, **Nordic Aurora**, **Deep Space Void**, **Terminal Phosphor**, **Alpine Dawn**, and **Tokyo Neon**.
- Live wallpaper switching via desktop context menu or settings.

### 2.2. Window Management System (`NexusWindowManager` & `NexusWindow`)
- **Geometry & Rounded Corners**: 20px uniform radius (`radius-lg`) with anti-aliased 1.5px border and elevation shadow.
- **Window Controls**: Traffic light controls:
  - Close (Red, `#FF5F56`)
  - Minimize (Amber, `#FFBD2E`)
  - Maximize / Restore (Green, `#27C93F`)
- **Dragging**: Smooth drag via headerbar within desktop boundary constraints.
- **Window Snapping**:
  - Dragging to the top snaps the window to full maximized geometry.
  - Dragging to the left or right edges snaps the window to 50% split-screen tiling.
  - Double-clicking the titlebar toggles between maximized and restored states.
- **Resizing**: Bottom-right diagonal resize grip with `minWidth: 480px` and `minHeight: 320px` constraints.
- **Focus Management**: Clicking any window brings it to the top z-index and marks its decorations as active.
- **Multi-Window Support**: Multiple application windows run concurrently on the desktop.

### 2.3. Floating Bottom Dock (`NexusDock`)
- Position: Floating 14px above the bottom display edge.
- Height: 60px with 24px radius (`radius-xl`).
- Running Indicators: Dynamic accent-colored dot below running apps.
- Hover Animations: Physics-based hover lift (-6px) and scale (1.12x) with smooth easing.
- Pin / Unpin: Right-click context menu on dock items to Pin/Unpin, Launch, or Quit.
- Pinned Applications:
  - `🚀` Application Launcher
  - `⌨` Nexus Terminal
  - `💻` Code Editor
  - `📁` Developer Hub
  - `🤖` Nexus AI Core
  - `⚙` System Settings

### 2.4. Top System Panel (`NexusTopPanel`)
- Height: 38px, slim, non-intrusive.
- **Left**: NEXUS brand logo button (triggers launcher), active focused application name, and 4 virtual workspace pills (`1 Code`, `2 AI / Models`, `3 DevOps`, `4 Web`).
- **Center**: Real-time Clock & Date pill. Clicking opens the Notification & Calendar center.
- **Right**:
  - Live hardware VRAM / RAM allocation pill.
  - Quick status icons: Wi-Fi 6 (`📶`), Volume (`🔊`), Battery (`🔋`), Notifications bell (`🔔` with unread dot).
  - Quick Settings pill (`⚙ Control`).

### 2.5. Application Launcher (`NexusLauncher`)
- Centered modal HUD overlay with 24px corner radius (`radius-xl`).
- Real-time search filter across applications, descriptions, and categories.
- Keyboard-first: `Meta+Space` or `Alt+Space` opens/closes; `Escape` closes.

### 2.6. Quick Settings Popover (`NexusQuickSettings`)
- Anchored at top-right below the system tray.
- Instant Dark / Light mode toggle.
- Network (Wi-Fi 6) and Bluetooth status.
- Volume slider and Display Brightness slider.
- Power profile selector (Power Saver, Balanced, Performance).

### 2.7. Notification Center (`NexusNotificationCenter`)
- Popover listing active notifications with timestamps.
- "Clear All" action and individual dismissal.

### 2.8. Virtual Workspaces (`NexusWorkspaces`)
- 4 independent workspaces: `Code`, `AI / Models`, `DevOps`, `Web`.
- Windows belong to specific workspaces; switching workspaces hides/shows the appropriate window sets.
- Keyboard shortcuts: `Ctrl+1`, `Ctrl+2`, `Ctrl+3`, `Ctrl+4`.

### 2.9. Embedded Real Developer Applications
1. **Nexus Terminal (`TerminalApp.qml`)**:
   - Monospace developer terminal with Starship-style git prompt.
   - Interactive commands: `help`, `clear`, `uname -a`, `cargo build`, `podman ps`, `ollama ps`, `nexus-ai`.
2. **Developer Hub (`DevHubApp.qml`)**:
   - Displays active polyglot project workspaces with git branch status and dirty flags.
   - Container launch and IDE launch triggers.
3. **Nexus AI Core (`AICoreApp.qml`)**:
   - GPU VRAM allocation monitor (RTX 4070 8GB governor).
   - Local Ollama model manager with interactive Load/Unload toggles.
   - Unified `/v1` proxy status indicator.
4. **System Settings (`SettingsApp.qml`)**:
   - Live theme switching across all 9 themes (Midnight, Nord, Dracula, Catppuccin, Tokyo Night, Terminal Green, Paper Light, AMOLED, Deep Space).
   - Live accent color picker (Indigo, Emerald, Amber, Crimson, Cyan, Violet, Rose).
   - System version and compositor information.
5. **Code Editor (`EditorApp.qml`)**:
   - Modern editor tab bar, line numbers column, code editing area with syntax styling, and bottom status bar.

---

## 3. Real vs. Mocked System Integration Boundaries

In adherence to NEXUS OS engineering rules, mocked functionality is clearly demarcated:

| Feature | Current Prototype Implementation | Production Target Integration (Milestone 2 & 4) |
| :--- | :--- | :--- |
| **Window Management** | In-process QML window manager with real drag, resize, snap, minimize, and z-index | KWin 6 Wayland Compositor script & QML desktop shell plugin |
| **Hardware Metrics (VRAM/RAM)** | Reactive mock state simulating active GPU VRAM governor | Direct `nvml-wrapper` / `rocm-smi` / `/sys/class/drm` sysfs via `nexus-aid` D-Bus |
| **Network & Bluetooth** | UI state toggles in Quick Settings | NetworkManager & BlueZ session D-Bus interfaces |
| **Volume & Brightness** | In-shell reactive volume & brightness sliders | PipeWire/WirePlumber and `logind` brightness D-Bus |
| **Terminal Shell** | Built-in interactive command engine with realistic system responses | Native PTY (pseudo-terminal) spawning real `/bin/zsh` or `/bin/bash` |
| **AI Models List** | Dynamic state matching default Ollama and proxy configurations | Live HTTP queries to `http://localhost:11430/v1/models` and Ollama daemon |

---

## 4. Running the Desktop Shell

To launch the native desktop shell:
```bash
python tools/run_desktop.py
```

To run the automated desktop test suite:
```bash
python tests/test_desktop_shell.py
```
