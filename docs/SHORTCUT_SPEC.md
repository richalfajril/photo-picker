# SHORTCUT_SPEC.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini mendefinisikan seluruh keyboard shortcut dan interaksi mouse pada Photo Picker MVP.

Seluruh shortcut dalam dokumen ini menjadi **Single Source of Truth**. Apabila terjadi perubahan shortcut di masa mendatang, perubahan hanya dilakukan pada dokumen ini, kemudian disesuaikan pada implementasi dan dokumentasi lainnya.

---

# 2. Design Principles

Photo Picker dirancang dengan prinsip:

- **Keyboard First** — seluruh workflow utama dapat dilakukan tanpa mouse.
- **Minimal Movement** — shortcut dipilih agar mudah dijangkau tangan kiri maupun kanan.
- **Instant Response** — setiap input harus memberikan respons secepat mungkin.
- **Consistency** — shortcut tidak berubah antar platform (Windows & macOS).

---

# 3. Keyboard Shortcut Reference

| Key       | Action            | Description                                                      |
| --------- | ----------------- | ---------------------------------------------------------------- |
| →         | Next Photo        | Menampilkan foto berikutnya                                      |
| ←         | Previous Photo    | Menampilkan foto sebelumnya                                      |
| Home      | First Photo       | Lompat ke foto pertama                                           |
| End       | Last Photo        | Lompat ke foto terakhir                                          |
| Space     | Copy + Next       | Menyalin foto ke Destination Folder lalu membuka foto berikutnya |
| Backspace | Undo              | Membatalkan seleksi terakhir                                     |
| F         | Toggle Fullscreen | Masuk atau keluar dari mode fullscreen                           |
| Esc       | Exit              | Menampilkan dialog keluar                                        |

---

# 4. Mouse Interaction

| Action            | Function   |
| ----------------- | ---------- |
| Scroll Up         | Zoom In    |
| Scroll Down       | Zoom Out   |
| Left Click + Drag | Pan Image  |
| Double Click      | Reset Zoom |

Mouse hanya digunakan untuk fitur visual dan tidak diperlukan selama proses seleksi utama.

---

# 5. Navigation

## Next Photo

**Shortcut**

```
→
```

Behavior

- Menampilkan foto berikutnya.
- Tidak mengubah status seleksi.
- Tidak memunculkan overlay.

---

## Previous Photo

**Shortcut**

```
←
```

Behavior

- Menampilkan foto sebelumnya.
- Tidak mengubah status seleksi.

---

## First Photo

**Shortcut**

```
Home
```

Behavior

- Langsung membuka foto pertama.

---

## Last Photo

**Shortcut**

```
End
```

Behavior

- Langsung membuka foto terakhir.

---

# 6. Selection

## Copy + Next

**Shortcut**

```
Space
```

Workflow

```text
Copy Image
      │
      ▼
Update Workspace
      │
      ▼
Play Sound
      │
      ▼
Show Overlay
      │
      ▼
Open Next Photo
```

Behavior

- File dicopy ke Destination Folder.
- Workspace diperbarui.
- Selected Counter bertambah.
- Overlay "COPIED" ditampilkan.
- Otomatis membuka foto berikutnya.

---

## Undo

**Shortcut**

```
Backspace
```

Workflow

```text
Remove Copied File
        │
        ▼
Update Workspace
        │
        ▼
Play Sound
        │
        ▼
Show Overlay
```

Behavior

- Menghapus file dari Destination Folder.
- Workspace diperbarui.
- Selected Counter berkurang.
- Overlay "REMOVED" ditampilkan.
- Tetap berada pada foto saat ini.

---

# 7. Viewer

## Toggle Fullscreen

**Shortcut**

```
F
```

Behavior

- Berpindah antara mode fullscreen dan windowed.
- Tidak mengubah posisi foto.
- Tidak mengubah zoom.

---

## Exit

**Shortcut**

```
Esc
```

Behavior

- Menampilkan Exit Dialog.
- Workspace akan disimpan sebelum aplikasi ditutup.
- Pengguna dapat membatalkan proses keluar.

---

# 8. Zoom

## Zoom In

Input

```
Mouse Wheel Up
```

Behavior

- Memperbesar gambar.
- Titik zoom mengikuti posisi kursor.

---

## Zoom Out

Input

```
Mouse Wheel Down
```

Behavior

- Memperkecil gambar.

---

## Reset Zoom

Input

```
Double Click
```

Behavior

- Mengembalikan zoom ke 100%.

---

# 9. Pan

Input

```
Left Mouse Button + Drag
```

Behavior

- Menggeser gambar ketika kondisi zoom lebih dari 100%.
- Tidak aktif ketika gambar berada pada ukuran normal.

---

# 10. Shortcut Priority

Apabila beberapa shortcut ditekan secara bersamaan, aplikasi memproses berdasarkan prioritas berikut:

| Priority | Action     |
| -------- | ---------- |
| 1        | Exit       |
| 2        | Undo       |
| 3        | Copy       |
| 4        | Navigation |
| 5        | Zoom & Pan |

---

# 11. Shortcut Availability

| Shortcut  | Startup | Loading | Viewer | Exit Dialog |
| --------- | :-----: | :-----: | :----: | :---------: |
| →         |    ✖    |    ✖    |   ✔    |      ✖      |
| ←         |    ✖    |    ✖    |   ✔    |      ✖      |
| Home      |    ✖    |    ✖    |   ✔    |      ✖      |
| End       |    ✖    |    ✖    |   ✔    |      ✖      |
| Space     |    ✖    |    ✖    |   ✔    |      ✖      |
| Backspace |    ✖    |    ✖    |   ✔    |      ✖      |
| F         |    ✖    |    ✖    |   ✔    |      ✖      |
| Esc       |    ✔    |    ✔    |   ✔    |      ✔      |

---

# 12. Future Shortcuts (v2.0)

Shortcut berikut belum termasuk dalam MVP dan hanya menjadi referensi untuk pengembangan berikutnya.

| Key      | Planned Action   |
| -------- | ---------------- |
| 1–5      | Rating Photo     |
| Delete   | Trash Mode       |
| C        | Compare Mode     |
| I        | EXIF Information |
| T        | Thumbnail Strip  |
| H        | Histogram        |
| Ctrl + Z | Multi-Level Undo |

---

# 13. Summary

Photo Picker menggunakan pendekatan **Keyboard First**, sehingga seluruh proses seleksi dapat dilakukan tanpa mouse.

Mouse hanya digunakan untuk fitur visual seperti Zoom dan Pan, sedangkan seluruh proses navigasi, seleksi, pembatalan, dan keluar aplikasi dilakukan menggunakan keyboard.

Dokumen ini menjadi acuan utama seluruh implementasi keyboard shortcut pada Photo Picker MVP.
