"""
Service for scanning and loading images from disk.
"""
from pathlib import Path
from typing import List, Optional

import rawpy
from PySide6.QtGui import QImage

SUPPORTED_STANDARD = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
SUPPORTED_RAW = {".cr2", ".cr3", ".nef", ".arw", ".dng"}
ALL_SUPPORTED = SUPPORTED_STANDARD | SUPPORTED_RAW


class ImageLoaderService:
    """
    Handles finding and reading images (Standard and RAW formats).
    """

    @staticmethod
    def scan_folder(folder_path: str) -> List[str]:
        """
        Scans a folder for supported images and returns a sorted list of absolute paths.
        """
        path = Path(folder_path)
        if not path.is_dir():
            return []

        images = []
        for file in path.iterdir():
            if file.is_file() and file.suffix.lower() in ALL_SUPPORTED:
                images.append(str(file.absolute()))

        # Sort alphanumerically
        images.sort()
        return images

    @staticmethod
    def load_image(filepath: str) -> Optional[QImage]:
        """
        Loads an image from disk. Supports both standard and RAW formats.
        Returns a QImage, or None if it fails.
        """
        path = Path(filepath)
        ext = path.suffix.lower()

        if ext in SUPPORTED_RAW:
            return ImageLoaderService._load_raw(filepath)
        elif ext in SUPPORTED_STANDARD:
            img = QImage(filepath)
            if img.isNull():
                return None
            return img
        
        return None

    @staticmethod
    def load_thumbnail(filepath: str) -> Optional[QImage]:
        """
        Loads a lower-resolution preview of an image to save memory and time.
        """
        path = Path(filepath)
        ext = path.suffix.lower()

        if ext in SUPPORTED_RAW:
            return ImageLoaderService._load_raw_thumbnail(filepath)
        elif ext in SUPPORTED_STANDARD:
            # For standard formats, we just load the full image.
            # (PySide6 doesn't have a native fast-thumb reader without loading it first)
            # Scaling will be done by the UI or CacheManager if needed.
            return ImageLoaderService.load_image(filepath)

        return None

    @staticmethod
    def _load_raw(filepath: str) -> Optional[QImage]:
        """Decodes a RAW file into a QImage."""
        try:
            with rawpy.imread(filepath) as raw:
                rgb = raw.postprocess(use_camera_wb=True)
                
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            # Use .copy() so QImage owns the memory, allowing rgb to be garbage collected
            img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
            return img
        except Exception as e:
            print(f"Failed to load RAW {filepath}: {e}")
            return None

    @staticmethod
    def _load_raw_thumbnail(filepath: str) -> Optional[QImage]:
        """Extracts the embedded thumbnail from a RAW file, or falls back to half-size decode."""
        try:
            with rawpy.imread(filepath) as raw:
                try:
                    thumb = raw.extract_thumb()
                    if thumb.format == rawpy.ThumbFormat.JPEG:  # type: ignore[attr-defined]
                        img = QImage.fromData(thumb.data)  # type: ignore[arg-type]
                        return img
                    elif thumb.format == rawpy.ThumbFormat.BITMAP:  # type: ignore[attr-defined]
                        rgb = thumb.data
                        h, w, ch = rgb.shape  # type: ignore[union-attr]
                        bytes_per_line = ch * w
                        img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()  # type: ignore[union-attr]
                        return img
                except rawpy.LibRawNoThumbnailError:  # type: ignore[attr-defined]
                    pass
                
                # Fallback to decoding at half size
                rgb = raw.postprocess(half_size=True, use_camera_wb=True)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
                return img
        except Exception as e:
            print(f"Failed to load RAW thumbnail {filepath}: {e}")
            return None
