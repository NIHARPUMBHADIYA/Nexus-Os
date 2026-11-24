"""
NEXUS OS — System Environment & Compatibility Detector (`compatibility.py`)
Identifies OS distribution (Fedora, other Linux, Dev Environment, VM, Container),
evaluates hardware tiers, checks subsystem capabilities, and governs graceful degradation.
"""

import os
import sys
import shutil
import platform
import subprocess
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict


class EnvironmentType(str, Enum):
    FEDORA_NATIVE = "fedora_native"     # Primary target: Native Fedora Linux installation
    OTHER_LINUX = "other_linux"         # Another Linux distribution (Ubuntu, Arch, Debian, etc.)
    DEV_ENVIRONMENT = "dev_environment" # Development host (Windows/macOS prototyping host)
    VIRTUAL_MACHINE = "virtual_machine" # Running inside a hypervisor (QEMU, KVM, VirtualBox, VMware)
    CONTAINER = "container"             # Running inside Docker, Podman, or toolbox container


class HardwareTier(str, Enum):
    TIER_1_MINIMAL = "tier_1_minimal"       # < 4GB RAM or single-core CPU (degraded, light mode)
    TIER_2_STANDARD = "tier_2_standard"     # 4GB - 12GB RAM, multi-core CPU (standard desktop)
    TIER_3_PERFORMANCE = "tier_3_performance" # >= 16GB RAM, discrete GPU (full AI/Robotics workstation)


@dataclass
class SystemCapabilities:
    has_systemd: bool = False
    has_dbus: bool = False
    has_polkit: bool = False
    has_dnf: bool = False
    has_rpm: bool = False
    has_flatpak: bool = False
    has_podman: bool = False
    has_pipewire: bool = False
    has_network_manager: bool = False
    has_bluez: bool = False
    has_wayland: bool = False
    has_gpu_acceleration: bool = False
    gpu_vendor: str = "Unknown"
    is_64bit: bool = True


@dataclass
class CompatibilityReport:
    environment: EnvironmentType
    environment_name: str
    distribution_name: str
    distribution_version: str
    is_target_os: bool
    is_virtual_machine: bool
    vm_hypervisor: Optional[str]
    is_container: bool
    hardware_tier: HardwareTier
    cpu_cores: int
    ram_total_gb: float
    capabilities: SystemCapabilities
    degraded_features: List[str]
    compatibility_score: int  # 0 to 100


class CompatibilityDetector:
    """
    Detects the host execution environment, distribution flavor,
    virtualization layer, and hardware capabilities.
    """

    def __init__(self):
        self._cached_report: Optional[CompatibilityReport] = None

    def _check_binary(self, name: str) -> bool:
        """Safely checks if a binary exists on system PATH."""
        return shutil.which(name) is not None

    def _read_os_release(self) -> Dict[str, str]:
        """Reads /etc/os-release or /usr/lib/os-release if present."""
        data = {}
        for candidate in [Path("/etc/os-release"), Path("/usr/lib/os-release")]:
            if candidate.exists():
                try:
                    with open(candidate, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and "=" in line and not line.startswith("#"):
                                k, v = line.split("=", 1)
                                data[k.strip()] = v.strip().strip('"').strip("'")
                    return data
                except Exception:
                    pass
        return data

    def _detect_virtualization(self) -> Tuple[bool, Optional[str]]:
        """Detects if running inside a hypervisor or container."""
        # 1. Container checks
        if Path("/.dockerenv").exists() or Path("/run/.containerenv").exists():
            return True, "Container (Docker/Podman)"

        # 2. Check systemd-detect-virt on Linux
        if self._check_binary("systemd-detect-virt"):
            try:
                res = subprocess.run(
                    ["systemd-detect-virt"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=1.0
                )
                out = res.stdout.strip()
                if out and out != "none":
                    return True, out.upper()
            except Exception:
                pass

        # 3. DMI sysfs check on Linux
        dmi_sys = Path("/sys/class/dmi/id/product_name")
        if dmi_sys.exists():
            try:
                name = dmi_sys.read_text(encoding="utf-8").strip().lower()
                for vm_kw in ["qemu", "kvm", "virtualbox", "vmware", "hyper-v", "wsl"]:
                    if vm_kw in name:
                        return True, name.title()
            except Exception:
                pass

        # 4. Check on Windows host (Hyper-V / VirtualBox / VMware)
        if sys.platform == "win32":
            # Prototyping host is considered physical dev environment unless explicitly in VM
            pass

        return False, None

    def _get_ram_total_gb(self) -> float:
        """Returns total physical system RAM in GB."""
        # Linux /proc/meminfo
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            try:
                with open(meminfo, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            kb = int(line.split()[1])
                            return round(kb / (1024 ** 2), 1)
            except Exception:
                pass

        # Windows GlobalMemoryStatusEx fallback
        if sys.platform == "win32":
            try:
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                    return round(stat.ullTotalPhys / (1024 ** 3), 1)
            except Exception:
                pass

        return 8.0  # Safe default baseline

    def _detect_gpu(self) -> Tuple[bool, str]:
        """Detects presence of discrete/integrated GPU acceleration."""
        # 1. Check NVIDIA GPU via nvidia-smi
        if self._check_binary("nvidia-smi"):
            try:
                res = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=1.5
                )
                if res.returncode == 0 and res.stdout.strip():
                    return True, f"NVIDIA {res.stdout.strip().splitlines()[0]}"
            except Exception:
                pass

        # 2. Check Linux DRM nodes in /sys/class/drm
        drm_path = Path("/sys/class/drm")
        if drm_path.exists():
            try:
                render_nodes = [p for p in drm_path.glob("renderD*")]
                if render_nodes:
                    return True, "Linux DRM Hardware Acceleration"
            except Exception:
                pass

        # 3. Check Windows DirectX / WMI
        if sys.platform == "win32":
            try:
                res = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2.0
                )
                names = [n.strip() for n in res.stdout.splitlines() if n.strip()]
                if names:
                    return True, names[0]
            except Exception:
                pass

        return False, "Software Rasterizer (llvmpipe)"

    def detect(self, force_refresh: bool = False) -> CompatibilityReport:
        """
        Runs comprehensive environment and compatibility inspection.
        """
        if self._cached_report and not force_refresh:
            return self._cached_report

        os_rel = self._read_os_release()
        distro_id = os_rel.get("ID", "").lower()
        distro_like = os_rel.get("ID_LIKE", "").lower()
        distro_name = os_rel.get("NAME", platform.system())
        distro_version = os_rel.get("VERSION_ID", platform.release())

        is_vm, hypervisor = self._detect_virtualization()
        is_container = hypervisor is not None and "container" in hypervisor.lower()

        # Determine Environment Type
        if sys.platform != "linux":
            env_type = EnvironmentType.DEV_ENVIRONMENT
            env_name = f"Development Environment ({platform.system()} Host)"
        elif is_container:
            env_type = EnvironmentType.CONTAINER
            env_name = f"Containerized Environment ({hypervisor})"
        elif is_vm:
            env_type = EnvironmentType.VIRTUAL_MACHINE
            env_name = f"Virtual Machine ({hypervisor})"
        elif distro_id == "fedora" or "fedora" in distro_like or Path("/etc/fedora-release").exists():
            env_type = EnvironmentType.FEDORA_NATIVE
            env_name = "Fedora Linux Native (Official NEXUS OS Base)"
        else:
            env_type = EnvironmentType.OTHER_LINUX
            env_name = f"Generic Linux ({distro_name})"

        is_target_os = (distro_id == "fedora") or ("fedora" in distro_like)

        # Probe Capabilities
        has_gpu, gpu_name = self._detect_gpu()
        caps = SystemCapabilities(
            has_systemd=self._check_binary("systemctl") or Path("/run/systemd/system").exists(),
            has_dbus=self._check_binary("dbus-send") or "DBUS_SESSION_BUS_ADDRESS" in os.environ,
            has_polkit=self._check_binary("pkexec"),
            has_dnf=self._check_binary("dnf") or self._check_binary("dnf5"),
            has_rpm=self._check_binary("rpm"),
            has_flatpak=self._check_binary("flatpak"),
            has_podman=self._check_binary("podman"),
            has_pipewire=self._check_binary("wpctl") or self._check_binary("pipewire"),
            has_network_manager=self._check_binary("nmcli"),
            has_bluez=self._check_binary("bluetoothctl"),
            has_wayland="WAYLAND_DISPLAY" in os.environ or "XDG_SESSION_TYPE" in os.environ and os.environ["XDG_SESSION_TYPE"] == "wayland",
            has_gpu_acceleration=has_gpu,
            gpu_vendor=gpu_name,
            is_64bit=platform.machine() in ("x86_64", "AMD64", "arm64", "aarch64")
        )

        # Hardware Tiering
        cpu_cores = os.cpu_count() or 4
        ram_gb = self._get_ram_total_gb()

        if ram_gb < 4.0 or cpu_cores < 2:
            tier = HardwareTier.TIER_1_MINIMAL
        elif ram_gb < 14.0:
            tier = HardwareTier.TIER_2_STANDARD
        else:
            tier = HardwareTier.TIER_3_PERFORMANCE

        # Graceful degradation assessment
        degraded = []
        score = 100

        if not is_target_os and env_type != EnvironmentType.DEV_ENVIRONMENT:
            degraded.append("Native Fedora DNF package hooks degraded to Flatpak/Container fallback.")
            score -= 15

        if not caps.has_systemd:
            degraded.append("systemd service manager unavailable; daemons run in user-process supervision mode.")
            score -= 10

        if not caps.has_polkit:
            degraded.append("Polkit privilege separation unavailable; administrative operations require manual elevation.")
            score -= 10

        if not caps.has_pipewire:
            degraded.append("PipeWire low-latency server unavailable; fallback audio backend active.")
            score -= 5

        if not caps.has_network_manager:
            degraded.append("NetworkManager unavailable; network status queries fall back to socket inspection.")
            score -= 5

        if not caps.has_gpu_acceleration:
            degraded.append("Hardware GPU acceleration not detected; compositor blur & 3D simulators use software rasterization.")
            score -= 15

        if tier == HardwareTier.TIER_1_MINIMAL:
            degraded.append("Low RAM detected (< 4GB); heavy AI models and Android emulator disabled.")
            score -= 20

        score = max(20, min(100, score))

        report = CompatibilityReport(
            environment=env_type,
            environment_name=env_name,
            distribution_name=distro_name,
            distribution_version=str(distro_version),
            is_target_os=is_target_os,
            is_virtual_machine=is_vm,
            vm_hypervisor=hypervisor,
            is_container=is_container,
            hardware_tier=tier,
            cpu_cores=cpu_cores,
            ram_total_gb=ram_gb,
            capabilities=caps,
            degraded_features=degraded,
            compatibility_score=score
        )
        self._cached_report = report
        return report
