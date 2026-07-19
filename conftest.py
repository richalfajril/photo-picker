"""Pytest configuration: run Qt tests headless."""
import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest


@pytest.fixture(scope="session")
def qapp():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def make_images():
    """Factory that writes real image files into a folder and returns their paths.

    Usage: make_images(folder, count=3, fmt="JPEG") -> list[str] (sorted).
    """
    from PIL import Image

    _ext = {"JPEG": ".jpg", "PNG": ".png", "BMP": ".bmp", "WEBP": ".webp"}

    def _make(folder, count=3, fmt="JPEG", size=(64, 48), prefix="img"):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        ext = _ext.get(fmt, ".jpg")
        paths = []
        for i in range(count):
            p = folder / f"{prefix}_{i:05d}{ext}"
            color = (i % 256, (i * 3) % 256, (i * 7) % 256)
            Image.new("RGB", size, color).save(p, fmt)
            paths.append(str(p))
        return sorted(paths)

    return _make
