# Contributing to NEXUS OS

> Thank you for helping build the future of developer-first, AI-native operating systems!

---

## 1. Code of Conduct

NEXUS OS is an open, welcoming, and professional community. We expect all contributors and maintainers to treat everyone with respect, courtesy, and professional collaboration.

---

## 2. Development Setup

You can develop and test NEXUS OS components on **any modern Linux distribution** (Fedora, Arch Linux, Ubuntu 24.04+, Debian 12+) without needing to replace your primary operating system.

### Prerequisites:
- **Rust Toolchain**: `rustup` (Rust 1.82+)
- **C++ / Qt6**: `gcc-c++` or `clang`, `cmake 3.28+`, `ninja-build`, `qt6-qtbase-devel`, `qt6-qtdeclarative-devel`
- **Container Runtime**: `podman` or `docker`
- **Code Linters**: `cargo-clippy`, `clang-format`, `shellcheck`

### Quick Start:
```bash
# Clone the repository
git clone https://github.com/nexus-os/nexus.git
cd nexus

# Run the local verification harness
./tools/verify-environment.sh

# Build all user-space core components
cargo build --workspace
```

---

## 3. Git Workflow & Commit Guidelines

We enforce the **Conventional Commits** specification:

```
<type>(<scope>): <short imperative description>

[optional body]

[optional footer(s)]
```

### Types:
- `feat`: A new user-facing feature or capability.
- `fix`: A bug fix.
- `docs`: Documentation changes.
- `arch`: Architectural decisions, specifications, or blueprints.
- `style`: Formatting, design token updates, no code logic changes.
- `refactor`: Code reorganization with no behavior change.
- `test`: Adding or updating test suites.
- `chore`: Build script, CI, or dependency updates.

### Examples:
- `feat(spotlight): implement tantivy project search indexer`
- `fix(aicore): resolve VRAM leak on Ollama process idle timeout`
- `docs(architecture): document D-Bus session bus interface`

---

## 4. Pull Request Standards

Before submitting a Pull Request:
1. Ensure your code passes all lint checks:
   ```bash
   cargo clippy --workspace --all-targets -- -D warnings
   cargo test --workspace
   ```
2. For UI components, verify both **Obsidian Core (Dark)** and **Alabaster Flow (Light)** themes.
3. Keep PRs focused on a single logical change or milestone component.
4. Update relevant documentation in `docs/` and architectural specifications if IPC or contracts change.
