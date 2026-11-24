"""
NEXUS OS — Personalization & Theme Engine
Manages themes, appearance settings, custom theme creation, import/export,
and WCAG 2.1 contrast / readability validation.
"""

import os
import sys
import json
import math
import time
from typing import Dict, Any, List, Optional, Tuple

class PersonalizationEngine:
    """
    Core engine managing system-wide themes, personalization tokens,
    dock/panel configuration, fonts, wallpapers, and accessibility.
    """

    DEFAULT_THEMES = [
        {"id": "midnight", "name": "Midnight", "type": "dark", "description": "Default deep indigo & navy dark theme with vibrant accents."},
        {"id": "nord", "name": "Nord", "type": "dark", "description": "Arctic, north-bluish clean color palette."},
        {"id": "dracula", "name": "Dracula", "type": "dark", "description": "Classic dark gothic theme with vibrant purple and green."},
        {"id": "catppuccin", "name": "Catppuccin", "type": "dark", "description": "Soothing pastel theme optimized for long coding sessions."},
        {"id": "tokyo-night", "name": "Tokyo Night", "type": "dark", "description": "Clean neon theme celebrating the lights of downtown Tokyo."},
        {"id": "terminal-green", "name": "Terminal Green", "type": "dark", "description": "Retro matrix phosphor green terminal aesthetic."},
        {"id": "paper-light", "name": "Paper Light", "type": "light", "description": "Warm, natural high-contrast daylight paper theme."},
        {"id": "amoled", "name": "AMOLED Black", "type": "dark", "description": "True pitch-black #000000 theme for OLED displays and maximum power saving."},
        {"id": "deep-space", "name": "Deep Space", "type": "dark", "description": "High-contrast celestial navy with cyan highlights."},
        {"id": "custom", "name": "Custom Theme", "type": "custom", "description": "User-crafted custom color tokens and accents."}
    ]

    WALLPAPERS = [
        {"id": "nebula", "name": "Cosmic Nebula", "path": "qrc:/wallpapers/nebula.jpg", "category": "Abstract", "color": "#171B2B"},
        {"id": "aurora", "name": "Nordic Aurora", "path": "qrc:/wallpapers/aurora.jpg", "category": "Nature", "color": "#242933"},
        {"id": "cyberpunk", "name": "Tokyo Neon", "path": "qrc:/wallpapers/cyberpunk.jpg", "category": "Cityscape", "color": "#16161E"},
        {"id": "minimal_dark", "name": "Minimal Obsidian", "path": "qrc:/wallpapers/minimal_dark.jpg", "category": "Minimal", "color": "#0B0D14"},
        {"id": "paper_horizon", "name": "Warm Dawn", "path": "qrc:/wallpapers/paper_horizon.jpg", "category": "Light", "color": "#FBFBFA"}
    ]

    ICON_THEMES = [
        {"id": "aether-default", "name": "Aether Rounded (Default)", "description": "Clean rounded SVG icons designed for NEXUS OS."},
        {"id": "papirus", "name": "Papirus Colors", "description": "Vibrant material-inspired open source icon set."},
        {"id": "breeze", "name": "KDE Breeze", "description": "Classic KDE Plasma desktop iconography."},
        {"id": "flat-color", "name": "Flat Minimal", "description": "Monochrome glyphs for zero visual distraction."}
    ]

    CURSOR_THEMES = [
        {"id": "aether-glow", "name": "Aether Glow", "description": "Subtle neon trailing cursor matching the active accent."},
        {"id": "breeze", "name": "Breeze Light", "description": "Precision crisp white vector cursor."},
        {"id": "adwaita", "name": "Adwaita Modern", "description": "Standard GNOME modern arrow cursor."},
        {"id": "bibata", "name": "Bibata Modern Amber", "description": "Rounded material cursor with warm accents."}
    ]

    FONT_FAMILIES = {
        "ui": ["Inter", "Cantarell", "Noto Sans", "system-ui", "Segoe UI"],
        "mono": ["JetBrains Mono", "Fira Code", "Cascadia Code", "Hack", "monospace"]
    }

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.expanduser(os.path.join("~", ".config", "nexus", "personalization"))
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, "theme_config.json")
        self.custom_theme_file = os.path.join(self.config_dir, "custom_theme.json")
        self.settings: Dict[str, Any] = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        default_settings = {
            "active_theme": "midnight",
            "theme_mode": "dark",  # "dark", "light", "auto"
            "custom_accent": "",
            "wallpaper_id": "nebula",
            "wallpaper_blur": 15,
            "icon_theme": "aether-default",
            "cursor_theme": "aether-glow",
            "cursor_size": 24,
            "font_ui": "Inter",
            "font_mono": "JetBrains Mono",
            "font_scale": 1.0,
            "dock_position": "bottom",  # "bottom", "left", "right"
            "dock_size": "medium",      # "small", "medium", "large"
            "dock_auto_dodge": True,
            "panel_opacity": 0.85,
            "panel_clock_format": "24h",
            "window_radius_scale": "medium",  # "small": 10, "medium": 14, "large": 20, "xl": 24
            "blur_enabled": True,
            "blur_radius": 20,
            "acrylic_glass": True,
            "animation_speed": "normal",      # "snappy": 100ms, "normal": 180ms, "relaxed": 280ms
            "reduced_motion": False,
            "custom_colors": {
                "background": "#0D1117",
                "secondaryBackground": "#161B22",
                "surface": "#21262D",
                "elevatedSurface": "#30363D",
                "border": "#30363D",
                "borderFocus": "#58A6FF",
                "primaryText": "#F0F6FC",
                "secondaryText": "#8B949E",
                "tertiaryText": "#6E7681",
                "accent": "#58A6FF",
                "accentHover": "#388BFD",
                "accentSubtle": "#1F3554",
                "success": "#3FB950",
                "warning": "#D29922",
                "error": "#F85149",
                "info": "#58A6FF",
                "isDark": True
            }
        }

        if os.path.isfile(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    saved = json.load(f)
                    default_settings.update(saved)
            except Exception:
                pass

        return default_settings

    def save_settings(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

    def get_settings(self) -> Dict[str, Any]:
        return dict(self.settings)

    def set_setting(self, key: str, value: Any) -> bool:
        if key in self.settings:
            self.settings[key] = value
            self.save_settings()
            return True
        return False

    def get_effective_theme_mode(self) -> str:
        """Resolve 'auto' mode based on system wall-clock time."""
        mode = self.settings.get("theme_mode", "dark")
        if mode == "auto":
            current_hour = time.localtime().tm_hour
            # Daytime 06:00 - 18:00 is light; nighttime is dark
            return "light" if 6 <= current_hour < 18 else "dark"
        return mode

    # --- WCAG 2.1 Contrast & Readability Engine ---

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)

    @classmethod
    def _relative_luminance(cls, hex_color: str) -> float:
        """Calculate WCAG 2.1 relative luminance."""
        r, g, b = cls._hex_to_rgb(hex_color)

        def adjust(c: float) -> float:
            return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    @classmethod
    def calculate_contrast_ratio(cls, foreground_hex: str, background_hex: str) -> float:
        """
        Calculate contrast ratio between foreground and background.
        Range: 1.0 (identical) to 21.0 (black on white).
        """
        try:
            l1 = cls._relative_luminance(foreground_hex)
            l2 = cls._relative_luminance(background_hex)
            lighter = max(l1, l2)
            darker = min(l1, l2)
            return round((lighter + 0.05) / (darker + 0.05), 2)
        except Exception:
            return 1.0

    @classmethod
    def evaluate_theme_contrast(cls, theme_tokens: Dict[str, str]) -> Dict[str, Any]:
        """
        Evaluate a theme's color tokens against WCAG 2.1 AA standards:
        - Normal text requires at least 4.5:1
        - Large text / UI components require at least 3.0:1
        """
        fg_primary = theme_tokens.get("primaryText", "#FFFFFF")
        fg_secondary = theme_tokens.get("secondaryText", "#A0A0A0")
        bg = theme_tokens.get("background", "#000000")
        surface = theme_tokens.get("surface", "#1A1A1A")
        accent = theme_tokens.get("accent", "#6366F1")

        primary_on_bg = cls.calculate_contrast_ratio(fg_primary, bg)
        primary_on_surface = cls.calculate_contrast_ratio(fg_primary, surface)
        secondary_on_bg = cls.calculate_contrast_ratio(fg_secondary, bg)
        accent_on_bg = cls.calculate_contrast_ratio(accent, bg)

        wcag_aa_normal = (primary_on_bg >= 4.5 and primary_on_surface >= 4.5)
        wcag_aa_secondary = (secondary_on_bg >= 3.0)

        rating = "Pass (AAA)" if primary_on_bg >= 7.0 else ("Pass (AA)" if primary_on_bg >= 4.5 else "Fail")

        return {
            "primary_on_bg": primary_on_bg,
            "primary_on_surface": primary_on_surface,
            "secondary_on_bg": secondary_on_bg,
            "accent_on_bg": accent_on_bg,
            "wcag_aa_passed": wcag_aa_normal and wcag_aa_secondary,
            "rating": rating
        }

    # --- Custom Theme & Import / Export ---

    def export_theme(self, theme_name: str, target_file: str) -> bool:
        """Export current custom theme configuration to a portable JSON file."""
        try:
            payload = {
                "name": theme_name,
                "exported_at": time.time(),
                "nexus_os_version": "1.0.0",
                "tokens": self.settings.get("custom_colors", {})
            }
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            return True
        except Exception:
            return False

    def import_theme(self, source_file: str) -> Dict[str, Any]:
        """Import and validate a community theme JSON file."""
        if not os.path.isfile(source_file):
            return {"success": False, "error": f"File '{source_file}' does not exist."}

        try:
            with open(source_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            tokens = data.get("tokens", {})
            required_tokens = ["background", "surface", "primaryText", "accent", "border"]
            missing = [t for t in required_tokens if t not in tokens]
            if missing:
                return {"success": False, "error": f"Theme missing required semantic tokens: {', '.join(missing)}"}

            self.settings["custom_colors"] = tokens
            self.settings["active_theme"] = "custom"
            self.save_settings()

            contrast = self.evaluate_theme_contrast(tokens)

            return {
                "success": True,
                "theme_name": data.get("name", "Imported Theme"),
                "contrast": contrast,
                "message": f"Successfully imported theme '{data.get('name', 'Custom')}'."
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to parse theme file: {e}"}
