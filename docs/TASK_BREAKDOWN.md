# TASK_BREAKDOWN.md

# Photo Picker MVP

**Version:** 1.0

---

# Overview

Dokumen ini berisi rincian pekerjaan implementasi Photo Picker MVP.

Setiap task disusun berdasarkan urutan pengembangan yang paling efisien sehingga setiap fitur dapat dibangun di atas fondasi yang sudah tersedia.

Status setiap task dapat diperbarui selama proses pengembangan.

---

# Development Phases

| Phase   | Description        |
| ------- | ------------------ |
| Phase 1 | Project Setup      |
| Phase 2 | Domain & Storage   |
| Phase 3 | Startup Window     |
| Phase 4 | Image Loading      |
| Phase 5 | Viewer             |
| Phase 6 | Photo Selection    |
| Phase 7 | Workspace Recovery |
| Phase 8 | Polish             |
| Phase 9 | Packaging          |

---

# Phase 1 — Project Setup

## 1.1 Initialize Project

- [x] Membuat struktur folder project
- [x] Membuat virtual environment
- [x] Install dependencies
- [x] Membuat requirements.txt
- [x] Konfigurasi Git

---

## 1.2 Create Project Structure

- [x] src/
- [x] presentation/
- [x] controllers/
- [x] domain/
- [x] repositories/
- [x] services/
- [x] storage/
- [x] config/
- [x] utils/
- [x] assets/
- [x] tests/

---

## 1.3 Application Entry

- [x] main.py
- [x] QApplication
- [x] Load Startup Window

---

# Phase 2 — Domain & Storage

## 2.1 Workspace

- [x] Workspace Model
- [x] Current Index
- [x] Selected Images
- [x] Statistics

---

## 2.2 WorkspaceRepository

- [x] Load Workspace
- [x] Save Workspace
- [x] Update Progress

---

## 2.3 SettingsRepository

- [x] Load settings.json
- [x] Save settings.json
- [x] Default Settings

---

## 2.4 Storage

- [x] Auto create storage folder
- [x] Auto create workspace folder
- [x] Auto create cache folder
- [x] Auto create logs folder

---

# Phase 3 — Startup Window

## 3.1 UI

- [x] Workspace Name
- [x] Source Folder
- [x] Destination Folder
- [x] Browse Button
- [x] Fullscreen Checkbox
- [x] Auto Next Checkbox
- [x] Sound Checkbox
- [x] Workspace Recovery Checkbox
- [x] Start Button

---

## 3.2 Validation

- [x] Workspace Name wajib diisi
- [x] Source Folder wajib dipilih
- [x] Destination Folder wajib dipilih
- [x] Enable Start Button jika valid

---

# Phase 4 — Image Loading

## 4.1 Scan Images

- [x] Scan folder
- [x] Filter supported format
- [x] Sort images
- [x] Count images

---

## 4.2 ImageLoaderService

- [x] Load image
- [x] Load RAW preview
- [x] Error handling

---

## 4.3 CacheManager

- [x] Memory Cache
- [x] Thumbnail Cache
- [x] Background Preload

---

## 4.4 Loading Screen

- [x] Progress Bar
- [x] Progress Text
- [x] Status Text

---

# Phase 5 — Viewer

## 5.1 Viewer Window

- [x] Fullscreen Image
- [x] Bottom Information
- [x] Selected Counter
- [x] Progress Counter

---

## 5.2 Keyboard Navigation

- [x] Next
- [x] Previous
- [x] First Image
- [x] Last Image

---

## 5.3 Zoom

- [x] Mouse Wheel
- [x] Reset Zoom

---

## 5.4 Pan

- [x] Drag Image
- [x] Smooth Movement

---

# Phase 6 — Photo Selection

## 6.1 Copy

- [x] Copy Image
- [x] Skip jika sudah ada
- [x] Update Workspace
- [x] Update Counter

---

## 6.2 Undo

- [x] Delete copied file
- [x] Update Workspace
- [x] Update Counter

---

## 6.3 Overlay

- [x] COPIED
- [x] REMOVED
- [x] COPY FAILED

---

## 6.4 Sound

- [x] Copy Sound
- [x] Undo Sound

---

## 6.5 Selected Badge

- [x] Show badge
- [x] Hide badge

---

# Phase 7 — Workspace Recovery

## 7.1 Save

- [x] Save current index
- [x] Save selected images
- [x] Save statistics

---

## 7.2 Recovery

- [x] Detect existing Workspace
- [x] Show Recovery Dialog
- [x] Continue Workspace
- [x] Start New Workspace

---

# Phase 8 — Polish

## 8.1 UI

- [x] Responsive Layout
- [x] Smooth Overlay
- [x] Icon
- [x] Cursor

---

## 8.2 Performance

- [x] Lazy Loading
- [x] Image Preload
- [x] Cache Optimization

---

## 8.3 Error Handling

- [x] Missing Source Folder
- [x] Missing Destination Folder
- [x] Copy Failed
- [x] Unsupported Image

---

# Phase 9 — Packaging

## 9.1 Windows

- [ ] PyInstaller
- [ ] EXE Build
- [ ] Icon

---

## 9.2 macOS

- [x] App Bundle
- [ ] Icon
- [ ] Signing (optional)

---

# Testing Checklist

## Startup

- [ ] Startup Window tampil
- [ ] Validasi input bekerja

---

## Viewer

- [ ] Viewer tampil
- [ ] Navigasi keyboard bekerja
- [ ] Zoom bekerja
- [ ] Pan bekerja

---

## Selection

- [ ] Copy berhasil
- [ ] Undo berhasil
- [ ] Overlay tampil
- [ ] Sound diputar

---

## Workspace

- [ ] Workspace tersimpan
- [ ] Workspace dipulihkan
- [ ] Progress sesuai

---

## Performance

- [ ] 100 foto
- [ ] 1.000 foto
- [ ] 10.000 foto
- [ ] 50.000 foto

---

# Definition of Done

Photo Picker MVP dianggap selesai apabila:

- Seluruh fitur pada PRD telah diimplementasikan.
- Seluruh checklist testing berhasil.
- Workspace dapat dipulihkan tanpa kehilangan progres.
- Aplikasi stabil pada ribuan foto.
- Build Windows dan macOS berhasil dibuat.
