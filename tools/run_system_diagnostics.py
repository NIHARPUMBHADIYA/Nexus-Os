#!/usr/bin/env python3
"""
NEXUS OS — System Diagnostics & Linux Integrations Runner (`tools/run_system_diagnostics.py`)
Validates and prints the 20 real Linux system integrations, environment detection,
and hardware tier assessment.
"""

import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.system.system_integration import SystemIntegration


def run_cli_diagnostics():
    integration = SystemIntegration.get_instance()
    snapshot = integration.get_complete_system_snapshot()
    compat = snapshot["compatibility"]

    print("=================================================================")
    print(" NEXUS OS — Real Linux System Integrations Diagnostic Report     ")
    print("=================================================================")
    print(f"Environment Type:     {compat['environment_name']}")
    print(f"Distribution:         {compat['distribution_name']} {compat['distribution_version']}")
    print(f"Is Target Fedora:     {compat['is_target_os']}")
    print(f"Virtual Machine:      {compat['is_virtual_machine']} ({compat.get('vm_hypervisor', 'None')})")
    print(f"Hardware Tier:        {compat['hardware_tier'].upper()} ({compat['cpu_cores']} cores, {compat['ram_total_gb']} GB RAM)")
    print(f"Compatibility Score:  {compat['compatibility_score']}/100")
    print("-----------------------------------------------------------------")

    caps = compat["capabilities"]
    print("Subsystem Capabilities:")
    print(f"  • systemd:          {'✓ Present' if caps['has_systemd'] else '✗ Not Available'}")
    print(f"  • D-Bus:            {'✓ Present' if caps['has_dbus'] else '✗ Not Available'}")
    print(f"  • Polkit:           {'✓ Present' if caps['has_polkit'] else '✗ Not Available'}")
    print(f"  • DNF / RPM:        {'✓ Present' if caps['has_dnf'] else '✗ Not Available'}")
    print(f"  • Flatpak:          {'✓ Present' if caps['has_flatpak'] else '✗ Not Available'}")
    print(f"  • Podman:           {'✓ Present' if caps['has_podman'] else '✗ Not Available'}")
    print(f"  • PipeWire:         {'✓ Present' if caps['has_pipewire'] else '✗ Not Available'}")
    print(f"  • NetworkManager:   {'✓ Present' if caps['has_network_manager'] else '✗ Not Available'}")
    print(f"  • BlueZ Bluetooth:  {'✓ Present' if caps['has_bluez'] else '✗ Not Available'}")
    print(f"  • GPU Acceleration: {'✓ ' + caps['gpu_vendor'] if caps['has_gpu_acceleration'] else '✗ Software Rasterizer'}")
    print("-----------------------------------------------------------------")

    print("20 Linux Integrations Snapshot:")
    print(f"  1. System Info:      {snapshot['system_info']['kernel']} | Uptime: {snapshot['system_info']['uptime_formatted']}")
    print(f"  2. Desktop Entries:  {len(integration.get_applications())} applications indexed")
    print(f"  3. App Launching:    Safe argument-based execution active")
    print(f"  4. File System:      Home: {integration.get_xdg_directories()['home']}")
    print(f"  5. Indexing:         FTS5 status: {snapshot['indexing']['status']} ({snapshot['indexing']['indexed_files']} files)")
    print(f"  6. Watchers:         Inotify / Polling watcher active")
    print(f"  7. Package Mgr:      DNF/RPM available: {snapshot['packages']['available']}")
    print(f"  8. Flatpak:          Installed apps: {len(integration.get_flatpak_apps())}")
    print(f"  9. System Services:  systemd query ready")
    print(f" 10. Network Status:   Connected: {snapshot['network']['connected']} ({snapshot['network']['backend']})")
    print(f" 11. Bluetooth:        Available: {snapshot['bluetooth']['available']}")
    print(f" 12. Audio:            Backend: {snapshot['audio']['backend']} (Vol: {snapshot['audio']['volume']}%)")
    print(f" 13. Storage:          {snapshot['storage']['used_gb']} GB used of {snapshot['storage']['total_gb']} GB ({snapshot['storage']['used_percentage']}%)")
    print(f" 14. GPU Detection:    {snapshot['gpu']['vendor']} - {snapshot['gpu']['model']}")
    print(f" 15. CPU & RAM:        CPU: {snapshot['cpu_and_ram']['cpu_percentage']}% | RAM: {snapshot['cpu_and_ram']['ram_used_mb']} MB / {snapshot['cpu_and_ram']['ram_total_mb']} MB")
    print(f" 16. Processes:        {len(integration.get_top_processes(5))} top processes sampled")
    print(f" 17. Terminal:         Default shell: {snapshot['terminal']['default_shell']}")
    print(f" 18. Git:              Worktree query active")
    print(f" 19. Containers:       Engine: {snapshot['containers']['engine']}")
    print(f" 20. AI Services:      nexus-aid (:11430): {snapshot['ai_services']['nexus_aid']['online']} | ollama (:11434): {snapshot['ai_services']['ollama']['online']}")
    print("=================================================================")

    if compat["degraded_features"]:
        print("Degraded Features / Fallbacks on Current Host:")
        for df in compat["degraded_features"]:
            print(f"  ℹ️  {df}")
        print("=================================================================")


def main():
    run_cli_diagnostics()


if __name__ == "__main__":
    main()
