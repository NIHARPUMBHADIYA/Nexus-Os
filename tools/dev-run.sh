#!/usr/bin/env bash
# NEXUS OS - Developer Run Script
# Launches standalone user-space components for rapid testing.

set -euo pipefail

echo "Starting NEXUS OS Standalone User-Space Suite..."

# 1. Start AI Core in background
echo "Starting nexus-aid daemon on :11430..."
cargo run --bin nexus-aid &
AID_PID=$!

echo "AI Core running (PID: $AID_PID). Press Ctrl+C to stop."

cleanup() {
    echo "Shutting down daemons..."
    kill "$AID_PID" 2>/dev/null || true
    echo "Stopped."
}

trap cleanup EXIT INT TERM
wait "$AID_PID"
