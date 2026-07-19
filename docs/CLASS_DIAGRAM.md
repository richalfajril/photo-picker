# CLASS_DIAGRAM.md

# Photo Picker MVP

**Version:** 1.0
**Derived From:** SYSTEM_ARCHITECTURE.md v5.0

---

# Overview

Dokumen ini mendefinisikan struktur class utama pada aplikasi Photo Picker MVP.

Class diagram hanya berisi class yang akan benar-benar diimplementasikan pada MVP. Seluruh class dibagi berdasarkan layer arsitektur agar tanggung jawab masing-masing jelas.

---

# Class Diagram

```text
┌──────────────────────────────┐
│         Presentation         │
└──────────────────────────────┘

+------------------+
|  StartWindow     |
+------------------+

+------------------+
|  ViewerWindow    |
+------------------+


            │
            ▼


┌──────────────────────────────┐
│          Controller          │
└──────────────────────────────┘

+----------------------+
| ViewerController     |
+----------------------+
| +nextImage()         |
| +previousImage()     |
| +selectImage()       |
| +undoSelection()     |
+----------------------+


            │
            ▼


┌──────────────────────────────┐
│            Domain            │
└──────────────────────────────┘

+--------------------------------------+
| Workspace                            |
+--------------------------------------+
| sourceFolder                         |
| destinationFolder                    |
| images[]                             |
| currentIndex                         |
| selectedImages                       |
| statistics                           |
+--------------------------------------+
| currentImage()                       |
| nextImage()                          |
| previousImage()                      |
| selectCurrent()                      |
| undoSelection()                      |
| progress()                           |
+--------------------------------------+


            │
            ▼


┌──────────────────────────────┐
│           Services           │
└──────────────────────────────┘

+---------------------------+
| ImageLoaderService        |
+---------------------------+
| loadImage()               |
| loadThumbnail()           |
+---------------------------+

+---------------------------+
| FileOperationService      |
+---------------------------+
| copyFile()                |
| undoCopy()                |
+---------------------------+

+---------------------------+
| CacheManager              |
+---------------------------+
| get()                     |
| put()                     |
| clear()                   |
+---------------------------+

+---------------------------+
| OverlayManager            |
+---------------------------+
| buildOverlay()            |
+---------------------------+


            │
            ▼


┌──────────────────────────────┐
│         Repository           │
└──────────────────────────────┘

+---------------------------+
| WorkspaceRepository       |
+---------------------------+
| load()                    |
| save()                    |
| create()                  |
| delete()                  |
+---------------------------+

+---------------------------+
| SettingsRepository        |
+---------------------------+
| load()                    |
| save()                    |
+---------------------------+
```

---

# Layer Description

## Presentation

Presentation hanya bertanggung jawab terhadap antarmuka pengguna.

Class:

- StartWindow
- ViewerWindow

Presentation tidak boleh mengakses Repository maupun Storage secara langsung.

---

## Controller

Controller menjadi penghubung antara UI dan Domain.

Class:

- ViewerController

Controller menerima input dari keyboard, memanggil Workspace, kemudian memperbarui tampilan.

Controller tidak menyimpan state aplikasi.

---

## Domain

Workspace merupakan pusat state aplikasi.

Workspace menyimpan:

- daftar gambar
- posisi gambar saat ini
- daftar gambar terpilih
- informasi folder
- statistik sederhana

Workspace tidak mengetahui bagaimana data disimpan ke disk.

---

## Services

Service menangani proses yang bersifat stateless.

### ImageLoaderService

Bertanggung jawab memuat gambar dari storage.

### FileOperationService

Bertanggung jawab terhadap seluruh operasi file.

Contoh:

- Copy
- Undo Copy

### CacheManager

Mengelola cache gambar agar navigasi lebih cepat.

### OverlayManager

Membangun informasi overlay yang ditampilkan pada Viewer.

---

## Repository

Repository menjadi satu-satunya komponen yang boleh membaca maupun menulis file.

### WorkspaceRepository

Mengelola lifecycle Workspace.

### SettingsRepository

Mengelola konfigurasi aplikasi.

---

# Relationships

```
StartWindow
        │
        ▼
ViewerWindow
        │
        ▼
ViewerController
        │
        ▼
Workspace
        ├──────────────┐
        ▼              ▼
ImageLoaderService   FileOperationService
        │              │
        └──────┬───────┘
               ▼
      WorkspaceRepository
               │
               ▼
            Storage
```

---

# Dependency Rules

Seluruh dependency mengikuti arah berikut.

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

Aturan implementasi:

- Presentation hanya berkomunikasi dengan Controller.
- Controller hanya berinteraksi dengan Workspace dan Service.
- Workspace tidak mengetahui Repository.
- Service tidak mengetahui UI.
- Repository tidak mengetahui UI maupun Controller.
- Storage hanya diakses melalui Repository.

---

# Summary

Photo Picker MVP terdiri dari **10 class utama** yang mencakup seluruh kebutuhan aplikasi tanpa menambahkan abstraksi yang belum diperlukan.

| Layer        | Class                                                                  |
| ------------ | ---------------------------------------------------------------------- |
| Presentation | StartWindow, ViewerWindow                                              |
| Controller   | ViewerController                                                       |
| Domain       | Workspace                                                              |
| Services     | ImageLoaderService, FileOperationService, CacheManager, OverlayManager |
| Repository   | WorkspaceRepository, SettingsRepository                                |

Struktur ini menjadi dasar implementasi kode pada MVP dan harus tetap konsisten dengan `SYSTEM_ARCHITECTURE.md`.
