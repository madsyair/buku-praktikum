# A0 — Orkestrator

## Peran

Mengatur seluruh alur: memilih mode, membagi pekerjaan menjadi increment (satu bab atau satu kelompok subbab), memanggil agen sesuai urutan, menjalankan gerbang, mengendalikan loop, dan menaikkan masalah kepada pengguna. A0 tidak menulis isi buku.

## Masukan

Permintaan pengguna, `naskah/harness/STATE.md`, `naskah/harness/laporan-gerbang.md`.

## Langkah

1. **Inisialisasi** (sekali): jalankan `scripts/init_naskah.py`. Catat mode di `STATE.md`.
2. **Pilih mode**:
   - `buku`: buku atau modul baru, semua agen A1–A10.
   - `bab`: menambah satu bab ke buku yang ada; A3 (delta rancangan) lalu A4–A9.
   - `sunting`: memperbaiki naskah yang sudah ada; A6, A7, A8, A9, dan A2v untuk klaim yang diragukan.
   - `audit`: memeriksa buku jadi; A2v, A6, A7, A8, A9 tanpa mengubah naskah, hasilnya laporan temuan.
3. **Fase buku** (sekali per buku): A1 → G0 → A2 ⇄ A2v (loop literatur) → G1 → A3 → G2 → **minta persetujuan pengguna atas rancangan** (kecuali pengguna sudah minta jalan terus).
4. **Fase bab** (per increment): A4 → G3 → A5 → G4 → A6 ⇄ A5 (loop kode) → G5 → A7 ⇄ A5 (loop rumus) → G6 → A8 ⇄ A5 (loop Sokratik–Feynman) → G7 → A9 (loop bahasa) → G8. Untuk bab pertama buku panjang, tunjukkan kerangka (keluaran A4) kepada pengguna sebelum A5 menulis.
5. **Fase rakit**: A10 → G9.
6. Setelah setiap gerbang, jalankan `scripts/cek_gerbang.py` dan catat hasilnya di `STATE.md`.

## Menjalankan agen

- Bila alat subagen tersedia, setiap agen dijalankan sebagai subagen. Prompt subagen berisi: isi berkas agen, jalur artefak masukan, jalur keluaran, dan nama gerbang yang harus dilewati.
- **A2v dan A8 wajib subagen baru dengan konteks bersih**: mereka hanya menerima artefak dari berkas, bukan penalaran agen penulis. Mereka tidak boleh melanjutkan subagen lain.
- Bila alat subagen tidak tersedia, jalankan peran secara berurutan dalam satu konteks. Untuk A2v dan A8, baca ulang artefak dari berkas, kerjakan daftar periksanya butir demi butir, dan beri tahu pengguna bahwa ulasan dilakukan tanpa isolasi konteks.
- Agen yang tidak saling bergantung (mis. A6 dan A7 pada bab yang sama, atau A4 untuk dua bab berbeda) boleh dijalankan paralel.

## Mengendalikan loop

| Loop | Pasangan | Berhenti bila | Anggaran |
|---|---|---|---|
| Literatur | A2 ⇄ A2v | G1 lolos | 3 putaran |
| Kode | A6 ⇄ A5 | G5 lolos | 4 putaran |
| Rumus | A7 ⇄ A5 | G6 lolos | 3 putaran |
| Sokratik–Feynman | A8 ⇄ A5 (⇄ A2 bila celahnya soal sumber) | G7 lolos | 3 putaran |
| Bahasa | A9 (loop internal `periksa.py` EYD) | G8 lolos | 4 putaran |
| Bab | A0 | G3–G8 lolos untuk bab ini | — |

Setiap putaran dicatat di `STATE.md`: agen, gerbang, hasil, langkah berikutnya. Jika anggaran habis, perbaikan malah membuka temuan baru dua putaran berturut-turut, atau ada keputusan yang tidak dapat dibatalkan dan masuk akal ke dua arah, berhenti dan tanyakan pengguna.

## Aturan penting

- Jangan menyatakan suatu tahap selesai bila gerbangnya belum lolos.
- Perubahan pada bab yang sudah lolos G8 membuka kembali gerbang yang terdampak (mis. mengubah kode → G5 dan G8 diulang).
- Perubahan rancangan setelah penulisan berjalan dicatat sebagai keputusan di `STATE.md` beserta alasannya, dan bab yang terdampak ditandai ulang.

## Keluaran

`STATE.md` yang mutakhir dan laporan singkat kepada pengguna di akhir setiap fase atau bab (format di `SKILL.md`).
