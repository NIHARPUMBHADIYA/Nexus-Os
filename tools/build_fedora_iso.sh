#!/usr/bin/env bash
# =============================================================================
# NEXUS OS — Official Fedora 41 Live Workstation ISO Build Script
# Builds a 100% pure Fedora 41-based bootable ISO with Aether Desktop Shell.
# Requirements: Linux environment (Fedora, RHEL, CentOS, or WSL2 / Docker).
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
KICKSTART_FILE="${PROJECT_ROOT}/packaging/kickstart/nexus-live-workstation.ks"
OUTPUT_ISO="${BUILD_DIR}/nexus-os-2026.1-x86_64.iso"

echo "================================================================="
echo " NEXUS OS 2026.1 — Official Fedora Live ISO Builder               "
echo " Target Base: Fedora 41 x86_64 Everything                       "
echo " Desktop:     Aether Wayland Desktop (KDE / Qt6 / QML)          "
echo "================================================================="

mkdir -p "${BUILD_DIR}"

# Check for build tools
if command -v livecd-creator >/dev/null 2>&1; then
    echo "[*] Using livecd-creator (Fedora LiveCD Tools)..."
    sudo livecd-creator \
        --config="${KICKSTART_FILE}" \
        --fslabel="NEXUS_OS_2026_1" \
        --cache="${BUILD_DIR}/cache" \
        --tmpdir="${BUILD_DIR}/tmp"

    # Move generated ISO to standard target path
    GENERATED_ISO=$(ls -t *.iso 2>/dev/null | head -n1 || true)
    if [ -n "${GENERATED_ISO}" ]; then
        mv "${GENERATED_ISO}" "${OUTPUT_ISO}"
        sha256sum "${OUTPUT_ISO}" > "${OUTPUT_ISO}.sha256"
        echo "[+] Successfully built: ${OUTPUT_ISO}"
    fi

elif command -v podman >/dev/null 2>&1 || command -v docker >/dev/null 2>&1; then
    CONTAINER_ENGINE=$(command -v podman || command -v docker)
    echo "[*] Using container-based image builder (${CONTAINER_ENGINE})..."
    
    # Build bootc container image
    ${CONTAINER_ENGINE} build \
        -t "nexus-os:2026.1" \
        -f "${PROJECT_ROOT}/packaging/bootc/Containerfile" \
        "${PROJECT_ROOT}"

    # Use bootc-image-builder to generate bootable ISO
    ${CONTAINER_ENGINE} run \
        --rm \
        --privileged \
        -v "${BUILD_DIR}:/output" \
        -v /var/lib/containers/storage:/var/lib/containers/storage \
        quay.io/centos-bootc/bootc-image-builder:latest \
        --type iso \
        --rootfs btrfs \
        "nexus-os:2026.1"

    echo "[+] Bootable ISO built in: ${BUILD_DIR}/bootiso/install.iso"
    if [ -f "${BUILD_DIR}/bootiso/install.iso" ]; then
        cp "${BUILD_DIR}/bootiso/install.iso" "${OUTPUT_ISO}"
        sha256sum "${OUTPUT_ISO}" > "${OUTPUT_ISO}.sha256"
        echo "[+] Final ISO ready: ${OUTPUT_ISO}"
    fi
else
    echo "[-] Error: Neither livecd-creator nor podman/docker found."
    echo "    To build on Fedora: sudo dnf install -y livecd-tools"
    echo "    To build with containers: sudo dnf install -y podman"
    exit 1
fi

echo "================================================================="
echo " Build Complete: $(ls -lh "${OUTPUT_ISO}")"
echo "================================================================="
