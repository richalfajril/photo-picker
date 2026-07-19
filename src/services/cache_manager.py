"""
Service for managing image cache and background preloading.
"""
import concurrent.futures
from collections import OrderedDict
from typing import Optional, Dict

from PySide6.QtGui import QImage
from PySide6.QtCore import QObject, Signal

from src.services.image_loader_service import ImageLoaderService


class CacheManager(QObject):
    """
    Manages in-memory image caching and background preloading 
    to ensure instant navigation between photos.
    """
    # Signal emitted when a background preload finishes
    preload_finished = Signal(str)

    def __init__(self, max_memory_items: int = 5) -> None:
        super().__init__()
        self.max_memory_items = max_memory_items
        self._memory_cache: OrderedDict[str, QImage] = OrderedDict()
        
        # Thread pool for background loading
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        # Keep track of what is currently being loaded so we don't load twice
        self._loading_futures: Dict[str, concurrent.futures.Future[None]] = {}

    def get_image(self, filepath: str) -> Optional[QImage]:
        """
        Retrieves the image from cache if available, otherwise loads it synchronously.
        """
        if filepath in self._memory_cache:
            # Move to end (most recently used)
            self._memory_cache.move_to_end(filepath)
            return self._memory_cache[filepath]

        # Not in cache, load it blocking
        img = ImageLoaderService.load_image(filepath)
        if img:
            self._add_to_cache(filepath, img)
        return img

    def preload_images(self, filepaths: list[str]) -> None:
        """
        Submits a list of file paths to be preloaded in the background.
        """
        for path in filepaths:
            if path not in self._memory_cache and path not in self._loading_futures:
                future = self._executor.submit(self._background_load, path)
                self._loading_futures[path] = future

    def _background_load(self, filepath: str) -> None:
        """Task executed in the thread pool."""
        img = ImageLoaderService.load_image(filepath)
        if img:
            self._add_to_cache(filepath, img)
            
        # Clean up tracking
        if filepath in self._loading_futures:
            del self._loading_futures[filepath]
            
        self.preload_finished.emit(filepath)

    def _add_to_cache(self, filepath: str, img: QImage) -> None:
        """Adds to LRU cache and evicts oldest if necessary."""
        self._memory_cache[filepath] = img
        if len(self._memory_cache) > self.max_memory_items:
            # Pop the first item (least recently used)
            self._memory_cache.popitem(last=False)
            
    def clear(self) -> None:
        """Clears all cached images."""
        self._memory_cache.clear()
        # We don't strictly cancel futures here for simplicity, 
        # but we clear the tracking dict.
        self._loading_futures.clear()
