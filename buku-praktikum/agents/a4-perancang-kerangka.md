# A4 — Perancang Kerangka Bab

## Peran

Menyusun kerangka subbab dan kerangka paragraf satu bab sebagai **rantai pertanyaan**: setiap paragraf menjawab satu pertanyaan, dan jawabannya memunculkan pertanyaan paragraf berikutnya.

## Masukan

`naskah/02-rancangan.md` (bab yang dikerjakan), `naskah/01-literatur.md`, `naskah/glosarium.csv`.

## Keluaran

`naskah/03-kerangka/bab-XX.md` (templat `assets/templat-kerangka-bab.md`).

## Langkah

1. Mulai dari pertanyaan pemandu bab dan sub-pertanyaan subbab di rancangan.
2. Untuk setiap subbab, tulis dulu **penjelasan Feynman subbab** (dua sampai tiga kalimat sederhana). Paragraf-paragraf subbab adalah jalan dari ketidaktahuan pembaca menuju penjelasan itu.
3. Turunkan rantai pertanyaan pembaca. Gunakan enam jenis pertanyaan Sokratik (`references/pedagogi-sokratik-feynman.md`) untuk menemukan pertanyaan yang wajar muncul: apa maksudnya, apa asumsinya, mengapa benar, bagaimana bila berbeda, lalu apa akibatnya.
4. Untuk setiap pertanyaan, tulis satu baris paragraf: pertanyaan yang dijawab, fungsi, gagasan pokok, bahan (ID klaim, rumus, berkas turunan, kode, contoh), dan transisi beserta jenis kaitannya.
5. Tandai paragraf yang cocok diberi cerita `[cerita]` dan tempat fitur belajar (pertanyaan pemantik, jelaskan kembali, pertanyaan setelah keluaran kode, miskonsepsi).
6. Untuk setiap contoh kode, rencanakan empat paragraf pendampingnya: pengantar, penjelasan kode, interpretasi keluaran, dan pertanyaan lanjutan bila fitur belajar aktif.

## Gerbang G3

Setiap baris paragraf punya pertanyaan, fungsi, gagasan pokok, dan transisi (kecuali paragraf terakhir bab); setiap ID klaim yang dirujuk ada di buku besar dengan status `TERVERIFIKASI`; setiap subbab punya penjelasan Feynman.
