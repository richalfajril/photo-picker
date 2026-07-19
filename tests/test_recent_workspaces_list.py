from src.repositories.workspace_repository import WorkspaceSummary
from src.presentation.recent_workspaces_list import RecentWorkspacesList


def _summary(name: str, source_exists: bool = True) -> WorkspaceSummary:
    return WorkspaceSummary(
        name=name, source_folder="/x", destination_folder="/y",
        current_index=1, total_images=10, updated_at="2026-07-19T12:00:00",
        source_exists=source_exists,
    )


def test_valid_row_emits_workspace_selected(qapp):
    widget = RecentWorkspacesList()
    widget.set_items([_summary("Wedding")])
    received = []
    widget.workspace_selected.connect(received.append)

    row = widget._rows_container.itemAt(0).widget()
    row.click()

    assert received == ["Wedding"]


def test_missing_source_row_does_not_emit(qapp):
    widget = RecentWorkspacesList()
    widget.set_items([_summary("Gone", source_exists=False)])
    received = []
    widget.workspace_selected.connect(received.append)

    row = widget._rows_container.itemAt(0).widget()
    row.click()  # disabled button: no effect

    assert received == []


def test_empty_state_shown_when_no_items(qapp):
    widget = RecentWorkspacesList()
    widget.set_items([])
    assert widget._empty_label.isHidden() is False


def test_empty_state_hidden_when_items_present(qapp):
    widget = RecentWorkspacesList()
    widget.set_items([_summary("Wedding")])
    assert widget._empty_label.isHidden() is True
