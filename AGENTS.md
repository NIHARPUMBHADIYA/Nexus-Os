# NEXUS OS AI Agent Guidelines & Architecture Rules

> **Audience:** Autonomous AI coding agents (Antigravity, Claude Code, Cursor, Windsurf, Aider, Codex, Gemini CLI) contributing to or developing within the NEXUS OS codebase.

---

## 1. Operating Principles for AI Agents

When acting as an engineer on the NEXUS OS codebase, you must adhere to the following rules without exception:

1. **Verify Before and After**: Always inspect existing code and architecture before making changes. Always verify your changes through compilation, test execution, or validation scripts before completing a task.
2. **Modular Architecture**: Keep clear separation between:
   - UI / Presentation (`src/spotlight`, `src/devhub/ui`, `src/desktop`)
   - Business Logic & Search Core (`src/spotlight/core`, `src/devhub/core`)
   - Daemons & System Integration (`src/aicore`, `src/settings`)
3. **No Fake Static Mockups**: Implement real, functional, testable code. If a subsystem requires an external service (e.g. an active Ollama instance or D-Bus daemon), provide a well-structured mock or test harness for local validation rather than faking UI data.
4. **Security-First**:
   - Never commit or print API keys, tokens, or personal paths.
   - Never introduce unsanitized shell execution (`sh -c` with string concatenation).
   - Never run or require root permissions for standard desktop operations.
5. **Aether Design Tokens**: Never hardcode colors, radiuses, or padding in UI code. Always consume tokens from the Aether Design System (`DESIGN_SYSTEM.md`).

---

## 2. Language & Coding Standards

### 2.1. Rust (`src/aicore`, `src/spotlight/core`)
- Use **Rust 2021/2024 edition**.
- Strict formatting: `cargo fmt --check` and `cargo clippy -- -D warnings`.
- Error handling: Use `thiserror` for library/daemon errors and `anyhow` for top-level application boundaries. **Never use `.unwrap()` or `.expect()` in production code paths.**
- Async: Use `tokio` as the asynchronous runtime. Keep CPU-bound tasks off the main async reactor using `tokio::task::spawn_blocking`.

### 2.2. C++ & Qt6 (`src/devhub`, `src/desktop`)
- Standard: **Modern C++20**.
- Memory Management: Adhere to Qt parent-child ownership or use `std::unique_ptr` / `std::shared_ptr`. Zero raw pointer leaks.
- Formatting: Follow `clang-format` based on the project `.clang-format` specification.
- QML: Clean separation of QML declarative UI from C++ backend controllers. Use `Q_PROPERTY` with `NOTIFY` signals for reactive bindings.

### 2.3. Shell & System Configuration (`tools/`, `packaging/`)
- Standard: POSIX-compliant or Bash with `set -euo pipefail`.
- Always validate scripts using `shellcheck`.
- Document all environment variables and exit codes clearly.

---

## 3. Interfacing with Nexus AI Core (`nexus-aid`)

When an agent needs to leverage local AI models or query system models:
- Target endpoint: `http://localhost:11430/v1`
- Standard headers: `Authorization: Bearer <ephemeral_token>` (if configured)
- Request format: Standard OpenAI chat completions specification (`/v1/chat/completions`).
- Model tags:
  - `nexus:default` -> Intelligently routed to best available local coding model.
  - `nexus:fast` -> Lightweight low-latency model.
  - Specific tags -> e.g. `qwen2.5-coder:7b`, `llama3.2:3b`.
