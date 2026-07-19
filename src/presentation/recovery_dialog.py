"""
Workspace Recovery Dialog UI Component.
"""
from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFrame, QWidget
)
from src.domain.workspace import Workspace


class RecoveryDialog(QDialog):
    """
    Dialog asking the user whether to continue an existing workspace
    or start a new one.
    """
    
    # Dialog Results
    CONTINUE = 1
    START_NEW = 2

    def __init__(self, workspace: Workspace, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.workspace = workspace
        self.setWindowTitle("Workspace Found")
        self.setModal(True)
        self.setStyleSheet("background-color: #111111; color: #FFFFFF;")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        lbl_title = QLabel("Workspace Found")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FACC15;")
        layout.addWidget(lbl_title)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #333333;")
        layout.addWidget(line)

        # Info
        layout.addWidget(self._create_info_row("Workspace", self.workspace.name))
        layout.addWidget(self._create_info_row("Source", self.workspace.source_folder))
        layout.addWidget(self._create_info_row("Destination", self.workspace.destination_folder))
        
        progress_text = f"{self.workspace.current_index + 1} / {self.workspace.total_images}" if self.workspace.total_images > 0 else "0 / 0"
        layout.addWidget(self._create_info_row("Progress", progress_text))
        
        selected_text = f"{len(self.workspace.selected_images)} Photos"
        layout.addWidget(self._create_info_row("Selected", selected_text))

        layout.addSpacing(20)

        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)

        btn_continue = QPushButton("Continue Workspace")
        btn_continue.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        btn_continue.clicked.connect(lambda: self.done(self.CONTINUE))

        btn_new = QPushButton("Start New Workspace")
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #444444; }
        """)
        btn_new.clicked.connect(lambda: self.done(self.START_NEW))

        btn_layout.addWidget(btn_continue)
        btn_layout.addWidget(btn_new)
        
        layout.addLayout(btn_layout)

    def _create_info_row(self, label: str, value: str) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        lbl_title = QLabel(label)
        lbl_title.setStyleSheet("font-size: 12px; color: #888888;")
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        lbl_value.setWordWrap(True)
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        
        return widget
