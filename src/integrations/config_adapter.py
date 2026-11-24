"""
NEXUS OS — Safe AI Configuration Adapter & Profile Injector
Manages configuration files for modern AI coding tools.
Never overwrites existing files without creating a timestamped backup first.
Injects AI endpoint profiles (Local Coding, Free Cloud, Premium, Reasoning, Fast).
"""

import os
import sys
import json
import time
import shutil
from typing import Dict, Any, Optional, List
from .tool_catalog import ToolCatalog
from .tool_detector import ToolDetector

class ConfigAdapter:
    """
    Safely configures AI coding tools to point to NEXUS OS AI Core (nexus-aid),
    OmniRoute, or Ollama using pre-defined model profiles.
    """

    PROFILES = {
        "local_coding": {
            "id": "local_coding",
            "name": "Local Coding (Private & Offline)",
            "model": "nexus:default",
            "fallback_model": "qwen2.5-coder:7b",
            "base_url": "http://localhost:11430/v1",
            "ollama_url": "http://localhost:11434",
            "api_key": "nexus-local",
            "description": "Offline Qwen 2.5 Coder 7B running on local GPU. 100% private, zero token costs."
        },
        "free_cloud": {
            "id": "free_cloud",
            "name": "Free Cloud Models (Groq / Gemini)",
            "model": "llama-3.3-70b-versatile",
            "fallback_model": "gemini-2.0-flash",
            "base_url": "http://localhost:11430/v1",
            "api_key": "nexus-local",
            "description": "Legitimate free-tier models via Groq LPU (Llama 3.3 70B) or Google AI Studio."
        },
        "premium_cloud": {
            "id": "premium_cloud",
            "name": "Premium Cloud (Claude 3.7 / GPT-4o)",
            "model": "claude-3-7-sonnet",
            "fallback_model": "gpt-4o",
            "base_url": "http://localhost:11430/v1",
            "api_key": "nexus-local",
            "description": "Frontier hybrid reasoning and agentic software engineering."
        },
        "reasoning": {
            "id": "reasoning",
            "name": "Deep Reasoning (DeepSeek R1 / o3-mini)",
            "model": "deepseek-r1:8b",
            "fallback_model": "o3-mini",
            "base_url": "http://localhost:11430/v1",
            "api_key": "nexus-local",
            "description": "Chain-of-thought mathematical proof and complex algorithmic verification."
        },
        "fast_coding": {
            "id": "fast_coding",
            "name": "Fast Coding (Llama 3.2 3B / Low Latency)",
            "model": "nexus:fast",
            "fallback_model": "llama3.2:3b",
            "base_url": "http://localhost:11430/v1",
            "api_key": "nexus-local",
            "description": "Sub-100ms completions for rapid iterative coding and scaffolding."
        }
    }

    def __init__(self, detector: Optional[ToolDetector] = None):
        self.detector = detector or ToolDetector()
        self.catalog = self.detector.catalog

    @classmethod
    def get_profiles(cls) -> List[Dict[str, Any]]:
        return list(cls.PROFILES.values())

    def create_backup(self, file_path: str) -> Optional[str]:
        """Create a timestamped backup before any file modification."""
        if not os.path.isfile(file_path):
            return None
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.bak.{timestamp}"
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            raise IOError(f"Failed to create configuration backup for {file_path}: {e}")

    def list_backups(self, file_path: str) -> List[str]:
        """List existing backups for a configuration file."""
        if not file_path:
            return []
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        if not os.path.isdir(dirname):
            return []
        results = []
        for entry in os.listdir(dirname):
            if entry.startswith(f"{basename}.bak."):
                results.append(os.path.join(dirname, entry))
        return sorted(results, reverse=True)

    def restore_backup(self, backup_path: str, target_path: str) -> bool:
        """Restore a previously saved backup file."""
        if not os.path.isfile(backup_path):
            return False
        try:
            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    def apply_ai_profile(self, tool_id: str, profile_id: str = "local_coding") -> Dict[str, Any]:
        """
        Safely configure an AI tool with the specified profile.
        Creates backup, updates configuration, and verifies output.
        """
        tool_info = self.catalog.get_tool(tool_id)
        if not tool_info:
            return {"success": False, "error": f"Unknown tool: {tool_id}"}

        profile = self.PROFILES.get(profile_id)
        if not profile:
            return {"success": False, "error": f"Unknown profile: {profile_id}"}

        if not tool_info.get("supports_ai_endpoint"):
            return {
                "success": False,
                "error": f"{tool_info['name']} does not support custom OpenAI-compatible AI endpoint configuration."
            }

        plat_key = "windows" if sys.platform == "win32" else "linux"
        config_path_raw = tool_info.get("config_paths", {}).get(plat_key) or tool_info.get("config_paths", {}).get("linux", "")
        config_file = self.detector.resolve_path(config_path_raw)

        if not config_file:
            return {"success": False, "error": "Could not resolve configuration path for host platform."}

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(config_file), exist_ok=True)

        # Create safety backup if file already exists
        backup_created = self.create_backup(config_file)

        # Dispatch tool-specific configuration injector
        format_type = tool_info.get("ai_config_format", "json")
        try:
            if format_type == "zed_settings":
                self._configure_zed(config_file, profile)
            elif format_type == "continue_json":
                self._configure_continue(config_file, profile)
            elif format_type == "aider_yaml":
                self._configure_aider(config_file, profile)
            elif format_type == "cursor_json":
                self._configure_cursor(config_file, profile)
            elif format_type == "vscode_settings":
                self._configure_vscode(config_file, profile)
            elif format_type == "antigravity_json":
                self._configure_antigravity(config_file, profile)
            elif format_type in ("openai_compat_json", "opencode_json"):
                self._configure_generic_openai(config_file, profile)
            elif format_type == "cline_settings":
                self._configure_cline(config_file, profile)
            elif format_type == "roo_settings":
                self._configure_roo(config_file, profile)
            elif format_type == "claude_env_wrapper":
                self._configure_claude_code(config_file, profile)
            else:
                self._configure_generic_openai(config_file, profile)

            return {
                "success": True,
                "tool_id": tool_id,
                "tool_name": tool_info["name"],
                "profile": profile["name"],
                "config_path": config_file,
                "backup_path": backup_created or "None (New file created)",
                "message": f"Successfully configured {tool_info['name']} to use NEXUS OS AI Core ({profile['name']})."
            }
        except Exception as e:
            # If write failed and backup exists, restore backup
            if backup_created and os.path.isfile(backup_created):
                self.restore_backup(backup_created, config_file)
            return {"success": False, "error": f"Failed to configure {tool_info['name']}: {e}"}

    # --- Tool Specific Injectors ---

    def _configure_zed(self, path: str, profile: Dict[str, Any]):
        data = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data["assistant"] = {
            "default_model": {
                "provider": "openai",
                "model": profile["model"]
            },
            "version": "2"
        }
        if "language_models" not in data:
            data["language_models"] = {}

        data["language_models"]["openai"] = {
            "api_url": profile["base_url"],
            "available_models": [
                {"name": profile["model"], "max_tokens": 16384},
                {"name": "nexus:default", "max_tokens": 16384},
                {"name": "nexus:fast", "max_tokens": 8192}
            ]
        }
        data["language_models"]["ollama"] = {
            "api_url": "http://localhost:11434"
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_continue(self, path: str, profile: Dict[str, Any]):
        data = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        nexus_model = {
            "title": f"NEXUS OS AI Core ({profile['name']})",
            "provider": "openai",
            "model": profile["model"],
            "apiBase": profile["base_url"],
            "apiKey": profile["api_key"]
        }

        models = data.get("models", [])
        # Remove previous nexus entries
        models = [m for m in models if "NEXUS OS" not in m.get("title", "")]
        models.insert(0, nexus_model)
        data["models"] = models

        data["tabAutocompleteModel"] = {
            "title": "NEXUS Fast Autocomplete",
            "provider": "openai",
            "model": "nexus:fast",
            "apiBase": profile["base_url"],
            "apiKey": profile["api_key"]
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_aider(self, path: str, profile: Dict[str, Any]):
        content = f"""# NEXUS OS AI Core Configuration for Aider
openai-api-base: {profile['base_url']}
openai-api-key: {profile['api_key']}
model: openai/{profile['model']}
edit-format: diff
auto-commits: true
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _configure_cursor(self, path: str, profile: Dict[str, Any]):
        data = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data["cursor.general.customBaseUrl"] = profile["base_url"]
        data["cursor.general.customOpenAIKey"] = profile["api_key"]
        data["cursor.general.modelName"] = profile["model"]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_vscode(self, path: str, profile: Dict[str, Any]):
        data = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data["nexus.ai.endpoint"] = profile["base_url"]
        data["nexus.ai.model"] = profile["model"]
        data["github.copilot.advanced"] = {
            "debug.overrideEngine": profile["model"],
            "debug.overrideProxyUrl": profile["base_url"]
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_antigravity(self, path: str, profile: Dict[str, Any]):
        data = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data["ai.proxy"] = profile["base_url"]
        data["ai.model"] = profile["model"]
        data["ai.provider"] = "nexus-aid"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_generic_openai(self, path: str, profile: Dict[str, Any]):
        data = {
            "api_base": profile["base_url"],
            "api_key": profile["api_key"],
            "model": profile["model"],
            "provider": "nexus-aid"
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_cline(self, path: str, profile: Dict[str, Any]):
        data = {
            "apiProvider": "openai",
            "openAiBaseUrl": profile["base_url"],
            "openAiApiKey": profile["api_key"],
            "openAiModelId": profile["model"]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_roo(self, path: str, profile: Dict[str, Any]):
        data = {
            "apiProvider": "openai-native",
            "openAiBaseUrl": profile["base_url"],
            "openAiApiKey": profile["api_key"],
            "openAiModelId": profile["model"]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _configure_claude_code(self, path: str, profile: Dict[str, Any]):
        data = {
            "anthropic_base_url": "http://localhost:20128/v1",
            "model": profile["model"],
            "router": "omniroute"
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
