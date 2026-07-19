import json

from src.presentation.start_window import StartWindow
from src.repositories.workspace_repository import WorkspaceRepository


def test_current_settings_returns_checkbox_states(qapp, tmp_path):
    window = StartWindow(workspace_repo=WorkspaceRepository(base_dir=tmp_path))
    window.cb_fullscreen.setChecked(True)
    window.cb_auto_next.setChecked(False)
    window.cb_sound.setChecked(True)
    window.cb_recovery.setChecked(False)

    assert window.current_settings() == {
        "fullscreen": True,
        "auto_next": False,
        "sound": True,
        "recovery": False,
    }


def test_reopen_requested_emitted_from_recent_list(qapp, tmp_path):
    d = tmp_path / "wedding"
    d.mkdir()
    (d / "workspace.json").write_text(json.dumps({
        "name": "Wedding", "source_folder": str(tmp_path),
        "current_index": 3, "total_images": 20,
        "updated_at": "2026-07-19T12:00:00",
    }), encoding="utf-8")

    window = StartWindow(workspace_repo=WorkspaceRepository(base_dir=tmp_path))
    received = []
    window.reopen_requested.connect(received.append)

    row = window.recent_list._rows_container.itemAt(0).widget()
    row.click()

    assert received == ["Wedding"]
