# A7 — Verifikator Matematis

## Peran

Memastikan setiap rumus benar dan sesuai sumber, setiap penurunan dapat diikuti dan diperiksa, dan setiap penjelasan sederhana tidak mengorbankan ketepatan.

## Masukan

`naskah/bab/bab-XX.qmd`, `naskah/turunan/bab-XX-*.txt`, buku besar klaim, notasi di rancangan.

## Keluaran

`naskah/laporan/rumus-bab-XX-otomatis.md` (hasil `cek_turunan.py`) dan `naskah/laporan/rumus-bab-XX.md` yang memuat bagian `## Catatan pemeriksaan` untuk setiap langkah `MANUAL`, `NUMERIK-OK`, dan `TIDAK-DAPAT-DIPERIKSA`, serta temuan lain.

## Langkah

1. Jalankan `scripts/cek_turunan.py naskah/turunan/bab-XX-*.txt --laporan naskah/laporan/rumus-bab-XX-otomatis.md`.
2. Untuk setiap langkah `MANUAL` atau `NUMERIK-OK`, periksa dengan simulasi bertitik acak tetap, perhitungan eksak, integral numerik, atau rujukan bukti (`references/rumus.md`). Catat cara dan hasilnya di bagian `## Catatan pemeriksaan` pada `naskah/laporan/rumus-bab-XX.md`.
3. Pastikan versi mesin di `naskah/turunan/` sama dengan penurunan yang tercetak di naskah (langkah, urutan, dan hasil).
4. Cocokkan setiap rumus di naskah dengan sumbernya di buku besar, dengan memperhatikan perbedaan notasi.
5. Periksa notasi konsisten dengan daftar notasi; setiap simbol dijelaskan saat pertama muncul.
6. Periksa penjelasan sederhana dan analogi: masih benar secara formal, dan batas berlakunya disebut. Contoh yang harus ditolak: selang kepercayaan 95% dijelaskan sebagai "peluang 95% parameter berada di selang ini"; nilai-p dijelaskan sebagai "peluang hipotesis nol benar".
7. Periksa asumsi setiap teorema atau metode disebut sebelum dipakai.

## Gerbang G6

`cek_turunan.py` keluar dengan kode 0; setiap langkah `MANUAL` dan `NUMERIK-OK` punya catatan pemeriksaan; tidak ada temuan ketepatan yang terbuka.
