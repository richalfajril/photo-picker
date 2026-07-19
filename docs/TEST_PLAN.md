# TEST_PLAN.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini berisi seluruh skenario pengujian untuk memastikan setiap fitur pada Photo Picker MVP bekerja sesuai spesifikasi.

Seluruh test dilakukan secara manual (Manual Testing) dan menjadi acuan sebelum aplikasi dinyatakan siap digunakan.

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
| ST-001 | Jalankan aplikasi         | Startup Window muncul   | ☐      |
| ST-002 | Workspace Name kosong     | Tombol START disabled   | ☐      |
| ST-003 | Source Folder kosong      | Tombol START disabled   | ☐      |
| ST-004 | Destination Folder kosong | Tombol START disabled   | ☐      |
| ST-005 | Semua input valid         | Tombol START aktif      | ☐      |
| ST-006 | Browse Source Folder      | Folder berhasil dipilih | ☐      |
| ST-007 | Browse Destination Folder | Folder berhasil dipilih | ☐      |

---

# 4. Workspace

| ID     | Test Case                        | Expected Result              | Status |
| ------ | -------------------------------- | ---------------------------- | ------ |
| WS-001 | Membuat Workspace baru           | Workspace berhasil dibuat    | ☐      |
| WS-002 | Membuka Workspace yang sudah ada | Workspace berhasil dimuat    | ☐      |
| WS-003 | Simpan Workspace                 | Progress tersimpan           | ☐      |
| WS-004 | Tutup aplikasi                   | Workspace tersimpan otomatis | ☐      |

---

# 5. Image Loading

| ID     | Test Case        | Expected Result                   | Status |
| ------ | ---------------- | --------------------------------- | ------ |
| LD-001 | Scan folder JPG  | Seluruh gambar ditemukan          | ☐      |
| LD-002 | Scan folder PNG  | Seluruh gambar ditemukan          | ☐      |
| LD-003 | Scan folder RAW  | Preview berhasil dimuat           | ☐      |
| LD-004 | Folder kosong    | Pesan informasi ditampilkan       | ☐      |
| LD-005 | Progress loading | Progress bertambah hingga selesai | ☐      |
| LD-006 | Cache dibuat     | Viewer lebih responsif            | ☐      |

---

# 6. Viewer

| ID     | Test Case        | Expected Result        | Status |
| ------ | ---------------- | ---------------------- | ------ |
| VW-001 | Viewer terbuka   | Foto tampil fullscreen | ☐      |
| VW-002 | Informasi file   | Nama file tampil       | ☐      |
| VW-003 | Progress         | Posisi foto benar      | ☐      |
| VW-004 | Selected Counter | Jumlah sesuai          | ☐      |
| VW-005 | Landscape image  | Rasio tetap benar      | ☐      |
| VW-006 | Portrait image   | Rasio tetap benar      | ☐      |

---

# 7. Keyboard Navigation

| ID     | Test Case | Expected Result           | Status |
| ------ | --------- | ------------------------- | ------ |
| KB-001 | →         | Pindah ke foto berikutnya | ☐      |
| KB-002 | ←         | Pindah ke foto sebelumnya | ☐      |
| KB-003 | Home      | Lompat ke foto pertama    | ☐      |
| KB-004 | End       | Lompat ke foto terakhir   | ☐      |
| KB-005 | F         | Toggle Fullscreen         | ☐      |
| KB-006 | Esc       | Exit Dialog muncul        | ☐      |

---

# 8. Photo Selection

| ID     | Test Case        | Expected Result              | Status |
| ------ | ---------------- | ---------------------------- | ------ |
| SL-001 | Tekan Space      | File berhasil dicopy         | ☐      |
| SL-002 | Auto Next        | Berpindah ke foto berikutnya | ☐      |
| SL-003 | Selected Counter | Bertambah satu               | ☐      |
| SL-004 | Selected Badge   | Badge muncul                 | ☐      |
| SL-005 | File sudah ada   | Tidak dicopy ulang           | ☐      |

---

# 9. Undo

| ID     | Test Case | Expected Result               | Status |
| ------ | --------- | ----------------------------- | ------ |
| UD-001 | Backspace | File dihapus dari destination | ☐      |
| UD-002 | Counter   | Berkurang satu                | ☐      |
| UD-003 | Viewer    | Tetap pada foto saat ini      | ☐      |
| UD-004 | Badge     | Menghilang                    | ☐      |

---

# 10. Overlay

| ID     | Test Case     | Expected Result              | Status |
| ------ | ------------- | ---------------------------- | ------ |
| OV-001 | Copy berhasil | Overlay "COPIED" muncul      | ☐      |
| OV-002 | Undo berhasil | Overlay "REMOVED" muncul     | ☐      |
| OV-003 | Copy gagal    | Overlay "COPY FAILED" muncul | ☐      |
| OV-004 | Durasi        | ±250–300 ms                  | ☐      |

---

# 11. Sound Feedback

| ID     | Test Case       | Expected Result | Status |
| ------ | --------------- | --------------- | ------ |
| SD-001 | Copy            | Sound diputar   | ☐      |
| SD-002 | Undo            | Sound diputar   | ☐      |
| SD-003 | Sound dimatikan | Tidak ada suara | ☐      |

---

# 12. Zoom & Pan

| ID     | Test Case    | Expected Result    | Status |
| ------ | ------------ | ------------------ | ------ |
| ZP-001 | Scroll       | Zoom In            | ☐      |
| ZP-002 | Scroll balik | Zoom Out           | ☐      |
| ZP-003 | Double Click | Reset Zoom         | ☐      |
| ZP-004 | Drag         | Pan berjalan halus | ☐      |

---

# 13. Workspace Recovery

| ID     | Test Case                       | Expected Result        | Status |
| ------ | ------------------------------- | ---------------------- | ------ |
| WR-001 | Tutup aplikasi di tengah proses | Workspace tersimpan    | ☐      |
| WR-002 | Buka kembali aplikasi           | Dialog Recovery muncul | ☐      |
| WR-003 | Continue Workspace              | Progress dipulihkan    | ☐      |
| WR-004 | Start New Workspace             | Workspace baru dimulai | ☐      |

---

# 14. Error Handling

| ID     | Test Case                      | Expected Result       | Status |
| ------ | ------------------------------ | --------------------- | ------ |
| ER-001 | Source Folder tidak ada        | Error ditampilkan     | ☐      |
| ER-002 | Destination tidak bisa ditulis | Error ditampilkan     | ☐      |
| ER-003 | File rusak                     | Viewer tetap berjalan | ☐      |
| ER-004 | Format tidak didukung          | File dilewati         | ☐      |

---

# 15. Performance

| ID     | Test Case   | Expected Result               | Status |
| ------ | ----------- | ----------------------------- | ------ |
| PF-001 | 100 foto    | Lancar                        | ☐      |
| PF-002 | 1.000 foto  | Lancar                        | ☐      |
| PF-003 | 10.000 foto | Lancar                        | ☐      |
| PF-004 | 50.000 foto | Tidak crash                   | ☐      |
| PF-005 | Navigasi    | Terasa instan setelah preload | ☐      |

---

# 16. Packaging

## Windows

| ID     | Test Case    | Expected Result   | Status |
| ------ | ------------ | ----------------- | ------ |
| PK-001 | Build EXE    | Berhasil          | ☐      |
| PK-002 | Jalankan EXE | Aplikasi berjalan | ☐      |

## macOS

| ID     | Test Case    | Expected Result   | Status |
| ------ | ------------ | ----------------- | ------ |
| PK-003 | Build App    | Berhasil          | ☐      |
| PK-004 | Jalankan App | Aplikasi berjalan | ☐      |

---

# 17. Regression Checklist

Lakukan pengujian ulang setelah setiap perubahan besar.

- ☐ Startup Window
- ☐ Workspace
- ☐ Image Loading
- ☐ Viewer
- ☐ Keyboard Navigation
- ☐ Copy
- ☐ Undo
- ☐ Overlay
- ☐ Sound
- ☐ Zoom
- ☐ Pan
- ☐ Workspace Recovery

---

# 18. Acceptance Criteria

Photo Picker MVP dinyatakan siap dirilis apabila:

- Seluruh test case berstatus **Passed**.
- Tidak terdapat bug kritis (Critical).
- Tidak terjadi kehilangan data Workspace.
- Tidak terjadi kerusakan pada file asli pengguna.
- Aplikasi tetap responsif saat menangani ribuan foto.
- Build Windows dan macOS berhasil dijalankan tanpa error.
