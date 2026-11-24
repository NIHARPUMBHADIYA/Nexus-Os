"""
NEXUS OS — AI Core Unit & Integration Test Suite
Verifies:
1. AES-GCM Encrypted Credential Vault & Masking
2. Hardware Governor & Compositor VRAM Headroom Defense
3. OmniRoute & Ollama Service Lifecycle Management
4. Provider Abstraction & Legitimate Free Tier Disclosures
5. Unified Model Center (7 Categories & Resource Tracking)
6. Reverse Proxy Multiplexer (OpenAI API /v1, Smart Routing, Anti-CSRF)
7. QML Component Compilation & Reactive Property Bindings
"""

import os
import sys
import json
import time
import shutil
import tempfile
import unittest
import urllib.request
import urllib.error

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.aicore.credential_vault import CredentialVault
from src.aicore.hardware_governor import HardwareGovernor
from src.aicore.service_manager import ServiceManager, OmniRouteManager, OllamaManager
from src.aicore.provider_manager import ProviderManager
from src.aicore.model_center import ModelCenter
from src.aicore.proxy_daemon import ProxyDaemon
from src.aicore.aicore_core import AICore
from src.aicore.aicore_bridge import AICoreBridge

class TestAICore(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="nexus_aicore_test_")
        self.vault_file = os.path.join(self.test_dir, "vault.enc")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_credential_vault_encryption_and_masking(self):
        """Verify AES-256-GCM encryption, plaintext absence on disk, and masking."""
        vault = CredentialVault(self.vault_file)
        secret_key = "sk-ant-api03-live-super-secret-key-987654321"

        # Store credential
        stored = vault.store_credential("anthropic", "api_key", secret_key)
        self.assertTrue(stored)

        # Retrieve and verify decrypted
        retrieved = vault.get_credential("anthropic", "api_key")
        self.assertEqual(retrieved, secret_key)

        # Verify masked representation
        masked = vault.get_masked_credential("anthropic", "api_key")
        self.assertTrue(masked.startswith("sk-"))
        self.assertTrue(masked.endswith("4321"))
        self.assertNotIn("super-secret", masked)

        # Verify file on disk is encrypted (zero plaintext leak)
        with open(self.vault_file, "rb") as f:
            raw_bytes = f.read()
        self.assertNotIn(b"sk-ant-api03", raw_bytes)
        self.assertNotIn(b"super-secret", raw_bytes)

        # Delete credential
        deleted = vault.delete_credential("anthropic")
        self.assertTrue(deleted)
        self.assertIsNone(vault.get_credential("anthropic"))

    def test_hardware_governor_vram_and_headroom(self):
        """Verify compositor safe headroom preservation and memory monitoring."""
        gov = HardwareGovernor(safe_vram_headroom_mb=2048, idle_timeout_minutes=15)

        # Check RAM
        ram = gov.get_system_ram()
        self.assertIn("total_gb", ram)
        self.assertIn("used_gb", ram)
        self.assertIn("percent", ram)
        self.assertGreater(ram["total_gb"], 0)

        # Check VRAM
        vram = gov.get_gpu_vram()
        self.assertIn("total_mb", vram)
        self.assertIn("free_mb", vram)
        self.assertEqual(vram["headroom_mb"], 2048)

        # Allocation within safe limit should pass
        can_small, _ = gov.can_allocate(required_mb=500)
        # Allocation of 500MB when free is typically > 2500MB
        if vram["free_mb"] - 500 >= 2048:
            self.assertTrue(can_small)

        # Allocation violating safe headroom must fail
        massive_mb = vram["free_mb"] - 1000  # leaves only 1000MB, less than 2048MB headroom
        if massive_mb > 0:
            can_massive, reason = gov.can_allocate(massive_mb)
            self.assertFalse(can_massive)
            self.assertIn("compositor safety headroom", reason)

        # Active model tracking and activity
        gov.register_loaded_model("qwen2.5-coder:7b", 4200)
        status = gov.get_full_status()
        self.assertIn("qwen2.5-coder:7b", status["active_models"])
        self.assertEqual(status["active_models_count"], 1)

    def test_service_manager_omniroute_and_ollama(self):
        """Verify OmniRoute and Ollama lifecycle controllers and systemd units."""
        sm = ServiceManager(self.test_dir)

        # OmniRoute Detection
        omni_det = sm.omniroute.detect_installation()
        self.assertIn("installed", omni_det)
        self.assertIn("npm install -g omniroute", omni_det["install_command"])
        self.assertEqual(sm.omniroute.port, 20128)

        # Ollama Detection
        ollama_det = sm.ollama.detect_installation()
        self.assertIn("installed", ollama_det)
        self.assertIn("ollama.com", ollama_det["install_command"])
        self.assertEqual(sm.ollama.port, 11434)

        # Systemd unit file content generation
        omni_unit = sm.omniroute.get_systemd_unit_content()
        self.assertIn("Description=Nexus OS OmniRoute AI Gateway Service", omni_unit)
        self.assertIn("Restart=on-failure", omni_unit)

        ollama_unit = sm.ollama.get_systemd_unit_content()
        self.assertIn("Description=Nexus OS Ollama Service", ollama_unit)
        self.assertIn("OLLAMA_HOST=127.0.0.1:11434", ollama_unit)

        # Consolidated status list
        services = sm.get_all_services_status()
        self.assertEqual(len(services), 2)
        service_ids = [s["id"] for s in services]
        self.assertIn("omniroute", service_ids)
        self.assertIn("ollama", service_ids)

    def test_provider_manager_and_free_tiers(self):
        """Verify provider abstraction and legitimate free tier disclosures."""
        vault = CredentialVault(self.vault_file)
        pm = ProviderManager(vault)

        providers = pm.list_providers()
        p_ids = [p["id"] for p in providers]
        self.assertIn("ollama", p_ids)
        self.assertIn("omniroute", p_ids)
        self.assertIn("groq", p_ids)
        self.assertIn("gemini", p_ids)
        self.assertIn("openai", p_ids)

        # Verify free tiers
        free_tiers = pm.get_free_tiers()
        self.assertGreaterEqual(len(free_tiers), 3)

        free_names = [f["provider"] for f in free_tiers]
        self.assertIn("Ollama (Local)", free_names)
        self.assertIn("Groq Cloud", free_names)
        self.assertIn("Google AI Studio", free_names)

        # Ensure disclosures exist
        for tier in free_tiers:
            self.assertTrue(len(tier["limits"]) > 10)
            self.assertTrue(len(tier["requirements"]) > 10)

        # Ensure paid-only models are NOT listed in free tiers
        all_free_models = []
        for tier in free_tiers:
            all_free_models.extend(tier["models"])

        self.assertNotIn("gpt-4o", all_free_models)
        self.assertNotIn("claude-3-7-sonnet", all_free_models)
        self.assertNotIn("o1-preview", all_free_models)

    def test_model_center_categories_and_actions(self):
        """Verify model catalog across 7 categories and lifecycle operations."""
        gov = HardwareGovernor(safe_vram_headroom_mb=2048)
        mc = ModelCenter(gov)

        categories = ["coding", "reasoning", "general", "vision", "embeddings", "lightweight", "large"]
        for cat in categories:
            models_in_cat = mc.list_models(category=cat)
            self.assertGreater(len(models_in_cat), 0, f"No models found for category: {cat}")

        # Search
        qwen = mc.list_models(query="qwen2.5-coder")
        self.assertGreater(len(qwen), 0)
        self.assertEqual(qwen[0]["id"], "qwen2.5-coder:7b")

        # Load / Unload a lightweight embedding model that fits in VRAM
        unload_res = mc.unload_model("nomic-embed-text")
        self.assertTrue(unload_res["success"])

        load_res = mc.load_model("nomic-embed-text")
        self.assertTrue(load_res["success"])

        # Test that loading a massive model exceeding safe headroom is blocked by governor
        massive_res = mc.load_model("llama3.3:70b")
        self.assertFalse(massive_res["success"])
        self.assertIn("compositor safety headroom", massive_res["error"])

        # Pull
        pull_res = mc.pull_model("smollm2:1.7b")
        self.assertTrue(pull_res["success"])
        pulled = mc.list_models(query="smollm2:1.7b")[0]
        self.assertTrue(pulled["installed"])

    def test_reverse_proxy_multiplexer_and_security(self):
        """Verify OpenAI-compatible /v1 proxy, smart model resolution, and CSRF protection."""
        test_port = 11438
        proxy = ProxyDaemon(port=test_port, host="127.0.0.1")
        started = proxy.start()
        self.assertTrue(started)
        time.sleep(0.3)

        try:
            # 1. Health check
            req = urllib.request.Request(f"http://127.0.0.1:{test_port}/health")
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertEqual(data["status"], "online")
                self.assertEqual(data["subsystem"], "nexus-aid")

            # 2. List models (/v1/models)
            req_models = urllib.request.Request(f"http://127.0.0.1:{test_port}/v1/models")
            with urllib.request.urlopen(req_models, timeout=2.0) as resp:
                self.assertEqual(resp.status, 200)
                models_data = json.loads(resp.read().decode())
                ids = [m["id"] for m in models_data["data"]]
                self.assertIn("nexus:default", ids)
                self.assertIn("nexus:fast", ids)
                self.assertIn("qwen2.5-coder:7b", ids)

            # 3. Chat completions with nexus:default
            req_chat = urllib.request.Request(
                f"http://127.0.0.1:{test_port}/v1/chat/completions",
                data=json.dumps({
                    "model": "nexus:default",
                    "messages": [{"role": "user", "content": "Write a Rust hello world"}]
                }).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req_chat, timeout=2.0) as resp:
                self.assertEqual(resp.status, 200)
                chat_data = json.loads(resp.read().decode())
                self.assertIn("choices", chat_data)
                self.assertTrue(len(chat_data["choices"]) > 0)
                self.assertIn("qwen2.5-coder:7b", chat_data["model"])

            # 4. Anti-CSRF Origin Validation (Reject evil web origins)
            req_csrf = urllib.request.Request(
                f"http://127.0.0.1:{test_port}/health",
                headers={"Origin": "https://malicious-website.com"}
            )
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(req_csrf, timeout=2.0)
            self.assertEqual(cm.exception.code, 403)

        finally:
            proxy.stop()

    def test_qml_view_compilation(self):
        """Verify QML syntax compilation and bridge binding."""
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QGuiApplication
        from PyQt6.QtQuick import QQuickView

        app = QGuiApplication.instance() or QGuiApplication(sys.argv)
        view = QQuickView()

        ds_qml = os.path.join(base_dir, "src", "design-system", "qml")
        aicore_qml = os.path.join(base_dir, "src", "aicore", "qml")

        view.engine().addImportPath(ds_qml)
        view.engine().addImportPath(aicore_qml)

        core = AICore(self.test_dir)
        bridge = AICoreBridge(core)
        view.rootContext().setContextProperty("aiCoreBridge", bridge)

        qml_path = os.path.join(aicore_qml, "NexusAICoreView.qml")
        view.setSource(QUrl.fromLocalFile(qml_path))

        status = view.status()
        self.assertEqual(
            status,
            QQuickView.Status.Ready,
            f"NexusAICoreView.qml failed compilation with status {status}"
        )

        core.shutdown()

if __name__ == "__main__":
    unittest.main()
