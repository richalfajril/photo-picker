"""MVP TEST_PLAN coverage — presentation widgets (Qt, headless).

Covers TEST_PLAN IDs: ST-002/003/005, VW-002/003/004/005/006, SL-004, UD-004,
KB-001/002/003/004/005/006, ZP-001/002/003, OV-001/002/003, WR-002(dialog build),
WR-003/004(result constants).
"""
from PySide6.QtGui import QImage, QKeyEvent, QWheelEvent
from PySide6.QtCore import Qt, QEvent, QPoint, QPointF

from src.presentation.viewer_window import ViewerWindow, PhotoGraphicsView
from src.presentation.start_window import StartWindow
from src.presentation.recovery_dialog import RecoveryDialog
from src.presentation.exit_dialog import ExitDialog
from src.services.overlay_manager import OverlayManager
from src.repositories.workspace_repository import WorkspaceRepository
from src.domain.workspace import Workspace


def _solid_image(w=80, h=40):
    img = QImage(w, h, QImage.Format.Format_RGB32)
    img.fill(0xFF3366)
    return img


# --- Viewer info bar (VW, SL-004, UD-004) --------------------------------

def test_VW002_003_004_labels_reflect_set_image(qapp):
    vw = ViewerWindow()
    vw.set_image(_solid_image(), filename="beach.jpg", current=3, total=10,
                 selected=2, is_selected=False)
    assert vw.lbl_filename.text() == "beach.jpg"      # VW-002
    assert vw.lbl_progress.text() == "3 / 10"          # VW-003
    assert vw.lbl_selected.text() == "Selected: 2"     # VW-004


def test_SL004_badge_shows_when_selected(qapp):
    vw = ViewerWindow()
    vw.set_image(_solid_image(), "a.jpg", 1, 5, 1, is_selected=True)
    assert vw.lbl_badge.isHidden() is False


def test_UD004_badge_hides_when_not_selected(qapp):
    vw = ViewerWindow()
    vw.set_image(_solid_image(), "a.jpg", 1, 5, 1, is_selected=True)
    vw.set_image(_solid_image(), "a.jpg", 1, 5, 0, is_selected=False)
    assert vw.lbl_badge.isHidden() is True


def test_VW005_006_aspect_ratio_uniform_scale(qapp):
    # KeepAspectRatio => uniform scale (m11 == m22), no distortion, for both
    # landscape and portrait source images.
    for w, h in [(120, 40), (40, 120)]:
        pv = PhotoGraphicsView()
        pv.resize(200, 200)
        pv.set_image(_solid_image(w, h))
        t = pv.transform()
        assert abs(t.m11() - t.m22()) < 1e-6


# --- Keyboard navigation (KB) --------------------------------------------

def _press(widget, key):
    ev = QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
    widget.keyPressEvent(ev)


def test_KB001_to_004_navigation_signals(qapp):
    vw = ViewerWindow()
    fired = []
    vw.next_requested.connect(lambda: fired.append("next"))
    vw.prev_requested.connect(lambda: fired.append("prev"))
    vw.first_requested.connect(lambda: fired.append("first"))
    vw.last_requested.connect(lambda: fired.append("last"))

    _press(vw, Qt.Key.Key_Right)
    _press(vw, Qt.Key.Key_Left)
    _press(vw, Qt.Key.Key_Home)
    _press(vw, Qt.Key.Key_End)
    assert fired == ["next", "prev", "first", "last"]


def test_KB005_f_toggles_fullscreen_flag(qapp):
    vw = ViewerWindow()
    before = vw._is_fullscreen
    _press(vw, Qt.Key.Key_F)
    assert vw._is_fullscreen != before


def test_KB006_escape_emits_exit_when_windowed(qapp):
    # NOTE: implementation emits exit_requested (controller closes the window);
    # TEST_PLAN's "Exit Dialog muncul" is not implemented — see results matrix.
    vw = ViewerWindow()
    fired = []
    vw.exit_requested.connect(lambda: fired.append("exit"))
    _press(vw, Qt.Key.Key_Escape)
    assert fired == ["exit"]


def test_KB_space_and_backspace_emit_copy_and_undo(qapp):
    vw = ViewerWindow()
    fired = []
    vw.copy_requested.connect(lambda: fired.append("copy"))
    vw.undo_requested.connect(lambda: fired.append("undo"))
    _press(vw, Qt.Key.Key_Space)
    _press(vw, Qt.Key.Key_Backspace)
    assert fired == ["copy", "undo"]


# --- Zoom (ZP) -----------------------------------------------------------

def _wheel(view, delta_y):
    pos = QPointF(view.viewport().rect().center())
    return QWheelEvent(
        pos, view.mapToGlobal(pos.toPoint()),
        QPoint(0, delta_y), QPoint(0, delta_y),
        Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier,
        Qt.ScrollPhase.NoScrollPhase, False,
    )


def test_ZP001_scroll_up_zooms_in(qapp):
    pv = PhotoGraphicsView()
    pv.resize(200, 200)
    pv.set_image(_solid_image())
    base = pv._zoom_level
    pv.wheelEvent(_wheel(pv, 120))
    assert pv._zoom_level > base


def test_ZP002_scroll_down_zooms_out(qapp):
    pv = PhotoGraphicsView()
    pv.resize(200, 200)
    pv.set_image(_solid_image())
    base = pv._zoom_level
    pv.wheelEvent(_wheel(pv, -120))
    assert pv._zoom_level < base


def test_ZP003_reset_zoom_returns_to_one(qapp):
    pv = PhotoGraphicsView()
    pv.resize(200, 200)
    pv.set_image(_solid_image())
    pv.wheelEvent(_wheel(pv, 120))
    pv.reset_zoom()
    assert pv._zoom_level == 1.0


# --- Overlay (OV) --------------------------------------------------------

def test_OV001_002_003_overlay_shows_text(qapp):
    from PySide6.QtWidgets import QWidget
    parent = QWidget()
    om = OverlayManager(parent)
    for text in ("COPIED", "REMOVED", "COPY FAILED"):
        om.show_overlay(text, "#22C55E")
        assert om.label.text() == text
        assert om.label.isHidden() is False


def test_OV004_overlay_duration_within_spec(qapp):
    from PySide6.QtWidgets import QWidget
    om = OverlayManager(QWidget())
    om.show_overlay("COPIED")
    om._start_fade_out()
    total = om.timer.interval() + om.fade_anim.duration()
    assert om.timer.interval() == OverlayManager.VISIBLE_MS
    assert om.fade_anim.duration() == OverlayManager.FADE_MS
    assert 250 <= total <= 320  # TEST_PLAN OV-004 (~250-300ms)


# --- Startup validation (ST) ---------------------------------------------

def _blank_repo(tmp_path):
    return WorkspaceRepository(base_dir=tmp_path / "store")


def test_ST002_start_disabled_when_name_empty(qapp, tmp_path):
    w = StartWindow(workspace_repo=_blank_repo(tmp_path))
    w.source_input.setText(str(tmp_path))
    w.dest_input.setText(str(tmp_path))
    w.workspace_name_input.setText("")
    w._validate_inputs()
    assert w.start_btn.isEnabled() is False


def test_ST003_start_disabled_when_source_empty(qapp, tmp_path):
    w = StartWindow(workspace_repo=_blank_repo(tmp_path))
    w.workspace_name_input.setText("X")
    w.dest_input.setText(str(tmp_path))
    w.source_input.setText("")
    w._validate_inputs()
    assert w.start_btn.isEnabled() is False


def test_ST004_start_disabled_when_dest_empty(qapp, tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    w = StartWindow(workspace_repo=_blank_repo(tmp_path))
    w.workspace_name_input.setText("X")
    w.source_input.setText(str(src))
    w.dest_input.setText("")
    w._validate_inputs()
    assert w.start_btn.isEnabled() is False


def test_ST005_start_enabled_when_all_valid(qapp, tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    w = StartWindow(workspace_repo=_blank_repo(tmp_path))
    w.workspace_name_input.setText("Wedding")
    w.source_input.setText(str(src))
    w.dest_input.setText(str(tmp_path / "dst"))
    w._validate_inputs()
    assert w.start_btn.isEnabled() is True


def test_ER001_start_disabled_when_source_missing(qapp, tmp_path):
    w = StartWindow(workspace_repo=_blank_repo(tmp_path))
    w.workspace_name_input.setText("Wedding")
    w.source_input.setText(str(tmp_path / "ghost"))  # does not exist
    w.dest_input.setText(str(tmp_path / "dst"))
    w._validate_inputs()
    assert w.start_btn.isEnabled() is False


# --- Recovery dialog (WR) ------------------------------------------------

def test_WR002_dialog_builds_with_workspace(qapp):
    ws = Workspace(name="W", source_folder="/s", destination_folder="/d",
                   current_index=4, total_images=20)
    dlg = RecoveryDialog(ws)
    assert dlg.workspace is ws


def test_WR003_004_result_constants(qapp):
    assert RecoveryDialog.CONTINUE == 1
    assert RecoveryDialog.START_NEW == 2


# --- Exit dialog (KB-006) ------------------------------------------------

def test_KB006_exit_dialog_builds_and_has_result_constants(qapp):
    dlg = ExitDialog()
    assert dlg.EXIT == 1
    assert dlg.CANCEL == 2
    assert dlg.isModal() is True
