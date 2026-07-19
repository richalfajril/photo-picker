# Recent Workspaces Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let the user see previously-saved workspaces on the Start window and reopen one in a single click, resuming at the last-viewed photo.

**Architecture:** A new `WorkspaceRepository.list_all()` scans the on-disk `workspaces/` directory and returns lightweight `WorkspaceSummary` objects. A new `RecentWorkspacesList` widget renders them below the Start form; clicking a valid row bubbles a `reopen_requested(name)` signal up through `StartWindow` to `main.py`, which loads the workspace and launches the existing `ViewerController(loaded_workspace=...)` path. The viewer layer is untouched.

**Tech Stack:** Python 3.12, PySide6 (Qt Widgets), pytest.

## Global Constraints

- All production code must pass `.venv/bin/ruff check src/` (clean) and `.venv/bin/mypy src/` (no issues).
- Python 3.12; every function has parameter and return type annotations.
- Tests run headless via `QT_QPA_PLATFORM=offscreen` (set in root `conftest.py`).
- Reference spec: `docs/superpowers/specs/2026-07-19-recent-workspaces-design.md`.
- Run all pytest commands from the project root so `src` is importable.

---

## File Structure

- Create: `conftest.py` (root) — sets offscreen Qt platform; provides session `qapp` fixture.
- Create: `tests/test_workspace_repository.py` — tests for `list_all()`.
- Create: `tests/test_time_format.py` — tests for the relative-time helper.
- Create: `tests/test_recent_workspaces_list.py` — tests for the list widget.
- Create: `tests/test_start_window.py` — tests for Start window integration.
- Create: `src/utils/time_format.py` — `format_relative_time()` helper.
- Create: `src/presentation/recent_workspaces_list.py` — `RecentWorkspacesList` widget.
- Modify: `src/repositories/workspace_repository.py` — add `WorkspaceSummary` + `list_all()`.
- Modify: `src/presentation/start_window.py` — embed list, add `current_settings()` + `reopen_requested`, accept injected repo.
- Modify: `src/main.py` — add `on_reopen` handler and wiring.
- Modify: `docs/CHANGELOG.md` — note the feature under `[Unreleased]`.

---

## Task 1: `WorkspaceRepository.list_all()` + test infra

**Files:**
- Create: `conftest.py`
- Modify: `src/repositories/workspace_repository.py`
- Test: `tests/test_workspace_repository.py`

**Interfaces:**
- Consumes: existing `WorkspaceRepository(base_dir: Path = WORKSPACES_DIR)`.
- Produces:
  - `WorkspaceSummary` dataclass with fields `name: str`, `source_folder: str`, `destination_folder: str`, `current_index: int`, `total_images: int`, `updated_at: str`, `source_exists: bool`.
  - `WorkspaceRepository.list_all(self) -> List[WorkspaceSummary]` — sorted by `updated_at` descending (empty timestamps last), skips unparseable files.

- [ ] **Step 1: Create the root conftest (test infra)**

Create `conftest.py` at the project root:

```python
"""Pytest configuration: run Qt tests headless."""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_workspace_repository.py`:

```python
import json
from pathlib import Path

from src.repositories.workspace_repository import WorkspaceRepository, WorkspaceSummary


def _write_workspace(base: Path, slug: str, meta: dict) -> None:
    d = base / slug
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "workspace.json", "w", encoding="utf-8") as f:
        json.dump(meta, f)


def test_list_all_sorted_newest_first(tmp_path):
    _write_workspace(tmp_path, "old", {
        "name": "Old", "source_folder": str(tmp_path),
        "updated_at": "2026-01-01T00:00:00",
    })
    _write_workspace(tmp_path, "new", {
        "name": "New", "source_folder": str(tmp_path),
        "updated_at": "2026-07-01T00:00:00",
    })
    repo = WorkspaceRepository(base_dir=tmp_path)
    result = repo.list_all()
    assert [s.name for s in result] == ["New", "Old"]


def test_list_all_skips_corrupt(tmp_path):
    _write_workspace(tmp_path, "good", {
        "name": "Good", "source_folder": str(tmp_path),
        "updated_at": "2026-07-01T00:00:00",
    })
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "workspace.json").write_text("{ not valid json", encoding="utf-8")
    repo = WorkspaceRepository(base_dir=tmp_path)
    result = repo.list_all()
    assert [s.name for s in result] == ["Good"]


def test_source_exists_reflects_filesystem(tmp_path):
    existing = tmp_path / "src_folder"
    existing.mkdir()
    _write_workspace(tmp_path, "a", {
        "name": "A", "source_folder": str(existing),
        "updated_at": "2026-07-02T00:00:00",
    })
    _write_workspace(tmp_path, "b", {
        "name": "B", "source_folder": str(tmp_path / "gone"),
        "updated_at": "2026-07-01T00:00:00",
    })
    repo = WorkspaceRepository(base_dir=tmp_path)
    by_name = {s.name: s for s in repo.list_all()}
    assert by_name["A"].source_exists is True
    assert by_name["B"].source_exists is False
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_workspace_repository.py -v`
Expected: FAIL with `ImportError: cannot import name 'WorkspaceSummary'`.

- [ ] **Step 4: Implement `WorkspaceSummary` + `list_all()`**

In `src/repositories/workspace_repository.py`, add `dataclass` to the imports:

```python
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
```

Add the summary dataclass just above the `WorkspaceRepository` class:

```python
@dataclass
class WorkspaceSummary:
    """Lightweight, read-only view of a saved workspace for the recent list."""
    name: str
    source_folder: str
    destination_folder: str
    current_index: int
    total_images: int
    updated_at: str
    source_exists: bool
```

Add this method to `WorkspaceRepository` (after `load`):

```python
def list_all(self) -> List[WorkspaceSummary]:
    """
    Scan the workspaces directory and return a summary for each saved workspace,
    sorted by updated_at descending. Unparseable entries are skipped.
    """
    summaries: List[WorkspaceSummary] = []
    for workspace_file in self.base_dir.glob("*/workspace.json"):
        try:
            with open(workspace_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue

        source = meta.get("source_folder", "")
        summaries.append(WorkspaceSummary(
            name=meta.get("name", workspace_file.parent.name),
            source_folder=source,
            destination_folder=meta.get("destination_folder", ""),
            current_index=meta.get("current_index", 0),
            total_images=meta.get("total_images", 0),
            updated_at=meta.get("updated_at", ""),
            source_exists=bool(source) and Path(source).exists(),
        ))

    summaries.sort(key=lambda s: s.updated_at, reverse=True)
    return summaries
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_workspace_repository.py -v`
Expected: PASS (3 passed).

- [ ] **Step 6: Lint & type-check**

Run: `.venv/bin/ruff check src/ && .venv/bin/mypy src/`
Expected: ruff "All checks passed!", mypy "Success".

- [ ] **Step 7: Commit**

```bash
git add conftest.py tests/test_workspace_repository.py src/repositories/workspace_repository.py
git commit -m "feat: add WorkspaceRepository.list_all() and WorkspaceSummary"
```

---

## Task 2: `format_relative_time()` helper

**Files:**
- Create: `src/utils/time_format.py`
- Test: `tests/test_time_format.py`

**Interfaces:**
- Produces: `format_relative_time(iso_timestamp: str, now: Optional[datetime] = None) -> str` — returns `"unknown"`, `"just now"`, `"N minute(s) ago"`, `"N hour(s) ago"`, or `"N day(s) ago"`. The `now` parameter exists for deterministic testing.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_time_format.py`:

```python
from datetime import datetime

from src.utils.time_format import format_relative_time


def test_missing_timestamp_returns_unknown():
    assert format_relative_time("") == "unknown"


def test_unparseable_returns_unknown():
    assert format_relative_time("not-a-date") == "unknown"


def test_seconds_ago_is_just_now():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-19T11:59:30", now=now) == "just now"


def test_minutes_ago_plural():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-19T11:30:00", now=now) == "30 minutes ago"


def test_hours_ago_plural():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-19T09:00:00", now=now) == "3 hours ago"


def test_days_ago_singular():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-18T12:00:00", now=now) == "1 day ago"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_time_format.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.utils.time_format'`.

- [ ] **Step 3: Implement the helper**

Create `src/utils/time_format.py`:

```python
"""Utilities for formatting timestamps into human-readable relative strings."""
from datetime import datetime
from typing import Optional


def format_relative_time(iso_timestamp: str, now: Optional[datetime] = None) -> str:
    """
    Convert an ISO timestamp into a short relative string like "2 days ago".
    Returns "unknown" if the timestamp is missing or unparseable.
    """
    if not iso_timestamp:
        return "unknown"
    try:
        then = datetime.fromisoformat(iso_timestamp)
    except ValueError:
        return "unknown"

    current = now or datetime.now()
    seconds = (current - then).total_seconds()

    if seconds < 60:
        return "just now"

    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    hours = int(minutes // 60)
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    days = int(hours // 24)
    return f"{days} day{'s' if days != 1 else ''} ago"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_time_format.py -v`
Expected: PASS (6 passed).

- [ ] **Step 5: Lint & type-check**

Run: `.venv/bin/ruff check src/ && .venv/bin/mypy src/`
Expected: ruff "All checks passed!", mypy "Success".

- [ ] **Step 6: Commit**

```bash
git add tests/test_time_format.py src/utils/time_format.py
git commit -m "feat: add format_relative_time helper"
```

---

## Task 3: `RecentWorkspacesList` widget

**Files:**
- Create: `src/presentation/recent_workspaces_list.py`
- Modify: `conftest.py` (add `qapp` fixture)
- Test: `tests/test_recent_workspaces_list.py`

**Interfaces:**
- Consumes: `WorkspaceSummary` (Task 1), `format_relative_time` (Task 2).
- Produces:
  - `RecentWorkspacesList(QWidget)` with signal `workspace_selected = Signal(str)`.
  - Method `set_items(self, summaries: List[WorkspaceSummary]) -> None`.
  - Internal layout `self._rows_container` (a `QVBoxLayout`) and `self._empty_label` (a `QLabel`) used by tests.

- [ ] **Step 1: Add the `qapp` fixture to conftest**

Append to `conftest.py`:

```python
import pytest


@pytest.fixture(scope="session")
def qapp():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_recent_workspaces_list.py`:

```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_recent_workspaces_list.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.presentation.recent_workspaces_list'`.

- [ ] **Step 4: Implement the widget**

Create `src/presentation/recent_workspaces_list.py`:

```python
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
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_recent_workspaces_list.py -v`
Expected: PASS (4 passed).

- [ ] **Step 6: Lint & type-check**

Run: `.venv/bin/ruff check src/ && .venv/bin/mypy src/`
Expected: ruff "All checks passed!", mypy "Success".

- [ ] **Step 7: Commit**

```bash
git add conftest.py tests/test_recent_workspaces_list.py src/presentation/recent_workspaces_list.py
git commit -m "feat: add RecentWorkspacesList widget"
```

---

## Task 4: Integrate the list into `StartWindow`

**Files:**
- Modify: `src/presentation/start_window.py`
- Test: `tests/test_start_window.py`

**Interfaces:**
- Consumes: `RecentWorkspacesList` (Task 3), `WorkspaceRepository` (Task 1).
- Produces:
  - `StartWindow.__init__(self, workspace_repo: Optional[WorkspaceRepository] = None)` — optional injection for tests; defaults to a real `WorkspaceRepository()`.
  - `StartWindow.current_settings(self) -> dict[str, bool]` — the four checkbox states.
  - New signal `reopen_requested = Signal(str)`, emitted with the workspace name when a recent row is clicked.
  - Attribute `self.recent_list: RecentWorkspacesList`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_start_window.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_start_window.py -v`
Expected: FAIL — `TypeError` on unexpected `workspace_repo` kwarg (or `AttributeError: current_settings`).

- [ ] **Step 3: Update imports and signals in `start_window.py`**

Replace the import block and class signal declaration. Change the top imports to add `Optional`, the repo, and the widget:

```python
"""
Startup Window UI Component.
"""
from typing import Any, Dict, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QFileDialog, QFormLayout
)
from PySide6.QtCore import Qt, Signal

from src.presentation.recent_workspaces_list import RecentWorkspacesList
from src.repositories.workspace_repository import WorkspaceRepository
```

Add the new signal beside `start_requested`:

```python
    # Signal emitted when start button is clicked
    start_requested = Signal(dict)
    # Signal emitted when a recent workspace row is clicked
    reopen_requested = Signal(str)
```

- [ ] **Step 4: Update `__init__` to accept and use a repo**

Replace the existing `__init__`:

```python
    def __init__(self, workspace_repo: Optional[WorkspaceRepository] = None) -> None:
        super().__init__()
        self.setWindowTitle("Photo Picker - Start")
        self._workspace_repo = workspace_repo or WorkspaceRepository()
        self._setup_ui()
        self._connect_signals()
        self._validate_inputs()
        self._load_recent_workspaces()
```

- [ ] **Step 5: Add the recent list to the layout**

In `_setup_ui`, immediately after `main_layout.addWidget(self.start_btn)` and before `self.setMinimumWidth(500)`, add:

```python
        # Recent Workspaces
        self.recent_list = RecentWorkspacesList()
        main_layout.addWidget(self.recent_list)
```

- [ ] **Step 6: Wire the child signal and add helpers**

In `_connect_signals`, add at the end:

```python
        self.recent_list.workspace_selected.connect(self.reopen_requested.emit)
```

Add these two methods to the class (e.g. after `_connect_signals`):

```python
    def _load_recent_workspaces(self) -> None:
        self.recent_list.set_items(self._workspace_repo.list_all())

    def current_settings(self) -> Dict[str, bool]:
        return {
            "fullscreen": self.cb_fullscreen.isChecked(),
            "auto_next": self.cb_auto_next.isChecked(),
            "sound": self.cb_sound.isChecked(),
            "recovery": self.cb_recovery.isChecked(),
        }
```

- [ ] **Step 7: Make `_on_start_clicked` reuse `current_settings` (DRY)**

Replace the body of `_on_start_clicked`:

```python
    def _on_start_clicked(self) -> None:
        payload: Dict[str, Any] = {
            "workspace_name": self.workspace_name_input.text().strip(),
            "source_folder": self.source_input.text().strip(),
            "destination_folder": self.dest_input.text().strip(),
            "settings": self.current_settings(),
        }
        self.start_requested.emit(payload)
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_start_window.py -v`
Expected: PASS (2 passed).

- [ ] **Step 9: Run the full suite, lint & type-check**

Run: `.venv/bin/pytest -q && .venv/bin/ruff check src/ && .venv/bin/mypy src/`
Expected: all tests pass; ruff "All checks passed!"; mypy "Success".

- [ ] **Step 10: Commit**

```bash
git add tests/test_start_window.py src/presentation/start_window.py
git commit -m "feat: show recent workspaces in the Start window"
```

---

## Task 5: Wire reopen in `main.py` + changelog

**Files:**
- Modify: `src/main.py`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: `StartWindow.reopen_requested` and `StartWindow.current_settings()` (Task 4); existing `WorkspaceRepository.load(name)` and `ViewerController(payload, loaded_workspace=...)`.
- Produces: no new public interface (composition-root wiring).

- [ ] **Step 1: Add the `on_reopen` handler**

In `src/main.py`, inside `main()`, after the existing `window.start_requested.connect(on_start)` line, add the handler and its connection:

```python
    def on_reopen(name: str) -> None:
        global active_controller
        ws = repo.load(name)
        if ws is None:
            return  # folder vanished between listing and click
        payload: dict[str, Any] = {
            "workspace_name": ws.name,
            "source_folder": ws.source_folder,
            "destination_folder": ws.destination_folder,
            "settings": window.current_settings(),
        }
        window.hide()
        active_controller = ViewerController(payload, loaded_workspace=ws)

    window.reopen_requested.connect(on_reopen)
```

(`Any` is already imported in `main.py`; `repo`, `window`, `ViewerController`, and `active_controller` are already in scope.)

- [ ] **Step 2: Verify the app still launches and the list appears (manual smoke test)**

Run: `.venv/bin/python -m src.main`
Expected: the Start window opens showing the form plus a "Recent Workspaces" section (empty placeholder if `storage/workspaces/` has no saved workspaces). Close the window to end. No traceback in the terminal.

- [ ] **Step 3: Update the changelog**

In `docs/CHANGELOG.md`, under `# [Unreleased]` → `## Added`, add one line:

```markdown
- Recent Workspaces: the Start window now lists previously-saved workspaces and reopens one at its last-viewed photo in a single click (`WorkspaceRepository.list_all`, `RecentWorkspacesList`).
```

- [ ] **Step 4: Final verification — full suite, lint, type-check**

Run: `.venv/bin/pytest -q && .venv/bin/ruff check src/ && .venv/bin/mypy src/`
Expected: all tests pass; ruff "All checks passed!"; mypy "Success".

- [ ] **Step 5: Commit**

```bash
git add src/main.py docs/CHANGELOG.md
git commit -m "feat: wire recent-workspace reopen into app entry point"
```

---

## Self-Review

**Spec coverage:**
- §2 scan-the-folder source of truth → Task 1 `list_all()` globs `workspaces/*/workspace.json`. ✅
- §4 `WorkspaceSummary` + skip corrupt + `source_exists` + sort → Task 1 (tests cover all three). ✅
- §5 `RecentWorkspacesList` (signal, `set_items`, name+progress+relative time, greyed missing-source, empty state) → Tasks 2 & 3. ✅
- §6 `main.py` `on_reopen` with live settings + `current_settings()` helper → Tasks 4 & 5. ✅
- §7 error handling: missing source (Task 3 disabled row), corrupt json (Task 1 skip), folder vanished (Task 5 `if ws is None`), empty dir (Task 3 empty state). ✅
- §8 testing: all listed cases mapped to Tasks 1–4. ✅
- §9 out of scope: no delete, no per-workspace settings, no thumbnails, `settings.json.recent_workspaces` left untouched. ✅

**Placeholder scan:** No TBD/TODO; every code step shows complete code. ✅

**Type consistency:** `WorkspaceSummary` fields used identically across Tasks 1/3/4. `list_all()`, `set_items()`, `current_settings()`, `reopen_requested`, `workspace_selected` names consistent across tasks. `format_relative_time` signature matches its consumer in Task 3. ✅
