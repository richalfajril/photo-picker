"""Recent Workspaces list widget for the Start window."""
from typing import List

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal

from src.repositories.workspace_repository import WorkspaceSummary
from src.utils.time_format import format_relative_time


class RecentWorkspacesList(QWidget):
    """
    Displays previously-saved workspaces. Emits workspace_selected(name)
    when a workspace whose source folder still exists is clicked.
    """

    workspace_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        heading = QLabel("Recent Workspaces")
        heading.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(heading)

        self._rows_container = QVBoxLayout()
        self._rows_container.setSpacing(4)
        layout.addLayout(self._rows_container)

        self._empty_label = QLabel("No recent workspaces yet")
        self._empty_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self._empty_label)

    def set_items(self, summaries: List[WorkspaceSummary]) -> None:
        """(Re)populate the list from workspace summaries."""
        while self._rows_container.count():
            item = self._rows_container.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self._empty_label.setVisible(len(summaries) == 0)

        for summary in summaries:
            self._rows_container.addWidget(self._build_row(summary))

    def _build_row(self, summary: WorkspaceSummary) -> QPushButton:
        if summary.source_exists:
            label = (
                f"{summary.name}    "
                f"{summary.current_index} / {summary.total_images}    "
                f"{format_relative_time(summary.updated_at)}"
            )
            btn = QPushButton(label)
            btn.setStyleSheet("text-align: left; padding: 8px;")
            btn.clicked.connect(lambda: self.workspace_selected.emit(summary.name))
            return btn

        btn = QPushButton(f"⚠ {summary.name}  (source missing)")
        btn.setEnabled(False)
        btn.setStyleSheet("text-align: left; padding: 8px; color: gray;")
        return btn
