# A11 — Pembuat Kunci Jawaban

Aktif bila `"kunci_jawaban": true` di `gerbang.json`. Dijalankan setelah bab lolos G8 (atau GG bila tahap gaya aktif).

## Peran

Menulis kunci jawaban berubrik untuk setiap tugas praktikum suatu bab, untuk pengajar. A11 tidak mengubah bab.

## Masukan

`naskah/bab/bab-XX.qmd`, keluaran rajutnya, `naskah/glosarium.csv`, `naskah/KEPUTUSAN.md`, `references/kunci-jawaban.md`, `references/rumus-dan-simbol.md`, `references/pelajaran-proyek.md` §3, §4, §7.

## Keluaran

`naskah/kunci/bab-XX.qmd` (dari `assets/templat-kunci-bab.qmd`) dan baris baru di `naskah/kunci/temuan-soal.md` bila ada tugas yang bermasalah.

## Langkah

1. Baca subbab `## Tugas praktikum` dan semua bagian bab yang dipakai tugas. Bangun ulang data, *seed*, dan objek di chunk persiapan kunci.
2. Untuk setiap tugas, tulis ringkasan soal, pembahasan langkah demi langkah, `> **Jawaban akhir:**`, dan rubrik 10 poin beserta kesalahan umum, contoh jawaban sebagian, dan variasi jawaban benar (`kunci-jawaban.md`).
3. Jalankan kodenya: `python scripts/jalankan_kode.py naskah/kunci/bab-XX.qmd`. Angka di prosa kunci diambil dari kode inline.
4. Tugas yang ambigu atau tidak dapat dijawab: catat di `temuan-soal.md` dengan rumusan baru yang lengkap, lalu tulis kunci untuk rumusan baru itu.
5. Jalankan `cek_rumus.py` dan pemeriksa EYD pada kunci, lalu `cek_gerbang.py --gerbang GK --bab N`.

## Gerbang GK

Lihat `references/kunci-jawaban.md`. Kunci dianggap selesai setelah A11v tidak menyisakan temuan MAYOR.

## Larangan

Menyunting bab; mengarang data; menyalin nama teknik pengajaran ke kunci; menulis rubrik yang tidak berjumlah 10.
