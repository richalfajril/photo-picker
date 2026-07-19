"""
Loading Screen UI Component.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class LoadingScreen(QWidget):
    """
    Displays progress during the initial folder scan and image caching phase.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Photo Picker - Loading")
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(60, 60, 60, 60)
        main_layout.setSpacing(20)

        # Title / Status
        self.title_label = QLabel("Loading Images...")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.title_label)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # We use custom text below
        self.progress_bar.setMinimumWidth(300)
        main_layout.addWidget(self.progress_bar)

        # Progress Text
        self.progress_text = QLabel("0 / 0")
        self.progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_text.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.progress_text)

        # Sub status Text
        self.status_text = QLabel("Preparing...")
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_text.setStyleSheet("font-size: 12px; color: gray;")
        main_layout.addWidget(self.status_text)
        
        self.setMinimumWidth(400)

    def set_progress(self, current: int, total: int, status_message: str = "") -> None:
        """Updates the progress bar and labels."""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.progress_text.setText(f"{current} / {total}")
        
        if status_message:
            self.status_text.setText(status_message)

    def set_status(self, status_message: str) -> None:
        """Updates only the status message."""
        self.status_text.setText(status_message)
