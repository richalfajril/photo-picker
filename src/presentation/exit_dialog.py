"""Exit Confirmation Dialog UI Component."""
from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)


class ExitDialog(QDialog):
    """
    Confirmation dialog shown before leaving the viewer, so an accidental
    Esc doesn't drop the user out of a culling session.
    """

    # Dialog Results
    EXIT = 1
    CANCEL = 2

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Exit Photo Picker")
        self.setModal(True)
        self.setStyleSheet("background-color: #111111; color: #FFFFFF;")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        lbl_title = QLabel("Exit Photo Picker?")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_title)

        lbl_info = QLabel("Your progress is saved automatically.")
        lbl_info.setStyleSheet("font-size: 13px; color: #888888;")
        layout.addWidget(lbl_info)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #444444; }
        """)
        btn_cancel.clicked.connect(lambda: self.done(self.CANCEL))

        btn_exit = QPushButton("Exit")
        btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #DC2626; }
        """)
        btn_exit.clicked.connect(lambda: self.done(self.EXIT))

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_exit)
        layout.addLayout(btn_layout)
