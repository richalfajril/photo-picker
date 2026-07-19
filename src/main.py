"""
Entry point for the Photo Picker application.
"""
import sys
from PySide6.QtWidgets import QApplication

from src.presentation.start_window import StartWindow


def main() -> None:
    # Initialize the application
    app = QApplication(sys.argv)
    app.setApplicationName("Photo Picker")
    app.setApplicationVersion("1.0.0")

    # Show the Startup Window
    window = StartWindow()
    window.show()

    # For now, just print the payload to verify it works
    # In Phase 4/5, this will instantiate the ViewerController
    window.start_requested.connect(lambda payload: print(f"Start requested with: {payload}"))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
