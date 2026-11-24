"""
NEXUS OS — AI Coding Tools Catalog
Accurate specifications for 15 modern AI developer tools, editors, and terminal agents.
Documents licensing, installation methods, Linux compatibility, config paths, and AI endpoints.
"""

from typing import Dict, Any, List

class ToolCatalog:
    """
    Central repository of verified metadata for modern AI coding tools.
    """

    TOOLS: Dict[str, Dict[str, Any]] = {
        "antigravity": {
            "id": "antigravity",
            "name": "Google Antigravity",
            "category": "ide",
            "type": "AI-Native IDE & Agent CLI",
            "description": "Google's developer-first agentic IDE with integrated terminal and workflow engines.",
            "binary_names": ["antigravity", "agy"],
            "licensing": "Google Proprietary / Developer Preview",
            "can_redistribute": False,
            "linux_compatibility": "Native (x86_64, aarch64)",
            "install_methods": [
                {"type": "rpm", "command": "sudo dnf install google-antigravity"},
                {"type": "tarball", "command": "curl -fsSL https://antigravity.google/install.sh | sh"},
                {"type": "manual", "command": "Download RPM/Tarball from official Google developer portal."}
            ],
            "uninstall_command": "sudo dnf remove google-antigravity",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/antigravity/settings.json",
                "windows": "~/.gemini/antigravity/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "antigravity_json",
            "icon": "🚀",
            "website": "https://antigravity.google"
        },
        "vscode": {
            "id": "vscode",
            "name": "Visual Studio Code",
            "category": "editor",
            "type": "Extensible Code Editor",
            "description": "Widely adopted code editor supporting extensive AI extension ecosystems.",
            "binary_names": ["code", "code-insiders"],
            "licensing": "Microsoft Proprietary (Binary) / MIT (Code-OSS)",
            "can_redistribute": False,
            "linux_compatibility": "Native (RPM, Flatpak, Snap)",
            "install_methods": [
                {"type": "rpm", "command": "sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc && sudo dnf install code"},
                {"type": "flatpak", "command": "flatpak install flathub com.visualstudio.code"}
            ],
            "uninstall_command": "sudo dnf remove code || flatpak uninstall com.visualstudio.code",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/Code/User/settings.json",
                "windows": "%APPDATA%/Code/User/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "vscode_settings",
            "icon": "🟦",
            "website": "https://code.visualstudio.com"
        },
        "vscodium": {
            "id": "vscodium",
            "name": "VSCodium",
            "category": "editor",
            "type": "Free/Libre Open Source Editor",
            "description": "Community-driven, telemetry-free open-source binaries of VS Code.",
            "binary_names": ["codium"],
            "licensing": "MIT (100% FLOSS)",
            "can_redistribute": True,
            "linux_compatibility": "Native (RPM, Flatpak, AppImage)",
            "install_methods": [
                {"type": "rpm", "command": "sudo dnf install codium"},
                {"type": "flatpak", "command": "flatpak install flathub com.vscodium.codium"}
            ],
            "uninstall_command": "sudo dnf remove codium || flatpak uninstall com.vscodium.codium",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/VSCodium/User/settings.json",
                "windows": "%APPDATA%/VSCodium/User/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "vscode_settings",
            "icon": "🟩",
            "website": "https://vscodium.com"
        },
        "cursor": {
            "id": "cursor",
            "name": "Cursor",
            "category": "ide",
            "type": "AI-First Code Editor",
            "description": "AI-native code editor built on VS Code with deep multi-file agentic code generation.",
            "binary_names": ["cursor"],
            "licensing": "Anysphere Proprietary",
            "can_redistribute": False,
            "linux_compatibility": "Native (AppImage, Tarball)",
            "install_methods": [
                {"type": "appimage", "command": "curl -fsSL -o cursor.AppImage https://downloader.cursor.sh/linux/appImage/x64 && chmod +x cursor.AppImage && mv cursor.AppImage ~/.local/bin/cursor"},
                {"type": "manual", "command": "Download AppImage from https://cursor.com"}
            ],
            "uninstall_command": "rm -f ~/.local/bin/cursor",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/Cursor/User/settings.json",
                "windows": "%APPDATA%/Cursor/User/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "cursor_json",
            "icon": "⚡",
            "website": "https://cursor.com"
        },
        "windsurf": {
            "id": "windsurf",
            "name": "Windsurf",
            "category": "ide",
            "type": "Agentic AI IDE",
            "description": "Codeium's agentic IDE featuring collaborative Cascade AI workflows.",
            "binary_names": ["windsurf"],
            "licensing": "Codeium Proprietary",
            "can_redistribute": False,
            "linux_compatibility": "Native (RPM, Tarball, AppImage)",
            "install_methods": [
                {"type": "rpm", "command": "sudo dnf install windsurf"},
                {"type": "manual", "command": "Download RPM or tarball from https://codeium.com/windsurf"}
            ],
            "uninstall_command": "sudo dnf remove windsurf",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/Windsurf/User/settings.json",
                "windows": "%APPDATA%/Windsurf/User/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "windsurf_json",
            "icon": "🏄",
            "website": "https://codeium.com/windsurf"
        },
        "zed": {
            "id": "zed",
            "name": "Zed Editor",
            "category": "editor",
            "type": "High-Performance Rust Editor",
            "description": "Ultra-fast GPU-accelerated code editor with native local and cloud LLM assistant integration.",
            "binary_names": ["zed", "zed-editor"],
            "licensing": "GPLv3 / Apache 2.0 (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "Native (Flatpak, Official Tarball)",
            "install_methods": [
                {"type": "script", "command": "curl -f https://zed.dev/install.sh | sh"},
                {"type": "flatpak", "command": "flatpak install flathub dev.zed.Zed"}
            ],
            "uninstall_command": "rm -rf ~/.local/zed.app ~/.local/bin/zed || flatpak uninstall dev.zed.Zed",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/zed/settings.json",
                "windows": "%APPDATA%/Zed/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "zed_settings",
            "icon": "⚡",
            "website": "https://zed.dev"
        },
        "claude_code": {
            "id": "claude_code",
            "name": "Claude Code",
            "category": "terminal_agent",
            "type": "Terminal Coding Agent",
            "description": "Anthropic's research-grade agentic terminal CLI for codebase edits and test loops.",
            "binary_names": ["claude"],
            "licensing": "Anthropic Proprietary",
            "can_redistribute": False,
            "linux_compatibility": "Native (Node.js Global NPM)",
            "install_methods": [
                {"type": "npm", "command": "npm install -g @anthropic-ai/claude-code"}
            ],
            "uninstall_command": "npm uninstall -g @anthropic-ai/claude-code",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.claude/config.json",
                "windows": "~/.claude/config.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "claude_env_wrapper",
            "icon": "🤖",
            "website": "https://anthropic.com/claude-code"
        },
        "codex_cli": {
            "id": "codex_cli",
            "name": "OpenAI Codex CLI",
            "category": "terminal_agent",
            "type": "CLI Code Generation Agent",
            "description": "Terminal tool for generating shell commands, refactoring code, and resolving errors.",
            "binary_names": ["codex"],
            "licensing": "OpenAI API / MIT Client",
            "can_redistribute": True,
            "linux_compatibility": "Native (Python / NPM)",
            "install_methods": [
                {"type": "pip", "command": "pip install codex-cli"},
                {"type": "npm", "command": "npm install -g @openai/codex"}
            ],
            "uninstall_command": "pip uninstall -y codex-cli || npm uninstall -g @openai/codex",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/codex/config.json",
                "windows": "~/.config/codex/config.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "openai_compat_json",
            "icon": "💬",
            "website": "https://openai.com"
        },
        "gemini_cli": {
            "id": "gemini_cli",
            "name": "Gemini CLI",
            "category": "terminal_agent",
            "type": "Terminal Developer Assistant",
            "description": "Google Gemini CLI tool for shell commands, code explanation, and workspace analysis.",
            "binary_names": ["gemini", "gemini-cli"],
            "licensing": "Apache 2.0 (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "Native (Python / NPM)",
            "install_methods": [
                {"type": "pip", "command": "pip install gemini-cli"},
                {"type": "npm", "command": "npm install -g gemini-cli"}
            ],
            "uninstall_command": "pip uninstall -y gemini-cli || npm uninstall -g gemini-cli",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/gemini/config.json",
                "windows": "~/.config/gemini/config.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "gemini_config",
            "icon": "✨",
            "website": "https://ai.google.dev"
        },
        "opencode": {
            "id": "opencode",
            "name": "OpenCode",
            "category": "terminal_agent",
            "type": "Open-Source Terminal Copilot",
            "description": "Terminal-based pair programmer supporting custom endpoints and local models.",
            "binary_names": ["opencode"],
            "licensing": "MIT (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "Native (Go Binary / NPM)",
            "install_methods": [
                {"type": "npm", "command": "npm install -g opencode-ai"},
                {"type": "curl", "command": "curl -fsSL https://opencode.ai/install.sh | sh"}
            ],
            "uninstall_command": "npm uninstall -g opencode-ai",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/opencode/config.json",
                "windows": "~/.config/opencode/config.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "openai_compat_json",
            "icon": "💻",
            "website": "https://opencode.ai"
        },
        "aider": {
            "id": "aider",
            "name": "Aider Pair Programmer",
            "category": "terminal_agent",
            "type": "Git-Aware CLI AI Copilot",
            "description": "Leaderboard-topping AI pair programming CLI with automatic Git commits.",
            "binary_names": ["aider"],
            "licensing": "Apache 2.0 (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "Native (Python / pipx)",
            "install_methods": [
                {"type": "pipx", "command": "pipx install aider-chat"},
                {"type": "pip", "command": "pip install aider-chat"}
            ],
            "uninstall_command": "pipx uninstall aider-chat || pip uninstall -y aider-chat",
            "config_type": "yaml",
            "config_paths": {
                "linux": "~/.aider.conf.yml",
                "windows": "~/.aider.conf.yml"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "aider_yaml",
            "icon": "🧑‍💻",
            "website": "https://aider.chat"
        },
        "github_copilot": {
            "id": "github_copilot",
            "name": "GitHub Copilot",
            "category": "extension",
            "type": "IDE Extension & GH CLI Extension",
            "description": "GitHub's AI assistant providing inline code completions and chat in editors.",
            "binary_names": ["github-copilot-cli"],
            "licensing": "GitHub Proprietary",
            "can_redistribute": False,
            "linux_compatibility": "Native Extension (VS Code, Neovim, JetBrains)",
            "install_methods": [
                {"type": "gh_cli", "command": "gh extension install github/gh-copilot"},
                {"type": "vscode_ext", "command": "code --install-extension GitHub.copilot"}
            ],
            "uninstall_command": "gh extension remove github/gh-copilot || code --uninstall-extension GitHub.copilot",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/gh/config.yml",
                "windows": "~/.config/gh/config.yml"
            },
            "supports_ai_endpoint": False,
            "ai_config_format": "copilot_gh",
            "icon": "🐙",
            "website": "https://github.com/features/copilot"
        },
        "cline": {
            "id": "cline",
            "name": "Cline (Autonomous Agent)",
            "category": "extension",
            "type": "Autonomous Agent Extension",
            "description": "Autonomous AI assistant in VS Code that can create/edit files, run commands, and browse.",
            "binary_names": [],
            "extension_id": "saoudrizwan.claude-dev",
            "licensing": "Apache 2.0 (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "VS Code / VSCodium Extension",
            "install_methods": [
                {"type": "vscode_ext", "command": "code --install-extension saoudrizwan.claude-dev"},
                {"type": "codium_ext", "command": "codium --install-extension saoudrizwan.claude-dev"}
            ],
            "uninstall_command": "code --uninstall-extension saoudrizwan.claude-dev",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
                "windows": "%APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "cline_settings",
            "icon": "🤖",
            "website": "https://github.com/cline/cline"
        },
        "roo_code": {
            "id": "roo_code",
            "name": "Roo Code",
            "category": "extension",
            "type": "Community AI Agent Extension",
            "description": "Multi-mode agentic assistant for VS Code with custom modes, tool management, and local LLM support.",
            "binary_names": [],
            "extension_id": "rooveterinaryinc.roo-cline",
            "licensing": "Apache 2.0 (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "VS Code / VSCodium Extension",
            "install_methods": [
                {"type": "vscode_ext", "command": "code --install-extension rooveterinaryinc.roo-cline"},
                {"type": "codium_ext", "command": "codium --install-extension rooveterinaryinc.roo-cline"}
            ],
            "uninstall_command": "code --uninstall-extension rooveterinaryinc.roo-cline",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/settings.json",
                "windows": "%APPDATA%/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/settings.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "roo_settings",
            "icon": "🦘",
            "website": "https://github.com/RooVetGit/Roo-Code"
        },
        "continue": {
            "id": "continue",
            "name": "Continue",
            "category": "extension",
            "type": "Open-Source AI Code Assistant",
            "description": "Connect any LLM to VS Code or JetBrains for tab autocomplete and conversational editing.",
            "binary_names": [],
            "extension_id": "continue.continue",
            "licensing": "Apache 2.0 (Open Source)",
            "can_redistribute": True,
            "linux_compatibility": "VS Code / VSCodium / JetBrains Extension",
            "install_methods": [
                {"type": "vscode_ext", "command": "code --install-extension Continue.continue"},
                {"type": "codium_ext", "command": "codium --install-extension Continue.continue"}
            ],
            "uninstall_command": "code --uninstall-extension Continue.continue",
            "config_type": "json",
            "config_paths": {
                "linux": "~/.continue/config.json",
                "windows": "~/.continue/config.json"
            },
            "supports_ai_endpoint": True,
            "ai_config_format": "continue_json",
            "icon": "⏩",
            "website": "https://continue.dev"
        }
    }

    @classmethod
    def get_all_tools(cls) -> List[Dict[str, Any]]:
        return list(cls.TOOLS.values())

    @classmethod
    def get_tool(cls, tool_id: str) -> Dict[str, Any]:
        return cls.TOOLS.get(tool_id)
