# STATE_MACHINE.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini mendefinisikan seluruh state aplikasi Photo Picker beserta transisi antar state.

State Machine digunakan sebagai acuan implementasi pada `ViewerController` agar perilaku aplikasi tetap konsisten dan mudah dipelihara.

---

# 2. State Overview

| State    | Description                           |
| -------- | ------------------------------------- |
| Startup  | Aplikasi baru dijalankan              |
| Loading  | Memuat Workspace dan gambar           |
| Viewing  | Pengguna melihat foto                 |
| Copying  | Menyalin foto ke Destination Folder   |
| Undoing  | Membatalkan seleksi terakhir          |
| Recovery | Menampilkan Workspace Recovery Dialog |
| Exiting  | Menampilkan Exit Dialog               |
| Closed   | Aplikasi telah ditutup                |

---

# 3. High-Level State Diagram

```text
                ┌──────────────┐
                │   Startup    │
                └──────┬───────┘
                       │
                       ▼
          Workspace ditemukan?
                 │          │
              Ya │          │ Tidak
                 ▼          ▼
          ┌──────────┐   ┌──────────┐
          │ Recovery │   │ Loading  │
          └────┬─────┘   └────┬─────┘
               │              │
               └──────┬───────┘
                      ▼
               ┌────────────┐
               │  Viewing   │
               └─┬────┬───┬─┘
                 │    │   │
     Space       │    │   │ Esc
                 │    │   ▼
                 ▼    │ Exiting
            Copying   │
                 │    │
                 ▼    │
              Viewing │
                      │
          Backspace   │
                      ▼
                 Undoing
                      │
                      ▼
                  Viewing

Exiting
   │
   ▼
Closed
```

---

# 4. Startup State

## Description

Aplikasi pertama kali dijalankan.

### Entry

- Inisialisasi aplikasi.
- Membaca `settings.json`.
- Menampilkan `StartWindow`.

### Exit

- Pengguna menekan tombol **Start**.

---

# 5. Recovery State

## Description

State ketika Workspace sebelumnya ditemukan.

### Entry

- Workspace Recovery diaktifkan.
- Workspace valid ditemukan.

### User Actions

- Continue Workspace
- Start New Workspace

### Exit

Menuju:

- Loading

---

# 6. Loading State

## Description

Memuat seluruh data Workspace.

### Responsibilities

- Scan folder.
- Membaca daftar gambar.
- Memuat cache awal.
- Menyiapkan Viewer.

### Exit Condition

Semua data berhasil dimuat.

Menuju:

- Viewing

---

# 7. Viewing State

## Description

State utama aplikasi.

Seluruh interaksi pengguna dilakukan pada state ini.

### Available Actions

| Input     | Next State |
| --------- | ---------- |
| →         | Viewing    |
| ←         | Viewing    |
| Home      | Viewing    |
| End       | Viewing    |
| Space     | Copying    |
| Backspace | Undoing    |
| Esc       | Exiting    |

---

# 8. Copying State

## Description

Menyalin foto ke Destination Folder.

### Workflow

```text
Copy File
    │
    ▼
Update Workspace
    │
    ▼
Update Counter
    │
    ▼
Show Overlay
    │
    ▼
Play Sound
```

### Success

Kembali ke:

- Viewing

### Failure

- Tampilkan "COPY FAILED"
- Kembali ke Viewing

---

# 9. Undoing State

## Description

Menghapus hasil seleksi terakhir.

### Workflow

```text
Delete File
     │
     ▼
Update Workspace
     │
     ▼
Update Counter
     │
     ▼
Show Overlay
     │
     ▼
Play Sound
```

### Exit

Kembali ke:

- Viewing

---

# 10. Exiting State

## Description

Menampilkan dialog keluar aplikasi.

### User Options

- Continue Working
- Exit Application

### Workflow

```text
Show Exit Dialog
       │
       ├──────── Continue
       │
       ▼
    Viewing

atau

Save Workspace
       │
       ▼
Close Application
```

---

# 11. Closed State

## Description

Aplikasi telah ditutup.

### Entry

- Workspace telah disimpan.
- Seluruh resource dilepas.
- Cache dibersihkan.

---

# 12. Invalid Transitions

Transisi berikut tidak diperbolehkan.

| From    | To      | Reason                  |
| ------- | ------- | ----------------------- |
| Startup | Viewing | Workspace belum dimuat  |
| Loading | Copying | Viewer belum siap       |
| Loading | Undoing | Belum ada gambar aktif  |
| Copying | Exiting | Operasi belum selesai   |
| Undoing | Exiting | Operasi belum selesai   |
| Closed  | Viewing | Aplikasi sudah berhenti |

---

# 13. Event Summary

| Event               | Current State | Next State |
| ------------------- | ------------- | ---------- |
| Application Start   | -             | Startup    |
| Start Button        | Startup       | Loading    |
| Workspace Found     | Startup       | Recovery   |
| Continue Workspace  | Recovery      | Loading    |
| Start New Workspace | Recovery      | Loading    |
| Loading Complete    | Loading       | Viewing    |
| Next Photo          | Viewing       | Viewing    |
| Previous Photo      | Viewing       | Viewing    |
| Copy Photo          | Viewing       | Copying    |
| Copy Complete       | Copying       | Viewing    |
| Undo                | Viewing       | Undoing    |
| Undo Complete       | Undoing       | Viewing    |
| Exit                | Viewing       | Exiting    |
| Cancel Exit         | Exiting       | Viewing    |
| Confirm Exit        | Exiting       | Closed     |

---

# 14. State Rules

- Hanya satu state aktif pada satu waktu.
- Transisi harus melalui event yang valid.
- Workspace disimpan sebelum berpindah ke `Closed`.
- Operasi Copy dan Undo bersifat atomik; state tidak boleh berubah hingga operasi selesai.
- Navigasi hanya tersedia pada state `Viewing`.

---

# 15. Summary

Photo Picker menggunakan pendekatan **Finite State Machine (FSM)** dengan delapan state utama untuk mengelola alur aplikasi secara konsisten.

Seluruh logika perpindahan state dipusatkan pada `ViewerController`, sehingga setiap aksi pengguna menghasilkan transisi yang terprediksi, mudah diuji, dan mudah dipelihara.
