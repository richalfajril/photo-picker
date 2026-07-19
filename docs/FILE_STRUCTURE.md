# FILE_STRUCTURE.md

# Photo Picker MVP

**Version:** 1.0
**Derived From:** SYSTEM_ARCHITECTURE.md v5.0
**Related:** CLASS_DIAGRAM.md

---

# Overview

Dokumen ini mendefinisikan struktur folder dan file proyek Photo Picker MVP.

Tujuannya adalah:

- Memisahkan kode berdasarkan tanggung jawab.
- Memudahkan navigasi source code.
- Mengikuti arsitektur yang telah ditetapkan.
- Menjaga struktur tetap sederhana dan mudah dikembangkan.

---

# Project Structure

```text
photo-picker/
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── styles/
│
├── docs/
│   ├── PRD.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── CLASS_DIAGRAM.md
│   ├── FILE_STRUCTURE.md
│   ├── STORAGE_ARCHITECTURE.md
│   ├── UI_SPEC.md
│   ├── SHORTCUT_SPEC.md
│   ├── TASK_BREAKDOWN.md
│   ├── TEST_PLAN.md
│   └── README.md
│
├── storage/
│   ├── settings.json
│   ├── workspaces/
│   ├── cache/
│   └── logs/
│
├── src/
│   ├── main.py
│   │
│   ├── presentation/
│   │   ├── start_window.py
│   │   └── viewer_window.py
│   │
│   ├── controllers/
│   │   └── viewer_controller.py
│   │
│   ├── domain/
│   │   └── workspace.py
│   │
│   ├── services/
│   │   ├── image_loader_service.py
│   │   ├── file_operation_service.py
│   │   ├── cache_manager.py
│   │   └── overlay_manager.py
│   │
│   ├── repositories/
│   │   ├── workspace_repository.py
│   │   └── settings_repository.py
│   │
│   ├── models/
│   │
│   ├── utils/
│   │
│   └── config/
│       └── constants.py
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# Directory Description

## assets/

Berisi seluruh aset statis aplikasi.

Contoh:

- Icon aplikasi
- Logo
- CSS / Style
- Placeholder image

---

## docs/

Seluruh dokumentasi proyek.

Dokumen pada folder ini menjadi acuan pengembangan aplikasi.

---

## storage/

Penyimpanan lokal aplikasi.

Berisi:

- konfigurasi
- workspace
- cache
- log

Folder ini dibuat otomatis saat aplikasi pertama kali dijalankan.

---

## src/

Seluruh source code aplikasi.

---

# Source Code Structure

## main.py

Entry point aplikasi.

Tanggung jawab:

- Inisialisasi aplikasi
- Memuat konfigurasi
- Menampilkan StartWindow

---

## presentation/

Seluruh komponen antarmuka pengguna.

File:

```text
start_window.py

viewer_window.py
```

Tidak mengandung business logic.

---

## controllers/

Berisi penghubung antara UI dan Domain.

File:

```text
viewer_controller.py
```

Tugas:

- menerima input keyboard
- mengatur navigasi
- memperbarui UI

---

## domain/

Berisi objek inti aplikasi.

File:

```text
workspace.py
```

Workspace menyimpan seluruh state aplikasi.

---

## services/

Berisi proses yang tidak menyimpan state.

File:

```text
image_loader_service.py

file_operation_service.py

cache_manager.py

overlay_manager.py
```

Services dapat dipanggil oleh Controller maupun Workspace sesuai kebutuhan arsitektur.

---

## repositories/

Berisi akses penyimpanan.

File:

```text
workspace_repository.py

settings_repository.py
```

Repository merupakan satu-satunya layer yang membaca maupun menulis file JSON.

---

## models/

Disediakan untuk model sederhana jika diperlukan di masa depan.

Pada MVP folder ini dapat tetap kosong.

---

## utils/

Berisi helper function umum.

Contoh:

- file helper
- path helper
- image helper
- validator

Utility tidak boleh menyimpan state aplikasi.

---

## config/

Berisi konfigurasi aplikasi.

Contoh:

```text
constants.py
```

Berisi:

- shortcut default
- ukuran thumbnail
- nama folder
- konstanta global

---

## tests/

Seluruh unit test dan integration test.

Struktur dapat mengikuti struktur pada folder `src`.

---

# Dependency Mapping

```text
presentation
        │
        ▼
controllers
        │
        ▼
domain
        │
        ▼
services
        │
        ▼
repositories
        │
        ▼
storage
```

Tidak diperbolehkan dependency yang melompati layer.

---

# Naming Convention

## File

Gunakan snake_case.

Contoh:

```text
viewer_controller.py

workspace_repository.py

image_loader_service.py
```

---

## Class

Gunakan PascalCase.

Contoh:

```text
ViewerController

Workspace

FileOperationService
```

---

## Function

Gunakan snake_case.

Contoh:

```python
load_workspace()

next_image()

copy_file()

save_settings()
```

---

# Future Expansion

Struktur folder ini dirancang agar mudah dikembangkan tanpa mengubah arsitektur dasar.

Contoh penambahan di masa depan:

```text
presentation/
    dialogs/

services/
    raw_decoder_service.py

controllers/
    settings_controller.py
```

Penambahan tersebut tidak mengubah struktur utama proyek.

---

# Summary

Struktur proyek Photo Picker MVP mengikuti pembagian berdasarkan layer arsitektur:

- **presentation** → antarmuka pengguna
- **controllers** → penghubung UI dan domain
- **domain** → state utama aplikasi (`Workspace`)
- **services** → proses stateless
- **repositories** → akses penyimpanan
- **storage** → data lokal aplikasi

Struktur ini menjaga kode tetap sederhana, mudah dipahami, dan siap dikembangkan seiring bertambahnya fitur tanpa perlu melakukan reorganisasi besar.
