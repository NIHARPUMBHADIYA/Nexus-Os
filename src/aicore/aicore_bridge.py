"""
NEXUS OS — AI Core PyQt6 / QML Bridge (`AICoreBridge`)
Exposes reactive properties and invokable slots to QML interfaces.
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from .aicore_core import AICore

class AICoreBridge(QObject):
    """
    Bridge connecting QML AI Core View to AICore system daemon.
    """

    hardwareChanged = pyqtSignal()
    servicesChanged = pyqtSignal()
    modelsChanged = pyqtSignal()
    providersChanged = pyqtSignal()

    def __init__(self, core: AICore = None, parent=None):
        super().__init__(parent)
        self._core = core or AICore()
        self._hardware = self._core.get_hardware_status()
        self._services = self._core.get_services_status()
        self._models = self._core.get_models()
        self._providers = self._core.get_providers()
        self._free_tiers = self._core.get_free_tiers()

    # --- Properties ---

    @pyqtProperty(QVariant, notify=hardwareChanged)
    def hardwareStatus(self):
        return self._hardware

    @pyqtProperty(QVariant, notify=servicesChanged)
    def servicesList(self):
        return self._services

    @pyqtProperty(QVariant, notify=modelsChanged)
    def modelsList(self):
        return self._models

    @pyqtProperty(QVariant, notify=providersChanged)
    def providersList(self):
        return self._providers

    @pyqtProperty(QVariant, constant=True)
    def freeTiersList(self):
        return self._free_tiers

    # --- Invokable Slots ---

    @pyqtSlot()
    def refreshAll(self):
        self._hardware = self._core.get_hardware_status()
        self.hardwareChanged.emit()

        self._services = self._core.get_services_status()
        self.servicesChanged.emit()

        self._models = self._core.get_models()
        self.modelsChanged.emit()

        self._providers = self._core.get_providers()
        self.providersChanged.emit()

    @pyqtSlot(str, str, bool)
    def filterModels(self, category: str, query: str, localOnly: bool):
        self._models = self._core.get_models(category, query, localOnly)
        self.modelsChanged.emit()

    @pyqtSlot(str, result=QVariant)
    def pullModel(self, modelId: str):
        res = self._core.pull_model(modelId)
        self._models = self._core.get_models()
        self.modelsChanged.emit()
        return res

    @pyqtSlot(str, result=QVariant)
    def deleteModel(self, modelId: str):
        res = self._core.delete_model(modelId)
        self._models = self._core.get_models()
        self.modelsChanged.emit()
        self._hardware = self._core.get_hardware_status()
        self.hardwareChanged.emit()
        return res

    @pyqtSlot(str, result=QVariant)
    def loadModel(self, modelId: str):
        res = self._core.load_model(modelId)
        self._models = self._core.get_models()
        self.modelsChanged.emit()
        self._hardware = self._core.get_hardware_status()
        self.hardwareChanged.emit()
        return res

    @pyqtSlot(str, result=QVariant)
    def unloadModel(self, modelId: str):
        res = self._core.unload_model(modelId)
        self._models = self._core.get_models()
        self.modelsChanged.emit()
        self._hardware = self._core.get_hardware_status()
        self.hardwareChanged.emit()
        return res

    @pyqtSlot(str, result=bool)
    def startService(self, serviceId: str):
        success = self._core.start_service(serviceId)
        self._services = self._core.get_services_status()
        self.servicesChanged.emit()
        return success

    @pyqtSlot(str, result=bool)
    def stopService(self, serviceId: str):
        success = self._core.stop_service(serviceId)
        self._services = self._core.get_services_status()
        self.servicesChanged.emit()
        return success

    @pyqtSlot(str, result=bool)
    def restartService(self, serviceId: str):
        success = self._core.restart_service(serviceId)
        self._services = self._core.get_services_status()
        self.servicesChanged.emit()
        return success

    @pyqtSlot(str, result=QVariant)
    def getServiceLogs(self, serviceId: str):
        return self._core.get_service_logs(serviceId)

    @pyqtSlot(str, str, result=bool)
    def saveCredential(self, providerId: str, apiKey: str):
        success = self._core.save_credential(providerId, apiKey)
        self._providers = self._core.get_providers()
        self.providersChanged.emit()
        return success

    @pyqtSlot(str, result=QVariant)
    def testProvider(self, providerId: str):
        return self._core.test_provider(providerId)
