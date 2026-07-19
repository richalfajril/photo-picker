# CONFIGURATION.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini mendefinisikan seluruh konfigurasi aplikasi Photo Picker MVP.

Seluruh konfigurasi pengguna disimpan pada satu file:

```text
storage/settings.json
```

Konfigurasi bersifat **global**, artinya berlaku untuk seluruh Workspace, kecuali data yang memang disimpan pada masing-masing Workspace (misalnya Source Folder, Destination Folder, Current Index, dan Selected Images).

---

# 2. Configuration Architecture

```text
storage/
│
├── settings.json
├── workspaces/
├── cache/
└── logs/
```

- **settings.json** → Konfigurasi aplikasi.
- **workspaces/** → Data setiap Workspace.
- **cache/** → Cache aplikasi.
- **logs/** → Log aplikasi.

---

# 3. Configuration Categories

Konfigurasi dibagi menjadi beberapa kategori:

| Category    | Description                  |
| ----------- | ---------------------------- |
| Display     | Tampilan aplikasi            |
| Viewer      | Perilaku Viewer              |
| Audio       | Pengaturan suara             |
| Workspace   | Workspace Recovery           |
| Performance | Optimasi performa            |
| System      | Pengaturan internal aplikasi |

---

# 4. Default Configuration

```json
{
  "display": {
    "fullscreen": true
  },

  "viewer": {
    "auto_next": true,
    "remember_zoom": false
  },

  "audio": {
    "enabled": true
  },

  "workspace": {
    "recovery_enabled": true
  },

  "performance": {
    "cache_enabled": true,
    "preload_count": 3
  },

  "system": {
    "theme": "system",
    "language": "en"
  }
}
```

---

# 5. Display Configuration

## fullscreen

### Type

```text
Boolean
```

### Default

```text
true
```

### Description

Menentukan apakah Viewer dibuka dalam mode fullscreen.

---

# 6. Viewer Configuration

## auto_next

### Type

```text
Boolean
```

### Default

```text
true
```

### Description

Setelah foto berhasil dipilih, Viewer otomatis berpindah ke foto berikutnya.

---

## remember_zoom

### Type

```text
Boolean
```

### Default

```text
false
```

### Description

Apabila diaktifkan, tingkat zoom dipertahankan saat berpindah antar foto.

Fitur ini belum termasuk MVP dan disiapkan untuk pengembangan selanjutnya.

---

# 7. Audio Configuration

## enabled

### Type

```text
Boolean
```

### Default

```text
true
```

### Description

Mengaktifkan atau menonaktifkan efek suara saat Copy dan Undo.

---

# 8. Workspace Configuration

## recovery_enabled

### Type

```text
Boolean
```

### Default

```text
true
```

### Description

Apabila aktif, aplikasi akan mendeteksi Workspace yang belum selesai dan menawarkan untuk melanjutkannya saat aplikasi dibuka kembali.

---

# 9. Performance Configuration

## cache_enabled

### Type

```text
Boolean
```

### Default

```text
true
```

### Description

Mengaktifkan Memory Cache untuk mempercepat perpindahan antar gambar.

---

## preload_count

### Type

```text
Integer
```

### Default

```text
3
```

### Description

Jumlah gambar yang dipersiapkan (preload) di depan posisi saat ini.

Contoh:

```text
Current Image
      │
      ▼
[125]
[126]
[127]
```

Semakin besar nilai preload, semakin besar penggunaan memori.

---

# 10. System Configuration

## theme

### Type

```text
String
```

### Values

- system
- light
- dark

### Default

```text
system
```

### Description

Tema antarmuka aplikasi.

Pada MVP hanya tersedia nilai `system`.

---

## language

### Type

```text
String
```

### Default

```text
en
```

### Description

Bahasa antarmuka aplikasi.

Untuk MVP hanya tersedia bahasa Inggris.

---

# 11. Configuration Lifecycle

```text
Application Start
        │
        ▼
Load settings.json
        │
        ▼
Validate Configuration
        │
        ├──────── Invalid
        │
        ▼
Restore Default Value
        │
        ▼
Launch Application
```

---

# 12. Validation Rules

| Setting          | Validation          |
| ---------------- | ------------------- |
| fullscreen       | Boolean             |
| auto_next        | Boolean             |
| remember_zoom    | Boolean             |
| enabled          | Boolean             |
| recovery_enabled | Boolean             |
| cache_enabled    | Boolean             |
| preload_count    | Integer ≥ 0         |
| theme            | system, light, dark |
| language         | Valid language code |

Jika konfigurasi tidak valid:

- Gunakan nilai bawaan (default).
- Catat peringatan ke log.
- Jangan menghentikan aplikasi.

---

# 13. Save Strategy

Konfigurasi disimpan ketika:

- Pengguna menekan tombol **Start** pada Startup Window.
- Pengguna mengubah preferensi aplikasi (fitur mendatang).
- Aplikasi ditutup dengan normal.

Konfigurasi tidak disimpan setiap kali pengguna berpindah foto agar mengurangi operasi tulis ke disk.

---

# 14. Configuration Ownership

| Setting            | Stored In       |
| ------------------ | --------------- |
| Fullscreen         | settings.json   |
| Auto Next          | settings.json   |
| Sound              | settings.json   |
| Workspace Recovery | settings.json   |
| Cache              | settings.json   |
| Theme              | settings.json   |
| Language           | settings.json   |
| Workspace Name     | workspace.json  |
| Source Folder      | workspace.json  |
| Destination Folder | workspace.json  |
| Current Index      | workspace.json  |
| Selected Images    | selections.json |

---

# 15. Future Configuration (v2.0)

Konfigurasi berikut belum termasuk dalam MVP:

- Thumbnail Size
- Overlay Duration
- Copy Confirmation
- Slideshow Speed
- Compare Mode
- Default Zoom Level
- Keyboard Shortcut Customization
- Recent Workspaces
- Automatic Update

---

# 16. Summary

Photo Picker menggunakan satu file konfigurasi global (`settings.json`) untuk menyimpan preferensi aplikasi. Seluruh data yang berkaitan dengan proses seleksi disimpan terpisah pada Workspace, sehingga konfigurasi aplikasi dan data pekerjaan pengguna tidak saling bercampur. Struktur ini menjaga konfigurasi tetap sederhana, mudah dipelihara, dan mudah diperluas pada versi berikutnya.
