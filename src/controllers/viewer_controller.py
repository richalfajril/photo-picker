"""
Main controller orchestrating the Viewer UI and business logic.
"""
from typing import Any, Dict, Optional
from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from src.presentation.viewer_window import ViewerWindow
from src.presentation.loading_screen import LoadingScreen
from src.presentation.exit_dialog import ExitDialog
from src.domain.workspace import Workspace
from src.services.image_loader_service import ImageLoaderService
from src.services.cache_manager import CacheManager
from src.services.file_operation_service import FileOperationService
from src.services.overlay_manager import OverlayManager
from src.repositories.workspace_repository import WorkspaceRepository
from src.utils.clamp import clamp_index


class ViewerController(QObject):
    """
    Connects the presentation layer to the domain and service layers.
    """
    def __init__(self, payload: Dict[str, Any], loaded_workspace: Optional[Workspace] = None) -> None:
        super().__init__()
        
        # 1. Initialize Domain
        if loaded_workspace:
            self.workspace = loaded_workspace
        else:
            self.workspace = Workspace(
                name=payload["workspace_name"],
                source_folder=payload["source_folder"],
                destination_folder=payload["destination_folder"],
            )
        self.settings = payload["settings"]
        
        # 2. Initialize Services
        self.cache_manager = CacheManager(max_memory_items=5)
        self.workspace_repo = WorkspaceRepository()
        
        # 3. Initialize UI
        self.viewer_window = ViewerWindow()
        self.loading_screen = LoadingScreen()
        
        # Initialize Overlay Manager on top of the Viewer Window
        self.overlay_manager = OverlayManager(self.viewer_window)
        
        # Connect Signals
        self._connect_signals()
        
        # 4. Start workflow
        self._start_initialization()

    def _connect_signals(self) -> None:
        self.viewer_window.next_requested.connect(self.next_image)
        self.viewer_window.prev_requested.connect(self.prev_image)
        self.viewer_window.first_requested.connect(self.first_image)
        self.viewer_window.last_requested.connect(self.last_image)
        self.viewer_window.exit_requested.connect(self.exit_app)
        self.viewer_window.copy_requested.connect(self.copy_image)
        self.viewer_window.undo_requested.connect(self.undo_image)

    def _start_initialization(self) -> None:
        """Shows loading screen and scans folder."""
        self.loading_screen.show()
        self.loading_screen.set_status("Scanning folder...")
        
        images = ImageLoaderService.scan_folder(self.workspace.source_folder)
        self.workspace.image_list = images
        self.workspace.current_index = clamp_index(self.workspace.current_index, len(images))

        self.loading_screen.set_progress(len(images), len(images), "Loading complete!")
        
        # Initial preload
        self._update_preload()
        
        self.loading_screen.hide()
        
        if self.settings.get("fullscreen", False):
            self.viewer_window.toggle_fullscreen()
            
        self.viewer_window.show()
        self._update_ui()

    def next_image(self) -> None:
        if self.workspace.current_index < len(self.workspace.image_list) - 1:
            self.workspace.current_index += 1
            self._update_preload()
            self._update_ui()

    def prev_image(self) -> None:
        if self.workspace.current_index > 0:
            self.workspace.current_index -= 1
            self._update_preload()
            self._update_ui()

    def first_image(self) -> None:
        if self.workspace.image_list:
            self.workspace.current_index = 0
            self._update_preload()
            self._update_ui()

    def last_image(self) -> None:
        if self.workspace.image_list:
            self.workspace.current_index = len(self.workspace.image_list) - 1
            self._update_preload()
            self._update_ui()

    def copy_image(self) -> None:
        if not self.workspace.image_list:
            return
            
        current_path = self.workspace.image_list[self.workspace.current_index]
        
        if current_path in self.workspace.selected_images:
            return
            
        success = FileOperationService.copy_file(current_path, self.workspace.destination_folder)
        if success:
            self.workspace.selected_images.append(current_path)
            self.overlay_manager.show_overlay("COPIED", "#22C55E")
            if self.settings.get("sound", False):
                QApplication.beep()
            self.workspace_repo.save(self.workspace)
            
            if self.settings.get("auto_next", False):
                self.next_image()
            else:
                self._update_ui()
        else:
            self.overlay_manager.show_overlay("COPY FAILED", "#EF4444")

    def undo_image(self) -> None:
        if not self.workspace.image_list:
            return
            
        current_path = self.workspace.image_list[self.workspace.current_index]
        
        if current_path not in self.workspace.selected_images:
            return
            
        success = FileOperationService.remove_file(current_path, self.workspace.destination_folder)
        if success:
            self.workspace.selected_images.remove(current_path)
            self.overlay_manager.show_overlay("REMOVED", "#EF4444")
            if self.settings.get("sound", False):
                QApplication.beep()
            self.workspace_repo.save(self.workspace)
            self._update_ui()

    def exit_app(self) -> None:
        dialog = ExitDialog(parent=self.viewer_window)
        if dialog.exec() == ExitDialog.EXIT:
            self.viewer_window.close()

    def _update_preload(self) -> None:
        """Preloads the next few images into memory cache."""
        idx = self.workspace.current_index
        total = len(self.workspace.image_list)
        
        to_preload = []
        for i in range(1, 4):
            if idx + i < total:
                to_preload.append(self.workspace.image_list[idx + i])
                
        self.cache_manager.preload_images(to_preload)

    def _update_ui(self) -> None:
        """Refreshes the ViewerWindow with the current image."""
        if not self.workspace.image_list:
            return
            
        current_path = self.workspace.image_list[self.workspace.current_index]
        filename = Path(current_path).name
        
        # Load from cache (or disk if not cached)
        img = self.cache_manager.get_image(current_path)
        
        if img:
            self.viewer_window.set_image(
                image=img,
                filename=filename,
                current=self.workspace.current_index + 1,
                total=len(self.workspace.image_list),
                selected=len(self.workspace.selected_images),
                is_selected=(current_path in self.workspace.selected_images)
            )
            
        self.workspace_repo.save(self.workspace)
