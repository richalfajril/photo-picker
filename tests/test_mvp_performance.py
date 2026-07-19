"""MVP TEST_PLAN coverage — performance (functional proxies).

These verify the scan/handle path stays correct and completes quickly at
modest volumes. Large-scale cases (PF-003 10k, PF-004 50k) require a real
dataset and are tracked as manual in the results matrix.

Covers TEST_PLAN IDs: PF-001 (100), PF-002 (1000).
"""
import time

from src.services.image_loader_service import ImageLoaderService


def test_PF001_scan_100_images(tmp_path, make_images):
    make_images(tmp_path / "src", count=100, fmt="JPEG", size=(16, 16))
    start = time.perf_counter()
    found = ImageLoaderService.scan_folder(str(tmp_path / "src"))
    elapsed = time.perf_counter() - start
    assert len(found) == 100
    assert found == sorted(found)
    assert elapsed < 2.0  # generous headroom; scan is a directory listing


def test_PF002_scan_1000_images(tmp_path, make_images):
    make_images(tmp_path / "src", count=1000, fmt="JPEG", size=(8, 8))
    start = time.perf_counter()
    found = ImageLoaderService.scan_folder(str(tmp_path / "src"))
    elapsed = time.perf_counter() - start
    assert len(found) == 1000
    assert elapsed < 5.0
