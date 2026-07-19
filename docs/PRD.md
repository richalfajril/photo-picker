# PRD.md

# Photo Picker

## Product Requirements Document (PRD)

**Version:** 1.0
**Status:** Draft
**Platform:** Desktop (Windows/macOS)
**Target Language:** Python (PySide6)

---

# 1. Overview

## Product Name

**Photo Picker**

## Product Summary

Photo Picker adalah aplikasi desktop untuk mempercepat proses **photo culling** (seleksi foto) setelah sesi pemotretan.

Aplikasi memungkinkan fotografer menelusuri ribuan foto menggunakan keyboard dan langsung menyalin foto yang dipilih ke folder tujuan tanpa perlu melakukan proses ekspor atau sinkronisasi tambahan.

Target utama aplikasi adalah menghadirkan pengalaman seleksi yang cepat, sederhana, dan minim distraksi.

---

# 2. Problem Statement

Fotografer sering menghasilkan ribuan foto dalam satu sesi pemotretan.

Workflow yang umum dilakukan saat ini memiliki beberapa kendala:

- Membuka File Explorer atau aplikasi galeri.
- Memilih foto satu per satu menggunakan mouse.
- Melakukan copy manual ke folder lain.
- Membutuhkan banyak klik.
- Membutuhkan waktu lama.

Semakin banyak jumlah foto, semakin tidak efisien proses tersebut.

---

# 3. Goals

Photo Picker bertujuan untuk:

- Mempercepat proses photo culling.
- Mengurangi penggunaan mouse.
- Memungkinkan seluruh proses dilakukan menggunakan keyboard.
- Langsung menghasilkan folder berisi foto terpilih.
- Memungkinkan pengguna melanjutkan proses seleksi melalui Workspace tanpa kehilangan progres.
- Tetap responsif untuk ribuan hingga puluhan ribu foto.

---

# 4. Non Goals

Versi 1.0 tidak mencakup:

- Photo editing
- RAW development
- Color grading
- Metadata editing
- Face recognition
- AI photo selection
- Cloud synchronization

---

# 5. Target Users

Primary Users

- Wedding Photographer
- Event Photographer
- Street Photographer
- Sports Photographer
- Travel Photographer

Secondary Users

- Content Creator
- Social Media Manager
- Digital Agency

---

# 6. User Journey

```text
Launch Application
        │
        ▼
Create / Open Workspace
        │
        ▼
Load Workspace
        │
        ▼
Scan Images (First Time Only)
        │
        ▼
Load Preview
        │
        ▼
Fullscreen Viewer
        │
        ▼
Navigate & Select Photos
        │
        ▼
Save Workspace
        │
        ▼
Exit
```

---

# 7. Functional Requirements

## FR-001 Source Folder

User dapat memilih folder yang berisi foto.

Acceptance Criteria

- Mendukung folder lokal.
- Menampilkan dialog pemilihan folder.
- Melakukan validasi folder.

---

## FR-002 Destination Folder

User dapat memilih folder tujuan.

Acceptance Criteria

- Folder dapat dipilih menggunakan dialog.
- Jika belum ada maka dibuat otomatis.
- Tidak menimpa folder lain.

---

## FR-003 Scan Images

Aplikasi melakukan scanning seluruh file gambar.

Acceptance Criteria

- Menampilkan progress.
- Menghitung jumlah foto.
- Mengurutkan foto secara konsisten.

---

## FR-004 Image Viewer

Menampilkan satu foto dalam mode fullscreen.

Acceptance Criteria

- Foto memenuhi layar.
- Tetap mempertahankan rasio.
- Mendukung landscape dan portrait.

---

## FR-005 Navigation

Navigasi menggunakan keyboard.

Shortcut

| Key  | Action      |
| ---- | ----------- |
| →    | Next        |
| ←    | Previous    |
| Home | First Photo |
| End  | Last Photo  |

---

## FR-006 Photo Selection

Tekan Space untuk memilih foto.

Workflow

```
Space

↓

Copy File

↓

Play Sound

↓

Show Overlay

↓

Open Next Photo
```

Acceptance Criteria

- Copy berlangsung otomatis.
- Tidak ada dialog konfirmasi.
- Berpindah ke foto berikutnya secara otomatis.

---

## FR-007 Undo

User dapat membatalkan pilihan terakhir.

Acceptance Criteria

- Menghapus file dari folder tujuan.
- Mengurangi jumlah selected.
- Tetap berada pada foto yang sama.

Shortcut

```
Backspace
```

---

## FR-008 Overlay Feedback

Memberikan konfirmasi visual.

Copy

```
✔

COPIED
```

Undo

```
↶

REMOVED
```

Acceptance Criteria

- Overlay fullscreen.
- Durasi sekitar 250–300 ms.
- Tidak mengganggu navigasi.

---

## FR-009 Sound Feedback

Memberikan konfirmasi audio.

Acceptance Criteria

- Sound saat Copy.
- Sound saat Undo.
- Dapat dinonaktifkan.

---

## FR-010 Selected Indicator

Jika foto pernah dipilih maka ditampilkan badge.

```
✓ SELECTED
```

Acceptance Criteria

- Badge muncul saat membuka kembali foto.
- Tidak menghalangi foto.

---

## FR-011 Progress Information

Viewer menampilkan informasi.

- Nama file
- Posisi foto
- Total foto
- Jumlah foto terpilih

Contoh

```
IMG_2481.CR3

2481 / 5482

Selected : 531
```

---

## FR-012 Zoom

User dapat melakukan zoom.

Acceptance Criteria

- Scroll untuk zoom.
- Double click kembali ke ukuran normal.
- Tetap mempertahankan kualitas gambar.

---

## FR-013 Pan

Saat zoom aktif.

Acceptance Criteria

- Klik kiri + drag.
- Pergerakan halus.

---

## FR-014 Exit

Shortcut

```
Esc
```

Acceptance Criteria

Muncul dialog konfirmasi.

```
Exit?

Selected : 531

Continue

Exit
```

---

## FR-015 Workspace Recovery

Jika aplikasi ditutup sebelum proses seleksi selesai, Workspace akan disimpan sehingga pengguna dapat melanjutkan pekerjaan dari posisi terakhir.

Acceptance Criteria

- Workspace disimpan secara otomatis saat aplikasi ditutup.
- Workspace dapat dibuka kembali tanpa kehilangan progres.
- Posisi foto terakhir dipulihkan secara otomatis.

---

# 8. Supported File Formats

Image

- JPG
- JPEG
- PNG

RAW Preview

- CR2
- CR3
- NEF
- ARW
- RAF
- ORF
- DNG

---

# 9. Non Functional Requirements

## Performance

- Startup kurang dari 3 detik (untuk folder kecil).
- Navigasi terasa instan setelah preload.
- Mampu menangani hingga 50.000 foto tanpa crash.

---

## Reliability

- Tidak melakukan copy ganda.
- Tidak merusak file asli.
- Seluruh operasi copy bersifat non-destruktif.

---

## Usability

- Seluruh workflow dapat dilakukan menggunakan keyboard.
- Antarmuka minimalis.
- Tidak memerlukan pelatihan khusus.

---

## Responsiveness

Target perpindahan foto:

- <100 ms untuk gambar yang telah dipreload.
- Overlay tampil tanpa menghambat navigasi.

---

# 10. User Interface

## Configuration Window

Komponen:

- Workspace Name
- Source Folder
- Destination Folder
- Browse Button
- Fullscreen Toggle
- Sound Toggle
- Workspace Recovery Toggle
- Start Button

---

## Viewer

Komponen:

- Fullscreen Image
- Progress Information
- Selected Counter
- Overlay Feedback
- Selected Badge

---

# 11. Keyboard Shortcut

| Shortcut  | Action            |
| --------- | ----------------- |
| →         | Next Photo        |
| ←         | Previous Photo    |
| Space     | Copy + Next       |
| Backspace | Undo              |
| Scroll    | Zoom              |
| Drag      | Pan               |
| Home      | First Photo       |
| End       | Last Photo        |
| F         | Toggle Fullscreen |
| Esc       | Exit              |

---

# 12. Success Metrics

Produk dianggap berhasil apabila:

- User dapat melakukan seleksi foto tanpa mouse.
- Folder tujuan langsung berisi seluruh foto terpilih.
- Tidak terjadi kehilangan file.
- Navigasi terasa lancar pada ribuan foto.
- Workspace dapat dibuka kembali tanpa kehilangan progres.
- Waktu seleksi berkurang dibanding workflow manual.

---

# 13. MVP Scope

### Included

- Source Folder Picker
- Destination Folder Picker
- Fullscreen Viewer
- Keyboard Navigation
- Copy on Space
- Auto Next
- Undo
- Overlay Feedback
- Sound Feedback
- Zoom
- Pan
- Selected Counter
- Progress Counter
- Workspace Recovery
- RAW Preview
- Image Cache
- Background Preload

### Excluded

- AI Photo Selection
- Rating
- Color Labels
- Duplicate Detection
- Face Recognition
- Editing Tools
- Metadata Editor
- Batch Rename
- Export Settings
- Cloud Storage Integration

---

# 14. Future Roadmap

## Version 1.1

- Rating (1–5)
- Favorite
- Trash Mode
- Keyboard Customization

## Version 1.2

- Compare Two Photos
- Histogram
- EXIF Information
- Multiple Destination Profiles

## Version 2.0

- AI Blur Detection
- AI Duplicate Detection
- AI Best Shot Recommendation
- GPU Image Rendering
- Multi-Monitor Support
- Plugin System
