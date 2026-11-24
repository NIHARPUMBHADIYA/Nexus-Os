# Subsystem: NEXUS OS Universal Spotlight Launcher

## 1. Overview & Architecture

**NEXUS Spotlight** (`src/spotlight/`) is the central, universal, keyboard-first HUD launcher for NEXUS OS. It activates via `Win + Space` (or `Super + Space`), providing sub-millisecond fuzzy search across 16 core categories.

```
+=============================================================================+
|                 NEXUS UNIVERSAL SPOTLIGHT HUD (680px, radius-xl)             |
| [🔍] Search apps, files, projects, models (Win+Space)       [TAB: Actions]   |
+-----------------------------------------------------------------------------+
| [All]  [Applications]  [Projects]  [Files]  [AI Models]  [Commands]  [Sys]  |
+-----------------------------------------------------------------------------+
| RESULTS:                                      │ CONTEXTUAL ACTIONS DRAWER   |
| > [⌨] Nexus Terminal   Default Zsh / Starship │ • Launch Terminal   [Enter] |
|   [📁] nexus-os         Rust/Qt6 • main (clean)│ • New Window        [Ctrl+N]|
|   [🤖] qwen2.5-coder:7b Loaded in VRAM (4.2GB)│ • Reveal in Files   [Ctrl+R]|
|   [⚡] > cargo build    Compile workspace      │ • Copy Path         [Ctrl+C]|
+-----------------------------------------------------------------------------+
| 5 items found               •  ↑↓ Navigate  •  ↵ Launch  •  TAB Actions  •  ESC Close |
+=============================================================================+
```

---

## 2. Core Search Engine (`src/spotlight/search_engine.py`)

### 2.1. Search Providers
The engine uses a pluggable, modular provider architecture (`SearchProvider` base class):
1. **Applications (`ApplicationProvider`)**: Discovers `.desktop` specifications, terminal, developer hub, code editor, AI manager, and browser.
2. **Projects (`ProjectProvider`)**: Scans developer directories for git repositories and workspaces with `Cargo.toml`, `package.json`, `pyproject.toml`, or `CMakeLists.txt`.
3. **Files & Folders (`FileProvider`)**: Indexes user documents and folders with strict security exclusion filtering.
4. **AI Models (`AIModelProvider`)**: Interfaces with local Ollama models (`qwen2.5-coder:7b`, `llama3.2:3b`, `deepseek-r1:8b`, `nomic-embed-text`), displaying VRAM residency.
5. **Commands (`CommandProvider`)**: Safe execution parser for common developer commands (`cargo build`, `cargo test`, `git status`, `podman ps`). Detects arbitrary CLI execution prefixed with `>`.
6. **System Actions (`SystemActionsProvider`)**: Lock Workstation, Log Out, Restart, Shut Down, Toggle Dark/Light Theme, Toggle Wi-Fi, Toggle Bluetooth.
7. **Web Search (`WebSearchProvider`)**: Quick queries dispatched to DuckDuckGo or Google.

### 2.2. Relevance & Ranking Algorithm
Items are ranked using a multi-factor scoring pipeline:
- Exact Title Match: `+1000`
- Title Prefix Match: `+800`
- Title Word Exact Match: `+750`
- Title Word Prefix Match: `+700`
- Substring Match: `+600`
- Description Match: `+400`
- **Usage Frequency Boost**: `+ min(launch_count * 25, 200)`
- **Recency Boost**: `+ 50` if launched within the last 24 hours

### 2.3. SQLite FTS5 Database
Search data and usage history are stored in a local SQLite database (`~/.cache/nexus/spotlight.db`):
- `items`: Canonical items table with JSON metadata.
- `items_fts`: SQLite FTS5 full-text search virtual table.
- `usage_history`: Tracks `launch_count` and `last_launched` timestamp per item.

---

## 3. Security & Safety Architecture

### 3.1. Sensitive Credential Exclusion
`FileProvider.is_safe_path()` strictly prohibits indexing or exposing private keys, certificates, and credentials:
- **Extensions**: `.pem`, `.key`, `.pfx`, `.p12`, `.crt`, `.kdbx`, `.env`, `.token`
- **Filenames**: `.env`, `.env.local`, `id_rsa`, `id_ed25519`, `credentials.json`, `token.txt`, `secrets.yaml`
- **Directories**: `.git`, `node_modules`, `target`, `dist`, `build`, `.ssh`, `.gnupg`, `__pycache__`, `.venv`

### 3.2. Destructive Command Safety & Confirmation Modal
Any action flagged as destructive (e.g. `rm -rf`, `dd if=`, `mkfs`, `shutdown`, `reboot`, `systemctl stop`, `kill -9`) requires explicit secondary confirmation.
- The UI triggers an interactive warning modal: `⚠️ Confirm Action: <Warning Message>`.
- The user must explicitly press "Confirm & Execute" or `Enter` to proceed.
- Prevents accidental execution of destructive commands from fuzzy typing.

### 3.3. Shortcut Conflict Detection
- Checks whether `Win + Space` / `Super + Space` conflicts with Linux input-method switchers (such as IBus or Fcitx).
- Provides conflict detection and automatically suggests alternatives: `Alt + Space`, `Ctrl + Space`, or `Meta + Shift + Space`.

---

## 4. UI & Keyboard Navigation

- **Activation**: `Win + Space` or `Alt + Space` (or clicking the search icon in dock/panel).
- **Navigation**:
  - `↑` / `↓` (Up / Down arrows): Move selection highlight up and down.
  - `↵` (Enter): Execute the default primary action.
  - `Tab` or `→` (Right arrow): Slide open the **Contextual Actions Drawer**.
  - `←` (Left arrow): Close the actions drawer.
  - `Esc`: Close the actions drawer or dismiss the Spotlight overlay.
- **Actions Drawer**: Displays secondary actions:
  - Open File / IDE
  - Reveal in Folder
  - Open Terminal Here
  - Copy Path
  - Unload / Load AI Model
  - Run CLI Command

---

## 5. Standalone Execution & Automated Verification

### Running Spotlight Standalone:
```bash
python tools/run_spotlight.py
```

### Running the Desktop Shell with Spotlight:
```bash
python tools/run_desktop.py
# Press Win+Space or Alt+Space to open Spotlight
```

### Running the Test Suite:
```bash
python tests/test_spotlight.py
```
*(Tests FTS5 indexing, fuzzy ranking, usage boost, sensitive exclusions, destructive command detection, and QML overlay loading).*
