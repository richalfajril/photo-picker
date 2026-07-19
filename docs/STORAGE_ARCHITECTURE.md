# STORAGE_ARCHITECTURE.md

# Photo Picker MVP

**Version:** 1.0
**Derived From:** SYSTEM_ARCHITECTURE.md v5.0

---

# 1. Overview

Photo Picker MVP menggunakan **file-based storage**.

Seluruh data aplikasi disimpan dalam bentuk file JSON pada penyimpanan lokal pengguna.

Aplikasi **tidak menggunakan database** pada MVP.

Keuntungan pendekatan ini:

- Mudah diimplementasikan
- Mudah dibackup
- Mudah dipindahkan
- Mudah diperiksa secara manual
- Tidak memerlukan proses instalasi database

---

# 2. Storage Structure

```text
storage/
│
├── settings.json
│
├── workspaces/
│   ├── wedding/
│   │   ├── workspace.json
│   │   └── selections.json
│   │
│   ├── graduation/
│   └── travel/
│
├── cache/
│
└── logs/
```

---

# 3. Storage Components

## settings.json

Menyimpan konfigurasi global aplikasi.

Contoh data:

- Tema aplikasi
- Ukuran window terakhir
- Daftar workspace terakhir
- Shortcut (jika dapat dikustomisasi)

Contoh struktur:

```json
{
  "theme": "dark",
  "window": {
    "width": 1600,
    "height": 900
  },
  "recent_workspaces": ["wedding", "graduation"]
}
```

---

## workspaces/

Setiap workspace memiliki folder sendiri.

Contoh:

```text
workspaces/
└── wedding/
```

Seluruh data workspace berada di dalam folder tersebut.

---

# 4. Workspace Storage

Struktur setiap workspace:

```text
workspace/
│
├── workspace.json
└── selections.json
```

---

## workspace.json

Berisi metadata workspace.

Contoh:

```json
{
  "name": "Wedding Adit & Sinta",
  "source_folder": "/Photos/Wedding",
  "destination_folder": "/Photos/Selected",
  "current_index": 152,
  "total_images": 1847,
  "created_at": "2026-07-19T10:00:00",
  "updated_at": "2026-07-19T11:45:30"
}
```

### Field Description

| Field              | Description             |
| ------------------ | ----------------------- |
| name               | Nama workspace          |
| source_folder      | Folder foto asli        |
| destination_folder | Folder hasil seleksi    |
| current_index      | Posisi foto terakhir    |
| total_images       | Total foto              |
| created_at         | Waktu pembuatan         |
| updated_at         | Waktu terakhir disimpan |

---

## selections.json

Berisi daftar foto yang telah dipilih.

Contoh:

```json
["IMG_0001.CR3", "IMG_0007.CR3", "IMG_0012.CR3", "IMG_0018.CR3"]
```

MVP hanya menyimpan nama file yang dipilih.

Tidak menyimpan:

- Rating
- Label warna
- Bookmark
- AI Score

---

# 5. Cache

```text
storage/
└── cache/
```

Digunakan untuk menyimpan data sementara yang membantu performa aplikasi.

Contoh:

- Thumbnail
- Preview yang telah diproses

Cache dapat dihapus kapan saja karena bukan sumber data utama.

---

# 6. Logs

```text
storage/
└── logs/
```

Digunakan untuk mencatat aktivitas dan error aplikasi.

Contoh:

```text
2026-07-19.log
```

Log dapat digunakan untuk proses debugging jika terjadi masalah.

---

# 7. Repository Mapping

Repository yang mengakses storage:

| Repository          | File            |
| ------------------- | --------------- |
| SettingsRepository  | settings.json   |
| WorkspaceRepository | workspace.json  |
| WorkspaceRepository | selections.json |

Repository menjadi satu-satunya komponen yang membaca atau menulis file JSON.

---

# 8. Data Flow

## Load Workspace

```text
Application
        │
        ▼
WorkspaceRepository
        │
        ▼
workspace.json
        │
        ▼
Workspace
```

---

## Save Workspace

```text
Workspace
        │
        ▼
WorkspaceRepository
        │
        ▼
workspace.json
```

---

## Save Selection

```text
Workspace
        │
        ▼
WorkspaceRepository
        │
        ▼
selections.json
```

---

# 9. Storage Principles

Seluruh penyimpanan mengikuti prinsip berikut:

- Seluruh data disimpan dalam format JSON.
- Satu folder mewakili satu Workspace.
- Setiap Workspace berdiri sendiri.
- Repository menjadi satu-satunya akses ke file.
- Cache bukan sumber data utama.
- Data harus tetap dapat dibaca dan dipulihkan tanpa database.

---

# Summary

Storage Photo Picker MVP menggunakan pendekatan **workspace-based file storage**.

Setiap Workspace memiliki folder sendiri yang berisi metadata (`workspace.json`) dan daftar foto terpilih (`selections.json`), sedangkan konfigurasi aplikasi disimpan secara terpisah pada `settings.json`.

Pendekatan ini sederhana, mudah dipelihara, mudah dibackup, dan sesuai dengan kebutuhan MVP tanpa menambahkan kompleksitas yang belum diperlukan.
