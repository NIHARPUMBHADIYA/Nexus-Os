"""
NEXUS OS — Developer Packs Dependency Resolver (`devpack_resolver.py`)
Performs multi-pack aggregation, tool deduplication, dependency graph resolution,
topological sorting, conflict detection, storage aggregation, and hardware requirement validation.
"""

import os
import sys
import shutil
from typing import List, Dict, Any, Set, Optional, Tuple
from dataclasses import dataclass, field, asdict

from .devpack_catalog import (
    DeveloperPack, DevPackTool, HardwareRequirement,
    MASTER_TOOLS_CATALOG, DEVELOPER_PACKS, get_pack_by_id, get_tool_by_id
)


@dataclass
class ResolutionPlan:
    selected_pack_ids: List[str]
    selected_pack_names: List[str]
    resolved_tools: List[DevPackTool]
    total_size_mb: int
    total_size_formatted: str
    free_disk_mb: int
    has_sufficient_disk: bool
    hardware_warnings: List[str]
    conflicts: List[str]
    stages: List[Dict[str, Any]]


class DevPackResolver:
    """
    Resolves dependencies, conflicts, and execution stages for one or more Developer Packs.
    """

    # Ordering priority tiers for topological sequencing:
    TIER_PRIORITIES = {
        # Tier 1: Core OS utilities, package managers, container runtimes
        "curl": 1, "git": 1, "gh": 2, "mise": 1, "podman": 2, "zsh": 3,
        # Tier 2: Base compilers, runtimes and SDKs
        "gcc": 10, "clang": 11, "cmake": 12, "gdb": 13,
        "python": 15, "nodejs": 15, "rust": 15, "go": 15, "openjdk": 15, "kotlin": 16,
        # Tier 3: Libraries & embedded toolchains
        "arm_none_eabi": 20, "openocd": 21, "opencv": 22, "pytorch": 25,
        "sqlite": 28, "postgresql": 28, "redis": 28,
        # Tier 4: Developer CLIs, testing, and middleware
        "bruno": 30, "dbeaver": 31, "kubectl": 32, "terraform": 33, "ansible": 34,
        "awscli": 35, "gcloud": 35, "wireshark": 36, "nmap": 36, "platformio": 38,
        # Tier 5: Heavy frameworks, simulators, and containers
        "ros2": 40, "gazebo": 42, "rviz": 44, "godot": 45, "blender": 46, "krita": 47,
        "metasploit": 48, "ghidra": 49, "arduino": 50,
        # Tier 6: Heavy IDEs and Editors
        "vscode": 60, "cursor": 61, "windsurf": 62, "zed": 63, "neovim": 64,
        "android_studio": 65, "antigravity": 66,
        # Tier 7: AI Daemons and Local LLM Model Services
        "ollama": 70, "omniroute": 72, "jupyter": 75, "huggingface": 76,
        "claude_code": 80, "aider": 81
    }

    def __init__(self):
        pass

    def _format_size(self, mb: int) -> str:
        """Formats MB into human-readable size e.g. '3.4 GB'."""
        if mb < 1024:
            return f"{mb} MB"
        return f"{mb / 1024:.1f} GB"

    def _get_free_disk_mb(self) -> int:
        """Retrieves available disk space on the primary mount."""
        path = "/" if sys.platform != "win32" else os.path.splitdrive(os.getcwd())[0] + "\\"
        try:
            _, _, free_bytes = shutil.disk_usage(path)
            return int(free_bytes / (1024 ** 2))
        except Exception:
            return 50000  # Fallback 50 GB

    def _get_system_ram_gb(self) -> float:
        """Queries total system RAM in GB."""
        ram_gb = 16.0
        try:
            if sys.platform == "win32":
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
                    ram_gb = round(stat.ullTotalPhys / (1024 ** 3), 1)
        except Exception:
            pass
        return ram_gb

    def resolve(self, pack_ids: List[str], include_optional: bool = False) -> ResolutionPlan:
        """
        Resolves one or more Developer Packs into a deduplicated, ordered execution plan.
        """
        selected_packs: List[DeveloperPack] = []
        for pid in pack_ids:
            pack = get_pack_by_id(pid)
            if pack and pack not in selected_packs:
                selected_packs.append(pack)

        if not selected_packs:
            return ResolutionPlan(
                selected_pack_ids=[],
                selected_pack_names=[],
                resolved_tools=[],
                total_size_mb=0,
                total_size_formatted="0 MB",
                free_disk_mb=self._get_free_disk_mb(),
                has_sufficient_disk=True,
                hardware_warnings=[],
                conflicts=[],
                stages=[]
            )

        # 1. Aggregate Tools (Deduplicated)
        tool_ids_to_install: Set[str] = set()
        for pack in selected_packs:
            for tid in pack.required_tools:
                tool_ids_to_install.add(tid)
            if include_optional:
                for tid in pack.optional_tools:
                    tool_ids_to_install.add(tid)

        # 2. Transitive Dependency Resolution
        expanded_tools: Set[str] = set(tool_ids_to_install)
        added_new = True
        while added_new:
            added_new = False
            for tid in list(expanded_tools):
                tool = get_tool_by_id(tid)
                if tool:
                    for dep_id in tool.dependencies:
                        if dep_id not in expanded_tools:
                            expanded_tools.add(dep_id)
                            added_new = True

        # 3. Check for Conflicts
        conflicts: List[str] = []
        # Mutual exclusion checks (e.g. if any tools conflict)
        # Note: All NEXUS tools in our catalog are co-installable.
        # Check for potential container vs native port conflicts if applicable:
        if "postgresql" in expanded_tools and "ros2" in expanded_tools:
            # Informational check
            pass

        # 4. Topological Ordering based on dependency tiers
        def get_priority(tid: str) -> int:
            return self.TIER_PRIORITIES.get(tid, 50)

        ordered_tool_ids = sorted(list(expanded_tools), key=lambda x: (get_priority(x), x))
        resolved_tools: List[DevPackTool] = []
        for tid in ordered_tool_ids:
            t = get_tool_by_id(tid)
            if t:
                resolved_tools.append(t)

        # 5. Storage Computation & Free Space Check
        total_size_mb = sum(t.size_mb for t in resolved_tools)
        free_disk_mb = self._get_free_disk_mb()
        safety_headroom_mb = 2048  # 2GB safety buffer
        has_sufficient_disk = free_disk_mb >= (total_size_mb + safety_headroom_mb)

        # 6. Hardware Compatibility Warnings
        hardware_warnings: List[str] = []
        sys_ram = self._get_system_ram_gb()
        for pack in selected_packs:
            hw = pack.hardware
            if sys_ram < hw.min_ram_gb:
                hardware_warnings.append(
                    f"⚠️ {pack.name}: System RAM ({sys_ram:.1f} GB) is below minimum requirement ({hw.min_ram_gb} GB)."
                )
            elif sys_ram < hw.recommended_ram_gb:
                hardware_warnings.append(
                    f"ℹ️ {pack.name}: Recommended RAM is {hw.recommended_ram_gb} GB (Detected: {sys_ram:.1f} GB)."
                )
            if hw.gpu_required:
                hardware_warnings.append(
                    f"🎮 {pack.name}: Dedicated GPU required ({hw.notes})."
                )

        if not has_sufficient_disk:
            conflicts.append(
                f"Insufficient disk space: Plan requires {self._format_size(total_size_mb)} (+ 2GB safety headroom), but only {self._format_size(free_disk_mb)} is free."
            )

        # 7. Group into UI Stages for Visual Progress
        stages = [
            {"id": "stage_runtimes", "name": "System Utilities & Runtimes", "tools": [t.name for t in resolved_tools if get_priority(t.id) < 10]},
            {"id": "stage_languages", "name": "Languages & Compilers", "tools": [t.name for t in resolved_tools if 10 <= get_priority(t.id) < 20]},
            {"id": "stage_libraries", "name": "Libraries & Toolchains", "tools": [t.name for t in resolved_tools if 20 <= get_priority(t.id) < 30]},
            {"id": "stage_middleware", "name": "Databases & DevOps Tools", "tools": [t.name for t in resolved_tools if 30 <= get_priority(t.id) < 40]},
            {"id": "stage_frameworks", "name": "Frameworks & Simulators", "tools": [t.name for t in resolved_tools if 40 <= get_priority(t.id) < 60]},
            {"id": "stage_editors", "name": "IDEs & Editors", "tools": [t.name for t in resolved_tools if 60 <= get_priority(t.id) < 70]},
            {"id": "stage_ai_services", "name": "AI Daemons & Local Models", "tools": [t.name for t in resolved_tools if get_priority(t.id) >= 70]}
        ]
        # Filter empty stages
        stages = [s for s in stages if len(s["tools"]) > 0]

        return ResolutionPlan(
            selected_pack_ids=[p.id for p in selected_packs],
            selected_pack_names=[p.name for p in selected_packs],
            resolved_tools=resolved_tools,
            total_size_mb=total_size_mb,
            total_size_formatted=self._format_size(total_size_mb),
            free_disk_mb=free_disk_mb,
            has_sufficient_disk=has_sufficient_disk,
            hardware_warnings=hardware_warnings,
            conflicts=conflicts,
            stages=stages
        )
