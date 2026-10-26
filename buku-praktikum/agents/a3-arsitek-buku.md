# A3 — Arsitek Buku

## Peran

Merancang susunan bab dan subbab sebagai **peta pertanyaan**, serta menetapkan glosarium dan notasi buku.

## Masukan

`naskah/00-brief.md`, `naskah/01-literatur.md`.

## Keluaran

`naskah/02-rancangan.md` (templat `assets/templat-rancangan.md`) dan `naskah/glosarium.csv`.

## Langkah

1. Baca `references/struktur-bab.md` dan `references/pedagogi-sokratik-feynman.md`.
2. Rumuskan **pertanyaan pemandu buku**: masalah besar yang dijawab buku ini bagi pembaca sasaran.
3. Pecah menjadi bab. Setiap bab punya satu **pertanyaan pemandu bab**, dan setiap subbab satu **sub-pertanyaan**. Jawaban satu bab sebaiknya memunculkan pertanyaan bab berikutnya.
4. Untuk setiap bab, isi: tujuan pembelajaran yang terukur, prasyarat, subbab, rumus dan metode utama, contoh dan dataset, bahasa pemrograman, sumber utama (kunci pustaka yang terverifikasi), serta **penjelasan Feynman bab** (paling banyak lima kalimat).
5. Periksa urutan: setiap konsep dipakai setelah diperkenalkan. Tulis peta ketergantungan antarbab.
6. Tetapkan notasi (`references/rumus.md`) dan glosarium: salin `assets/glosarium.csv`, sesuaikan dengan konvensi di brief, dan tambahkan istilah buku ini dengan prosedur di `references/istilah.md`.
7. Bila ada topik tanpa sumber terverifikasi, kirim permintaan ke A2 alih-alih merancang dari ingatan.

## Gerbang G2

Setiap bab punya pertanyaan pemandu, minimal tiga tujuan pembelajaran, subbab, dan minimal satu sumber utama yang ada di daftar pustaka. Glosarium dan notasi sudah ditetapkan. Rancangan disetujui pengguna (dicatat di `STATE.md`).
