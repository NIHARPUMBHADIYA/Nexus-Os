"""
NEXUS OS — Central AI Core Orchestrator (`nexus-aid`)
Unifies ServiceManager, HardwareGovernor, ModelCenter, ProviderManager,
CredentialVault, and the ProxyDaemon into a single coordinated system daemon.
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional

from .credential_vault import CredentialVault
from .hardware_governor import HardwareGovernor
from .service_manager import ServiceManager
from .provider_manager import ProviderManager
from .model_center import ModelCenter
from .proxy_daemon import ProxyDaemon

class AICore:
    """
    Singleton-style coordinator for all AI operations on NEXUS OS.
    """

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.expanduser(os.path.join("~", ".config", "nexus", "aicore"))
        os.makedirs(self.config_dir, exist_ok=True)

        self.vault = CredentialVault(os.path.join(self.config_dir, "vault.enc"))
        self.hardware = HardwareGovernor(safe_vram_headroom_mb=2048, idle_timeout_minutes=15)
        self.services = ServiceManager(self.config_dir)
        self.providers = ProviderManager(self.vault)
        self.model_center = ModelCenter(self.hardware)
        self.proxy = ProxyDaemon(
            port=11430,
            host="127.0.0.1",
            services=self.services,
            hardware=self.hardware,
            model_center=self.model_center,
            vault=self.vault
        )

        # Auto-start proxy multiplexer
        self.proxy.start()

    def get_hardware_status(self) -> Dict[str, Any]:
        """Fetch current RAM, VRAM, and governor metrics."""
        return self.hardware.get_full_status()

    def get_services_status(self) -> List[Dict[str, Any]]:
        """Fetch status for OmniRoute and Ollama daemons."""
        return self.services.get_all_services_status()

    def get_models(self, category: str = "all", query: str = "", local_only: bool = False) -> List[Dict[str, Any]]:
        """Query unified model center."""
        return self.model_center.list_models(category, query, local_only)

    def pull_model(self, model_id: str) -> Dict[str, Any]:
        """Download or register a model."""
        return self.model_center.pull_model(model_id)

    def delete_model(self, model_id: str) -> Dict[str, Any]:
        """Delete local model."""
        return self.model_center.delete_model(model_id)

    def load_model(self, model_id: str) -> Dict[str, Any]:
        """Load model into VRAM under governor policy."""
        return self.model_center.load_model(model_id)

    def unload_model(self, model_id: str) -> Dict[str, Any]:
        """Unload model from VRAM."""
        return self.model_center.unload_model(model_id)

    def get_providers(self) -> List[Dict[str, Any]]:
        """List AI providers with masked credentials."""
        return self.providers.list_providers()

    def get_free_tiers(self) -> List[Dict[str, Any]]:
        """List legitimate free model tiers with usage limit disclosures."""
        return self.providers.get_free_tiers()

    def save_credential(self, provider_id: str, api_key: str) -> bool:
        """Securely store an API key in the vault."""
        return self.providers.set_credential(provider_id, api_key)

    def test_provider(self, provider_id: str) -> Dict[str, Any]:
        """Test API reachability and auth."""
        return self.providers.test_provider_connection(provider_id)

    def start_service(self, service_id: str) -> bool:
        """Start a managed daemon (omniroute or ollama)."""
        if service_id == "omniroute":
            return self.services.omniroute.start()
        elif service_id == "ollama":
            return self.services.ollama.start()
        return False

    def stop_service(self, service_id: str) -> bool:
        """Stop a managed daemon."""
        if service_id == "omniroute":
            return self.services.omniroute.stop()
        elif service_id == "ollama":
            return self.services.ollama.stop()
        return False

    def restart_service(self, service_id: str) -> bool:
        """Restart a managed daemon."""
        if service_id == "omniroute":
            return self.services.omniroute.restart()
        elif service_id == "ollama":
            return self.services.ollama.restart()
        return False

    def get_service_logs(self, service_id: str) -> List[str]:
        """Get recent logs from daemon buffer."""
        if service_id == "omniroute":
            return self.services.omniroute.logs.get_lines()
        elif service_id == "ollama":
            return self.services.ollama.logs.get_lines()
        return []

    def shutdown(self):
        """Clean shutdown of background proxy and services."""
        self.proxy.stop()
