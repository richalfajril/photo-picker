# SYSTEM_ARCHITECTURE.md

# Photo Picker MVP

**Version:** 5.0
**Status:** Final (MVP)
**Last Updated:** July 2026

---

# 1. Overview

## Purpose

Photo Picker adalah aplikasi desktop yang membantu fotografer melakukan proses **photo culling** dengan sangat cepat menggunakan keyboard.

Aplikasi ini berfokus pada satu pekerjaan utama:

1. Membuka folder berisi ribuan foto.
2. Menampilkan foto secara cepat.
3. Memilih foto yang layak.
4. Menyalin foto terpilih ke folder tujuan.
5. Menyimpan progres sehingga pekerjaan dapat dilanjutkan kapan saja.

MVP tidak bertujuan menggantikan Lightroom atau Photo Mechanic. Fokus utama adalah kecepatan, stabilitas, dan kemudahan penggunaan.

---

## Goals

- Keyboard-first workflow.
- Fast image navigation.
- Offline-first.
- Resume workspace.
- Simple architecture.
- Easy to maintain.

---

## Non Goals (MVP)

Fitur berikut tidak termasuk dalam MVP:

- Database
- Cloud Sync
- AI Culling
- Face Recognition
- Rating bintang
- Color Label
- Compare Mode
- Image Editing
- Plugin System

---

# 2. Design Principles

Seluruh implementasi mengikuti prinsip berikut.

## 2.1 Simplicity First

Solusi paling sederhana yang memenuhi kebutuhan lebih diprioritaskan daripada desain yang kompleks.

---

## 2.2 Keyboard First

Seluruh proses seleksi dapat dilakukan tanpa mouse.

---

## 2.3 Offline First

Seluruh data disimpan secara lokal.

Aplikasi tidak membutuhkan koneksi internet.

---

## 2.4 Workspace Based

Seluruh state aplikasi berada di dalam sebuah Workspace.

Workspace menjadi pusat aktivitas pengguna.

---

## 2.5 Separation of Responsibility

Setiap komponen hanya memiliki satu tanggung jawab utama.

---

# 3. High-Level Architecture

Aplikasi menggunakan arsitektur berlapis (Layered Architecture).

```text
Presentation
      │
Controller
      │
Domain (Workspace)
      │
Services
      │
Repositories
      │
Storage
```

## Layer Responsibilities

### Presentation

Bertanggung jawab menampilkan antarmuka pengguna.

Contoh:

- StartWindow
- ViewerWindow

---

### Controller

Menghubungkan UI dengan business logic.

Contoh:

- ViewerController

---

### Domain

Berisi objek inti aplikasi.

Pada MVP hanya terdapat satu domain utama:

- Workspace

---

### Services

Berisi proses yang tidak menyimpan state.

Contoh:

- FileOperationService
- ImageLoaderService

---

### Repository

Bertanggung jawab membaca dan menyimpan data.

Contoh:

- WorkspaceRepository
- SettingsRepository

---

### Storage

Menyimpan seluruh data aplikasi dalam bentuk file lokal.

---

# 4. Core Components

## Application

Titik masuk aplikasi.

Tanggung jawab:

- Inisialisasi aplikasi
- Memuat settings
- Menampilkan StartWindow

---

## StartWindow

Menampilkan halaman awal.

Fitur:

- Open Workspace
- Create Workspace
- Recent Workspace

---

## ViewerWindow

Menampilkan foto yang sedang dipilih.

Fitur:

- Preview
- Overlay
- Navigation

---

## ViewerController

Menghubungkan ViewerWindow dengan Workspace.

Tanggung jawab:

- Navigasi
- Shortcut Keyboard
- Memanggil Service

---

## Workspace

Workspace adalah pusat state aplikasi.

Workspace menyimpan:

- Source Folder
- Destination Folder
- Image List
- Current Index
- Selected Images
- Statistics

Workspace tidak mengetahui cara membaca atau menyimpan file.

---

## WorkspaceRepository

Mengelola penyimpanan Workspace.

Tanggung jawab:

- Load
- Save
- Create
- Delete

---

## SettingsRepository

Mengelola konfigurasi aplikasi.

Contoh:

- Theme
- Recent Workspace
- Shortcut Preference

---

## ImageLoaderService

Memuat gambar dari storage.

Tanggung jawab:

- Load Image
- Decode
- Thumbnail

---

## FileOperationService

Melakukan operasi file.

Contoh:

- Copy
- Undo Copy

Semua manipulasi file harus melalui service ini.

---

## CacheManager

Mengelola cache gambar untuk mempercepat navigasi.

---

## OverlayManager

Mengelola informasi yang ditampilkan di atas gambar.

Contoh:

- Nomor foto
- Progress
- Status Selected

---

# 5. Workspace Model

Workspace adalah Aggregate Root dari aplikasi.

```
Workspace
│
├── Metadata
├── Source Folder
├── Destination Folder
├── Images
├── Current Index
├── Selected Images
└── Statistics
```

Workspace bertanggung jawab terhadap:

- posisi foto saat ini
- daftar foto
- foto terpilih
- progres pekerjaan

Workspace tidak melakukan operasi file secara langsung.

---

# 6. Runtime Flow

## Startup

```
Application

↓

Load Settings

↓

StartWindow
```

---

## Open Workspace

```
User

↓

StartWindow

↓

WorkspaceRepository

↓

Workspace

↓

ViewerWindow
```

---

## Navigate Image

```
Keyboard

↓

ViewerController

↓

Workspace

↓

ImageLoaderService

↓

ViewerWindow
```

---

## Select Image

```
Space

↓

ViewerController

↓

Workspace

↓

FileOperationService

↓

WorkspaceRepository

↓

Storage
```

---

## Exit

```
WorkspaceRepository

↓

Save Workspace

↓

Close Application
```

---

# 7. Storage Architecture

```
storage/
│
├── settings.json
│
├── workspaces/
│   └── <workspace_name>/
│       ├── workspace.json
│       └── selections.json
│
├── cache/
│
└── logs/
```

## settings.json

Menyimpan konfigurasi aplikasi.

Contoh:

- Theme
- Recent Workspace
- Window Size

---

## workspace.json

Menyimpan informasi workspace.

Contoh:

- Source Folder
- Destination Folder
- Current Index
- Created Date

---

## selections.json

Menyimpan daftar foto yang telah dipilih.

---

## cache/

Digunakan untuk menyimpan cache sementara.

Dapat dihapus kapan saja.

---

## logs/

Menyimpan log aplikasi untuk debugging.

---

# 8. Dependency Rules

Seluruh dependency harus mengikuti arah berikut.

```
Presentation
      │
Controller
      │
Workspace
      │
Services
      │
Repositories
      │
Storage
```

Aturan yang harus dipatuhi:

- Presentation tidak boleh mengakses Storage secara langsung.
- Controller tidak boleh membaca atau menulis file.
- Workspace tidak boleh mengetahui implementasi penyimpanan.
- Semua operasi file dilakukan melalui FileOperationService.
- Hanya Repository yang boleh membaca atau menulis file JSON.
- Services bersifat stateless.
- Cache hanya digunakan untuk meningkatkan performa dan tidak menjadi sumber data utama.

---

# Summary

Arsitektur MVP dibangun dengan prinsip sederhana, mudah dipahami, dan mudah dikembangkan.

Workspace menjadi pusat state aplikasi, Repository menangani penyimpanan, Service menangani proses, Controller mengatur alur, dan Presentation bertanggung jawab terhadap antarmuka pengguna.

Dokumen ini menjadi acuan utama bagi implementasi serta dokumen turunan seperti CLASS_DIAGRAM.md, FILE_STRUCTURE.md, dan STORAGE_ARCHITECTURE.md.
