"""MVP TEST_PLAN coverage — ViewerController orchestration (Qt, headless).

The real ViewerController is driven end-to-end; its WorkspaceRepository is
monkeypatched to a temp store so tests never touch real app storage.

Covers TEST_PLAN IDs: SL-001/002/003, UD-001/002/003/004, SD-001/003,
OV-001/002/003 (via controller), ER-003, WR-003/004, WS-004.
"""
import os

import pytest

from src.controllers import viewer_controller as vc_mod
from src.repositories.workspace_repository import WorkspaceRepository
from src.domain.workspace import Workspace


DEFAULT_SETTINGS = {"fullscreen": False, "auto_next": False, "sound": False, "recovery": False}


@pytest.fixture
def make_controller(qapp, monkeypatch, tmp_path, make_images):
    store = tmp_path / "store"

    def _make(count=3, settings=None, loaded_workspace=None, extra_corrupt=False):
        src = tmp_path / "source"
        paths = make_images(src, count=count)
        if extra_corrupt:
            corrupt = src / "zzz_broken.jpg"  # sorts last
            corrupt.write_bytes(b"not a jpeg")
            paths.append(str(corrupt))
        dst = tmp_path / "dest"

        monkeypatch.setattr(vc_mod, "WorkspaceRepository",
                            lambda: WorkspaceRepository(base_dir=store))

        payload = {
            "workspace_name": loaded_workspace.name if loaded_workspace else "T",
            "source_folder": str(src),
            "destination_folder": str(dst),
            "settings": settings or dict(DEFAULT_SETTINGS),
        }
        ctrl = vc_mod.ViewerController(payload, loaded_workspace=loaded_workspace)
        return ctrl, paths, dst, store

    return _make


def _loaded_ws(name, src, index, total):
    return Workspace(name=name, source_folder=str(src), destination_folder="",
                     current_index=index, total_images=total)


# --- Selection (SL) ------------------------------------------------------

def test_SL001_space_copies_current_file(make_controller):
    ctrl, paths, dst, _ = make_controller(count=3)
    ctrl.copy_image()
    assert (dst / os.path.basename(paths[0])).exists()
    assert ctrl.workspace.selected_images == [paths[0]]


def test_SL002_auto_next_advances_after_copy(make_controller):
    settings = dict(DEFAULT_SETTINGS, auto_next=True)
    ctrl, paths, dst, _ = make_controller(count=3, settings=settings)
    assert ctrl.workspace.current_index == 0
    ctrl.copy_image()
    assert ctrl.workspace.current_index == 1  # advanced


def test_SL003_counter_increments_on_copy(make_controller):
    ctrl, paths, dst, _ = make_controller(count=3)
    ctrl.copy_image()
    assert len(ctrl.workspace.selected_images) == 1
    assert ctrl.viewer_window.lbl_selected.text() == "Selected: 1"


def test_SL005_copy_twice_does_not_duplicate(make_controller):
    ctrl, paths, dst, _ = make_controller(count=3)
    ctrl.copy_image()
    ctrl.copy_image()  # same photo, already selected -> no-op
    assert ctrl.workspace.selected_images == [paths[0]]
    assert len(list(dst.iterdir())) == 1


def test_OV001_copy_shows_copied_overlay(make_controller):
    ctrl, paths, dst, _ = make_controller(count=2)
    ctrl.copy_image()
    assert ctrl.overlay_manager.label.text() == "COPIED"


# --- Undo (UD) -----------------------------------------------------------

def test_UD001_002_003_undo_removes_file_and_counter(make_controller):
    ctrl, paths, dst, _ = make_controller(count=3)
    ctrl.copy_image()
    copied = dst / os.path.basename(paths[0])
    assert copied.exists()

    ctrl.undo_image()
    assert not copied.exists()                       # UD-001
    assert ctrl.workspace.selected_images == []      # UD-002 counter back to 0
    assert ctrl.workspace.current_index == 0         # UD-003 stays on current photo
    assert os.path.exists(paths[0])                  # original untouched


def test_UD004_badge_hidden_after_undo(make_controller):
    ctrl, paths, dst, _ = make_controller(count=3)
    ctrl.copy_image()
    ctrl.undo_image()
    assert ctrl.viewer_window.lbl_badge.isHidden() is True


def test_OV002_undo_shows_removed_overlay(make_controller):
    ctrl, paths, dst, _ = make_controller(count=2)
    ctrl.copy_image()
    ctrl.undo_image()
    assert ctrl.overlay_manager.label.text() == "REMOVED"


# --- Overlay failure path (OV-003) ---------------------------------------

def test_OV003_copy_failure_shows_failed_overlay(make_controller, monkeypatch):
    monkeypatch.setattr(vc_mod.FileOperationService, "copy_file",
                        lambda src, dst: False)
    ctrl, paths, dst, _ = make_controller(count=2)
    ctrl.copy_image()
    assert ctrl.overlay_manager.label.text() == "COPY FAILED"
    assert ctrl.workspace.selected_images == []


# --- Sound feedback (SD) -------------------------------------------------

def test_SD001_sound_on_beeps_on_copy(make_controller, monkeypatch):
    beeps = []
    monkeypatch.setattr(vc_mod.QApplication, "beep", lambda: beeps.append(1))
    settings = dict(DEFAULT_SETTINGS, sound=True)
    ctrl, paths, dst, _ = make_controller(count=2, settings=settings)
    ctrl.copy_image()
    assert len(beeps) >= 1


def test_SD002_sound_on_beeps_on_undo(make_controller, monkeypatch):
    beeps = []
    monkeypatch.setattr(vc_mod.QApplication, "beep", lambda: beeps.append(1))
    settings = dict(DEFAULT_SETTINGS, sound=True)
    ctrl, paths, dst, _ = make_controller(count=2, settings=settings)
    ctrl.copy_image()
    ctrl.undo_image()
    assert len(beeps) >= 2  # one for copy, one for undo


def test_SD003_sound_off_is_silent_on_copy(make_controller, monkeypatch):
    beeps = []
    monkeypatch.setattr(vc_mod.QApplication, "beep", lambda: beeps.append(1))
    settings = dict(DEFAULT_SETTINGS, sound=False)
    ctrl, paths, dst, _ = make_controller(count=2, settings=settings)
    ctrl.copy_image()
    assert beeps == []


# --- Error handling: corrupt image (ER-003) ------------------------------

def test_ER003_corrupt_image_does_not_crash_navigation(make_controller):
    ctrl, paths, dst, _ = make_controller(count=1, extra_corrupt=True)
    # index 0 is valid; index 1 is the corrupt file (sorts last)
    ctrl.next_image()
    assert ctrl.workspace.current_index == 1  # navigated onto corrupt frame, no crash
    ctrl.prev_image()                          # and can navigate back off it
    assert ctrl.workspace.current_index == 0


# --- Exit confirmation (KB-006) ------------------------------------------

def test_KB006_exit_confirmed_closes_viewer(make_controller, monkeypatch):
    ctrl, paths, dst, _ = make_controller(count=2)
    closed = []
    monkeypatch.setattr(ctrl.viewer_window, "close", lambda: closed.append(1))
    # Simulate the user choosing "Exit" in the dialog (exec returns EXIT).
    monkeypatch.setattr(vc_mod.ExitDialog, "exec",
                        lambda self: vc_mod.ExitDialog.EXIT)
    ctrl.exit_app()
    assert closed == [1]


def test_KB006_exit_cancelled_keeps_viewer_open(make_controller, monkeypatch):
    ctrl, paths, dst, _ = make_controller(count=2)
    closed = []
    monkeypatch.setattr(ctrl.viewer_window, "close", lambda: closed.append(1))
    monkeypatch.setattr(vc_mod.ExitDialog, "exec",
                        lambda self: vc_mod.ExitDialog.CANCEL)
    ctrl.exit_app()
    assert closed == []  # cancelled -> viewer stays open


# --- Workspace recovery resume (WR) --------------------------------------

def test_WR003_resume_restores_saved_index(make_controller, tmp_path, make_images):
    src = tmp_path / "source"
    make_images(src, count=4)
    loaded = _loaded_ws("Resume", src, index=2, total=4)
    ctrl, paths, dst, _ = make_controller(count=4, loaded_workspace=loaded)
    assert ctrl.workspace.current_index == 2


def test_WR003_stale_index_is_clamped(make_controller, tmp_path, make_images):
    src = tmp_path / "source"
    make_images(src, count=3)
    loaded = _loaded_ws("Stale", src, index=99, total=50)  # folder now smaller
    ctrl, paths, dst, _ = make_controller(count=3, loaded_workspace=loaded)
    assert ctrl.workspace.current_index == 2  # clamped to last valid index


def test_WR004_start_new_begins_at_zero(make_controller):
    ctrl, paths, dst, _ = make_controller(count=3, loaded_workspace=None)
    assert ctrl.workspace.current_index == 0


# --- Lazy loading, no blocking wait (LD-005) -----------------------------

def test_LD005_does_not_load_all_images_into_cache(make_controller):
    # Lazy design: the viewer opens without loading every image; the memory
    # cache is bounded (LRU eviction), so a large folder never fully loads.
    ctrl, paths, dst, _ = make_controller(count=20)
    assert len(paths) == 20
    cached = len(ctrl.cache_manager._memory_cache)
    assert cached <= ctrl.cache_manager.max_memory_items  # bounded
    assert cached < len(paths)                            # not all loaded


# --- Auto-save on navigation (WS-004) ------------------------------------

def test_WS004_progress_autosaved_on_navigation(make_controller):
    ctrl, paths, dst, store = make_controller(count=3)
    ctrl.next_image()  # index -> 1, triggers save
    reloaded = WorkspaceRepository(base_dir=store).load(ctrl.workspace.name)
    assert reloaded is not None
    assert reloaded.current_index == 1
