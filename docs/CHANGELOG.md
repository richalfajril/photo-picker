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
