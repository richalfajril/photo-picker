# 📷 Photo Picker

## User Flow & UX Specification v1.0

---

# Overview

Photo Picker adalah aplikasi desktop sederhana untuk mempercepat proses **photo culling** (memilih foto terbaik) setelah sesi pemotretan.

Fokus utama aplikasi adalah memberikan workflow yang cepat, ringan, dan sepenuhnya dapat dioperasikan menggunakan keyboard.

Target penggunaan:

- Wedding Photographer
- Event Photographer
- Street Photographer
- Wildlife Photographer
- Travel Photographer
- Content Creator

---

# Goals

- Memilih ribuan foto dengan cepat.
- Tidak perlu menggunakan mouse selama proses seleksi.
- Langsung menyalin foto terpilih ke folder tujuan.
- Tampilan fullscreen agar fokus pada foto.
- Respons sangat cepat meskipun folder berisi ribuan foto.

---

# Workflow

```text
Run Application
      │
      ▼
Workspace Manager
      │
      ├── Open Existing Workspace
      │
      └── Create New Workspace
              │
              ▼
     Configuration Window
              │
              ▼
      Load Workspace
              │
              ▼
 Scan Images (First Time Only)
              │
              ▼
      Loading Preview
              │
              ▼
     Fullscreen Viewer
              │
              ▼
      Photo Selection
              │
              ▼
     Save Workspace
              │
              ▼
             Exit
```

---

# 1. Launch Application

User menjalankan aplikasi.

```bash
python main.py
```

atau

```text
PhotoPicker.exe
```

Yang muncul adalah window aplikasi, bukan terminal interaktif.

---

# 2. Configuration Window

Saat aplikasi dibuka, user melihat halaman konfigurasi.

```
┌─────────────────────────────────────────────────────────────┐
│                    📷 PHOTO PICKER                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📝 Workspace Name                                           │
│ [ Wedding Adit & Sinta______________________________ ]      │
│                                                             │
│ 📂 Source Folder                                            │
│ [ D:\Wedding\__________________________ ] [ Browse ]        │
│                                                             │
│ 📂 Destination Folder                                       │
│ [ D:\Wedding Selected\_________________ ] [ Browse ]        │
│                                                             │
│ ☑ Fullscreen                                                │
│ ☑ Auto Next after Copy                                      │
│ ☑ Sound Feedback                                            │
│ ☑ Workspace Recovery                                        │
│                                                             │
│                       [ START ]                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Source Folder

Folder yang berisi seluruh hasil foto.

Contoh:

```
D:\Wedding\
```

---

## Destination Folder

Folder tujuan hasil copy foto terpilih.

Contoh:

```
D:\Wedding Selected\
```

Jika folder belum ada:

```
Folder belum ditemukan.

Buat folder ini?

[ Yes ]
```

Program akan membuat folder secara otomatis.

---

## Settings

### Fullscreen

Viewer dibuka dalam mode fullscreen.

Default:

```
Enabled
```

---

### Auto Next after Copy

Setelah Space ditekan, otomatis berpindah ke foto berikutnya.

Default:

```
Enabled
```

---

### Sound Feedback

Memberikan efek suara ketika:

- Copy
- Undo

Default:

```
Enabled
```

---

### Workspace Recovery

Workspace akan disimpan secara otomatis ketika aplikasi ditutup sehingga proses seleksi dapat dilanjutkan di lain waktu.

Default:

```
Enabled
```

---

# 3. Scan Folder

Setelah START ditekan.

Program melakukan:

- Membuat Workspace baru (jika belum ada)
- Memuat Workspace yang sudah ada
- Validasi folder
- Scan seluruh file gambar (hanya saat pertama kali)
- Mengurutkan file
- Menghitung total foto

Contoh:

```
Scanning...

5482 photos found.
```

---

# 4. Loading

Program melakukan:

- Load foto pertama
- Preload beberapa foto berikutnya
- Menyiapkan cache

```
Loading Preview...

█████████████░░░░░░

248 / 5482
```

---

# 5. Fullscreen Viewer

Setelah loading selesai.

Viewer langsung fullscreen.

```
+------------------------------------------------------+

                    FOTO

+------------------------------------------------------+

IMG_2481.CR3

2481 / 5482

Selected : 531
```

UI dibuat seminimal mungkin.

Tidak ada:

- Sidebar
- Toolbar
- Ribbon
- Menu

Fokus utama hanya pada foto.

---

# Keyboard Shortcut

| Tombol    | Fungsi            |
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

# Photo Selection Flow

## Skip

Tekan

```
→
```

Program langsung membuka foto berikutnya.

Tidak ada proses lain.

---

## Select Photo

Tekan

```
Space
```

Program menjalankan urutan berikut.

```
Copy File
      │
      ▼
Play Sound
      │
      ▼
Overlay "COPIED"
      │
      ▼
Auto Next
```

---

# Copy Process

Saat Space ditekan.

Program:

```
Source

IMG_2481.CR3
```

↓

```
Copy
```

↓

```
Destination

IMG_2481.CR3
```

Jika file sudah ada.

```
Already Copied
```

Tidak dilakukan copy ulang.

---

# Copy Overlay

Overlay fullscreen muncul selama sekitar 250–300 ms.

```
██████████████████████████████

            ✔

          COPIED

██████████████████████████████
```

Setelah itu otomatis berpindah ke foto berikutnya.

---

# Sound Feedback

Saat berhasil copy.

```
🔊 Click
```

Durasi sekitar 100–200 ms.

---

# Next Photo

Setelah overlay selesai.

Program membuka foto berikutnya.

Workflow menjadi:

```
→ → → Space → → Space → Space → → → Space
```

---

# Undo

Jika salah memilih.

Tekan:

```
Backspace
```

Program:

- Menghapus file dari folder tujuan
- Mengurangi counter
- Memainkan suara
- Menampilkan overlay

---

# Undo Overlay

```
██████████████████████████████

            ↶

         REMOVED

██████████████████████████████
```

Viewer tetap berada di foto yang sama.

---

# Selected Badge

Jika user kembali ke foto yang sebelumnya sudah dipilih.

Muncul badge kecil.

```
✓ SELECTED
```

Tidak perlu overlay lagi.

---

# Progress Information

Bagian bawah viewer.

```
IMG_2481.CR3

2481 / 5482

Selected : 531
```

---

# Zoom

Mouse Wheel

```
100%

150%

200%

400%
```

Double Click

```
100%
```

---

# Pan

Saat zoom aktif.

Klik kiri.

↓

Geser foto.

---

# Supported Format

Image

- JPG
- JPEG
- PNG

RAW

- CR2
- CR3
- NEF
- ARW
- DNG
- RAF
- ORF

---

# Performance

Program menggunakan:

- Lazy Loading
- Memory Cache
- Background Preload

Sehingga navigasi tetap instan walaupun terdapat puluhan ribu foto.

---

# Exit

Tekan:

```
Esc
```

Dialog:

```
Keluar Workspace?

Workspace akan disimpan secara otomatis.

Selected : 531 photos

[ Continue ]

[ Exit ]
```

---

# Workspace Recovery

Jika aplikasi ditutup sebelum proses seleksi selesai, Workspace akan disimpan secara otomatis.

Saat aplikasi dibuka kembali, pengguna dapat melanjutkan Workspace terakhir.

```
Workspace ditemukan

Workspace
Wedding Adit & Sinta

Source
D:\Wedding

Destination
D:\Wedding Selected

Progress

2486 / 5482

Selected

531 photos

[ Continue Workspace ]

[ Start New Workspace ]
```

---

# Complete User Flow

```text
Run Application
      │
      ▼
Workspace Manager
      │
      ├── Open Existing Workspace
      │
      └── Create New Workspace
              │
              ▼
     Configuration Window
              │
              ├── Workspace Name
              ├── Source Folder
              ├── Destination Folder
              ├── Configure Options
              └── START
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
              ├── → Skip Photo
              ├── ← Previous Photo
              ├── Space
              │      ├── Copy File
              │      ├── Play Sound
              │      ├── Show "COPIED"
              │      └── Next Photo
              │
              ├── Backspace
              │      ├── Remove Copied File
              │      ├── Play Sound
              │      └── Show "REMOVED"
              │
              ├── Scroll = Zoom
              ├── Drag = Pan
              └── Esc = Save Workspace & Exit
              │
              ▼
      Destination Folder
```

---

# MVP Scope (v1.0)

## Core Features

- ✅ Configuration Window
- ✅ Source Folder Picker
- ✅ Destination Folder Picker
- ✅ Fullscreen Viewer
- ✅ Keyboard Navigation
- ✅ Space = Copy + Auto Next
- ✅ Backspace = Undo
- ✅ Fullscreen Overlay
- ✅ Sound Feedback
- ✅ Selected Badge
- ✅ Progress Counter
- ✅ Selected Counter
- ✅ Zoom & Pan
- ✅ Preload Image Cache
- ✅ JPG / PNG Support
- ✅ RAW Preview Support
- ✅ Workspace Recovery

---

# Future Enhancements (v2.0)

- ⭐ Rating (1–5)
- ❤️ Favorite
- 🗑 Trash Mode
- 📊 Workspace Statistics
- 📁 Multiple Destination Profiles
- 🎵 Custom Sound Packs
- 🌙 Dark/Light Theme
- ⚡ GPU-Accelerated Image Rendering
- 🖥 Multi-Monitor Support
- 🔄 Compare Two Photos Side-by-Side
- 🤖 AI Blur & Duplicate Detection
