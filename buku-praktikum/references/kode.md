# Contoh Kode: Berjalan, Dijelaskan, dan Ditafsirkan

Kode di buku ajar adalah janji kepada pembaca: bila diketik ulang di lingkungan yang sama, hasilnya sama. Janji itu hanya bisa ditepati bila setiap blok benar-benar dijalankan sebelum diserahkan.

## Pola tetap setiap contoh kode

Setiap contoh kode terdiri atas lima bagian, dalam urutan ini.

1. **Pengantar** (1–3 kalimat): apa yang akan dikerjakan, mengapa, dan kaitannya dengan teori yang baru dibahas.
2. **Blok kode** yang pendek dan terfokus. Satu blok mengerjakan satu langkah logis; blok yang lebih dari kira-kira 20 baris biasanya perlu dipecah.
3. **Penjelasan kode**: apa fungsi baris atau kelompok baris yang penting, argumen yang tidak jelas dari namanya, dan bawaan (*default*) yang memengaruhi hasil. Jangan menjelaskan baris yang sudah jelas dengan sendirinya. Untuk pembaca pemula, penjelasan boleh berupa daftar bernomor yang merujuk baris.
4. **Keluaran asli** hasil eksekusi. Di Quarto, keluaran dihasilkan otomatis saat *render*. Di format lain, salin keluaran dari laporan `jalankan_kode.py`. Keluaran yang terlalu panjang boleh dipotong dengan tanda pemotongan yang jelas, tetapi bagian yang dibahas tidak boleh dipotong.
5. **Interpretasi keluaran**: makna angka atau grafik dalam konteks masalah, bukan sekadar membaca ulang angka. Interpretasi yang baik menjawab "lalu apa artinya?": besaran efek beserta satuannya, arah, ketidakpastian (galat baku, selang kepercayaan), keputusan uji beserta asumsinya, dan batasan kesimpulan. Bila contoh manual sudah dihitung sebelumnya, cocokkan hasilnya di sini.

Contoh ringkas:

````markdown
Kita hitung rata-rata dan simpangan baku pengeluaran per kapita sepuluh rumah tangga contoh,
lalu membandingkannya dengan hasil hitung manual di Subbab 2.3.

```{r}
pengeluaran <- c(812, 945, 1020, 760, 1105, 890, 998, 1210, 875, 930)  # ribu rupiah
mean(pengeluaran)
sd(pengeluaran)
```

Fungsi `mean()` menghitung rata-rata aritmetika, sedangkan `sd()` menghitung simpangan baku
sampel dengan pembagi $n - 1$, sama dengan rumus (2.4).

[keluaran asli hasil eksekusi]

Rata-rata pengeluaran sekitar ... ribu rupiah per kapita per bulan, sama dengan hasil hitung
manual. Simpangan baku ... ribu rupiah menunjukkan bahwa ...
````

Angka di bagian interpretasi ditulis setelah kode dijalankan dan diambil dari keluaran asli, lalu ditulis dalam format angka Indonesia (koma desimal).

## Lingkungan dan reprodusibilitas

- **Catat versi.** Di awal buku atau modul, cantumkan versi R/Python/Julia dan paket utama yang dipakai saat menulis. `jalankan_kode.py` mencatat versi interpreter di laporannya; untuk paket, akhiri setiap bab atau lampiran dengan `sessionInfo()` (R), `import sys; print(sys.version)` beserta versi paket (Python), atau `versioninfo()` dan `Pkg.status()` (Julia).
- **Tetapkan *seed*** untuk setiap proses acak: `set.seed(2025)` (R), `rng = np.random.default_rng(2025)` (Python), `Random.seed!(2025)` (Julia). Jelaskan sekali bahwa *seed* membuat hasil dapat diulang, dan bahwa versi perangkat lunak yang berbeda bisa saja menghasilkan bilangan acak yang berbeda.
- **Data** dimuat dari sumber yang dapat diakses pembaca: dataset bawaan paket, berkas yang disertakan bersama buku, atau data yang dibangkitkan di kode. Sertakan sumber dan lisensi data nyata. Hindari jalur absolut (`C:/Users/...`); pakai jalur relatif terhadap direktori proyek.
- **Pemasangan paket** ditulis di subbab persiapan, terpisah dari kode analisis, dan blok pemasangan ditandai agar tidak dijalankan berulang (`#| eval: false` di Quarto).
- **Idiom bahasa**: R memakai gaya tidyverse atau R dasar secara konsisten dalam satu buku; Python memakai NumPy/pandas/statsmodels/SciPy dengan impor baku (`import numpy as np`, `import pandas as pd`); Julia memakai paket ekosistem utama (DataFrames.jl, Distributions.jl, GLM.jl). Pilihan ini dicatat di brief.
- **Nama objek** bermakna dan konsisten. Nama dalam bahasa Indonesia boleh dipakai bila membantu pembaca pemula (`pengeluaran`, `model_regresi`), tetapi jangan dicampur dengan bahasa Inggris dalam satu buku.
- **Komentar di kode** singkat dan dalam bahasa naskah. Penjelasan panjang ditaruh di prosa, bukan di komentar.

## Menjalankan dan memeriksa

1. Jalankan `scripts/jalankan_kode.py` untuk setiap bab:

   ```bash
   python <skill-dir>/scripts/jalankan_kode.py naskah/bab/bab-03.qmd --laporan naskah/laporan/kode-bab-03.md
   ```

   - Blok dijalankan berurutan dalam satu sesi per bahasa, sehingga objek dari blok sebelumnya tersedia di blok berikutnya, seperti di Quarto.
   - Blok yang tidak boleh dijalankan (mis. pemasangan paket atau contoh kode yang sengaja salah) diberi `#| eval: false` atau komentar `# tidak-dijalankan` pada baris pertamanya.
   - Blok yang sengaja menghasilkan galat untuk tujuan pengajaran diberi `#| error: true`; skrip mencatatnya sebagai galat yang diharapkan.
   - Kode keluar skrip 0 berarti semua blok yang dijalankan berhasil.
2. Bila interpreter tidak ada, coba pasang dulu. Bila tetap tidak bisa, laporan menandai blok itu sebagai `TIDAK DIJALANKAN`. Sampaikan hal ini kepada pengguna dan jangan menulis keluaran karangan; biarkan tempat keluaran kosong dengan catatan yang jelas.
3. Bandingkan keluaran di naskah dengan laporan. Angka di interpretasi harus cocok dengan keluaran.
4. Peringatan (*warning*) dari perangkat lunak dibaca dan ditangani: diperbaiki, atau dijelaskan kepada pembaca bila memang bagian dari pelajaran.
5. Bila `quarto` tersedia, `quarto render` atas bab atau seluruh buku adalah pemeriksaan akhir yang paling dekat dengan pengalaman pembaca.

## Kesalahan yang sering terjadi

- Keluaran di naskah berasal dari versi kode lama.
- Kode memakai objek yang baru dibuat di bab lain tanpa dibuat ulang atau dirujuk.
- Interpretasi hanya mengulang angka ("nilai-p sebesar 0,003") tanpa keputusan dan maknanya.
- Interpretasi melampaui data, misalnya menyimpulkan sebab-akibat dari regresi data observasi.
- Grafik tanpa judul sumbu, satuan, atau keterangan.
- Angka desimal di prosa masih memakai titik.
