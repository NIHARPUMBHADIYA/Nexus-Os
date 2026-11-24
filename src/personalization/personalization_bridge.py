"""
NEXUS OS — Personalization PyQt6 Bridge (`PersonalizationBridge`)
Exposes reactive personalization properties and slots to QML.
"""

from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant
from .personalization_engine import PersonalizationEngine

class PersonalizationBridge(QObject):
    """
    QObject bridge for reactive theme and personalization bindings in QML.
    """

    settingsChanged = pyqtSignal()
    contrastChanged = pyqtSignal()

    def __init__(self, engine: Optional[PersonalizationEngine] = None, parent=None):
        super().__init__(parent)
        self._engine = engine or PersonalizationEngine()
        self._settings = self._engine.get_settings()
        self._update_contrast()

    def _update_contrast(self):
        active_id = self._settings.get("active_theme", "midnight")
        if active_id == "custom":
            tokens = self._settings.get("custom_colors", {})
        else:
            # Look up theme in default themes
            tokens = self._get_theme_tokens(active_id)
        self._contrast = self._engine.evaluate_theme_contrast(tokens)

    def _get_theme_tokens(self, theme_id: str) -> Dict[str, str]:
        # Minimal fallback mapping matching NexusTheme.qml
        color_maps = {
            "midnight": {"background": "#0B0D14", "surface": "#171B2B", "primaryText": "#F3F4F6", "secondaryText": "#94A3B8", "accent": "#6366F1"},
            "nord": {"background": "#242933", "surface": "#3B4252", "primaryText": "#ECEFF4", "secondaryText": "#D8DEE9", "accent": "#88C0D0"},
            "dracula": {"background": "#1E1F29", "surface": "#343746", "primaryText": "#F8F8F2", "secondaryText": "#A2ABCC", "accent": "#BD93F9"},
            "catppuccin": {"background": "#181825", "surface": "#313244", "primaryText": "#CDD6F4", "secondaryText": "#A6ADC8", "accent": "#CBA6F7"},
            "tokyo-night": {"background": "#16161E", "surface": "#24283B", "primaryText": "#C0CAF5", "secondaryText": "#9AA5CE", "accent": "#7AA2F7"},
            "terminal-green": {"background": "#050B06", "surface": "#0F1E12", "primaryText": "#4ADE80", "secondaryText": "#22C55E", "accent": "#22C55E"},
            "paper-light": {"background": "#FBFBFA", "surface": "#FFFFFF", "primaryText": "#1C1917", "secondaryText": "#57534E", "accent": "#4F46E5"},
            "amoled": {"background": "#000000", "surface": "#121212", "primaryText": "#FFFFFF", "secondaryText": "#A1A1AA", "accent": "#6366F1"},
            "deep-space": {"background": "#030712", "surface": "#0D1938", "primaryText": "#F0F9FF", "secondaryText": "#7DD3FC", "accent": "#0284C7"}
        }
        return color_maps.get(theme_id, color_maps["midnight"])

    # --- Properties ---

    @pyqtProperty(QVariant, notify=settingsChanged)
    def settings(self):
        return self._settings

    @pyqtProperty(QVariant, constant=True)
    def themesList(self):
        return self._engine.DEFAULT_THEMES

    @pyqtProperty(QVariant, constant=True)
    def wallpapersList(self):
        return self._engine.WALLPAPERS

    @pyqtProperty(QVariant, constant=True)
    def iconThemesList(self):
        return self._engine.ICON_THEMES

    @pyqtProperty(QVariant, constant=True)
    def cursorThemesList(self):
        return self._engine.CURSOR_THEMES

    @pyqtProperty(QVariant, notify=contrastChanged)
    def contrastEvaluation(self):
        return self._contrast

    # --- Slots ---

    @pyqtSlot(str)
    def setTheme(self, themeId: str):
        self._engine.set_setting("active_theme", themeId)
        self._settings = self._engine.get_settings()
        self._update_contrast()
        self.settingsChanged.emit()
        self.contrastChanged.emit()

    @pyqtSlot(str)
    def setThemeMode(self, mode: str):
        self._engine.set_setting("theme_mode", mode)
        self._settings = self._engine.get_settings()
        self.settingsChanged.emit()

    @pyqtSlot(str)
    def setAccent(self, hexColor: str):
        self._engine.set_setting("custom_accent", hexColor)
        self._settings = self._engine.get_settings()
        self._update_contrast()
        self.settingsChanged.emit()
        self.contrastChanged.emit()

    @pyqtSlot(str, int)
    def setWallpaper(self, wallpaperId: str, blur: int):
        self._engine.set_setting("wallpaper_id", wallpaperId)
        self._engine.set_setting("wallpaper_blur", blur)
        self._settings = self._engine.get_settings()
        self.settingsChanged.emit()

    @pyqtSlot(bool)
    def setReducedMotion(self, enabled: bool):
        self._engine.set_setting("reduced_motion", enabled)
        self._settings = self._engine.get_settings()
        self.settingsChanged.emit()

    @pyqtSlot(str, str, bool)
    def setDockConfig(self, position: str, size: str, autoDodge: bool):
        self._engine.set_setting("dock_position", position)
        self._engine.set_setting("dock_size", size)
        self._engine.set_setting("dock_auto_dodge", autoDodge)
        self._settings = self._engine.get_settings()
        self.settingsChanged.emit()

    @pyqtSlot(float, str)
    def setPanelConfig(self, opacity: float, clockFormat: str):
        self._engine.set_setting("panel_opacity", opacity)
        self._engine.set_setting("panel_clock_format", clockFormat)
        self._settings = self._engine.get_settings()
        self.settingsChanged.emit()

    @pyqtSlot(str, bool, int, bool)
    def setWindowConfig(self, radiusScale: str, blurEnabled: bool, blurRadius: int, acrylic: bool):
        self._engine.set_setting("window_radius_scale", radiusScale)
        self._engine.set_setting("blur_enabled", blurEnabled)
        self._engine.set_setting("blur_radius", blurRadius)
        self._engine.set_setting("acrylic_glass", acrylic)
        self._settings = self._engine.get_settings()
        self.settingsChanged.emit()

    @pyqtSlot(str, str)
    def updateCustomColor(self, tokenName: str, hexColor: str):
        colors = self._settings.get("custom_colors", {})
        colors[tokenName] = hexColor
        self._engine.set_setting("custom_colors", colors)
        self._engine.set_setting("active_theme", "custom")
        self._settings = self._engine.get_settings()
        self._update_contrast()
        self.settingsChanged.emit()
        self.contrastChanged.emit()

    @pyqtSlot(str, str, result=bool)
    def exportTheme(self, themeName: str, filePath: str):
        return self._engine.export_theme(themeName, filePath)

    @pyqtSlot(str, result=QVariant)
    def importTheme(self, filePath: str):
        res = self._engine.import_theme(filePath)
        if res.get("success"):
            self._settings = self._engine.get_settings()
            self._update_contrast()
            self.settingsChanged.emit()
            self.contrastChanged.emit()
        return res

    @pyqtSlot(str, result=QVariant)
    def evaluateThemeContrast(self, themeId: str):
        tokens = self._get_theme_tokens(themeId)
        return self._engine.evaluate_theme_contrast(tokens)
