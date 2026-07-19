# TEST_PLAN.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini berisi seluruh skenario pengujian untuk memastikan setiap fitur pada Photo Picker MVP bekerja sesuai spesifikasi.

Semula seluruh test dirancang sebagai Manual Testing. Pada 2026-07-19 sebagian besar kasus dengan inti logika telah **diotomatiskan** (pytest, headless Qt) sehingga menjadi regression suite; sisanya tetap memerlukan verifikasi manual (visual/audio/GUI) atau aset khusus.

---

# 1a. Results Summary (2026-07-19)

**Legend:**

| Symbol | Arti |
| ------ | ---- |
| ✅ | Automated — terverifikasi oleh pytest (lihat Coverage Map §1b) |
| 👤 | Manual — perlu manusia di GUI (dialog/visual) |
| 🎨 | Manual (visual/interaksi) — tampilan atau kehalusan yang tak terukur otomatis |
| ⛔ | Blocked — butuh aset (file RAW / dataset besar) atau build eksternal |
| ⚠️ | Discrepancy — implementasi berbeda dari ekspektasi TEST_PLAN (lihat §19) |

**Tally (66 test case):** ✅ 53 automated · ⚠️ 0 · 👤/🎨 8 · ⛔ 5

> Update 2026-07-19: 3 discrepancy (§19) telah diselesaikan — OV-004 & KB-006 diperbaiki di kode, LD-005 diselaraskan ke desain lazy-load. Semuanya kini ✅.

**Cara menjalankan automated suite:**

```bash
.venv/bin/pytest tests/test_mvp_services.py tests/test_mvp_widgets.py \
                 tests/test_mvp_controller.py tests/test_mvp_performance.py -v
# atau seluruh suite:
.venv/bin/pytest -q     # 80 passed
```

Semua test berjalan headless (`QT_QPA_PLATFORM=offscreen`, diset di `conftest.py`) dengan fixture gambar yang dibuat on-the-fly (Pillow), tanpa menyentuh storage aplikasi asli.

---

# 1b. Automated Coverage Map

| File | Test Case IDs |
| ---- | ------------- |
| `tests/test_mvp_services.py` | LD-001/002/004/006, SL-001/005, UD-001, WS-001/002/003, WR-001, ER-002/003/004 |
| `tests/test_mvp_widgets.py` | ST-002/003/004/005, ER-001, VW-002/003/004/005/006, SL-004, UD-004, KB-001…006, ZP-001/002/003, OV-001/002/003/004, WR-002/003/004 |
| `tests/test_mvp_controller.py` | SL-001/002/003/005, OV-001/002/003, UD-001/002/003/004, SD-001/002/003, KB-006, ER-003, LD-005, WR-003/004, WS-004 |
| `tests/test_mvp_performance.py` | PF-001, PF-002 |

---

# 2. Testing Scope

Fitur yang diuji meliputi:

- Startup Window
- Workspace
- Image Loading
- Viewer
- Keyboard Navigation
- Photo Selection
- Overlay
- Sound Feedback
- Workspace Recovery
- Performance
- Error Handling
- Packaging

---

# 3. Startup Window

| ID     | Test Case                 | Expected Result         | Status |
| ------ | ------------------------- | ----------------------- | ------ |
| ST-001 | Jalankan aplikasi         | Startup Window muncul   | ✅ (smoke launch, no traceback) |
| ST-002 | Workspace Name kosong     | Tombol START disabled   | ✅      |
| ST-003 | Source Folder kosong      | Tombol START disabled   | ✅      |
| ST-004 | Destination Folder kosong | Tombol START disabled   | ✅      |
| ST-005 | Semua input valid         | Tombol START aktif      | ✅      |
| ST-006 | Browse Source Folder      | Folder berhasil dipilih | 👤 (QFileDialog) |
| ST-007 | Browse Destination Folder | Folder berhasil dipilih | 👤 (QFileDialog) |

---

# 4. Workspace

| ID     | Test Case                        | Expected Result              | Status |
| ------ | -------------------------------- | ---------------------------- | ------ |
| WS-001 | Membuat Workspace baru           | Workspace berhasil dibuat    | ✅      |
| WS-002 | Membuka Workspace yang sudah ada | Workspace berhasil dimuat    | ✅      |
| WS-003 | Simpan Workspace                 | Progress tersimpan           | ✅      |
| WS-004 | Tutup aplikasi                   | Workspace tersimpan otomatis | ✅ (auto-save saat navigasi; event close aktual = 👤) |

---

# 5. Image Loading

| ID     | Test Case        | Expected Result                   | Status |
| ------ | ---------------- | --------------------------------- | ------ |
| LD-001 | Scan folder JPG  | Seluruh gambar ditemukan          | ✅      |
| LD-002 | Scan folder PNG  | Seluruh gambar ditemukan          | ✅      |
| LD-003 | Scan folder RAW  | Preview berhasil dimuat           | ⛔ (butuh file RAW asli) |
| LD-004 | Folder kosong    | Pesan informasi ditampilkan       | ✅ (scan → []; pesan GUI = 👤) |
| LD-005 | Loading (lazy)   | Tidak menunggu semua gambar; siap instan | ✅ (by design: scan instan + lazy preload) |
| LD-006 | Cache dibuat     | Viewer lebih responsif            | ✅ (cache hit)  |

---

# 6. Viewer

| ID     | Test Case        | Expected Result        | Status |
| ------ | ---------------- | ---------------------- | ------ |
| VW-001 | Viewer terbuka   | Foto tampil fullscreen | 🎨 (visual) |
| VW-002 | Informasi file   | Nama file tampil       | ✅      |
| VW-003 | Progress         | Posisi foto benar      | ✅      |
| VW-004 | Selected Counter | Jumlah sesuai          | ✅      |
| VW-005 | Landscape image  | Rasio tetap benar      | ✅ (uniform scale) |
| VW-006 | Portrait image   | Rasio tetap benar      | ✅ (uniform scale) |

---

# 7. Keyboard Navigation

| ID     | Test Case | Expected Result           | Status |
| ------ | --------- | ------------------------- | ------ |
| KB-001 | →         | Pindah ke foto berikutnya | ✅      |
| KB-002 | ←         | Pindah ke foto sebelumnya | ✅      |
| KB-003 | Home      | Lompat ke foto pertama    | ✅      |
| KB-004 | End       | Lompat ke foto terakhir   | ✅      |
| KB-005 | F         | Toggle Fullscreen         | ✅      |
| KB-006 | Esc       | Exit Dialog muncul        | ✅ (ExitDialog konfirmasi Exit/Cancel) |

---

# 8. Photo Selection

| ID     | Test Case        | Expected Result              | Status |
| ------ | ---------------- | ---------------------------- | ------ |
| SL-001 | Tekan Space      | File berhasil dicopy         | ✅      |
| SL-002 | Auto Next        | Berpindah ke foto berikutnya | ✅      |
| SL-003 | Selected Counter | Bertambah satu               | ✅      |
| SL-004 | Selected Badge   | Badge muncul                 | ✅      |
| SL-005 | File sudah ada   | Tidak dicopy ulang           | ✅      |

---

# 9. Undo

| ID     | Test Case | Expected Result               | Status |
| ------ | --------- | ----------------------------- | ------ |
| UD-001 | Backspace | File dihapus dari destination | ✅      |
| UD-002 | Counter   | Berkurang satu                | ✅      |
| UD-003 | Viewer    | Tetap pada foto saat ini      | ✅      |
| UD-004 | Badge     | Menghilang                    | ✅      |

---

# 10. Overlay

| ID     | Test Case     | Expected Result              | Status |
| ------ | ------------- | ---------------------------- | ------ |
| OV-001 | Copy berhasil | Overlay "COPIED" muncul      | ✅      |
| OV-002 | Undo berhasil | Overlay "REMOVED" muncul     | ✅      |
| OV-003 | Copy gagal    | Overlay "COPY FAILED" muncul | ✅      |
| OV-004 | Durasi        | ±250–300 ms                  | ✅ (180 ms tampil + 120 ms fade = 300 ms) |

---

# 11. Sound Feedback

| ID     | Test Case       | Expected Result | Status |
| ------ | --------------- | --------------- | ------ |
| SD-001 | Copy            | Sound diputar   | ✅ (QApplication.beep dipanggil) |
| SD-002 | Undo            | Sound diputar   | ✅ (QApplication.beep dipanggil) |
| SD-003 | Sound dimatikan | Tidak ada suara | ✅      |

---

# 12. Zoom & Pan

| ID     | Test Case    | Expected Result    | Status |
| ------ | ------------ | ------------------ | ------ |
| ZP-001 | Scroll       | Zoom In            | ✅      |
| ZP-002 | Scroll balik | Zoom Out           | ✅      |
| ZP-003 | Double Click | Reset Zoom         | ✅      |
| ZP-004 | Drag         | Pan berjalan halus | 🎨 (interaksi/visual) |

---

# 13. Workspace Recovery

| ID     | Test Case                       | Expected Result        | Status |
| ------ | ------------------------------- | ---------------------- | ------ |
| WR-001 | Tutup aplikasi di tengah proses | Workspace tersimpan    | ✅      |
| WR-002 | Buka kembali aplikasi           | Dialog Recovery muncul | 👤 (wiring di main.on_start; dialog build = ✅) |
| WR-003 | Continue Workspace              | Progress dipulihkan    | ✅ (resume + clamp index) |
| WR-004 | Start New Workspace             | Workspace baru dimulai | ✅      |

---

# 14. Error Handling

| ID     | Test Case                      | Expected Result       | Status |
| ------ | ------------------------------ | --------------------- | ------ |
| ER-001 | Source Folder tidak ada        | Error ditampilkan     | ✅ (START disabled bila source tak ada) |
| ER-002 | Destination tidak bisa ditulis | Error ditampilkan     | ✅ (copy → False; skip bila root) |
| ER-003 | File rusak                     | Viewer tetap berjalan | ✅      |
| ER-004 | Format tidak didukung          | File dilewati         | ✅      |

---

# 15. Performance

| ID     | Test Case   | Expected Result               | Status |
| ------ | ----------- | ----------------------------- | ------ |
| PF-001 | 100 foto    | Lancar                        | ✅ (scan < 2s) |
| PF-002 | 1.000 foto  | Lancar                        | ✅ (scan < 5s) |
| PF-003 | 10.000 foto | Lancar                        | ⛔ (dataset besar — manual) |
| PF-004 | 50.000 foto | Tidak crash                   | ⛔ (dataset besar — manual) |
| PF-005 | Navigasi    | Terasa instan setelah preload | 🎨 (subjektif; mekanisme cache = ✅ LD-006) |

---

# 16. Packaging

## Windows

| ID     | Test Case    | Expected Result   | Status |
| ------ | ------------ | ----------------- | ------ |
| PK-001 | Build EXE    | Berhasil          | ⛔ (belum dibuat) |
| PK-002 | Jalankan EXE | Aplikasi berjalan | ⛔ (butuh Windows) |

## macOS

| ID     | Test Case    | Expected Result   | Status |
| ------ | ------------ | ----------------- | ------ |
| PK-003 | Build App    | Berhasil          | 👤 (.app sudah dibuat; verifikasi manual) |
| PK-004 | Jalankan App | Aplikasi berjalan | 👤 (verifikasi manual) |

---

# 17. Regression Checklist

Lakukan pengujian ulang setelah setiap perubahan besar. Otomatis via `.venv/bin/pytest -q`.

- ✅ Startup Window
- ✅ Workspace
- ✅ Image Loading
- ✅ Viewer
- ✅ Keyboard Navigation
- ✅ Copy
- ✅ Undo
- ✅ Overlay
- ✅ Sound
- ✅ Zoom
- 🎨 Pan (manual)
- ✅ Workspace Recovery

---

# 18. Acceptance Criteria

Photo Picker MVP dinyatakan siap dirilis apabila:

- Seluruh test case berstatus **Passed**.
- Tidak terdapat bug kritis (Critical).
- Tidak terjadi kehilangan data Workspace.
- Tidak terjadi kerusakan pada file asli pengguna.
- Aplikasi tetap responsif saat menangani ribuan foto.
- Build Windows dan macOS berhasil dijalankan tanpa error.

**Status 2026-07-19:** 53/66 automated pass, 0 bug kritis, 0 discrepancy. Sisa: 8 manual (visual/audio), 5 blocked (aset/build). File asli tidak pernah disentuh (copy/remove hanya di destination — terverifikasi UD-001).

---

# 19. Discrepancies — Resolved (2026-07-19)

Tiga selisih spec↔implementasi ditemukan saat mengotomatiskan TEST_PLAN, dan sudah diselesaikan:

1. **OV-004 — Durasi overlay.** ✅ **Fixed (kode).** `OverlayManager` diperpendek menjadi `VISIBLE_MS=180` + `FADE_MS=120` = 300 ms, sesuai ekspektasi ±250–300 ms (`src/services/overlay_manager.py`). Diverifikasi `test_OV004_overlay_duration_within_spec`.
2. **KB-006 — Esc.** ✅ **Fixed (kode).** Ditambahkan `ExitDialog` (Exit/Cancel) yang muncul saat keluar viewer; `ViewerController.exit_app` hanya menutup bila user memilih Exit (`src/presentation/exit_dialog.py`, `src/controllers/viewer_controller.py`). Diverifikasi `test_KB006_exit_*`.
3. **LD-005 — Loading.** ✅ **Resolved (spec).** Diselaraskan ke desain lazy-load: aplikasi tidak menunggu semua gambar dimuat — hanya preload beberapa di depan dengan cache ber-LRU. TEST_PLAN diperbarui; diverifikasi `test_LD005_does_not_load_all_images_into_cache`.

**Juga diperbaiki:** `OverlayManager` sebelumnya memicu `RuntimeWarning` libpyside pada overlay pertama (disconnect sinyal tanpa koneksi). Diperbaiki dengan connect `finished→hide` sekali di `__init__`.
