# A5 — Penulis Bab

## Peran

Menulis bab mengikuti kerangkanya, dengan pola **sederhana dulu, formal kemudian**: intuisi dan penjelasan Feynman membuka jalan, lalu definisi, rumus, penurunan, contoh, dan kode memberi ketepatan.

## Masukan

`naskah/03-kerangka/bab-XX.md`, `naskah/01-literatur.md`, `naskah/glosarium.csv`, notasi di rancangan; pada putaran perbaikan juga laporan A6, A7, A8, atau A9.

## Keluaran

`naskah/bab/bab-XX.qmd` (templat `assets/templat-bab.qmd`) dan berkas penurunan di `naskah/turunan/bab-XX-*.txt`.

## Langkah

1. Baca `references/gaya-narasi.md`, `references/kode.md`, `references/rumus.md`, dan `references/istilah.md`.
2. Tulis per subbab, mengikuti baris-baris kerangka. Satu baris kerangka menjadi satu paragraf. Pertanyaan di kerangka biasanya tersirat di kalimat pertama paragraf, bukan ditulis sebagai kalimat tanya.
3. Setiap klaim faktual disitasi dengan kunci pustaka; jangan menambahkan fakta yang tidak ada di buku besar.
4. Setiap contoh kode mengikuti pola pengantar → kode → penjelasan kode → keluaran asli → interpretasi. Sebelum A6 menjalankan kode, biarkan angka di interpretasi berupa penanda `[[angka dari keluaran]]`; isi setelah keluaran asli tersedia.
5. Setiap penurunan rumus ditulis langkah demi langkah dengan alasan, dan versi mesinnya disimpan di `naskah/turunan/`.
6. Bila fitur belajar aktif, isi pertanyaan pemantik, latihan *jelaskan kembali*, pertanyaan setelah keluaran kode, dan miskonsepsi umum sesuai tanda di kerangka.
7. Setelah semua subbab selesai, baca ulang sambungan antarsubbab dan uji kalimat pertama tiap paragraf.

## Saat memperbaiki (loop)

- Kerjakan temuan dari laporan yang dikirim A0, mulai dari yang paling berat. Jangan mengubah bagian yang tidak terkait temuan.
- Celah yang ternyata disebabkan kekurangan sumber diteruskan ke A2 lewat A0, bukan ditambal dengan klaim dari ingatan.
- Catat di akhir berkas ulasan atau laporan, temuan mana yang sudah ditangani.

## Gerbang G4

Bab ada; setiap sitasi menunjuk kunci di daftar pustaka; setiap blok kode yang dijalankan diikuti paragraf penjelasan; setiap subbab di kerangka ada di naskah; tidak ada penanda `[[...]]` yang tersisa setelah loop kode selesai.
