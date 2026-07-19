# Recent Workspaces — Design Spec

**Date:** 2026-07-19
**Target release:** v0.2.0
**Status:** Approved (design), pending implementation plan

---

## 1. Problem

Today the Start window only supports creating a *new* workspace by typing a name and
browsing for source/destination folders. The only way to return to a previous workspace is
to re-type its exact name with the "Workspace Recovery" checkbox enabled. Every workspace is
already persisted to disk (`workspaces/<slug>/workspace.json` + `selections.json`), but that
history is invisible in the UI.

**Goal:** Let the user see previously-used workspaces on the Start window and reopen one with
a single click, resuming at the last-viewed photo.

---

## 2. Decisions (locked)

| Question | Decision |
| --- | --- |
| Source of truth for the list | **Scan the workspaces directory** — the folders on disk *are* the recent list. No duplicate state in `settings.json`. |
| UI placement | **List panel below the form** in `StartWindow`. |
| Reopen behavior | **Resume immediately** at saved `current_index` — no Recovery dialog (the list already implies "continue"). |
| Settings on reopen | **Use current checkbox states** (fullscreen / auto-next / sound) at click time. No per-workspace settings storage. |
| Missing source folder | **Show the row greyed** with a `⚠ source missing` warning; launch is blocked for that row. |
| Delete from list | **Out of scope (YAGNI).** |
| Component structure | Recent list lives in its **own `RecentWorkspacesList` widget**, separate from `StartWindow`. |
| Per-row metadata | Show **name + progress + relative "last opened"** (e.g. "2 days ago"). |

---

## 3. Architecture & data flow

```
StartWindow.__init__
  └─ WorkspaceRepository.list_all() ──> [WorkspaceSummary, ...]   (sorted by updated_at, newest first)
        └─ RecentWorkspacesList.set_items(summaries) renders rows
              └─ valid row clicked ─> RecentWorkspacesList emits workspace_selected(name)
                    └─ StartWindow re-emits reopen_requested(name)
                          └─ main.on_reopen(name):
                                ws = repo.load(name)
                                payload = { workspace fields + live checkbox settings }
                                ViewerController(payload, loaded_workspace=ws)
```

No changes to `ViewerController`, `Workspace`, or the viewer layer — the existing
`ViewerController(payload, loaded_workspace=...)` path is reused.

---

## 4. Data layer — `WorkspaceRepository.list_all()`

New method on `WorkspaceRepository` returning lightweight summaries (selections are **not**
loaded for the list — only `workspace.json` is read).

```python
@dataclass
class WorkspaceSummary:
    name: str
    source_folder: str
    destination_folder: str
    current_index: int
    total_images: int
    updated_at: str        # ISO string as stored in workspace.json
    source_exists: bool     # Path(source_folder).exists()
```

Behavior:
- Glob `self.base_dir/*/workspace.json`.
- Read + `json.load` each; on any parse/IO error, **skip that entry silently** (self-healing —
  consistent with the folder-is-source-of-truth decision).
- Compute `source_exists = Path(source_folder).exists()` (empty string ⇒ `False`).
- Return the list sorted by `updated_at` descending. Entries with a missing/empty `updated_at`
  sort last.

`WorkspaceSummary` lives alongside the repository (or in `src/domain/`) — decided during
plan-writing to match existing conventions.

---

## 5. UI — `RecentWorkspacesList` (new component)

New widget in `src/presentation/recent_workspaces_list.py`.

- **Signal:** `workspace_selected = Signal(str)` — emits the workspace `name` on a valid click.
- **API:** `set_items(summaries: list[WorkspaceSummary]) -> None` to (re)populate.
- **Row content:** `name`  ·  `current_index / total_images`  ·  relative "last opened"
  (derived from `updated_at`; helper formats e.g. "just now", "2 hours ago", "3 days ago").
- **Missing source:** rows with `source_exists == False` are greyed, show `⚠ source missing`,
  and do **not** emit `workspace_selected` on click.
- **Empty state:** muted placeholder text "No recent workspaces yet".
- Scrollable when the list is long.

`StartWindow` changes:
- Instantiate `RecentWorkspacesList`, populate it via `WorkspaceRepository.list_all()` in
  `__init__`, and add it below the START button under a "Recent Workspaces" heading.
- Add signal `reopen_requested = Signal(str)`; connect the child's `workspace_selected` to
  re-emit it.

---

## 6. Launch wiring — `main.py`

Add an `on_reopen(name)` handler beside the existing `on_start`:

```python
def on_reopen(name: str) -> None:
    global active_controller
    ws = repo.load(name)
    if ws is None:
        return  # defensive: folder vanished between listing and click
    payload = {
        "workspace_name": ws.name,
        "source_folder": ws.source_folder,
        "destination_folder": ws.destination_folder,
        "settings": window.current_settings(),  # live checkbox states
    }
    window.hide()
    active_controller = ViewerController(payload, loaded_workspace=ws)

window.reopen_requested.connect(on_reopen)
```

`StartWindow` exposes a small `current_settings()` helper returning the checkbox dict (the
same structure already built in `_on_start_clicked`), so both flows share one source.

---

## 7. Error handling

| Case | Handling |
| --- | --- |
| Source folder missing | Row greyed + `⚠ source missing`; click is a no-op. |
| Corrupt / partial `workspace.json` | Skipped silently by `list_all()`. |
| Workspace folder deleted between listing and click | `repo.load()` returns `None`; `on_reopen` returns early (no crash). |
| Empty workspaces directory | `RecentWorkspacesList` shows empty-state placeholder. |

---

## 8. Testing (pytest)

Using a temporary workspaces directory injected into `WorkspaceRepository(base_dir=...)`:

- `list_all()` returns summaries sorted newest-first by `updated_at`.
- `list_all()` skips a corrupt `workspace.json` without raising.
- `source_exists` is `True` when the folder exists, `False` when it doesn't / is empty.
- Relative-time helper formats representative deltas correctly.
- `RecentWorkspacesList` emits `workspace_selected` with the right name on a valid row, and
  does **not** emit for a `source_exists == False` row.

---

## 9. Out of scope (YAGNI)

- Deleting / removing workspaces from the list.
- Per-workspace settings persistence.
- Thumbnails / previews.
- Search / filter / pagination.
- Populating or reading the `recent_workspaces` array in `settings.json` (kept unused; the
  scan-the-folder approach supersedes it).
