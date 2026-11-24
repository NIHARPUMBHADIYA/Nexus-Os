"""
NEXUS OS — AI Provider Abstraction & Management (`nexus-aid`)
Unified provider interface for Ollama, OmniRoute, OpenAI, Anthropic, Gemini,
Groq, OpenRouter, and generic OpenAI-compatible endpoints.
Maintains verified free-tier catalog with accurate usage disclosures.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from .credential_vault import CredentialVault

class BaseAIProvider:
    """Base class for all AI provider integrations."""
    def __init__(self, provider_id: str, name: str, base_url: str, is_local: bool = False):
        self.provider_id = provider_id
        self.name = name
        self.base_url = base_url
        self.is_local = is_local

    def test_connection(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Test API reachability and authentication."""
        raise NotImplementedError

    def list_models(self, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """List models accessible through this provider."""
        raise NotImplementedError

class ProviderManager:
    """
    Manages configured providers, credential binding, and free-tier discovery.
    """

    # Verified Legitimate Free Tiers with strict disclosures
    VERIFIED_FREE_TIERS = [
        {
            "id": "ollama_local",
            "provider": "Ollama (Local)",
            "name": "Local Hardware Execution",
            "tier_type": "100% Free & Offline",
            "limits": "Unlimited requests, zero telemetry, private to your workstation.",
            "requirements": "Requires local GPU or CPU RAM.",
            "models": ["qwen2.5-coder:7b", "llama3.2:3b", "deepseek-r1:8b", "smollm2:1.7b"],
            "url": "https://ollama.com",
            "requires_api_key": False
        },
        {
            "id": "groq_free",
            "provider": "Groq Cloud",
            "name": "LPU Inference Free Tier",
            "tier_type": "Free Developer Tier",
            "limits": "30 Requests/min, 14,400 Tokens/min, 500k Tokens/day.",
            "requirements": "Requires a free account and API key from console.groq.com.",
            "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
            "url": "https://console.groq.com",
            "requires_api_key": True
        },
        {
            "id": "gemini_free",
            "provider": "Google AI Studio",
            "name": "Gemini Developer Tier",
            "tier_type": "Free Tier (Rate-Limited)",
            "limits": "15 Requests/min, 1,500 Requests/day for Flash models.",
            "requirements": "Requires a free Google account and API key from aistudio.google.com. Data may be used for model training under free terms.",
            "models": ["gemini-2.0-flash", "gemini-1.5-flash"],
            "url": "https://aistudio.google.com",
            "requires_api_key": True
        },
        {
            "id": "openrouter_free",
            "provider": "OpenRouter",
            "name": "Community Free Models",
            "tier_type": "Free Tier (:free tag)",
            "limits": "20 Requests/min. Models designated with the ':free' suffix.",
            "requirements": "Requires free account and key from openrouter.ai.",
            "models": ["meta-llama/llama-3.2-3b-instruct:free", "deepseek/deepseek-r1:free"],
            "url": "https://openrouter.ai",
            "requires_api_key": True
        }
    ]

    def __init__(self, vault: Optional[CredentialVault] = None):
        self.vault = vault or CredentialVault()
        self.providers: Dict[str, Dict[str, Any]] = {
            "ollama": {
                "id": "ollama",
                "name": "Ollama (Local)",
                "category": "local",
                "base_url": "http://127.0.0.1:11434",
                "requires_key": False,
                "description": "Local offline execution engine for open-weights models."
            },
            "omniroute": {
                "id": "omniroute",
                "name": "OmniRoute Gateway",
                "category": "router",
                "base_url": "http://127.0.0.1:20128/v1",
                "requires_key": False,
                "description": "Multi-provider AI routing gateway and token compressor."
            },
            "groq": {
                "id": "groq",
                "name": "Groq Cloud (Fast / Free Tier)",
                "category": "cloud",
                "base_url": "https://api.groq.com/openai/v1",
                "requires_key": True,
                "description": "Ultra-low latency LPU inference with generous free quota."
            },
            "gemini": {
                "id": "gemini",
                "name": "Google Gemini",
                "category": "cloud",
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "requires_key": True,
                "description": "Multimodal flagship reasoning and code analysis."
            },
            "openai": {
                "id": "openai",
                "name": "OpenAI",
                "category": "cloud",
                "base_url": "https://api.openai.com/v1",
                "requires_key": True,
                "description": "GPT-4o, o1, and o3 reasoning models."
            },
            "anthropic": {
                "id": "anthropic",
                "name": "Anthropic Claude",
                "category": "cloud",
                "base_url": "https://api.anthropic.com/v1",
                "requires_key": True,
                "description": "Claude 3.7 Sonnet and Claude 3.5 Haiku coding models."
            },
            "openrouter": {
                "id": "openrouter",
                "name": "OpenRouter",
                "category": "aggregator",
                "base_url": "https://openrouter.ai/api/v1",
                "requires_key": True,
                "description": "Unified cloud aggregator with community free models."
            },
            "custom_openai": {
                "id": "custom_openai",
                "name": "Custom OpenAI Compatible Endpoint",
                "category": "custom",
                "base_url": "http://127.0.0.1:8000/v1",
                "requires_key": False,
                "description": "Self-hosted vLLM, LM Studio, LocalAI, or private inference server."
            }
        }

    def list_providers(self) -> List[Dict[str, Any]]:
        """Return provider list with credential configuration status."""
        configured = set(self.vault.list_configured_providers())
        result = []
        for pid, info in self.providers.items():
            has_key = pid in configured
            masked = self.vault.get_masked_credential(pid) if has_key else ""
            result.append({
                "id": info["id"],
                "name": info["name"],
                "category": info["category"],
                "base_url": info["base_url"],
                "requires_key": info["requires_key"],
                "is_configured": (not info["requires_key"]) or has_key,
                "masked_key": masked,
                "description": info["description"]
            })
        return result

    def get_free_tiers(self) -> List[Dict[str, Any]]:
        """Return vetted free tiers and usage rules."""
        return self.VERIFIED_FREE_TIERS

    def set_credential(self, provider_id: str, api_key: str) -> bool:
        """Securely store API key in the vault."""
        if not api_key:
            return self.vault.delete_credential(provider_id)
        return self.vault.store_credential(provider_id, "api_key", api_key)

    def test_provider_connection(self, provider_id: str) -> Dict[str, Any]:
        """Verify reachability and authentication for a specific provider."""
        info = self.providers.get(provider_id)
        if not info:
            return {"success": False, "error": f"Unknown provider: {provider_id}"}

        # Local Ollama check
        if provider_id == "ollama":
            try:
                req = urllib.request.Request("http://127.0.0.1:11434/api/version")
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    data = json.loads(resp.read().decode())
                    return {"success": True, "message": f"Connected to local Ollama v{data.get('version', '')}"}
            except Exception as e:
                return {"success": False, "error": f"Ollama not responding on port 11434: {e}"}

        # Local OmniRoute check
        if provider_id == "omniroute":
            try:
                req = urllib.request.Request("http://127.0.0.1:20128/")
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    return {"success": True, "message": "Connected to local OmniRoute gateway on port 20128"}
            except Exception as e:
                return {"success": False, "error": f"OmniRoute gateway not responding on port 20128: {e}"}

        # Cloud API check
        api_key = self.vault.get_credential(provider_id)
        if info["requires_key"] and not api_key:
            return {"success": False, "error": "API key is not configured in the secure vault."}

        # Validate standard OpenAI-compatible endpoints (/v1/models)
        if provider_id in ("groq", "openai", "openrouter", "custom_openai"):
            try:
                url = f"{info['base_url']}/models"
                headers = {"Authorization": f"Bearer {api_key}" if api_key else ""}
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    return {"success": True, "message": f"Successfully authenticated with {info['name']}"}
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    return {"success": False, "error": "Authentication failed: Invalid API key."}
                return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
            except Exception as e:
                return {"success": False, "error": f"Network error: {e}"}

        return {"success": True, "message": f"Configuration saved for {info['name']}."}
