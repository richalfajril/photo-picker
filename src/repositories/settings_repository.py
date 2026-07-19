"""
Repository for managing global Application Settings.
"""
import json
from pathlib import Path
from typing import Dict, Any

from src.config.constants import SETTINGS_FILE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT


class SettingsRepository:
    """
    Handles reading and writing application settings to settings.json.
    """

    def __init__(self, settings_file: Path = SETTINGS_FILE) -> None:
        self.settings_file = settings_file
        # Ensure parent directory exists
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_default_settings(self) -> Dict[str, Any]:
        """Returns the default settings structure."""
        return {
            "theme": "dark",
            "window": {
                "width": DEFAULT_WINDOW_WIDTH,
                "height": DEFAULT_WINDOW_HEIGHT
            },
            "recent_workspaces": []
        }

    def load(self) -> Dict[str, Any]:
        """Load settings from file, returning defaults if not found or corrupted."""
        if not self.settings_file.exists():
            return self._get_default_settings()

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Merge with defaults to ensure all keys exist
            settings = self._get_default_settings()
            
            # Basic deep merge for nested dicts like 'window'
            for key, value in data.items():
                if isinstance(value, dict) and key in settings and isinstance(settings[key], dict):
                    settings[key].update(value)
                else:
                    settings[key] = value
                    
            return settings
        except Exception:
            return self._get_default_settings()

    def save(self, settings: Dict[str, Any]) -> None:
        """Save settings to the file system."""
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

    def reset_to_default(self) -> None:
        """Reset settings to default and save."""
        self.save(self._get_default_settings())
