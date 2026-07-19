"""MVP TEST_PLAN coverage — service & repository layer (no Qt).

Covers TEST_PLAN IDs: LD-001/002/004/006, SL-001/005, UD-001, WS-001/002/003,
ER-002/003/004, WR-001.
"""
import os
import stat

import pytest

from src.services.image_loader_service import ImageLoaderService
from src.services.cache_manager import CacheManager
from src.services.file_operation_service import FileOperationService
from src.repositories.workspace_repository import WorkspaceRepository
from src.domain.workspace import Workspace


# --- Image Loading (LD) --------------------------------------------------

def test_LD001_scan_folder_jpg_finds_all(tmp_path, make_images):
    made = make_images(tmp_path / "src", count=5, fmt="JPEG")
    found = ImageLoaderService.scan_folder(str(tmp_path / "src"))
    assert len(found) == 5
    assert found == sorted(found)  # sorted order
    assert {os.path.basename(p) for p in found} == {os.path.basename(p) for p in made}


def test_LD002_scan_folder_png_finds_all(tmp_path, make_images):
    make_images(tmp_path / "src", count=4, fmt="PNG")
    found = ImageLoaderService.scan_folder(str(tmp_path / "src"))
    assert len(found) == 4
    assert all(p.lower().endswith(".png") for p in found)


def test_LD004_empty_folder_returns_empty_list(tmp_path):
    (tmp_path / "empty").mkdir()
    assert ImageLoaderService.scan_folder(str(tmp_path / "empty")) == []


def test_LD004_missing_folder_returns_empty_list(tmp_path):
    assert ImageLoaderService.scan_folder(str(tmp_path / "does_not_exist")) == []


def test_LD006_cache_returns_same_instance_on_hit(tmp_path, make_images):
    paths = make_images(tmp_path / "src", count=1, fmt="PNG")
    cache = CacheManager(max_memory_items=5)
    first = cache.get_image(paths[0])
    second = cache.get_image(paths[0])
    assert first is not None
    assert first is second  # served from memory cache, not reloaded


# --- Photo Selection / Undo file ops (SL, UD) ----------------------------

def test_SL001_copy_file_copies_to_destination(tmp_path, make_images):
    paths = make_images(tmp_path / "src", count=1)
    dst = tmp_path / "dst"
    ok = FileOperationService.copy_file(paths[0], str(dst))
    assert ok is True
    assert (dst / os.path.basename(paths[0])).exists()


def test_SL005_copy_is_idempotent_no_duplicate(tmp_path, make_images):
    paths = make_images(tmp_path / "src", count=1)
    dst = tmp_path / "dst"
    assert FileOperationService.copy_file(paths[0], str(dst)) is True
    assert FileOperationService.copy_file(paths[0], str(dst)) is True  # already exists
    assert len(list(dst.iterdir())) == 1


def test_UD001_remove_file_deletes_copy_not_original(tmp_path, make_images):
    paths = make_images(tmp_path / "src", count=1)
    dst = tmp_path / "dst"
    FileOperationService.copy_file(paths[0], str(dst))
    copied = dst / os.path.basename(paths[0])
    assert copied.exists()

    ok = FileOperationService.remove_file(paths[0], str(dst))
    assert ok is True
    assert not copied.exists()          # copy removed
    assert os.path.exists(paths[0])     # original untouched


def test_UD001_remove_missing_copy_is_success(tmp_path, make_images):
    paths = make_images(tmp_path / "src", count=1)
    assert FileOperationService.remove_file(paths[0], str(tmp_path / "dst")) is True


# --- Error Handling (ER) -------------------------------------------------

def test_ER004_unsupported_formats_are_skipped(tmp_path, make_images):
    src = tmp_path / "src"
    make_images(src, count=2, fmt="JPEG")
    (src / "notes.txt").write_text("not an image", encoding="utf-8")
    (src / "archive.zip").write_bytes(b"PK\x03\x04")
    found = ImageLoaderService.scan_folder(str(src))
    assert len(found) == 2
    assert all(p.lower().endswith(".jpg") for p in found)


def test_ER003_corrupt_image_returns_none_not_crash(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    bad = src / "broken.jpg"
    bad.write_bytes(b"this is not a real jpeg")
    # scan still lists it (extension-based), but load degrades to None
    assert str(bad) in ImageLoaderService.scan_folder(str(src))
    assert ImageLoaderService.load_image(str(bad)) is None


@pytest.mark.skipif(os.getuid() == 0, reason="root bypasses filesystem permissions")
def test_ER002_unwritable_destination_returns_false(tmp_path, make_images):
    paths = make_images(tmp_path / "src", count=1)
    dst = tmp_path / "readonly"
    dst.mkdir()
    os.chmod(dst, stat.S_IREAD | stat.S_IEXEC)  # r-x, no write
    try:
        ok = FileOperationService.copy_file(paths[0], str(dst))
        assert ok is False
    finally:
        os.chmod(dst, stat.S_IRWXU)  # restore so tmp cleanup works


# --- Workspace persistence (WS, WR) --------------------------------------

def test_WS001_save_creates_workspace_files(tmp_path):
    repo = WorkspaceRepository(base_dir=tmp_path / "store")
    ws = Workspace(name="Wedding", source_folder="/s", destination_folder="/d")
    repo.save(ws)
    slug_dir = (tmp_path / "store" / "wedding")
    assert (slug_dir / "workspace.json").exists()
    assert (slug_dir / "selections.json").exists()


def test_WS002_load_roundtrips_fields(tmp_path):
    repo = WorkspaceRepository(base_dir=tmp_path / "store")
    ws = Workspace(name="Trip", source_folder="/s", destination_folder="/d",
                   current_index=7, total_images=42)
    ws.selected_images = ["/s/a.jpg", "/s/b.jpg"]
    repo.save(ws)

    loaded = repo.load("Trip")
    assert loaded is not None
    assert loaded.name == "Trip"
    assert loaded.source_folder == "/s"
    assert loaded.destination_folder == "/d"
    assert loaded.current_index == 7
    assert loaded.total_images == 42
    assert loaded.selected_images == ["/s/a.jpg", "/s/b.jpg"]


def test_WS003_WR001_save_persists_progress_and_selection(tmp_path):
    repo = WorkspaceRepository(base_dir=tmp_path / "store")
    ws = Workspace(name="Shoot", source_folder="/s", destination_folder="/d")
    ws.current_index = 3
    ws.selected_images = ["/s/x.jpg"]
    repo.save(ws)

    reloaded = repo.load("Shoot")
    assert reloaded is not None
    assert reloaded.current_index == 3
    assert reloaded.selected_images == ["/s/x.jpg"]


def test_WS002_load_missing_returns_none(tmp_path):
    repo = WorkspaceRepository(base_dir=tmp_path / "store")
    assert repo.load("nope") is None
