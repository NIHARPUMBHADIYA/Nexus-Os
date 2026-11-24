# NEXUS OS Security Architecture & Policies

> **Classification:** Public Technical Specification  
> **Security Philosophy:** Defense-in-Depth, Least Privilege, Zero Unverified Telemetry  

---

## 1. Threat Model & Principles

Modern developer workstations face unique security threats: developer environments frequently run untrusted third-party code (e.g. `npm install`, `pip install`, cloned repositories), execute local AI models, and store high-value cloud credentials (SSH keys, AWS/GCP tokens, AI API keys).

NEXUS OS establishes security as a core architectural primitive:
1. **Never Run Daemons as Root**: All Nexus core services (`nexus-aid`, `nexus-searchd`, `nexus-spotlight`, `nexus-devhub`) run strictly under the unprivileged user session.
2. **Zero Plaintext Credentials on Disk**: External API keys and secrets must never be committed to repository files or written as plaintext in environment variables or configuration files.
3. **Transparent Execution**: No destructive or privileged command is ever executed silently without explicit user confirmation.
4. **Hardware-Guarded AI Execution**: Local AI models must not be allowed to exhaust system VRAM/RAM or execute unsanitized arbitrary code.

---

## 2. Subsystem Security Specifications

### 2.1. Credential Management & Secret Storage
- **Protocol**: FreeDesktop Secret Service API (`org.freedesktop.secrets`).
- **Implementation**: Backed by **KDE KWallet** or **GNOME Keyring** using hardware-backed TPM 2.0 keys or user master password encryption.
- **Provider Keys**: When a user adds an Anthropic, OpenAI, or Gemini key, `nexus-aid` stores it directly in the system keyring.
- **Agent Access**: External coding agents obtain ephemeral authorization tokens via the local proxy; the raw master API key is never exposed to the client.

---

### 2.2. Local AI Security & Proxy Protection (`nexus-aid`)
- **Loopback Binding**: The local OpenAI-compatible HTTP proxy (`localhost:11430`) binds strictly to `127.0.0.1` and `::1`. It is never bound to `0.0.0.0` or public network interfaces.
- **Local Origin Validation**: Requests to `nexus-aid` validate standard `Origin` and `Host` headers to prevent Cross-Site Request Forgery (CSRF) attacks originating from web browsers.
- **Model File Integrity**: All downloaded local GGUF models are verified against cryptographic SHA-256 checksums before loading into GPU memory.
- **Resource Exhaustion Defense**: `nexus-aid` monitors VRAM before model allocation. If loading a model would starve KWin's compositor buffers of VRAM, the load is rejected with a descriptive error.

---

### 2.3. Universal Spotlight Command Safety
- **Destructive Command Guard**: Spotlight parses command inputs using an AST-aware parser. Commands matching high-risk signatures (e.g. `rm -rf`, `dd`, `mkfs`, `chmod -R 777`, raw block device writes) display a high-visibility warning badge requiring secondary confirmation.
- **Privilege Escalation**: Commands requiring elevated privileges (`sudo`, `pkexec`) are dispatched through the system's standard `polkit` authentication agent with a graphical password dialog. Spotlight itself never runs with `setuid` or elevated permissions.

---

### 2.4. Toolchain & Workspace Isolation
- **Container-First Development**: Rather than encouraging developers to install thousands of conflicting packages directly into the host OS, Developer Hub defaults to isolated **Podman** rootless containers or **Distrobox** environments.
- **Host Protection**: Rootless containers share the user's UID mapping without granting real root privileges on the host kernel, preventing host system compromise even if a containerized dependency is malicious.
- **SELinux Enforcement**: On the base Fedora distribution, SELinux remains in `enforcing` mode. Targeted policies constrain desktop daemons to their expected filesystem trees (`~/.local/share/nexus`, `~/.config/nexus`).

---

## 3. Vulnerability Reporting & Disclosure

If you discover a security vulnerability within NEXUS OS or any of its core daemons:
1. **Do not open a public GitHub issue.**
2. Send an encrypted email with technical reproduction steps to: `security@nexus-os.org` (or open a confidential security advisory in the repository).
3. The security team will acknowledge receipt within 48 hours and provide an estimated remediation timeline.
