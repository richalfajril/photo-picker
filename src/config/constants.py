"""
Global constants for Photo Picker MVP.
"""
from pathlib import Path

# Application
APP_NAME = "Photo Picker"
APP_VERSION = "1.0.0"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
STORAGE_DIR = PROJECT_ROOT / "storage"
WORKSPACES_DIR = STORAGE_DIR / "workspaces"
CACHE_DIR = STORAGE_DIR / "cache"
LOGS_DIR = STORAGE_DIR / "logs"
SETTINGS_FILE = STORAGE_DIR / "settings.json"

# UI Defaults
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800

# Supported Image Formats
SUPPORTED_FORMATS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp",
    ".cr2", ".cr3", ".nef", ".arw", ".dng"
}
