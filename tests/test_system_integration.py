"""
NEXUS OS — Linux System Integration Test Suite (`tests/test_system_integration.py`)
Verifies:
1. Environment and compatibility detection (Fedora, other Linux, Dev Host, VM, Container).
2. Hardware tier classification and capability flags.
3. All 20 subsystem providers:
   1. System information
   2. Desktop entries
   3. Application launching (safety sanitization & execution)
   4. File system (XDG dirs, safe directory listing)
   5. Filesystem indexing
   6. Filesystem watchers
   7. Package management (DNF/RPM)
   8. Flatpak
   9. System services (systemd)
   10. Network status
   11. Bluetooth
   12. Audio (PipeWire/PulseAudio)
   13. Storage
   14. GPU detection
   15. CPU and RAM monitoring
   16. Process management
   17. Terminal integration
   18. Git repository status
   19. Containers (Podman/Docker)
   20. AI services health monitoring
4. Unified SystemIntegration snapshot generation.
"""

import os
import sys
import time
import shutil
import tempfile
import unittest

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.system.compatibility import CompatibilityDetector, EnvironmentType, HardwareTier
from src.system.system_integration import SystemIntegration


class TestSystemIntegration(unittest.TestCase):

    def setUp(self):
        self.integration = SystemIntegration.get_instance()
        self.detector = CompatibilityDetector()

    def test_environment_and_compatibility_detection(self):
        """Verify environment classification, hardware tiering, and capability flags."""
        report = self.detector.detect(force_refresh=True)
        self.assertIn(report.environment, [
            EnvironmentType.FEDORA_NATIVE,
            EnvironmentType.OTHER_LINUX,
            EnvironmentType.DEV_ENVIRONMENT,
            EnvironmentType.VIRTUAL_MACHINE,
            EnvironmentType.CONTAINER
        ])
        self.assertIn(report.hardware_tier, [
            HardwareTier.TIER_1_MINIMAL,
            HardwareTier.TIER_2_STANDARD,
            HardwareTier.TIER_3_PERFORMANCE
        ])
        self.assertGreater(report.cpu_cores, 0)
        self.assertGreater(report.ram_total_gb, 0.0)
        self.assertGreaterEqual(report.compatibility_score, 20)
        self.assertLessEqual(report.compatibility_score, 100)

    def test_01_system_info(self):
        """Verify system info returns kernel, architecture, hostname, and uptime."""
        info = self.integration.get_system_info()
        self.assertEqual(info["os_name"], "NEXUS OS")
        self.assertTrue(info["kernel"])
        self.assertTrue(info["architecture"])
        self.assertTrue(info["hostname"])
        self.assertGreaterEqual(info["uptime_seconds"], 0.0)
        self.assertTrue(info["uptime_formatted"])

    def test_02_desktop_entries(self):
        """Verify desktop entries parsing and fallback applications."""
        apps = self.integration.get_applications()
        self.assertGreater(len(apps), 0)
        first_app = apps[0]
        self.assertIn("id", first_app)
        self.assertIn("name", first_app)
        self.assertIn("exec", first_app)

    def test_03_app_launch_safety(self):
        """Verify application launcher rejects empty commands and unsanitized non-existent bins."""
        # Empty command
        res_empty = self.integration.launch_application("")
        self.assertFalse(res_empty["success"])

        # Non-existent command
        res_missing = self.integration.launch_application("non_existent_nexus_fake_binary_12345 %u")
        self.assertFalse(res_missing["success"])
        self.assertIn("not found", res_missing["error"])

        # Valid safe command (e.g. python)
        res_valid = self.integration.launch_application(f'"{sys.executable}" --version')
        self.assertTrue(res_valid["success"])
        self.assertGreater(res_valid["pid"], 0)
        time.sleep(0.1)

    def test_04_file_system(self):
        """Verify XDG directory paths and safe directory listing."""
        xdg = self.integration.get_xdg_directories()
        self.assertTrue(os.path.isdir(xdg["home"]))
        self.assertIn("documents", xdg)
        self.assertIn("projects", xdg)

        # List home directory
        res_list = self.integration.list_directory(xdg["home"], max_items=10)
        self.assertTrue(res_list["success"])
        self.assertGreater(len(res_list["entries"]), 0)

        # Non-existent path
        res_err = self.integration.list_directory("/non_existent_nexus_fake_path_xyz")
        self.assertFalse(res_err["success"])

    def test_05_fs_index_and_06_watchers(self):
        """Verify index statistics and directory watcher registration."""
        stats = self.integration.get_index_stats()
        self.assertIn("status", stats)
        self.assertIn("indexed_files", stats)

        # Watcher
        watched = self.integration.watch_directory(base_dir)
        self.assertTrue(watched)
        self.assertIn(str(os.path.abspath(base_dir)), self.integration.get_watched_directories())

    def test_07_package_mgr_and_08_flatpak(self):
        """Verify DNF package manager status and Flatpak query."""
        pkg = self.integration.get_package_management_status()
        self.assertIn("available", pkg)
        self.assertIn("installed_rpm_count", pkg)

        flatpaks = self.integration.get_flatpak_apps()
        self.assertIsInstance(flatpaks, list)

    def test_09_systemd_services(self):
        """Verify systemd service queries handle units gracefully."""
        status = self.integration.get_service_status("nexus-aid.service")
        self.assertIn("unit", status)
        self.assertIn("status", status)

    def test_10_network_and_11_bluetooth(self):
        """Verify network connectivity and Bluetooth status."""
        net = self.integration.get_network_status()
        self.assertIn("connected", net)
        self.assertIn("backend", net)

        bt = self.integration.get_bluetooth_status()
        self.assertIn("available", bt)

    def test_12_audio_and_13_storage(self):
        """Verify audio volume status and storage metrics."""
        audio = self.integration.get_audio_status()
        self.assertIn("volume", audio)
        self.assertIn("backend", audio)

        storage = self.integration.get_storage_metrics()
        self.assertGreater(storage["total_gb"], 0.0)
        self.assertGreaterEqual(storage["used_gb"], 0.0)
        self.assertGreaterEqual(storage["used_percentage"], 0.0)

    def test_14_gpu_and_15_cpu_ram(self):
        """Verify hardware GPU detection and CPU/RAM load metrics."""
        gpu = self.integration.get_gpu_info()
        self.assertIn("vendor", gpu)
        self.assertIn("model", gpu)

        cpu_ram = self.integration.get_cpu_and_ram()
        self.assertGreater(cpu_ram["cpu_cores"], 0)
        self.assertGreater(cpu_ram["cpu_percentage"], 0.0)
        self.assertGreater(cpu_ram["ram_total_mb"], 0)
        self.assertGreater(cpu_ram["ram_percentage"], 0.0)

    def test_16_processes_and_17_terminal(self):
        """Verify process list sampling and terminal environment."""
        procs = self.integration.get_top_processes(limit=5)
        self.assertIsInstance(procs, list)

        term = self.integration.get_terminal_environment()
        self.assertTrue(term["default_shell"])
        self.assertTrue(term["terminal_emulator"])

    def test_18_git_repo_status(self):
        """Verify Git repository status for git and non-git directories."""
        # Non-git directory check
        tmp_non_git = tempfile.mkdtemp(prefix="nexus_nongit_")
        try:
            non_git = self.integration.get_git_status(tmp_non_git)
            self.assertFalse(non_git.get("is_git", False))
        finally:
            shutil.rmtree(tmp_non_git, ignore_errors=True)

        # Create temporary git repo to test git inspection
        git_bin = shutil.which("git")
        if git_bin:
            tmp_git = tempfile.mkdtemp(prefix="nexus_git_test_")
            try:
                import subprocess
                subprocess.run([git_bin, "-C", tmp_git, "init"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                git_status = self.integration.get_git_status(tmp_git)
                self.assertTrue(git_status.get("is_git", False))
                self.assertTrue(git_status.get("branch"))
            finally:
                shutil.rmtree(tmp_git, ignore_errors=True)

    def test_19_containers_and_20_ai_services(self):
        """Verify container status and AI services loopback probes."""
        containers = self.integration.get_container_status()
        self.assertIn("available", containers)
        self.assertIn("engine", containers)

        ai = self.integration.get_ai_services_status()
        self.assertIn("nexus_aid", ai)
        self.assertIn("omniroute", ai)
        self.assertIn("ollama", ai)
        self.assertEqual(ai["nexus_aid"]["port"], 11430)
        self.assertEqual(ai["omniroute"]["port"], 20128)
        self.assertEqual(ai["ollama"]["port"], 11434)

    def test_complete_snapshot(self):
        """Verify complete system snapshot gathers all 20 integrations."""
        snapshot = self.integration.get_complete_system_snapshot()
        self.assertIn("compatibility", snapshot)
        self.assertIn("system_info", snapshot)
        self.assertIn("cpu_and_ram", snapshot)
        self.assertIn("gpu", snapshot)
        self.assertIn("storage", snapshot)
        self.assertIn("network", snapshot)
        self.assertIn("bluetooth", snapshot)
        self.assertIn("audio", snapshot)
        self.assertIn("packages", snapshot)
        self.assertIn("containers", snapshot)
        self.assertIn("terminal", snapshot)
        self.assertIn("ai_services", snapshot)
        self.assertIn("indexing", snapshot)


if __name__ == "__main__":
    unittest.main()
