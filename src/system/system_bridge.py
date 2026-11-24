"""
NEXUS OS — System Integration PyQt6 Bridge (`system_bridge.py`)
Exposes reactive hardware monitoring, environment compatibility, real process inspection,
and safe application launching to QML.
"""

from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from .system_integration import SystemIntegration


class SystemBridge(QObject):
    """
    Reactive PyQt6 Bridge connecting the Linux Integration Layer to QML.
    """

    compatibilityChanged = pyqtSignal()
    systemInfoChanged = pyqtSignal()
    hardwareMetricsChanged = pyqtSignal()
    storageChanged = pyqtSignal()
    networkChanged = pyqtSignal()
    bluetoothChanged = pyqtSignal()
    audioChanged = pyqtSignal()
    processesChanged = pyqtSignal()
    containersChanged = pyqtSignal()
    aiServicesChanged = pyqtSignal()

    def __init__(self, integration: Optional[SystemIntegration] = None, parent=None):
        super().__init__(parent)
        self._integration = integration or SystemIntegration.get_instance()
        self._compat_data = self._integration.get_compatibility_report()
        self._sys_info = self._integration.get_system_info()
        self._hw_metrics = self._integration.get_cpu_and_ram()
        self._gpu_info = self._integration.get_gpu_info()
        self._storage_data = self._integration.get_storage_metrics()
        self._network_data = self._integration.get_network_status()
        self._bluetooth_data = self._integration.get_bluetooth_status()
        self._audio_data = self._integration.get_audio_status()
        self._processes = self._integration.get_top_processes(10)
        self._containers_data = self._integration.get_container_status()
        self._ai_services_data = self._integration.get_ai_services_status()
        self._apps_list = self._integration.get_applications()

    # --- Properties ---

    @pyqtProperty(QVariant, notify=compatibilityChanged)
    def compatibility(self):
        return self._compat_data

    @pyqtProperty(QVariant, notify=systemInfoChanged)
    def systemInfo(self):
        return self._sys_info

    @pyqtProperty(QVariant, notify=hardwareMetricsChanged)
    def hardwareMetrics(self):
        return self._hw_metrics

    @pyqtProperty(QVariant, constant=True)
    def gpuInfo(self):
        return self._gpu_info

    @pyqtProperty(QVariant, notify=storageChanged)
    def storageMetrics(self):
        return self._storage_data

    @pyqtProperty(QVariant, notify=networkChanged)
    def networkStatus(self):
        return self._network_data

    @pyqtProperty(QVariant, notify=bluetoothChanged)
    def bluetoothStatus(self):
        return self._bluetooth_data

    @pyqtProperty(QVariant, notify=audioChanged)
    def audioStatus(self):
        return self._audio_data

    @pyqtProperty(QVariant, notify=processesChanged)
    def topProcesses(self):
        return self._processes

    @pyqtProperty(QVariant, notify=containersChanged)
    def containers(self):
        return self._containers_data

    @pyqtProperty(QVariant, notify=aiServicesChanged)
    def aiServices(self):
        return self._ai_services_data

    @pyqtProperty(QVariant, constant=True)
    def applicationsList(self):
        return self._apps_list

    # --- Slots ---

    @pyqtSlot()
    def refreshMetrics(self):
        """Samples live CPU, RAM, network, storage, and processes."""
        self._hw_metrics = self._integration.get_cpu_and_ram()
        self._storage_data = self._integration.get_storage_metrics()
        self._network_data = self._integration.get_network_status()
        self._processes = self._integration.get_top_processes(10)
        self._ai_services_data = self._integration.get_ai_services_status()

        self.hardwareMetricsChanged.emit()
        self.storageChanged.emit()
        self.networkChanged.emit()
        self.processesChanged.emit()
        self.aiServicesChanged.emit()

    @pyqtSlot(str, str, result=QVariant)
    def launchApp(self, command_or_exec: str, working_dir: str = ""):
        """Safely executes an application without shell injection."""
        return self._integration.launch_application(command_or_exec, working_dir=working_dir or None)

    @pyqtSlot(str, result=QVariant)
    def getGitStatus(self, path: str):
        """Queries Git repository status."""
        return self._integration.get_git_status(path)

    @pyqtSlot(str, result=QVariant)
    def listDirectory(self, path: str):
        """Lists directory entries safely."""
        return self._integration.list_directory(path)

    @pyqtSlot(str, result=QVariant)
    def getServiceStatus(self, unit_name: str):
        """Queries systemd service unit status."""
        return self._integration.get_service_status(unit_name)

    @pyqtSlot(result=QVariant)
    def checkDnfUpdates(self):
        """Queries DNF package update availability."""
        return self._integration.get_package_management_status()
