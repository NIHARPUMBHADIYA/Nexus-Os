"""
NEXUS OS — AI Service & Daemon Lifecycle Manager (`nexus-aid`)
Detects, monitors, manages, and supervises OmniRoute and Ollama.
Supports systemd user services, process supervisor, and live log ring buffers.
"""

import os
import sys
import json
import time
import shutil
import urllib.request
import urllib.error
import subprocess
from collections import deque
from typing import Dict, Any, Optional, List

class ServiceLogBuffer:
    """Ring buffer for capturing real-time service logs."""
    def __init__(self, max_lines: int = 500):
        self._lines = deque(maxlen=max_lines)

    def append(self, text: str):
        timestamp = time.strftime("%H:%M:%S")
        for line in text.splitlines():
            line = line.strip()
            if line:
                self._lines.append(f"[{timestamp}] {line}")

    def get_lines(self, limit: int = 100) -> List[str]:
        return list(self._lines)[-limit:]

class OmniRouteManager:
    """
    OmniRoute AI Router & Gateway Lifecycle Manager.
    Endpoint: http://localhost:20128/v1
    Web Dashboard: http://localhost:20128
    """

    def __init__(self, port: int = 20128):
        self.port = port
        self.endpoint = f"http://127.0.0.1:{port}/v1"
        self.dashboard_url = f"http://127.0.0.1:{port}"
        self.process: Optional[subprocess.Popen] = None
        self.logs = ServiceLogBuffer()
        self.auto_start = True
        self.last_health: Dict[str, Any] = {
            "online": False,
            "latency_ms": 0.0,
            "checked_at": 0.0,
            "version": "unknown"
        }

    def detect_installation(self) -> Dict[str, Any]:
        """Detect whether omniroute is installed on the host."""
        bin_path = shutil.which("omniroute")
        installed = bin_path is not None
        version = "not installed"

        if installed:
            try:
                res = subprocess.run(["omniroute", "--version"], capture_output=True, text=True, timeout=2)
                if res.returncode == 0:
                    version = res.stdout.strip()
            except Exception:
                version = "installed"

        # Check Node.js prerequisite
        node_path = shutil.which("node")
        npm_path = shutil.which("npm")

        return {
            "installed": installed,
            "binary_path": bin_path or "",
            "version": version,
            "node_available": node_path is not None,
            "npm_available": npm_path is not None,
            "install_command": "npm install -g omniroute",
            "prerequisites": "Node.js >= 22.22 or >= 24"
        }

    def check_health(self) -> Dict[str, Any]:
        """Probe local OmniRoute HTTP endpoint."""
        now = time.time()
        start = time.perf_counter()
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{self.port}/", headers={"User-Agent": "Nexus-AICore/1.0"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                latency = round((time.perf_counter() - start) * 1000, 2)
                self.last_health = {
                    "online": resp.status in (200, 301, 302, 404),
                    "status_code": resp.status,
                    "latency_ms": latency,
                    "checked_at": now,
                    "version": "OmniRoute/1.x"
                }
        except Exception as e:
            self.last_health = {
                "online": False,
                "error": str(e),
                "latency_ms": 0.0,
                "checked_at": now,
                "version": "offline"
            }
        return self.last_health

    def start(self) -> bool:
        """Start OmniRoute background process."""
        if self.is_running():
            self.logs.append("OmniRoute is already running.")
            return True

        det = self.detect_installation()
        if not det["installed"]:
            self.logs.append("Cannot start OmniRoute: binary not found. Run 'npm install -g omniroute'.")
            return False

        try:
            cmd = ["omniroute", "run"]
            self.logs.append(f"Starting OmniRoute gateway on port {self.port}...")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            self.logs.append(f"OmniRoute process spawned with PID {self.process.pid}")
            time.sleep(0.5)
            self.check_health()
            return True
        except Exception as e:
            self.logs.append(f"Error starting OmniRoute: {e}")
            return False

    def stop(self) -> bool:
        """Stop running OmniRoute process."""
        if not self.is_running():
            self.logs.append("OmniRoute is not running.")
            return True

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
                self.logs.append("OmniRoute stopped cleanly.")
            except Exception:
                try:
                    self.process.kill()
                    self.logs.append("OmniRoute force terminated.")
                except Exception:
                    pass
            self.process = None
        self.check_health()
        return True

    def restart(self) -> bool:
        """Restart OmniRoute service."""
        self.logs.append("Restarting OmniRoute service...")
        self.stop()
        time.sleep(1)
        return self.start()

    def is_running(self) -> bool:
        """Check if process is active or endpoint was confirmed online."""
        if self.process and self.process.poll() is None:
            return True
        return self.last_health.get("online", False)

    def get_systemd_unit_content(self) -> str:
        """Generate systemd user service definition."""
        bin_path = shutil.which("omniroute") or "/usr/local/bin/omniroute"
        return f"""[Unit]
Description=Nexus OS OmniRoute AI Gateway Service
After=network.target

[Service]
Type=simple
ExecStart={bin_path} run
Restart=on-failure
RestartSec=5s
Environment=NODE_ENV=production
LimitNOFILE=65536

[Install]
WantedBy=default.target
"""

class OllamaManager:
    """
    Ollama Local LLM Lifecycle Manager.
    Endpoint: http://localhost:11434
    """

    def __init__(self, port: int = 11434):
        self.port = port
        self.endpoint = f"http://127.0.0.1:{port}"
        self.process: Optional[subprocess.Popen] = None
        self.logs = ServiceLogBuffer()
        self.auto_start = True
        self.last_health: Dict[str, Any] = {
            "online": False,
            "latency_ms": 0.0,
            "checked_at": 0.0,
            "version": "unknown"
        }

    def detect_installation(self) -> Dict[str, Any]:
        """Detect whether ollama is installed on the host."""
        bin_path = shutil.which("ollama")
        installed = bin_path is not None
        version = "not installed"

        if installed:
            try:
                res = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=2)
                if res.returncode == 0:
                    version = res.stdout.strip()
            except Exception:
                version = "installed"

        return {
            "installed": installed,
            "binary_path": bin_path or "",
            "version": version,
            "install_command": "curl -fsSL https://ollama.com/install.sh | sh",
            "supported_architectures": "x86_64, aarch64, CUDA, ROCm, Metal"
        }

    def check_health(self) -> Dict[str, Any]:
        """Probe local Ollama HTTP endpoint."""
        now = time.time()
        start = time.perf_counter()
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{self.port}/api/version", headers={"User-Agent": "Nexus-AICore/1.0"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                latency = round((time.perf_counter() - start) * 1000, 2)
                self.last_health = {
                    "online": True,
                    "version": data.get("version", "unknown"),
                    "latency_ms": latency,
                    "checked_at": now
                }
        except Exception as e:
            self.last_health = {
                "online": False,
                "error": str(e),
                "latency_ms": 0.0,
                "checked_at": now,
                "version": "offline"
            }
        return self.last_health

    def start(self) -> bool:
        """Start Ollama background daemon."""
        if self.is_running():
            self.logs.append("Ollama daemon is already active.")
            return True

        det = self.detect_installation()
        if not det["installed"]:
            self.logs.append("Cannot start Ollama: binary not found. Install from https://ollama.com.")
            return False

        try:
            cmd = ["ollama", "serve"]
            self.logs.append(f"Starting Ollama daemon on port {self.port}...")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            self.logs.append(f"Ollama process spawned with PID {self.process.pid}")
            time.sleep(0.5)
            self.check_health()
            return True
        except Exception as e:
            self.logs.append(f"Error starting Ollama: {e}")
            return False

    def stop(self) -> bool:
        """Stop running Ollama process."""
        if not self.is_running():
            self.logs.append("Ollama is not running.")
            return True

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
                self.logs.append("Ollama stopped cleanly.")
            except Exception:
                try:
                    self.process.kill()
                    self.logs.append("Ollama force terminated.")
                except Exception:
                    pass
            self.process = None
        self.check_health()
        return True

    def restart(self) -> bool:
        """Restart Ollama service."""
        self.logs.append("Restarting Ollama service...")
        self.stop()
        time.sleep(1)
        return self.start()

    def is_running(self) -> bool:
        """Check if process is active or endpoint was confirmed online."""
        if self.process and self.process.poll() is None:
            return True
        return self.last_health.get("online", False)

    def get_systemd_unit_content(self) -> str:
        """Generate systemd user service definition for Ollama."""
        bin_path = shutil.which("ollama") or "/usr/local/bin/ollama"
        return f"""[Unit]
Description=Nexus OS Ollama Service
After=network.target

[Service]
Type=simple
ExecStart={bin_path} serve
Restart=always
RestartSec=3s
Environment="OLLAMA_HOST=127.0.0.1:11434"

[Install]
WantedBy=default.target
"""

class ServiceManager:
    """
    Central Coordinator for NEXUS OS AI Background Services.
    """

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.expanduser(os.path.join("~", ".config", "nexus", "aicore"))
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, "services.json")

        self.omniroute = OmniRouteManager()
        self.ollama = OllamaManager()
        self._load_config()

    def _load_config(self):
        if os.path.isfile(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    cfg = json.load(f)
                    self.omniroute.auto_start = cfg.get("autostart_omniroute", True)
                    self.ollama.auto_start = cfg.get("autostart_ollama", True)
            except Exception:
                pass

    def save_config(self):
        try:
            cfg = {
                "autostart_omniroute": self.omniroute.auto_start,
                "autostart_ollama": self.ollama.auto_start,
                "omniroute_port": self.omniroute.port,
                "ollama_port": self.ollama.port,
                "updated_at": time.time()
            }
            with open(self.config_file, "w") as f:
                json.dump(cfg, f, indent=2)
        except Exception:
            pass

    def get_all_services_status(self) -> List[Dict[str, Any]]:
        """Return status payload for UI display."""
        omni_det = self.omniroute.detect_installation()
        omni_health = self.omniroute.check_health()

        ollama_det = self.ollama.detect_installation()
        ollama_health = self.ollama.check_health()

        return [
            {
                "id": "omniroute",
                "name": "OmniRoute AI Gateway",
                "role": "Multi-Provider Dynamic Router & Context Compressor",
                "endpoint": self.omniroute.endpoint,
                "dashboard_url": self.omniroute.dashboard_url,
                "installed": omni_det["installed"],
                "version": omni_det["version"],
                "running": omni_health["online"],
                "latency_ms": omni_health.get("latency_ms", 0.0),
                "auto_start": self.omniroute.auto_start,
                "install_command": omni_det["install_command"],
                "icon": "🔀"
            },
            {
                "id": "ollama",
                "name": "Ollama Local Engine",
                "role": "Offline High-Performance Local Model Server",
                "endpoint": self.ollama.endpoint,
                "dashboard_url": "",
                "installed": ollama_det["installed"],
                "version": ollama_det["version"],
                "running": ollama_health["online"],
                "latency_ms": ollama_health.get("latency_ms", 0.0),
                "auto_start": self.ollama.auto_start,
                "install_command": ollama_det["install_command"],
                "icon": "🦙"
            }
        ]
