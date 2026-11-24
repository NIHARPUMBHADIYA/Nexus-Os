"""
NEXUS OS — Multi-Backend Software Installation Engine
Supports DNF (native RPM via Polkit/pkexec), Flatpak, Mise toolchains,
AppImages, and OCI Container backends.
Provides asynchronous progress tracking, cancellation, and secure execution.
"""

import os
import sys
import time
import shutil
import threading
import subprocess
from typing import Dict, Any, Optional, Callable, List
from .catalog_models import SoftwarePackage

class InstallTask:
    """Tracks an asynchronous installation or removal operation."""
    def __init__(self, task_id: str, package: SoftwarePackage, action: str = "install", version: Optional[str] = None):
        self.task_id = task_id
        self.package = package
        self.action = action  # "install", "uninstall", "update"
        self.version = version or package.version
        self.status = "queued"  # "queued", "downloading", "verifying", "installing", "completed", "failed", "cancelled"
        self.progress_percent = 0
        self.error_message = ""
        self.log_lines: List[str] = []
        self.cancelled = False
        self.started_at = time.time()
        self.finished_at: Optional[float] = None
        self._process: Optional[subprocess.Popen] = None

    def add_log(self, line: str):
        ts = time.strftime("%H:%M:%S")
        self.log_lines.append(f"[{ts}] {line.strip()}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "package_id": self.package.id,
            "package_name": self.package.name,
            "action": self.action,
            "version": self.version,
            "status": self.status,
            "progress_percent": self.progress_percent,
            "error_message": self.error_message,
            "logs": self.log_lines[-20:],
            "cancelled": self.cancelled
        }

class InstallEngine:
    """
    Coordinates multi-backend installation workflows with safety checks.
    """

    def __init__(self):
        self.tasks: Dict[str, InstallTask] = {}
        self._lock = threading.Lock()

    def submit_task(
        self,
        package: SoftwarePackage,
        action: str = "install",
        version: Optional[str] = None,
        dry_run: bool = False,
        on_complete: Optional[Callable[[InstallTask], None]] = None
    ) -> InstallTask:
        """Queue and launch an asynchronous install/uninstall operation."""
        task_id = f"task_{package.id}_{action}_{int(time.time() * 1000)}"
        task = InstallTask(task_id, package, action, version)

        with self._lock:
            self.tasks[task_id] = task

        thread = threading.Thread(
            target=self._run_task,
            args=(task, dry_run, on_complete),
            daemon=True
        )
        thread.start()
        return task

    def cancel_task(self, task_id: str) -> bool:
        """Cancel an in-progress installation task."""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task or task.status in ("completed", "failed", "cancelled"):
                return False

            task.cancelled = True
            task.status = "cancelled"
            task.add_log("Task cancellation requested by user.")

            if task._process:
                try:
                    task._process.terminate()
                except Exception:
                    pass
            return True

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            task = self.tasks.get(task_id)
            return task.to_dict() if task else None

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [t.to_dict() for t in self.tasks.values() if t.status in ("queued", "downloading", "verifying", "installing")]

    def _run_task(
        self,
        task: InstallTask,
        dry_run: bool = False,
        on_complete: Optional[Callable[[InstallTask], None]] = None
    ):
        """Worker executing backend installation logic."""
        pkg = task.package
        backend = pkg.backend

        task.status = "downloading"
        task.progress_percent = 15
        task.add_log(f"Initiating {task.action} for {pkg.name} ({pkg.id}) v{task.version} via {backend}...")

        if dry_run:
            # Deterministic simulation for verification tests & environments without root
            time.sleep(0.05)
            task.status = "verifying"
            task.progress_percent = 50
            task.add_log("Verifying package checksums, dependencies, and signature...")
            time.sleep(0.05)
            task.status = "installing"
            task.progress_percent = 85
            task.add_log(f"Applying payload to system via {backend} backend...")
            time.sleep(0.05)

            if task.cancelled:
                task.status = "cancelled"
                return

            task.status = "completed"
            task.progress_percent = 100
            task.finished_at = time.time()
            if task.action == "install":
                pkg.installed = True
                pkg.installed_version = task.version
            elif task.action == "uninstall":
                pkg.installed = False
                pkg.installed_version = None

            task.add_log(f"Successfully completed {task.action} of {pkg.name}.")
            if on_complete:
                on_complete(task)
            return

        # Real Execution Dispatch
        try:
            if backend == "dnf":
                self._execute_dnf(task)
            elif backend == "flatpak":
                self._execute_flatpak(task)
            elif backend == "mise":
                self._execute_mise(task)
            elif backend == "container":
                self._execute_container(task)
            elif backend == "appimage":
                self._execute_appimage(task)
            else:
                self._execute_generic(task)

            if task.cancelled:
                task.status = "cancelled"
                return

            # Verification of real binary presence
            if task.action == "install" and pkg.check_binary:
                if shutil.which(pkg.check_binary):
                    pkg.installed = True
                    pkg.installed_version = task.version
                    task.status = "completed"
                    task.progress_percent = 100
                    task.add_log(f"Installation verified: {pkg.check_binary} detected on system PATH.")
                else:
                    task.status = "failed"
                    task.error_message = f"Binary {pkg.check_binary} was not found on PATH after execution."
            else:
                task.status = "completed"
                task.progress_percent = 100
                if task.action == "uninstall":
                    pkg.installed = False

        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            task.add_log(f"Error executing installation: {e}")
        finally:
            task.finished_at = time.time()
            if on_complete:
                on_complete(task)

    def _execute_dnf(self, task: InstallTask):
        """Execute DNF via pkexec for Polkit authorization."""
        task.status = "installing"
        task.progress_percent = 40
        cmd = ["pkexec", "dnf"]
        if task.action == "install":
            cmd.extend(["install", "-y", task.package.package_ref])
        else:
            cmd.extend(["remove", "-y", task.package.package_ref])

        task.add_log(f"Dispatching authorization request: {' '.join(cmd)}")
        self._spawn_and_monitor(task, cmd)

    def _execute_flatpak(self, task: InstallTask):
        """Execute Flatpak in rootless user mode."""
        task.status = "downloading"
        task.progress_percent = 30
        cmd = ["flatpak"]
        if task.action == "install":
            cmd.extend(["install", "--user", "-y", "flathub", task.package.package_ref])
        else:
            cmd.extend(["uninstall", "--user", "-y", task.package.package_ref])

        task.add_log(f"Running user-space Flatpak: {' '.join(cmd)}")
        self._spawn_and_monitor(task, cmd)

    def _execute_mise(self, task: InstallTask):
        """Execute mise toolchain runtime installation."""
        task.status = "installing"
        task.progress_percent = 35
        ref = task.package.package_ref
        if task.action == "install":
            cmd = ["mise", "install", f"{ref}@{task.version}"]
        else:
            cmd = ["mise", "uninstall", f"{ref}@{task.version}"]

        task.add_log(f"Running mise: {' '.join(cmd)}")
        self._spawn_and_monitor(task, cmd)

    def _execute_container(self, task: InstallTask):
        """Execute Podman container pull."""
        task.status = "downloading"
        task.progress_percent = 25
        ref = task.package.package_ref
        if task.action == "install":
            cmd = ["podman", "pull", ref]
        else:
            cmd = ["podman", "rmi", ref]

        task.add_log(f"Running Podman rootless container pull: {' '.join(cmd)}")
        self._spawn_and_monitor(task, cmd)

    def _execute_appimage(self, task: InstallTask):
        """Download and install AppImage to ~/.local/bin."""
        task.status = "downloading"
        task.progress_percent = 30
        dest_dir = os.path.expanduser(os.path.join("~", ".local", "bin"))
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, task.package.id)

        if task.action == "uninstall":
            if os.path.exists(dest_file):
                os.remove(dest_file)
            task.status = "completed"
            task.progress_percent = 100
            return

        cmd = ["curl", "-fsSL", "-o", dest_file, task.package.homepage]
        task.add_log(f"Downloading AppImage: {task.package.homepage}")
        self._spawn_and_monitor(task, cmd)
        if os.path.exists(dest_file):
            os.chmod(dest_file, 0o755)

    def _execute_generic(self, task: InstallTask):
        cmd = task.package.install_args if task.action == "install" else task.package.uninstall_args
        self._spawn_and_monitor(task, cmd)

    def _spawn_and_monitor(self, task: InstallTask, cmd: List[str]):
        """Safe subprocess spawn with stdout/stderr streaming into log buffer."""
        task._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in iter(task._process.stdout.readline, ''):
            if task.cancelled:
                task._process.terminate()
                break
            line_str = line.strip()
            if line_str:
                task.add_log(line_str)
                task.progress_percent = min(95, task.progress_percent + 2)

        task._process.stdout.close()
        ret = task._process.wait()
        if ret != 0 and not task.cancelled:
            raise RuntimeError(f"Command '{' '.join(cmd)}' exited with return code {ret}")
