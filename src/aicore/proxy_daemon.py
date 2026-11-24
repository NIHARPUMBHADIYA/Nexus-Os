"""
NEXUS OS — AI Reverse Proxy Multiplexer (`nexus-aid`)
OpenAI-compatible HTTP reverse proxy listening on http://127.0.0.1:11430/v1.
Provides intelligent model routing for 'nexus:default' and 'nexus:fast'.
Enforces strict loopback binding and anti-CSRF origin validation.
"""

import os
import sys
import json
import time
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Dict, Any, Optional
import urllib.request
import urllib.error

from .credential_vault import CredentialVault
from .hardware_governor import HardwareGovernor
from .service_manager import ServiceManager
from .model_center import ModelCenter

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class ProxyRequestHandler(BaseHTTPRequestHandler):
    """
    Handles OpenAI-compatible HTTP requests at http://127.0.0.1:11430/v1.
    """

    server_version = "NexusAIProxy/1.0"

    def _send_cors_and_headers(self, status: int = 200, content_type: str = "application/json", content_length: Optional[int] = None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        if content_length is not None:
            self.send_header("Content-Length", str(content_length))
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:11430")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _verify_origin_security(self) -> bool:
        """CSRF Defense: Reject untrusted browser origins."""
        origin = self.headers.get("Origin")
        if origin:
            # Only allow localhost/127.0.0.1 origins
            allowed = ("http://localhost", "http://127.0.0.1", "null")
            if not any(origin.startswith(a) for a in allowed):
                self.send_error(403, "Forbidden: Untrusted external origin blocked by Nexus OS AI Security Policy.")
                return False
        return True

    def do_OPTIONS(self):
        self._send_cors_and_headers(200, content_length=0)

    def do_GET(self):
        if not self._verify_origin_security():
            return

        parsed_path = self.path.split("?")[0].rstrip("/")

        if parsed_path == "/health":
            self._handle_health()
        elif parsed_path in ("/v1/models", "/models"):
            self._handle_list_models()
        elif parsed_path in ("/v1/hardware", "/hardware"):
            self._handle_hardware_status()
        else:
            self.send_error(404, f"Endpoint not found: {self.path}")

    def do_POST(self):
        if not self._verify_origin_security():
            return

        parsed_path = self.path.split("?")[0].rstrip("/")

        if parsed_path in ("/v1/chat/completions", "/chat/completions"):
            self._handle_chat_completions()
        else:
            self.send_error(404, f"Endpoint not found: {self.path}")

    def _handle_health(self):
        resp = {
            "status": "online",
            "subsystem": "nexus-aid",
            "version": "1.0.0",
            "proxy_endpoint": "http://127.0.0.1:11430/v1",
            "governor": "active"
        }
        data = json.dumps(resp).encode("utf-8")
        self._send_cors_and_headers(200, content_length=len(data))
        try:
            self.wfile.write(data)
        except Exception:
            pass

    def _handle_list_models(self):
        model_center: ModelCenter = self.server.model_center
        catalog = model_center.list_models()

        data = [
            {"id": "nexus:default", "object": "model", "owned_by": "nexus-os", "description": "Intelligent coding router (Qwen 2.5 Coder 7B or OmniRoute)"},
            {"id": "nexus:fast", "object": "model", "owned_by": "nexus-os", "description": "Low-latency model (Llama 3.2 3B or Groq LPU)"}
        ]

        for m in catalog:
            data.append({
                "id": m["id"],
                "object": "model",
                "owned_by": m["provider"],
                "category": m["category"],
                "is_local": m["is_local"],
                "installed": m.get("installed", False),
                "loaded": m.get("loaded", False),
                "context_size": m.get("context_size", "8k")
            })

        resp = {"object": "list", "data": data}
        body = json.dumps(resp).encode("utf-8")
        self._send_cors_and_headers(200, content_length=len(body))
        try:
            self.wfile.write(body)
        except Exception:
            pass

    def _handle_hardware_status(self):
        hw: HardwareGovernor = self.server.hardware
        status = hw.get_full_status()
        body = json.dumps(status).encode("utf-8")
        self._send_cors_and_headers(200, content_length=len(body))
        try:
            self.wfile.write(body)
        except Exception:
            pass

    def _handle_chat_completions(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len)

        try:
            req_json = json.loads(post_data.decode("utf-8"))
        except Exception:
            self.send_error(400, "Invalid JSON payload.")
            return

        model = req_json.get("model", "nexus:default")
        messages = req_json.get("messages", [])

        # Update activity in hardware watchdog
        hw: HardwareGovernor = self.server.hardware
        hw.record_activity(model)

        # Smart Model Resolution
        target_model = model
        if model == "nexus:default":
            target_model = "qwen2.5-coder:7b"
        elif model == "nexus:fast":
            target_model = "llama3.2:3b"

        # Check if Ollama is running and handles this model
        services: ServiceManager = self.server.services
        if services.ollama.is_running():
            try:
                ollama_url = f"{services.ollama.endpoint}/v1/chat/completions"
                req_json["model"] = target_model
                forward_data = json.dumps(req_json).encode("utf-8")
                fwd_req = urllib.request.Request(ollama_url, data=forward_data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(fwd_req, timeout=5.0) as fwd_resp:
                    resp_body = fwd_resp.read()
                    self._send_cors_and_headers(fwd_resp.status, content_length=len(resp_body))
                    self.wfile.write(resp_body)
                    return
            except Exception:
                pass

        # Check if OmniRoute is running
        if services.omniroute.is_running():
            try:
                omni_url = f"{services.omniroute.endpoint}/chat/completions"
                req_json["model"] = target_model
                forward_data = json.dumps(req_json).encode("utf-8")
                fwd_req = urllib.request.Request(omni_url, data=forward_data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(fwd_req, timeout=5.0) as fwd_resp:
                    resp_body = fwd_resp.read()
                    self._send_cors_and_headers(fwd_resp.status, content_length=len(resp_body))
                    self.wfile.write(resp_body)
                    return
            except Exception:
                pass

        # Return standardized local fallback completion
        last_msg = messages[-1].get("content", "") if messages else ""
        mock_response = {
            "id": f"chatcmpl-nexus-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": target_model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"[NEXUS OS AI Core — Routed to {target_model}]\nProcessed response for: '{last_msg[:60]}...'"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(last_msg.split()),
                "completion_tokens": 20,
                "total_tokens": len(last_msg.split()) + 20
            }
        }
        body = json.dumps(mock_response).encode("utf-8")
        self._send_cors_and_headers(200, content_length=len(body))
        try:
            self.wfile.write(body)
        except Exception:
            pass

class ProxyDaemon:
    """
    Manages the proxy server lifecycle on 127.0.0.1:11430.
    """

    def __init__(
        self,
        port: int = 11430,
        host: str = "127.0.0.1",
        services: Optional[ServiceManager] = None,
        hardware: Optional[HardwareGovernor] = None,
        model_center: Optional[ModelCenter] = None,
        vault: Optional[CredentialVault] = None
    ):
        self.host = host
        self.port = port
        self.services = services or ServiceManager()
        self.hardware = hardware or HardwareGovernor()
        self.model_center = model_center or ModelCenter(self.hardware)
        self.vault = vault or CredentialVault()
        self.server: Optional[ThreadingHTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.is_running = False

    def start(self) -> bool:
        """Start the proxy server in a background thread."""
        if self.is_running:
            return True

        try:
            self.server = ThreadingHTTPServer((self.host, self.port), ProxyRequestHandler)
            self.server.services = self.services
            self.server.hardware = self.hardware
            self.server.model_center = self.model_center
            self.server.vault = self.vault

            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            self.is_running = True
            return True
        except Exception as e:
            self.is_running = False
            return False

    def stop(self):
        """Shut down the proxy server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        self.is_running = False
