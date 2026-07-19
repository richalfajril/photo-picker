import json
from pathlib import Path

from src.repositories.workspace_repository import WorkspaceRepository


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


def test_list_all_skips_non_dict_json(tmp_path):
    _write_workspace(tmp_path, "good", {
        "name": "Good", "source_folder": str(tmp_path),
        "updated_at": "2026-07-01T00:00:00",
    })
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "workspace.json").write_text("null", encoding="utf-8")
    repo = WorkspaceRepository(base_dir=tmp_path)
    result = repo.list_all()
    assert [s.name for s in result] == ["Good"]


def test_list_all_empty_updated_at_sorts_last(tmp_path):
    _write_workspace(tmp_path, "dated", {
        "name": "Dated", "source_folder": str(tmp_path),
        "updated_at": "2026-07-01T00:00:00",
    })
    _write_workspace(tmp_path, "nodate", {
        "name": "NoDate", "source_folder": str(tmp_path),
    })
    repo = WorkspaceRepository(base_dir=tmp_path)
    result = repo.list_all()
    assert [s.name for s in result] == ["Dated", "NoDate"]
