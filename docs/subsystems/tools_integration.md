# Subsystem: Modern AI Coding Tools Integration (`nexus-tools`)

## 1. Architectural Overview

The **Nexus Modern AI Tools Integration Layer** connects the NEXUS OS developer ecosystem with 15 leading modern AI coding tools, editors, and terminal agents. It eliminates the friction of configuring diverse endpoints, ensures configuration safety through automatic timestamped backups, and respects software licensing and distribution boundaries.

```
+=============================================================================+
|                      NEXUS TOOLS INTEGRATION VIEW                           |
|   - Real-time Installation Scanner       - 5 Preset AI Routing Profiles     |
|   - Multi-format Configuration Injector  - FreeDesktop Shortcut Generator   |
+=============================================================================+
                                      │
                         (ToolsIntegrationBridge)
                                      │
+=====================================▼=======================================+
|                   SAFE CONFIGURATION ADAPTER & BACKUP                       |
|   - Non-destructive Writes: <config_file>.bak.<timestamp>                   |
|   - Reversible Restorations                                                 |
|   - Native JSON & YAML Schema Parsers                                       |
+=============================================================================+
                                      │
              ┌───────────────────────┼────────────────────────┐
              v                       v                        v
      +---------------+      +-----------------+      +-----------------+
      |  Full IDEs    |      | Terminal Agents |      | AI Extensions   |
      | - Antigravity |      | - Claude Code   |      | - Continue      |
      | - Cursor      |      | - Aider         |      | - Cline         |
      | - Windsurf    |      | - OpenCode      |      | - Roo Code      |
      | - Zed         |      | - Gemini CLI    |      | - GitHub Copilot|
      | - VS Code     |      | - Codex CLI     |      |                 |
      | - VSCodium    |      |                 |      |                 |
      +---------------+      +-----------------+      +-----------------+
```

---

## 2. Supported Tools Catalog (15 Tools)

| ID | Name | Category | License | Linux Compatibility | Config Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `antigravity` | Google Antigravity | IDE & CLI | Google Proprietary | Native Linux (x86_64, aarch64) | `~/.config/antigravity/settings.json` |
| `vscode` | Visual Studio Code | Editor | Microsoft Proprietary | Native (RPM, Flatpak, Snap) | `~/.config/Code/User/settings.json` |
| `vscodium` | VSCodium | Editor | MIT (100% FLOSS) | Native (RPM, Flatpak, AppImage) | `~/.config/VSCodium/User/settings.json` |
| `cursor` | Cursor | AI IDE | Anysphere Proprietary | Native (AppImage, Tarball) | `~/.config/Cursor/User/settings.json` |
| `windsurf` | Windsurf | Agentic IDE | Codeium Proprietary | Native (RPM, AppImage) | `~/.config/Windsurf/User/settings.json` |
| `zed` | Zed Editor | Editor | GPLv3 / Apache 2.0 | Native (Flatpak, Official Tarball) | `~/.config/zed/settings.json` |
| `claude_code` | Claude Code | CLI Agent | Anthropic Proprietary | Native (Node.js Global NPM) | `~/.claude/config.json` |
| `codex_cli` | OpenAI Codex CLI | CLI Agent | OpenAI API / MIT Client | Native (Python / NPM) | `~/.config/codex/config.json` |
| `gemini_cli` | Gemini CLI | CLI Agent | Apache 2.0 (Open Source) | Native (Python / NPM) | `~/.config/gemini/config.json` |
| `opencode` | OpenCode | CLI Agent | MIT (Open Source) | Native (Go Binary / NPM) | `~/.config/opencode/config.json` |
| `aider` | Aider | CLI Agent | Apache 2.0 (Open Source) | Native (Python / pipx) | `~/.aider.conf.yml` |
| `github_copilot` | GitHub Copilot | Extension / CLI | GitHub Proprietary | Native Extension / GH CLI | `~/.config/gh/config.yml` |
| `cline` | Cline | Extension | Apache 2.0 (Open Source) | VS Code / VSCodium Extension | `~/.config/Code/User/globalStorage/.../` |
| `roo_code` | Roo Code | Extension | Apache 2.0 (Open Source) | VS Code / VSCodium Extension | `~/.config/Code/User/globalStorage/.../` |
| `continue` | Continue | Extension | Apache 2.0 (Open Source) | VS Code / JetBrains Extension | `~/.continue/config.json` |

---

## 3. Availability & Detection Rules

In adherence to NEXUS OS principles:
- **No Fake Availability**: An application is marked as "Installed" strictly if its official binary exists on system `PATH` or its extension manifest is detected on disk.
- **Licensing Integrity**: Proprietary applications (Cursor, Windsurf, VS Code, Antigravity) are not bundled illegally into OS media. Instead, NEXUS OS provides official upstream installation workflows (DNF repositories, Flatpak, AppImage, or direct download scripts).

---

## 4. AI Routing Profiles

Users can select a target profile to inject into any supported tool:

1. **Local Coding (`local_coding`)**:
   - Provider: `nexus-aid` / `ollama`
   - Endpoint: `http://localhost:11430/v1` (or `http://localhost:11434`)
   - Model: `nexus:default` (`qwen2.5-coder:7b`)
   - Privacy: 100% offline, zero external network traffic, zero token fees.
2. **Free Cloud Models (`free_cloud`)**:
   - Provider: Groq LPU / Google AI Studio
   - Endpoint: `http://localhost:11430/v1`
   - Model: `llama-3.3-70b-versatile` or `gemini-2.0-flash`
   - Features: High-throughput free developer tier inference.
3. **Premium Cloud Models (`premium_cloud`)**:
   - Provider: Anthropic / OpenAI
   - Endpoint: `http://localhost:11430/v1`
   - Model: `claude-3-7-sonnet` or `gpt-4o`
   - Features: Frontier hybrid reasoning and multi-file agentic capabilities.
4. **Deep Reasoning (`reasoning`)**:
   - Provider: DeepSeek R1 / OpenAI o-series
   - Endpoint: `http://localhost:11430/v1`
   - Model: `deepseek-r1:8b` or `o3-mini`
   - Features: Chain-of-thought mathematical and algorithmic verification.
5. **Fast Coding (`fast_coding`)**:
   - Provider: Local lightweight or Groq
   - Endpoint: `http://localhost:11430/v1`
   - Model: `nexus:fast` (`llama3.2:3b`)
   - Features: Sub-100ms completions for real-time scaffolding.

---

## 5. Non-Destructive Backup Guarantee

Modifying configuration files carries inherent risk of breaking custom user bindings or deleting personal settings.

- **Automatic Pre-Modification Backups**:
  - Before writing to any configuration file (e.g. `settings.json`, `.aider.conf.yml`), the adapter creates a backup:
    ```
    <config_file>.bak.<YYYYMMDD_HHMMSS>
    ```
- **Permission Requirements**:
  - The adapter modifies only the designated AI endpoint keys (e.g. `assistant`, `language_models`, `models`, `openai-api-base`), leaving all other editor preferences intact.
- **One-Click Restoration**:
  - Previous backups are indexed and can be reverted at any time via the UI or bridge API (`restoreBackup`).

---

## 6. Verification and Testing

Automated testing is maintained in **`tests/test_tool_integrations.py`**:
- Catalog completeness: 15/15 tools present with verified licensing.
- Detection accuracy: confirms absence of mock state.
- Backup & restore: tests real file creation, corruption simulation, and recovery.
- Format injectors: tests Zed JSON, Continue JSON, Aider YAML, and Cursor JSON.
- FreeDesktop shortcut generation: validates compliance with the XDG specification.
- QML UI compilation: validates reactive property bindings.
