"""
Startup Window UI Component.
"""
from typing import Any, Dict, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QFileDialog, QFormLayout, QScrollArea
)
from PySide6.QtCore import Qt, Signal

from src.presentation.recent_workspaces_list import RecentWorkspacesList
from src.repositories.workspace_repository import WorkspaceRepository


class StartWindow(QWidget):
    """
    The initial window for workspace configuration.
    """

    # Signal emitted when start button is clicked
    start_requested = Signal(dict)
    # Signal emitted when a recent workspace row is clicked
    reopen_requested = Signal(str)

    def __init__(self, workspace_repo: Optional[WorkspaceRepository] = None) -> None:
        super().__init__()
        self.setWindowTitle("Photo Picker - Start")
        self._workspace_repo = workspace_repo or WorkspaceRepository()
        self._setup_ui()
        self._connect_signals()
        self._validate_inputs()
        self._load_recent_workspaces()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("📷 PHOTO PICKER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Workspace Name
        self.workspace_name_input = QLineEdit()
        self.workspace_name_input.setPlaceholderText("e.g. Wedding Adit & Sinta")
        form_layout.addRow("Workspace Name", self.workspace_name_input)

        # Source Folder
        self.source_input = QLineEdit()
        self.source_input.setReadOnly(True)
        self.source_input.setPlaceholderText("Select source directory...")
        self.source_browse_btn = QPushButton("Browse")
        
        source_layout = QHBoxLayout()
        source_layout.addWidget(self.source_input)
        source_layout.addWidget(self.source_browse_btn)
        form_layout.addRow("Source Folder", source_layout)

        # Destination Folder
        self.dest_input = QLineEdit()
        self.dest_input.setReadOnly(True)
        self.dest_input.setPlaceholderText("Select destination directory...")
        self.dest_browse_btn = QPushButton("Browse")
        
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(self.dest_input)
        dest_layout.addWidget(self.dest_browse_btn)
        form_layout.addRow("Destination Folder", dest_layout)

        main_layout.addLayout(form_layout)

        # Checkboxes
        self.cb_fullscreen = QCheckBox("Fullscreen")
        self.cb_fullscreen.setChecked(True)
        self.cb_auto_next = QCheckBox("Auto Next after Copy")
        self.cb_auto_next.setChecked(True)
        self.cb_sound = QCheckBox("Sound Feedback")
        self.cb_sound.setChecked(True)
        self.cb_recovery = QCheckBox("Workspace Recovery")
        self.cb_recovery.setChecked(True)

        main_layout.addWidget(self.cb_fullscreen)
        main_layout.addWidget(self.cb_auto_next)
        main_layout.addWidget(self.cb_sound)
        main_layout.addWidget(self.cb_recovery)

        # Start Button
        self.start_btn = QPushButton("START")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(self.start_btn)

        # Recent Workspaces
        self.recent_list = RecentWorkspacesList()
        recent_scroll = QScrollArea()
        recent_scroll.setWidgetResizable(True)
        recent_scroll.setMaximumHeight(220)
        recent_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        recent_scroll.setWidget(self.recent_list)
        main_layout.addWidget(recent_scroll)

        self.setMinimumWidth(500)

    def _connect_signals(self) -> None:
        self.workspace_name_input.textChanged.connect(self._validate_inputs)
        self.source_browse_btn.clicked.connect(self._browse_source)
        self.dest_browse_btn.clicked.connect(self._browse_dest)
        self.start_btn.clicked.connect(self._on_start_clicked)
        self.recent_list.workspace_selected.connect(self.reopen_requested.emit)

    def _load_recent_workspaces(self) -> None:
        self.recent_list.set_items(self._workspace_repo.list_all())

    def current_settings(self) -> Dict[str, bool]:
        return {
            "fullscreen": self.cb_fullscreen.isChecked(),
            "auto_next": self.cb_auto_next.isChecked(),
            "sound": self.cb_sound.isChecked(),
            "recovery": self.cb_recovery.isChecked(),
        }

    def _browse_source(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_input.setText(folder)
            self._validate_inputs()

    def _browse_dest(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.dest_input.setText(folder)
            self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Enables the Start button only if all required fields are filled and source exists."""
        ws_name = self.workspace_name_input.text().strip()
        src = self.source_input.text().strip()
        dst = self.dest_input.text().strip()
        
        is_valid = bool(ws_name and src and dst)
        
        if is_valid:
            from pathlib import Path
            is_valid = Path(src).exists()
            
        self.start_btn.setEnabled(is_valid)

    def _on_start_clicked(self) -> None:
        payload: Dict[str, Any] = {
            "workspace_name": self.workspace_name_input.text().strip(),
            "source_folder": self.source_input.text().strip(),
            "destination_folder": self.dest_input.text().strip(),
            "settings": self.current_settings(),
        }
        self.start_requested.emit(payload)
