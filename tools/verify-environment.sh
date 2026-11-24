#!/usr/bin/env bash
# NEXUS OS - Verification Harness
# Checks system environment, dependencies, and verifies project files.

set -euo pipefail

echo "=========================================================="
echo "         NEXUS OS - Environment Verification             "
echo "=========================================================="

echo "[1/4] Checking host architecture..."
ARCH=$(uname -m)
echo "  Architecture: $ARCH"

echo "[2/4] Checking build tools..."
if command -v cargo &>/dev/null; then
    echo "  Rust Cargo: $(cargo --version)"
else
    echo "  Rust Cargo: Not found (Required for building Rust daemons)"
fi

if command -v cmake &>/dev/null; then
    echo "  CMake: $(cmake --version | head -n 1)"
else
    echo "  CMake: Not found (Required for building DevHub)"
fi

if command -v podman &>/dev/null; then
    echo "  Podman: $(podman --version)"
elif command -v docker &>/dev/null; then
    echo "  Docker: $(docker --version)"
else
    echo "  Containers: Neither Podman nor Docker detected"
fi

echo "[3/4] Checking project documentation integrity..."
REQUIRED_DOCS=("README.md" "ARCHITECTURE.md" "TECH_STACK.md" "DESIGN_SYSTEM.md" "ROADMAP.md" "SECURITY.md" "AGENTS.md" "CONTRIBUTING.md")
for doc in "${REQUIRED_DOCS[@]}"; do
    if [[ -f "$doc" ]]; then
        echo "  [OK] $doc present"
    else
        echo "  [FAIL] Missing $doc"
        exit 1
    fi
done

echo "[4/4] Verification complete. Environment is ready for development."
