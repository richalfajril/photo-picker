# UI_SPEC.md

# Photo Picker

## User Interface Specification

**Version:** 1.0
**Status:** Draft

---

# 1. Overview

Dokumen ini mendefinisikan seluruh tampilan (screen), komponen, layout, interaksi, dan state pada aplikasi **Photo Picker**.

Tujuan utama desain UI adalah:

- Fokus pada foto.
- Navigasi sangat cepat.
- Hampir seluruh interaksi menggunakan keyboard.
- Minim distraksi.
- Konsisten di Windows maupun macOS.

---

# 2. Design Principles

## Minimal UI

Foto harus menjadi elemen terbesar pada layar.

Semua komponen lain hanya sebagai pendukung.

---

## Keyboard First

Seluruh workflow utama dapat dilakukan tanpa mouse.

Mouse hanya digunakan untuk:

- Zoom
- Drag (Pan)
- Folder Picker

---

## Zero Distraction

Tidak ada:

- Ribbon
- Sidebar
- Toolbar permanen
- Floating menu
- Pop-up yang tidak diperlukan

---

## Instant Feedback

Setiap aksi memberikan feedback visual dan audio.

Contoh:

- Overlay "COPIED"
- Overlay "REMOVED"
- Click Sound

---

# 3. Screen List

Aplikasi terdiri dari 5 screen utama.

| Screen                    | Purpose                          |
| ------------------------- | -------------------------------- |
| Startup Window            | Membuat atau membuka Workspace   |
| Loading Screen            | Scan & preload gambar            |
| Viewer                    | Seleksi foto                     |
| Exit Dialog               | Konfirmasi keluar                |
| Workspace Recovery Dialog | Melanjutkan Workspace sebelumnya |

---

# 4. Startup Window

## Purpose

Memilih folder dan konfigurasi awal.

---

## Layout

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                     📷 PHOTO PICKER                         │
│                                                             │
│  Workspace Name                                             │
│  ┌────────────────────────────────────────────┐             │
│  │ Wedding Adit & Sinta                       │             │
│  └────────────────────────────────────────────┘             │
│                                                             │
│  Source Folder                                              │
│  ┌──────────────────────────────────────┐ [ Browse ]        │
│  │ D:\Wedding\                          │                   │
│  └──────────────────────────────────────┘                   │
│                                                             │
│  Destination Folder                                         │
│  ┌──────────────────────────────────────┐ [ Browse ]        │
│  │ D:\Wedding Selected\                 │                   │
│  └──────────────────────────────────────┘                   │
│                                                             │
│  ☑ Fullscreen                                               │
│  ☑ Auto Next after Copy                                     │
│  ☑ Sound Feedback                                           │
│  ☑ Workspace Recovery                                       │
│                                                             │
│                     [ START ]                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### Workspace Name

Type

- Text Input

Description

Nama Workspace yang digunakan untuk menyimpan progres seleksi.

Contoh:

Wedding Adit & Sinta

### Source Folder

Type

- Text Input
- Read Only

Action

Browse Folder

---

### Destination Folder

Type

- Text Input
- Read Only

Action

Browse Folder

---

### Browse Button

Action

Open Native Folder Picker

---

### Checkboxes

- Fullscreen
- Auto Next after Copy
- Sound Feedback
- Workspace Recovery

---

### Start Button

Action

Saat tombol START ditekan, aplikasi akan:

- Membuat Workspace baru apabila belum ada.
- Memuat Workspace yang sudah ada apabila ditemukan.
- Memulai proses scan gambar (hanya saat pertama kali).
- Membuka Viewer setelah proses loading selesai.

Disabled apabila:

- Workspace Name kosong.
- Source Folder belum dipilih.
- Destination Folder belum dipilih.

---

# 5. Loading Screen

## Purpose

Memberikan informasi bahwa aplikasi sedang mempersiapkan gambar.

---

## Layout

```text
┌──────────────────────────────────────┐

        Loading Images...

        ███████████░░░░░░░░

          248 / 5482

 Preparing image cache...

└──────────────────────────────────────┘
```

---

## Components

Progress Bar

Progress Text

Status Text

---

# 6. Viewer Screen

## Purpose

Screen utama aplikasi.

---

## Layout

```text
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                                                            │
│                                                            │
│                      PHOTO AREA                            │
│                                                            │
│                                                            │
│                                                            │
│                                                            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│ IMG_2481.CR3                                               │
│                                                            │
│ 2481 / 5482                                                │
│                                                            │
│ Selected : 531                                             │
└────────────────────────────────────────────────────────────┘
```

---

# 7. Viewer Components

## Photo Area

Mengisi ±95% layar.

Behavior

- Fit to screen
- Maintain aspect ratio
- High quality rendering

---

## Bottom Information Bar

Height

±60 px

Isi:

- Filename
- Current Position
- Total Images
- Selected Counter

---

Contoh

```text
IMG_2481.CR3

2481 / 5482

Selected : 531
```

---

# 8. Overlay Feedback

Overlay muncul ketika:

- Copy berhasil
- Undo berhasil
- Error

Overlay menggunakan latar hitam transparan.

Opacity

40–50%

---

## Copy Overlay

```text
████████████████████████████

            ✔

          COPIED

████████████████████████████
```

Durasi

250–300 ms

---

## Undo Overlay

```text
████████████████████████████

            ↶

         REMOVED

████████████████████████████
```

Durasi

250–300 ms

---

## Error Overlay

```text
████████████████████████████

            !

      COPY FAILED

████████████████████████████
```

---

# 9. Selected Badge

Jika foto sudah pernah dipilih.

Muncul badge kecil.

Lokasi

Top Right

```text
┌─────────────────────┐

             ✓ SELECTED

        PHOTO

└─────────────────────┘
```

Badge tidak menutupi area penting foto.

---

# 10. Zoom

Input

Mouse Wheel

Behavior

- Smooth Zoom
- Center pada posisi cursor

Zoom Level

- 100%
- 150%
- 200%
- 300%
- 400%

---

# 11. Pan

Saat zoom aktif.

Input

Left Mouse Button + Drag

Behavior

Smooth Movement

---

# 12. Exit Dialog

Shortcut

Esc

## Layout

```text
┌──────────────────────────────┐

 Exit Workspace?

 Workspace akan disimpan
 secara otomatis.

 Selected

 531 Photos

 [ Continue ]

 [ Exit ]

└──────────────────────────────┘
```

---

## Layout

```text
┌────────────────────────────┐

 Exit Photo Picker?

 Selected

 531 Photos

 [ Continue ]

 [ Exit ]

└────────────────────────────┘
```

---

# 13. Workspace Recovery Dialog

Muncul ketika aplikasi menemukan Workspace yang belum selesai.

```text
┌────────────────────────────────────┐

 Workspace Found

 Workspace

 Wedding Adit & Sinta

 Source

 D:\Wedding

 Destination

 D:\Wedding Selected

 Progress

 2481 / 5482

 Selected

 531 Photos

 [ Continue Workspace ]

 [ Start New Workspace ]

└────────────────────────────────────┘
```

---

# 14. Keyboard Interaction

| Key       | Action            |
| --------- | ----------------- |
| →         | Next              |
| ←         | Previous          |
| Space     | Copy              |
| Backspace | Undo              |
| Home      | First Image       |
| End       | Last Image        |
| F         | Toggle Fullscreen |
| Esc       | Exit              |

---

# 15. Mouse Interaction

| Action       | Result     |
| ------------ | ---------- |
| Scroll       | Zoom       |
| Left Drag    | Pan        |
| Double Click | Reset Zoom |

---

# 16. UI States

## Idle

Viewer siap menerima input.

---

## Loading

Input keyboard dinonaktifkan.

Progress bar aktif.

---

## Copying

Overlay tampil.

Keyboard dikunci sementara ±250 ms.

---

## Undo

Overlay REMOVED.

Tetap pada foto saat ini.

---

## Error

Overlay merah.

Menampilkan pesan kesalahan.

---

# 17. Visual Hierarchy

Prioritas elemen:

1. Foto
2. Overlay Feedback
3. Progress Information
4. Selected Badge

Elemen lain bersifat sekunder.

---

# 18. Responsive Behavior

## Landscape

Foto memenuhi tinggi layar.

---

## Portrait

Foto memenuhi tinggi layar dengan ruang kosong di sisi kiri dan kanan jika diperlukan.

---

## Ultra Wide Monitor

Foto tetap berada di tengah layar.

Bottom Information Bar tetap memenuhi lebar layar.

---

# 19. Animation

## Overlay

Animation

Fade In

↓

Hold

↓

Fade Out

Durasi

250–300 ms

---

## Next Image

Tidak menggunakan animasi transisi.

Tujuan:

Navigasi terasa instan.

---

## Zoom

Smooth interpolation.

---

# 20. Color Palette

Background

```text
#111111
```

Text

```text
#FFFFFF
```

Overlay Background

```text
Black 50% Opacity
```

Success

```text
#22C55E
```

Warning

```text
#FACC15
```

Error

```text
#EF4444
```

---

# 21. Typography

Primary Font

- Segoe UI (Windows)
- SF Pro / San Francisco (macOS)

Fallback

- Arial
- Sans Serif

---

# 22. Iconography

Gunakan ikon sederhana.

| Action   | Icon |
| -------- | ---- |
| Copy     | ✔    |
| Undo     | ↶    |
| Error    | !    |
| Selected | ✓    |
| Folder   | 📂   |

---

# 23. Accessibility

- Kontras warna tinggi.
- Seluruh fungsi utama dapat diakses melalui keyboard.
- Target area tombol minimal 40×40 px.
- Teks tetap terbaca pada resolusi Full HD hingga 4K.

---

# 24. Future UI Enhancements

Versi berikutnya dapat menambahkan:

- Mini Thumbnail Strip
- EXIF Information Panel
- Histogram Panel
- Compare Mode (Side-by-Side)
- Rating Overlay (⭐ 1–5)
- Favorite Indicator (❤️)
- Dark / Light Theme
- Custom Overlay Theme

---

# 25. UI Summary

```text
Application
│
├── Startup Window
│     ├── Workspace Name
│     ├── Source Folder
│     ├── Destination Folder
│     ├── Settings
│     └── Start Button
│
├── Loading Screen
│     ├── Progress Bar
│     └── Status Text
│
├── Viewer
│     ├── Photo Area
│     ├── Bottom Information Bar
│     ├── Overlay Feedback
│     └── Selected Badge
│
├── Workspace Recovery Dialog
│
└── Exit Dialog
```

---

# 26. Design Philosophy

Photo Picker mengutamakan **kecepatan seleksi**, bukan banyaknya fitur.

Setiap elemen antarmuka harus memiliki tujuan yang jelas. Jika suatu komponen tidak membantu pengguna memilih foto lebih cepat, maka komponen tersebut tidak perlu ditampilkan.

Prinsip utama UI adalah:

- **Photo First** — foto selalu menjadi fokus utama.
- **Keyboard First** — seluruh alur seleksi dapat dilakukan tanpa mouse.
- **Minimal Distraction** — antarmuka sesederhana mungkin.
- **Instant Feedback** — setiap aksi memberikan konfirmasi visual dan audio yang cepat.
- **Performance First** — navigasi harus terasa instan meskipun menangani ribuan foto.
