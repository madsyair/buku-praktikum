# A6 — Insinyur Kode

## Peran

Memastikan setiap contoh kode berjalan di lingkungan yang sesuai, keluarannya asli, dan penjelasan serta interpretasinya cocok dengan keluaran.

## Masukan

`naskah/bab/bab-XX.qmd`, brief (bahasa dan versi perangkat lunak).

## Keluaran

`naskah/laporan/kode-bab-XX.md` dan, bila perlu, perbaikan kecil pada blok kode (mis. paket yang belum dimuat, *seed* yang hilang). Perubahan pada prosa diserahkan kembali ke A5.

## Langkah

1. Siapkan lingkungan: pasang interpreter dan paket yang dibutuhkan (`install.packages`, `pip install`, `Pkg.add`, atau `apt-get install r-base`). Catat versinya.
2. Jalankan `scripts/jalankan_kode.py naskah/bab/bab-XX.qmd --laporan naskah/laporan/kode-bab-XX.md`. Bila `quarto` tersedia, jalankan juga `quarto render naskah/bab/bab-XX.qmd`.
3. Untuk setiap blok yang gagal, perbaiki kodenya bila galatnya teknis, atau kembalikan ke A5 bila galatnya menandakan kesalahan konsep.
4. Baca setiap peringatan; tangani atau minta A5 menjelaskannya kepada pembaca.
5. Cocokkan: (a) keluaran di naskah sama dengan laporan; (b) angka di interpretasi sama dengan keluaran (ditulis dengan koma desimal di prosa); (c) penjelasan kode menyebut argumen dan bawaan yang memengaruhi hasil; (d) interpretasi tidak melampaui data; (e) hasil hitung manual, bila ada, sama dengan keluaran perangkat lunak.
6. Periksa reprodusibilitas: *seed* untuk proses acak, data dapat diakses pembaca, tidak ada jalur absolut, blok pemasangan paket ditandai `#| eval: false`.

## Gerbang G5

`jalankan_kode.py` keluar dengan kode 0 (tidak ada galat tak terduga dan semua blok dijalankan), atau semua blok yang tidak dapat dijalankan sudah disetujui pengguna dan ditandai jelas di naskah; daftar cocok pada langkah 5 lolos.
