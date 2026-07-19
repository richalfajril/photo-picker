# COMPONENT_SPEC.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini mendeskripsikan spesifikasi setiap komponen utama pada Photo Picker MVP.

Setiap komponen memiliki tanggung jawab yang jelas sesuai dengan prinsip **Single Responsibility Principle (SRP)** sehingga mudah dikembangkan, diuji, dan dipelihara.

---

# 2. Component Overview

| Layer        | Component            |
| ------------ | -------------------- |
| Presentation | StartWindow          |
| Presentation | ViewerWindow         |
| Controller   | ViewerController     |
| Domain       | Workspace            |
| Repository   | WorkspaceRepository  |
| Repository   | SettingsRepository   |
| Service      | ImageLoaderService   |
| Service      | FileOperationService |
| Service      | CacheManager         |
| Service      | OverlayManager       |

---

# 3. Presentation Layer

## StartWindow

### Responsibility

- Menampilkan konfigurasi awal aplikasi.
- Mengumpulkan input pengguna.
- Memvalidasi seluruh field.
- Memulai Workspace.

### Input

- Workspace Name
- Source Folder
- Destination Folder
- Fullscreen
- Auto Next
- Sound
- Workspace Recovery

### Output

- Workspace baru
- Membuka ViewerWindow

### Dependencies

- ViewerController

---

## ViewerWindow

### Responsibility

- Menampilkan foto.
- Menampilkan informasi Workspace.
- Menangani interaksi pengguna.
- Menampilkan Overlay.

### Display

- Current Image
- File Name
- Progress
- Selected Counter
- Overlay

### Dependencies

- ViewerController

---

# 4. Controller Layer

## ViewerController

### Responsibility

Menghubungkan UI dengan Domain, Service, dan Repository.

### Main Responsibilities

- Memuat Workspace.
- Navigasi foto.
- Menjalankan Copy.
- Menjalankan Undo.
- Memperbarui UI.
- Menyimpan Workspace.
- Mengelola keyboard shortcut.

### Dependencies

- Workspace
- WorkspaceRepository
- SettingsRepository
- ImageLoaderService
- FileOperationService
- CacheManager
- OverlayManager

---

# 5. Domain Layer

## Workspace

### Responsibility

Menyimpan seluruh state aplikasi.

### Stored Data

- Workspace Name
- Source Folder
- Destination Folder
- Image List
- Current Index
- Selected Images
- Statistics

### Business Rules

- Satu Workspace hanya memiliki satu Source Folder.
- Workspace selalu memiliki Destination Folder.
- Progress harus dapat dipulihkan.
- Workspace disimpan otomatis.

---

# 6. Repository Layer

## WorkspaceRepository

### Responsibility

Mengelola penyimpanan Workspace.

### Operations

- Create Workspace
- Load Workspace
- Save Workspace
- Delete Workspace

### Storage

```text
storage/workspaces/
```

---

## SettingsRepository

### Responsibility

Mengelola konfigurasi aplikasi.

### Operations

- Load Settings
- Save Settings
- Reset Default Settings

### Storage

```text
storage/settings.json
```

---

# 7. Service Layer

## ImageLoaderService

### Responsibility

Memuat gambar dari disk.

### Features

- Scan Folder
- Load Image
- Load RAW Preview
- Validate Format

### Supported Formats

- JPG
- JPEG
- PNG
- BMP
- TIFF
- WEBP
- CR2
- CR3
- NEF
- ARW
- DNG

---

## FileOperationService

### Responsibility

Melakukan operasi file.

### Features

- Copy File
- Remove File
- Check Existing File
- Validate Destination

### Rules

- Tidak mengubah file asli.
- Tidak overwrite file yang sudah ada.
- Seluruh operasi harus aman (safe).

---

## CacheManager

### Responsibility

Mengelola cache gambar.

### Features

- Memory Cache
- Thumbnail Cache
- Background Preload
- Cache Cleanup

### Goals

- Mempercepat perpindahan foto.
- Mengurangi pembacaan disk berulang.

---

## OverlayManager

### Responsibility

Mengelola seluruh notifikasi visual.

### Supported Overlay

- COPIED
- REMOVED
- COPY FAILED

### Behavior

- Overlay muncul singkat.
- Overlay tidak mengganggu navigasi.
- Overlay menghilang otomatis.

---

# 8. Component Interaction

```text
StartWindow
      │
      ▼
ViewerController
      │
      ├──────────────► Workspace
      │
      ├──────────────► WorkspaceRepository
      │
      ├──────────────► SettingsRepository
      │
      ├──────────────► ImageLoaderService
      │
      ├──────────────► FileOperationService
      │
      ├──────────────► CacheManager
      │
      └──────────────► OverlayManager
              │
              ▼
        ViewerWindow
```

---

# 9. Dependency Rules

- Presentation tidak boleh mengakses Repository secara langsung.
- Presentation hanya berkomunikasi melalui Controller.
- Controller menjadi pusat koordinasi aplikasi.
- Domain tidak bergantung pada UI.
- Repository hanya bertanggung jawab terhadap penyimpanan data.
- Service hanya menangani logika operasional.
- Setiap komponen memiliki satu tanggung jawab utama.

---

# 10. Lifecycle

```text
Application Start
        │
        ▼
StartWindow
        │
        ▼
ViewerController
        │
        ▼
Workspace Created / Loaded
        │
        ▼
ImageLoaderService
        │
        ▼
ViewerWindow
        │
        ▼
User Interaction
        │
        ▼
Workspace Updated
        │
        ▼
WorkspaceRepository
        │
        ▼
Auto Save
```

---

# 11. Future Components (v2.0)

Komponen berikut belum termasuk dalam MVP dan disiapkan sebagai referensi pengembangan selanjutnya.

- RatingService
- MetadataService (EXIF/IPTC)
- ThumbnailStrip
- CompareMode
- SlideshowController
- ExportService
- PluginManager

---

# 12. Summary

Arsitektur Photo Picker MVP terdiri dari **10 komponen utama** yang dipisahkan ke dalam lima layer: Presentation, Controller, Domain, Repository, dan Service.

Pemisahan ini menjaga kode tetap modular, mudah diuji, dan mudah dikembangkan tanpa menimbulkan ketergantungan yang tidak diperlukan antar komponen.
