# CHANGELOG.md

# Changelog

Semua perubahan penting pada proyek **Photo Picker** akan dicatat dalam dokumen ini.

Format changelog mengikuti prinsip **Keep a Changelog** dan menggunakan **Semantic Versioning (SemVer)**.

---

# Versioning

Format versi:

```text
MAJOR.MINOR.PATCH
```

Contoh:

```text
1.2.3
│ │ └── Patch
│ └──── Minor
└────── Major
```

Keterangan:

- **MAJOR** → Perubahan besar yang tidak kompatibel (breaking changes).
- **MINOR** → Penambahan fitur baru tanpa merusak kompatibilitas.
- **PATCH** → Perbaikan bug, optimasi, atau perubahan kecil.

---

# Release Types

## Added

Fitur baru.

## Changed

Perubahan pada fitur yang sudah ada.

## Fixed

Perbaikan bug.

## Removed

Fitur yang dihapus.

## Deprecated

Fitur masih tersedia tetapi akan dihapus pada versi berikutnya.

## Security

Perubahan yang berkaitan dengan keamanan.

---

# [Unreleased]

## Added
- Phase 1: Project Setup (`src/` structure, `main.py` entry point, dependencies).
- Phase 2: Domain & Storage (`Workspace` model, `WorkspaceRepository`, `SettingsRepository`, and auto-creation of storage folders).
- Phase 3: Startup Window (`StartWindow` UI with layout, configuration inputs, and validation logic).
- Phase 4: Image Loading (`ImageLoaderService` with RAW support via `rawpy`, `CacheManager` with background preloading, and `LoadingScreen`).
- Phase 5: Viewer (`ViewerWindow` with custom `QGraphicsView` for smooth panning/zooming, and `ViewerController` handling keyboard shortcuts and UI updates).
- Phase 6: Photo Selection (`FileOperationService` for safe file copying and removal, and `OverlayManager` for fading visual notifications, plus Workspace auto-saving).
- Phase 7: Workspace Recovery (`RecoveryDialog` UI, auto-saving index on navigation, and intercepting app start to load existing workspaces).
- Phase 8: Polish & Error Handling (Added "Selected Badge", basic Sound beep, and Path.exists() validation for the Source Folder).
- Phase 9: Packaging (Added PyInstaller to dependencies and built macOS standalone `.app` bundle).
- Recent Workspaces: the Start window now lists previously-saved workspaces and reopens one at its last-viewed photo in a single click (`WorkspaceRepository.list_all`, `RecentWorkspacesList`).
- Automated MVP test suite (54 pytest cases across services, widgets, controller, and performance) covering the TEST_PLAN's logic-level cases; results matrix and remaining manual/blocked items recorded in `docs/TEST_PLAN.md`.

## Fixed
- `OverlayManager` emitted a libpyside `RuntimeWarning` on the first overlay (disconnecting a signal with no connection); now connects `finished→hide` once at construction.

## Planned

### Added

- Workspace Recovery
- Background Image Preloading
- Memory Cache
- Overlay Notification
- Auto Save Workspace

### Changed

- —

### Fixed

- —

---

# [0.1.0] - Initial Planning

Tanggal: 2026-07-20

## Added

### Documentation

- PRD
- SYSTEM_ARCHITECTURE
- CLASS_DIAGRAM
- FILE_STRUCTURE
- STORAGE_ARCHITECTURE
- USERFLOW
- UI_SPEC
- TASK_BREAKDOWN
- TEST_PLAN
- SHORTCUT_SPEC
- COMPONENT_SPEC
- STATE_MACHINE
- ERROR_HANDLING
- CONFIGURATION

### Architecture

- Five-layer architecture:
  - Presentation
  - Controller
  - Domain
  - Service
  - Repository

### Domain

- Workspace sebagai Aggregate Root.
- Auto Save Workspace.
- Workspace Recovery.

### UI

- Startup Window.
- Loading Screen.
- Viewer Window.
- Exit Dialog.
- Workspace Recovery Dialog.

### Features

- Keyboard Navigation.
- Zoom & Pan.
- Copy + Next.
- Undo.
- Overlay Notification.
- Sound Feedback.
- Cache Manager.

---

# Future Releases

## v0.2.0

### Planned

- Recent Workspaces
- Better Cache Strategy
- Loading Optimization
- Improved Overlay Animation
- More RAW Format Support

---

## v0.3.0

### Planned

- Theme Support
- Multi-language
- EXIF Viewer
- Thumbnail Strip
- Histogram

---

## v0.4.0

### Planned

- Rating System
- Compare Mode
- Batch Selection
- Smart Filtering

---

## v1.0.0

### Stable Release

Target:

- MVP selesai.
- Windows Build.
- macOS Build.
- Dokumentasi lengkap.
- Seluruh test case lulus.
- Performa stabil pada ribuan foto.

---

# Changelog Rules

Setiap perubahan harus dicatat pada versi yang sesuai.

Contoh:

## Added

- Menambahkan OverlayManager.

## Changed

- Mengubah mekanisme Workspace Recovery.

## Fixed

- Memperbaiki bug Copy gagal pada file RAW.

## Removed

- Menghapus SessionManager.

---

# Commit Convention

Gunakan format commit berikut agar konsisten dengan changelog:

```text
feat: add Workspace Recovery

fix: prevent duplicate copy

docs: update UI specification

refactor: simplify ViewerController

perf: improve image preloading

test: add workspace recovery tests

chore: update dependencies
```

---

# Release Checklist

Sebelum membuat release baru, pastikan:

- Seluruh fitur pada `TASK_BREAKDOWN.md` selesai.
- Seluruh test pada `TEST_PLAN.md` berstatus **Passed**.
- Dokumentasi telah diperbarui.
- CHANGELOG telah diperbarui.
- Nomor versi telah dinaikkan sesuai SemVer.
- Build Windows dan macOS berhasil dibuat.
- Tidak ada bug kritis yang diketahui.

---

# Notes

- Changelog hanya mencatat perubahan yang berdampak pada proyek.
- Perubahan kecil seperti typo, formatting, atau komentar kode tidak perlu dicatat kecuali memengaruhi dokumentasi atau perilaku aplikasi.
- Bagian **[Unreleased]** selalu digunakan sebagai tempat mencatat perubahan yang sedang dikembangkan sebelum dirilis.

---

# Summary

Dokumen ini menjadi catatan resmi perkembangan Photo Picker dari tahap perencanaan hingga rilis. Setiap fitur, perubahan, perbaikan bug, dan versi baru harus dicatat secara konsisten agar riwayat proyek mudah ditelusuri oleh seluruh kontributor.
