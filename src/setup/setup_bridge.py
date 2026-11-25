#!/usr/bin/env python3
"""
NEXUS OS — First-Boot Setup & Local Account Creation Bridge (PyQt6)
Handles user validation, account creation, privilege assignment,
and SDDM autologin configuration.
"""

import os
import re
import subprocess
import sys
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class SetupBridge(QObject):
    isConfiguredChanged = pyqtSignal()
    errorMessageChanged = pyqtSignal()
    isLoadingChanged = pyqtSignal()
    setupCompleted = pyqtSignal(str)  # returns created username

    def __init__(self, parent=None):
        super().__init__(parent)
        self._error_message = ""
        self._is_loading = False
        self._marker_file = "/var/lib/nexus/setup_done"
        self._legacy_marker = "/etc/nexus/user_configured"

    @pyqtProperty(bool, notify=isConfiguredChanged)
    def isConfigured(self) -> bool:
        return os.path.exists(self._marker_file) or os.path.exists(self._legacy_marker)

    @pyqtProperty(str, notify=errorMessageChanged)
    def errorMessage(self) -> str:
        return self._error_message

    @pyqtProperty(bool, notify=isLoadingChanged)
    def isLoading(self) -> bool:
        return self._is_loading

    def set_error(self, msg: str):
        self._error_message = msg
        self.errorMessageChanged.emit()

    def set_loading(self, loading: bool):
        self._is_loading = loading
        self.isLoadingChanged.emit()

    @pyqtSlot(str, str, str, str, bool, bool, result=bool)
    def createAccount(
        self,
        full_name: str,
        username: str,
        password: str,
        confirm_password: str,
        is_admin: bool,
        auto_login: bool,
    ) -> bool:
        self.set_error("")
        self.set_loading(True)

        full_name = full_name.strip()
        username = username.strip().lower()

        # 1. Validation checks
        if not full_name:
            self.set_error("Please enter your full name.")
            self.set_loading(False)
            return False

        if not username:
            self.set_error("Please enter a username.")
            self.set_loading(False)
            return False

        if not re.match(r"^[a-z_][a-z0-9_-]{1,31}$", username):
            self.set_error(
                "Username must start with a letter and contain only lowercase letters, digits, or dashes (2-32 chars)."
            )
            self.set_loading(False)
            return False

        if not password:
            self.set_error("Please enter a password.")
            self.set_loading(False)
            return False

        if password != confirm_password:
            self.set_error("Passwords do not match. Please re-type your password.")
            self.set_loading(False)
            return False

        if len(password) < 4:
            self.set_error("Password must be at least 4 characters long.")
            self.set_loading(False)
            return False

        # 2. System Execution (Linux Production Environment)
        is_linux = sys.platform.startswith("linux")

        if is_linux:
            try:
                # Check if user already exists
                user_check = subprocess.run(
                    ["id", "-u", username],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                user_exists = user_check.returncode == 0

                if not user_exists:
                    # Create user account
                    cmd = [
                        "useradd",
                        "-m",
                        "-c",
                        full_name,
                        "-s",
                        "/bin/bash",
                    ]
                    if is_admin:
                        cmd.extend(["-G", "wheel"])
                    cmd.append(username)

                    proc = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    if proc.returncode != 0:
                        self.set_error(f"Failed to create user: {proc.stderr.strip()}")
                        self.set_loading(False)
                        return False
                else:
                    # Update comment/gecos
                    subprocess.run(
                        ["usermod", "-c", full_name, username],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    if is_admin:
                        subprocess.run(
                            ["usermod", "-aG", "wheel", username],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )

                # Set password
                chpasswd_proc = subprocess.run(
                    ["chpasswd"],
                    input=f"{username}:{password}\n",
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if chpasswd_proc.returncode != 0:
                    self.set_error(f"Failed to set password: {chpasswd_proc.stderr.strip()}")
                    self.set_loading(False)
                    return False

                # Configure sudoers if admin
                if is_admin:
                    sudoers_dir = "/etc/sudoers.d"
                    os.makedirs(sudoers_dir, exist_ok=True)
                    sudoers_path = os.path.join(sudoers_dir, username)
                    with open(sudoers_path, "w") as f:
                        f.write(f"{username} ALL=(ALL) NOPASSWD: ALL\n")
                    os.chmod(sudoers_path, 0o440)

                # Configure SDDM autologin if requested
                if auto_login:
                    sddm_dir = "/etc/sddm.conf.d"
                    os.makedirs(sddm_dir, exist_ok=True)
                    conf_path = os.path.join(sddm_dir, "nexus_theme.conf")
                    conf_content = (
                        "[Theme]\n"
                        "Current=breeze\n\n"
                        "[General]\n"
                        "InputMethod=\n"
                        "Numlock=none\n"
                        "DisplayServer=wayland\n\n"
                        "[Autologin]\n"
                        f"User={username}\n"
                        "Session=plasma\n"
                        "Relogin=false\n"
                    )
                    with open(conf_path, "w") as f:
                        f.write(conf_content)

                # Mark setup as completed
                os.makedirs(os.path.dirname(self._marker_file), exist_ok=True)
                with open(self._marker_file, "w") as f:
                    f.write(f"configured_user={username}\nfull_name={full_name}\n")

                os.makedirs("/etc/nexus", exist_ok=True)
                with open(self._legacy_marker, "w") as f:
                    f.write(f'{{"user": "{username}", "full_name": "{full_name}"}}\n')

            except Exception as e:
                self.set_error(f"Unexpected error creating account: {str(e)}")
                self.set_loading(False)
                return False
        else:
            # Development / Mock environment (e.g. Windows)
            print(f"[MOCK SETUP] Created user: {username} ({full_name}), Admin: {is_admin}, Autologin: {auto_login}")
            os.makedirs("build", exist_ok=True)
            with open("build/mock_setup_done.txt", "w") as f:
                f.write(f"user={username}\nname={full_name}\n")

        self.set_loading(False)
        self.setupCompleted.emit(username)
        return True
