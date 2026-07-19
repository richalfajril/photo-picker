# ERROR_HANDLING.md

# Photo Picker MVP

**Version:** 1.0

---

# 1. Overview

Dokumen ini mendefinisikan strategi penanganan error pada Photo Picker MVP.

Tujuan utama adalah:

- Mencegah kehilangan data pengguna.
- Menjaga aplikasi tetap berjalan (Graceful Degradation).
- Memberikan pesan yang jelas kepada pengguna.
- Mencatat error penting ke log untuk keperluan debugging.

---

# 2. Error Handling Principles

Photo Picker menerapkan prinsip berikut:

- **Fail Safely** — jangan merusak file pengguna.
- **Recover Whenever Possible** — lanjutkan proses jika memungkinkan.
- **Clear Feedback** — tampilkan pesan yang mudah dipahami.
- **Automatic Logging** — simpan informasi error untuk analisis.
- **Never Crash Unexpectedly** — hindari aplikasi berhenti mendadak.

---

# 3. Error Severity

| Level    | Description                      | Action                                           |
| -------- | -------------------------------- | ------------------------------------------------ |
| Info     | Informasi biasa                  | Tidak perlu tindakan                             |
| Warning  | Masalah ringan                   | Tampilkan notifikasi                             |
| Error    | Operasi gagal                    | Batalkan operasi dan tampilkan pesan             |
| Critical | Aplikasi tidak dapat melanjutkan | Simpan Workspace lalu tutup aplikasi dengan aman |

---

# 4. Startup Errors

## Workspace Name Kosong

### Condition

Pengguna belum mengisi nama Workspace.

### Handling

- Tombol **Start** tetap nonaktif.
- Tampilkan validasi pada field.

---

## Source Folder Belum Dipilih

### Handling

- Tombol **Start** tetap nonaktif.
- Minta pengguna memilih folder.

---

## Destination Folder Belum Dipilih

### Handling

- Tombol **Start** tetap nonaktif.
- Minta pengguna memilih folder.

---

## Folder Tidak Ditemukan

### Possible Causes

- Folder dipindahkan.
- Folder dihapus.
- Drive dilepas.

### Handling

- Tampilkan dialog kesalahan.
- Kembali ke Startup Window.
- Minta pengguna memilih folder lain.

---

# 5. Workspace Errors

## Workspace Tidak Ditemukan

### Handling

- Abaikan proses Recovery.
- Buat Workspace baru.

---

## Workspace Rusak

### Condition

File JSON tidak dapat dibaca atau format tidak valid.

### Handling

- Tampilkan pesan bahwa Workspace rusak.
- Beri pilihan membuat Workspace baru.
- Jangan menghapus file Workspace secara otomatis.

---

## Gagal Menyimpan Workspace

### Handling

- Tampilkan pesan kesalahan.
- Coba simpan kembali.
- Catat error ke log.

---

# 6. Image Loading Errors

## Folder Kosong

### Handling

- Tampilkan informasi bahwa tidak ada gambar yang ditemukan.
- Jangan membuka Viewer.

---

## Format Tidak Didukung

### Handling

- Lewati file tersebut.
- Lanjutkan proses scan.

---

## File Gambar Rusak

### Handling

- Lewati file.
- Catat ke log.
- Lanjutkan ke gambar berikutnya.

---

## RAW Preview Gagal Dibuat

### Handling

- Gunakan thumbnail bawaan jika tersedia.
- Jika tidak tersedia, tampilkan placeholder.
- Lanjutkan proses.

---

# 7. File Operation Errors

## Copy Gagal

### Possible Causes

- Hak akses tidak cukup.
- Disk penuh.
- File sedang digunakan aplikasi lain.

### Handling

- Overlay: **COPY FAILED**
- Jangan menambah Selected Counter.
- Jangan memperbarui Workspace.
- Tetap berada pada foto saat ini.
- Catat ke log.

---

## File Sudah Ada

### Handling

- Jangan menimpa file.
- Tandai sebagai sudah dipilih.
- Lanjutkan sesuai aturan aplikasi.

---

## Undo Gagal

### Possible Causes

- File sudah dihapus secara manual.
- Tidak memiliki izin menghapus.

### Handling

- Tampilkan pesan kesalahan.
- Jangan mengubah Workspace jika operasi gagal.
- Catat ke log.

---

# 8. Viewer Errors

## Gagal Memuat Gambar

### Handling

- Tampilkan placeholder.
- Izinkan pengguna berpindah ke foto berikutnya.
- Catat ke log.

---

## Zoom Error

### Handling

- Reset zoom ke nilai default.
- Jangan menutup Viewer.

---

# 9. Cache Errors

## Cache Tidak Dapat Dibuat

### Handling

- Nonaktifkan cache.
- Muat gambar langsung dari disk.
- Catat peringatan ke log.

---

## Cache Rusak

### Handling

- Hapus cache lama.
- Bangun ulang cache secara otomatis.

---

# 10. Recovery Errors

## Workspace Recovery Gagal

### Handling

- Tampilkan dialog bahwa Workspace tidak dapat dipulihkan.
- Tawarkan membuat Workspace baru.

---

## Progress Tidak Valid

### Condition

Current Index melebihi jumlah gambar.

### Handling

- Reset Current Index ke foto pertama.
- Simpan kembali Workspace.

---

# 11. Exit Errors

## Gagal Menyimpan Workspace Saat Keluar

### Handling

- Tampilkan dialog konfirmasi.
- Beri pilihan:
  - Coba Lagi
  - Keluar Tanpa Menyimpan
  - Batal

---

# 12. Logging

Seluruh error penting dicatat pada:

```text
storage/logs/
```

Informasi minimal yang dicatat:

- Timestamp
- Error Level
- Component
- Message
- Stack Trace (jika tersedia)

Contoh:

```text
[2026-07-20 14:21:15]
ERROR
FileOperationService
Failed to copy image:
IMG_1234.CR3
Permission denied
```

---

# 13. User Messages

| Condition              | Message                                           |
| ---------------------- | ------------------------------------------------- |
| Folder kosong          | No supported images found in the selected folder. |
| Folder tidak ditemukan | Source folder could not be found.                 |
| Workspace rusak        | Workspace could not be loaded.                    |
| Copy gagal             | Failed to copy the selected image.                |
| Undo gagal             | Failed to remove the selected image.              |
| Cache gagal            | Cache is unavailable. Performance may be reduced. |
| Gambar rusak           | Unable to load this image.                        |

---

# 14. Recovery Strategy

| Error                   | Continue Application |
| ----------------------- | :------------------: |
| Unsupported Format      |          ✔           |
| Corrupted Image         |          ✔           |
| Cache Failure           |          ✔           |
| Copy Failure            |          ✔           |
| Undo Failure            |          ✔           |
| Missing Workspace       |          ✔           |
| Corrupted Workspace     |          ✔           |
| Disk Full               |          ✔           |
| Permission Denied       |          ✔           |
| Critical Internal Error |          ✖           |

---

# 15. Critical Failure

Aplikasi hanya boleh berhenti apabila terjadi kondisi berikut:

- Kerusakan internal yang tidak dapat dipulihkan.
- Kegagalan inisialisasi framework GUI.
- Error fatal yang menyebabkan state aplikasi tidak lagi konsisten.

Sebelum keluar, aplikasi harus:

1. Mencoba menyimpan Workspace.
2. Menutup resource yang masih aktif.
3. Menulis log terakhir jika memungkinkan.
4. Keluar secara aman.

---

# 16. Summary

Photo Picker dirancang untuk mengutamakan keamanan data pengguna. Setiap error harus ditangani secara konsisten, tidak merusak file asli, dan sedapat mungkin memungkinkan pengguna melanjutkan pekerjaan tanpa kehilangan progres. Seluruh error penting dicatat ke log untuk memudahkan proses debugging dan pemeliharaan aplikasi.
