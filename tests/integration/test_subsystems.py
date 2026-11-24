#!/usr/bin/env python3
"""
NEXUS OS - Integration Test Suite
Verifies structure, documentation, and subsystem configurations.
"""

import os
import sys

REQUIRED_DOCUMENTS = [
    "README.md",
    "ARCHITECTURE.md",
    "TECH_STACK.md",
    "DESIGN_SYSTEM.md",
    "ROADMAP.md",
    "SECURITY.md",
    "AGENTS.md",
    "CONTRIBUTING.md"
]

REQUIRED_DIRECTORIES = [
    "docs/subsystems",
    "docs/specifications",
    "src/aicore",
    "src/spotlight",
    "src/devhub",
    "src/desktop",
    "src/settings",
    "packaging/bootc",
    "packaging/kickstart",
    "packaging/rpm",
    "packaging/flatpak",
    "tools"
]

def run_tests():
    print("Running NEXUS OS Architectural & Structure Verification Tests...")
    errors = 0

    # 1. Verify all required architecture documents exist and are non-empty
    for doc in REQUIRED_DOCUMENTS:
        if not os.path.isfile(doc):
            print(f"FAILED: Document missing: {doc}")
            errors += 1
        elif os.path.getsize(doc) < 200:
            print(f"FAILED: Document suspiciously small: {doc}")
            errors += 1
        else:
            print(f"PASSED: {doc}")

    # 2. Verify directories exist
    for directory in REQUIRED_DIRECTORIES:
        if not os.path.isdir(directory):
            print(f"FAILED: Directory missing: {directory}")
            errors += 1
        else:
            print(f"PASSED: Directory {directory}")

    # 3. Verify Cargo workspace exists
    if not os.path.isfile("Cargo.toml"):
        print("FAILED: Root Cargo.toml missing")
        errors += 1
    else:
        print("PASSED: Root Cargo.toml workspace file")

    if errors == 0:
        print("\nAll architectural and structure tests passed successfully (100%).")
        return 0
    else:
        print(f"\nCompleted with {errors} errors.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
