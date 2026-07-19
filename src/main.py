"""
Entry point for the Photo Picker application.
"""
from typing import Any
import sys
from PySide6.QtWidgets import QApplication

from src.presentation.start_window import StartWindow
from src.controllers.viewer_controller import ViewerController
from src.repositories.workspace_repository import WorkspaceRepository
from src.presentation.recovery_dialog import RecoveryDialog

# Keep a global reference to the controller so it isn't garbage collected
active_controller = None

def main() -> None:
    global active_controller
    # Initialize the application
    app = QApplication(sys.argv)
    app.setApplicationName("Photo Picker")
    app.setApplicationVersion("1.0.0")

    # Show the Startup Window
    window = StartWindow()
    repo = WorkspaceRepository()
    
    def on_start(payload: dict[str, Any]) -> None:
        global active_controller
        
        workspace_name = payload["workspace_name"]
        settings = payload["settings"]
        loaded_workspace = None
        
        if settings.get("recovery", False):
            existing = repo.load(workspace_name)
            if existing:
                dialog = RecoveryDialog(existing, parent=window)
                result = dialog.exec()
                if result == RecoveryDialog.CONTINUE:
                    loaded_workspace = existing
                elif result == RecoveryDialog.START_NEW:
                    pass
                else:
                    return # Abort start if user closes dialog
                    
        window.hide()
        active_controller = ViewerController(payload, loaded_workspace=loaded_workspace)

    def on_reopen(name: str) -> None:
        global active_controller
        ws = repo.load(name)
        if ws is None:
            return  # folder vanished between listing and click
        payload: dict[str, Any] = {
            "workspace_name": ws.name,
            "source_folder": ws.source_folder,
            "destination_folder": ws.destination_folder,
            "settings": window.current_settings(),
        }
        window.hide()
        active_controller = ViewerController(payload, loaded_workspace=ws)

    window.start_requested.connect(on_start)
    window.reopen_requested.connect(on_reopen)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
