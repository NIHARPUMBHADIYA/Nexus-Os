"""
NEXUS OS — System Integration Facade (`system_integration.py`)
Provides the unified integration abstraction layer uniting all 20 Linux subsystem providers
and environment compatibility detection into a single point of entry.
"""

from typing import Dict, Any, List, Optional
from dataclasses import asdict

from .compatibility import CompatibilityDetector, CompatibilityReport, EnvironmentType, HardwareTier
from .providers import (
    SystemInfoProvider, DesktopEntriesProvider, AppLaunchProvider,
    FileSystemProvider, FSIndexProvider, FSWatcherProvider,
    PackageManagerProvider, FlatpakProvider, SystemdProvider,
    NetworkProvider, BluetoothProvider, AudioProvider,
    StorageProvider, GPUProvider, HardwareMonitorProvider,
    ProcessManagerProvider, TerminalIntegrationProvider,
    GitProvider, ContainerProvider, AIServicesProvider
)


class SystemIntegration:
    """
    Central abstraction facade for NEXUS OS Linux system integrations.
    Decouples UI and application code from direct command execution.
    """

    _instance: Optional["SystemIntegration"] = None

    @classmethod
    def get_instance(cls) -> "SystemIntegration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.detector = CompatibilityDetector()
        self.system_info = SystemInfoProvider()
        self.desktop_entries = DesktopEntriesProvider()
        self.app_launch = AppLaunchProvider()
        self.filesystem = FileSystemProvider()
        self.fs_index = FSIndexProvider()
        self.fs_watcher = FSWatcherProvider()
        self.package_mgr = PackageManagerProvider()
        self.flatpak = FlatpakProvider()
        self.systemd = SystemdProvider()
        self.network = NetworkProvider()
        self.bluetooth = BluetoothProvider()
        self.audio = AudioProvider()
        self.storage = StorageProvider()
        self.gpu = GPUProvider()
        self.hardware_monitor = HardwareMonitorProvider()
        self.process_mgr = ProcessManagerProvider()
        self.terminal = TerminalIntegrationProvider()
        self.git = GitProvider()
        self.container = ContainerProvider()
        self.ai_services = AIServicesProvider()

    # --- Compatibility & Environment ---

    def get_compatibility_report(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Returns the full environment detection and hardware tier report."""
        report = self.detector.detect(force_refresh=force_refresh)
        d = asdict(report)
        d["environment"] = report.environment.value
        d["hardware_tier"] = report.hardware_tier.value
        return d

    # --- 1. System Information ---
    def get_system_info(self) -> Dict[str, Any]:
        return self.system_info.get_system_info()

    # --- 2. Applications & Desktop Entries ---
    def get_applications(self) -> List[Dict[str, Any]]:
        return self.desktop_entries.get_applications()

    # --- 3. Application Launching ---
    def launch_application(self, command_or_exec: str, working_dir: Optional[str] = None) -> Dict[str, Any]:
        return self.app_launch.launch(command_or_exec, working_dir=working_dir)

    # --- 4. File System ---
    def get_xdg_directories(self) -> Dict[str, str]:
        return self.filesystem.get_xdg_directories()

    def list_directory(self, path: str, max_items: int = 200) -> Dict[str, Any]:
        return self.filesystem.list_directory(path, max_items=max_items)

    # --- 5. Filesystem Indexing ---
    def get_index_stats(self) -> Dict[str, Any]:
        return self.fs_index.get_index_stats()

    # --- 6. Filesystem Watchers ---
    def watch_directory(self, path: str) -> bool:
        return self.fs_watcher.watch_path(path)

    def get_watched_directories(self) -> List[str]:
        return self.fs_watcher.get_watched_paths()

    # --- 7. Package Management ---
    def get_package_management_status(self) -> Dict[str, Any]:
        return {
            "available": self.package_mgr.is_available(),
            "installed_rpm_count": self.package_mgr.get_installed_rpm_count(),
            "updates": self.package_mgr.check_updates()
        }

    # --- 8. Flatpak ---
    def get_flatpak_apps(self) -> List[Dict[str, Any]]:
        return self.flatpak.get_installed_apps()

    # --- 9. System Services ---
    def get_service_status(self, unit_name: str, user_unit: bool = True) -> Dict[str, Any]:
        return self.systemd.get_service_status(unit_name, user_unit=user_unit)

    # --- 10. Network Status ---
    def get_network_status(self) -> Dict[str, Any]:
        return self.network.get_network_status()

    # --- 11. Bluetooth ---
    def get_bluetooth_status(self) -> Dict[str, Any]:
        return self.bluetooth.get_bluetooth_status()

    # --- 12. Audio ---
    def get_audio_status(self) -> Dict[str, Any]:
        return self.audio.get_audio_status()

    # --- 13. Storage ---
    def get_storage_metrics(self) -> Dict[str, Any]:
        return self.storage.get_storage_metrics()

    # --- 14. GPU Detection ---
    def get_gpu_info(self) -> Dict[str, Any]:
        return self.gpu.get_gpu_info()

    # --- 15. CPU and RAM Monitoring ---
    def get_cpu_and_ram(self) -> Dict[str, Any]:
        return self.hardware_monitor.get_cpu_and_ram()

    # --- 16. Process Management ---
    def get_top_processes(self, limit: int = 15) -> List[Dict[str, Any]]:
        return self.process_mgr.get_top_processes(limit=limit)

    # --- 17. Terminal Integration ---
    def get_terminal_environment(self) -> Dict[str, Any]:
        return self.terminal.get_terminal_environment()

    # --- 18. Git ---
    def get_git_status(self, repo_path: str) -> Dict[str, Any]:
        return self.git.get_repo_status(repo_path)

    # --- 19. Containers ---
    def get_container_status(self) -> Dict[str, Any]:
        return self.container.get_container_status()

    # --- 20. AI Services ---
    def get_ai_services_status(self) -> Dict[str, Any]:
        return self.ai_services.get_ai_services_status()

    # --- Complete Snapshot ---
    def get_complete_system_snapshot(self) -> Dict[str, Any]:
        """Gathers an aggregated real-time diagnostic snapshot across all 20 integrations."""
        return {
            "compatibility": self.get_compatibility_report(),
            "system_info": self.get_system_info(),
            "cpu_and_ram": self.get_cpu_and_ram(),
            "gpu": self.get_gpu_info(),
            "storage": self.get_storage_metrics(),
            "network": self.get_network_status(),
            "bluetooth": self.get_bluetooth_status(),
            "audio": self.get_audio_status(),
            "packages": self.get_package_management_status(),
            "containers": self.get_container_status(),
            "terminal": self.get_terminal_environment(),
            "ai_services": self.get_ai_services_status(),
            "indexing": self.get_index_stats()
        }
