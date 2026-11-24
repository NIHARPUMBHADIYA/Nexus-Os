# Subsystem: Nexus AI Core (`nexus-aid`)

## 1. Architectural Overview

The **Nexus AI Core** (`nexus-aid`) is the operating system's native AI infrastructure layer. It provides local model execution, multi-provider smart routing, hardware resource governance, and a secure OpenAI-compatible reverse proxy at `http://127.0.0.1:11430/v1`.

AI Core unifies background daemons (**OmniRoute** and **Ollama**), hardware monitoring, credential encryption, and model lifecycle management into a single, cohesive developer-first experience adhering strictly to the **Aether Design System** and **Least Privilege Security Architecture**.

```
+=============================================================================+
|                      APPLICATIONS & CLIENT TOOLS                            |
|    - Spotlight HUD         - Developer Hub Copilot    - Cursor / Zed        |
|    - System Terminal CLI   - Claude Code / Aider      - Web Apps            |
+=============================================================================+
                                      │ HTTP /v1 (Loopback: 127.0.0.1:11430)
+=====================================▼=======================================+
|                     NEXUS AI CORE PROXY MULTIPLEXER                         |
|  - Anti-CSRF Origin Guard          - Smart Alias Resolver (nexus:default)   |
|  - Internal Credential Injection   - Safe Compositor Headroom Enforcement   |
+=============================================================================+
        │                                  │                        │
        v                                  v                        v
+-------------------+            +-------------------+    +-------------------+
|  OLLAMA ENGINE    |            | OMNIROUTE GATEWAY |    | CLOUD PROVIDERS   |
|  - Port 11434     |            | - Port 20128/v1   |    | - Anthropic       |
|  - Local GGUF     |            | - Auto-Routing    |    | - Google Gemini   |
|  - Offline / Free |            | - Token Compress  |    | - Groq / OpenAI   |
+-------------------+            +-------------------+    +-------------------+
        │                                  │                        │
        └────────────────────────┬─────────┴────────────────────────┘
                                 │
+================================▼============================================+
|                       SYSTEM DAEMONS & GOVERNORS                            |
|  +------------------------+  +----------------------+  +------------------+ |
|  | Hardware Governor      |  | Credential Vault     |  | Service Manager  | |
|  | (2GB VRAM KWin Guard)  |  | (AES-256-GCM PBKDF2) |  | (systemd --user) | |
|  +------------------------+  +----------------------+  +------------------+ |
+=============================================================================+
```

---

## 2. OmniRoute Integration

**OmniRoute** is an open-source AI router and gateway designed to unify multi-provider LLMs under a single OpenAI-compatible endpoint:

- **Local Endpoint**: `http://localhost:20128/v1`
- **Dashboard Interface**: `http://localhost:20128`
- **Installation Integration**: Detects Node.js (`>= 22.22` or `>= 24`) and provides one-click or CLI installation via `npm install -g omniroute`.
- **System Service Supervison**:
  - Configured as a background systemd user service (`packaging/systemd/nexus-omniroute.service`).
  - Auto-starts on session login with auto-restart on failure (`Restart=on-failure`, `RestartSec=5s`).
  - Health monitoring via HTTP probes with millisecond latency tracking.
  - Live log streaming captured via internal ring buffer (`ServiceLogBuffer`).
- **Score-Driven Auto-Routing**:
  - Routes requests dynamically using model prefixes: `auto`, `auto/coding`, `auto/fast`, `auto/cheap`, and `auto/offline`.
  - Built-in token compression reduces prompt token overhead by 15% to 95%.

---

## 3. Ollama Integration

**Ollama** powers the local, private, offline execution of open-weights models:

- **Local Endpoint**: `http://127.0.0.1:11434`
- **Installation Integration**: Automatic detection of `ollama` binary with installer dispatch (`curl -fsSL https://ollama.com/install.sh | sh`).
- **System Service**:
  - Managed via `packaging/systemd/nexus-ollama.service`.
  - Restricted loopback binding (`OLLAMA_HOST=127.0.0.1:11434`).
- **Model Lifecycle Operations**:
  - Pull / Download: Downloads models into local disk storage.
  - Delete: Removes unneeded weights to free disk storage.
  - Load into VRAM: Allocates weights into GPU memory.
  - Unload: Releases GPU memory back to the system.

---

## 4. Hardware Governor & Compositor Safety Headroom

Local model execution must never destabilize or freeze the desktop shell. KWin and Wayland compositors require dedicated VRAM to render windows at 60/120+ FPS without dropped frames.

- **Compositor Headroom Defense**:
  - Enforces a strict minimum of **2048 MB** free VRAM reserved exclusively for the desktop compositor.
  - Any model allocation request (`can_allocate(model_vram)`) that would leave less than 2048 MB free VRAM is **blocked** by the governor with a descriptive error.
- **Hardware Telemetry**:
  - Live GPU VRAM metrics queried via NVIDIA NVML (`nvidia-smi`), AMD ROCm, or system memory APIs.
  - System RAM metrics with used, free, and total values.
- **Inactivity Idle Unallocation**:
  - Automatically unallocates models from GPU VRAM after **15 minutes** of inactivity to preserve power and thermal headroom.

---

## 5. Secure Credential Vault

- **Zero Plaintext Credentials**: API keys are never stored in plain text files or environment variable dumps.
- **Encryption Specification**:
  - Backed by **AES-256-GCM** authenticated encryption with a 12-byte random nonce and 16-byte authentication tag.
  - Keys derived via **PBKDF2** (SHA-256, 100,000 iterations) salted with machine-specific seeds.
  - Restrictive file permissions (`0600`, user read/write only).
- **Security & Privacy Safeguards**:
  - Raw keys are never written to log files.
  - UI displays keys strictly masked (e.g. `sk-...4321` or `••••••••`).
  - External applications never receive the raw master key; they call `localhost:11430/v1` which injects credentials internally.

---

## 6. Unified Model Center (7 Categories)

The Model Center organizes models into 7 standardized developer categories:

1. **Coding**: `qwen2.5-coder:7b` (default), `deepseek-coder:6.7b`, `claude-3-7-sonnet`.
2. **Reasoning**: `deepseek-r1:8b`, `qwq:32b`, `deepseek-r1:70b`.
3. **General Conversation**: `llama3.2:3b`, `mistral:7b`, `gemini-2.0-flash`.
4. **Vision**: `llava:7b` (UI & screenshot understanding).
5. **Embeddings**: `nomic-embed-text` (project indexing), `bge-m3`.
6. **Lightweight**: `smollm2:1.7b` (ultra-efficient 1GB model).
7. **Large Models**: `llama3.3:70b` (frontier open weights).

Every model in the catalog displays:
- Provider (Local vs. Cloud)
- Required System RAM & VRAM Allocation
- GPU Compatibility
- Size on Disk
- Availability & Download Status
- Context Window Size (e.g. 32k, 128k, 200k, 1M)

---

## 7. Legitimate Free Tiers Disclosures

NEXUS OS maintains a strict policy: **Never falsely label paid models as free.**

| Provider / Tier | Tier Type | Limit & Quota Disclosures | Requirements |
| :--- | :--- | :--- | :--- |
| **Ollama (Local)** | 100% Free & Offline | Unlimited requests, zero telemetry, private to workstation. | Requires local GPU/CPU RAM. |
| **Groq Cloud** | Free Developer Tier | 30 RPM, 14,400 TPM, 500k Tokens/day on Llama 3.3 70B & Gemma 2. | Free account & key at console.groq.com. |
| **Google AI Studio** | Free Tier (Rate-Limited) | 15 RPM, 1,500 Requests/day on Gemini 2.0 Flash / 1.5 Flash. | Free key at aistudio.google.com. Terms permit model training on free tier. |
| **OpenRouter Free** | Community Free Tier | Models tagged with `:free` (e.g. `llama-3.2-3b:free`). | Free account at openrouter.ai. |

---

## 8. Reverse Proxy Multiplexer (`:11430/v1`)

The local HTTP proxy provides an OpenAI-compatible endpoint for IDEs, CLI tools, and system agents:

- **Loopback-Only Binding**: Strictly binds to `127.0.0.1:11430` (never public interfaces).
- **Anti-CSRF Origin Validation**: Rejects requests originating from untrusted web browser origins with `403 Forbidden`.
- **Virtual Model Aliases**:
  - `nexus:default` -> Intelligently routed to best available local coding model (`qwen2.5-coder:7b`) if VRAM allows, or routed to OmniRoute / configured cloud.
  - `nexus:fast` -> Lightweight low-latency model (`llama3.2:3b` or Groq LPU).
- **Endpoints**:
  - `GET /health`: Health status and subsystem version.
  - `GET /v1/models`: Unified list of available local and cloud models.
  - `GET /v1/hardware`: Real-time RAM, VRAM, and governor metrics.
  - `POST /v1/chat/completions`: Standard chat completions with smart model routing.

---

## 9. Verification & Testing

The subsystem is validated by automated test suites:
- **`tests/test_aicore.py`**:
  - `test_credential_vault_encryption_and_masking`: Verifies AES-256-GCM encryption, zero plaintext on disk, and key masking.
  - `test_hardware_governor_vram_and_headroom`: Validates compositor headroom enforcement, preventing VRAM starvation.
  - `test_service_manager_omniroute_and_ollama`: Verifies installation detection, health checks, and systemd unit generation.
  - `test_provider_manager_and_free_tiers`: Validates provider listing and verifies paid models are not mislabeled as free.
  - `test_model_center_categories_and_actions`: Verifies 7 categories, search, pull, and memory load/unload.
  - `test_reverse_proxy_multiplexer_and_security`: Verifies `/health`, `/v1/models`, `/v1/chat/completions`, and anti-CSRF 403 protection.
  - `test_qml_view_compilation`: Validates QML compilation and reactive property binding.
