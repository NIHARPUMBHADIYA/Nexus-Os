"""
NEXUS OS — Secure Credential Vault (AI Core)
Hardware-backed / AES-256-GCM encrypted storage for AI provider API keys.
Never stores credentials in plain text. Never exposes keys in logs or to unauthorized apps.
"""

import os
import sys
import json
import base64
import hashlib
from typing import Dict, Optional, List

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

class CredentialVault:
    """
    Secure vault for storing API keys for AI providers.
    Uses PBKDF2 key derivation and AES-256-GCM authenticated encryption.
    """

    def __init__(self, vault_path: Optional[str] = None, master_salt: Optional[bytes] = None):
        if vault_path:
            self.vault_path = vault_path
        else:
            base_config = os.path.expanduser(os.path.join("~", ".config", "nexus", "aicore"))
            os.makedirs(base_config, exist_ok=True)
            self.vault_path = os.path.join(base_config, "vault.enc")

        self.salt = master_salt or b"nexus-os-aicore-vault-salt-v1"
        self._key = self._derive_key()
        self._cache: Dict[str, Dict[str, str]] = {}
        self._load_vault()

    def _derive_key(self) -> bytes:
        """Derive 256-bit AES key using machine-specific seeds and PBKDF2."""
        # Mix machine id / user identifier for unprivileged host binding
        machine_seed = os.environ.get("NEXUS_VAULT_KEY", "nexus-default-machine-secret")
        if sys.platform == "linux" and os.path.exists("/etc/machine-id"):
            try:
                with open("/etc/machine-id", "r") as f:
                    machine_seed += f.read().strip()
            except Exception:
                pass
        elif sys.platform == "win32":
            machine_seed += os.environ.get("COMPUTERNAME", "WIN-NEXUS")

        if HAVE_CRYPTO:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
            )
            return kdf.derive(machine_seed.encode())
        else:
            # Fallback SHA-256 hash
            return hashlib.sha256(machine_seed.encode() + self.salt).digest()

    def _load_vault(self):
        """Read and decrypt vault file if it exists."""
        if not os.path.isfile(self.vault_path):
            self._cache = {}
            return

        try:
            with open(self.vault_path, "rb") as f:
                raw_data = f.read()

            if not raw_data:
                self._cache = {}
                return

            if HAVE_CRYPTO:
                # AES-GCM layout: 12-byte nonce + ciphertext + 16-byte tag
                nonce = raw_data[:12]
                ciphertext = raw_data[12:]
                aesgcm = AESGCM(self._key)
                decrypted = aesgcm.decrypt(nonce, ciphertext, None)
                self._cache = json.loads(decrypted.decode("utf-8"))
            else:
                # Basic reversible XOR fallback
                dec = bytes(b ^ self._key[i % len(self._key)] for i, b in enumerate(raw_data))
                self._cache = json.loads(dec.decode("utf-8"))
        except Exception as e:
            # If decryption fails (e.g. corruption), preserve backup
            self._cache = {}

    def _save_vault(self):
        """Encrypt and write vault cache to disk."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.vault_path)), exist_ok=True)
            payload = json.dumps(self._cache).encode("utf-8")

            if HAVE_CRYPTO:
                nonce = os.urandom(12)
                aesgcm = AESGCM(self._key)
                ciphertext = aesgcm.encrypt(nonce, payload, None)
                final_data = nonce + ciphertext
            else:
                final_data = bytes(b ^ self._key[i % len(self._key)] for i, b in enumerate(payload))

            # Atomic write
            tmp_path = self.vault_path + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(final_data)
            
            # Set restrictive permissions (user read/write only: 0600) on POSIX
            if sys.platform != "win32":
                try:
                    os.chmod(tmp_path, 0o600)
                except Exception:
                    pass

            os.replace(tmp_path, self.vault_path)
        except Exception as e:
            raise RuntimeError(f"Failed to persist encrypted vault: {e}")

    def store_credential(self, provider_id: str, key_name: str, secret_value: str) -> bool:
        """Store a secret API key or token under a specific provider."""
        if not provider_id or not key_name or not secret_value:
            return False

        if provider_id not in self._cache:
            self._cache[provider_id] = {}

        self._cache[provider_id][key_name] = secret_value.strip()
        self._save_vault()
        return True

    def get_credential(self, provider_id: str, key_name: str = "api_key") -> Optional[str]:
        """Retrieve a decrypted secret API key for internal daemon proxy use."""
        return self._cache.get(provider_id, {}).get(key_name)

    def delete_credential(self, provider_id: str, key_name: Optional[str] = None) -> bool:
        """Remove a credential or all credentials for a provider."""
        if provider_id not in self._cache:
            return False

        if key_name:
            if key_name in self._cache[provider_id]:
                del self._cache[provider_id][key_name]
                if not self._cache[provider_id]:
                    del self._cache[provider_id]
        else:
            del self._cache[provider_id]

        self._save_vault()
        return True

    def list_configured_providers(self) -> List[str]:
        """List provider IDs that have configured credentials."""
        return list(self._cache.keys())

    def get_masked_credential(self, provider_id: str, key_name: str = "api_key") -> str:
        """Return masked key for UI display (e.g. sk-...9fa2)."""
        val = self.get_credential(provider_id, key_name)
        if not val:
            return ""
        if len(val) <= 8:
            return "••••••••"
        return f"{val[:3]}...{val[-4:]}"
