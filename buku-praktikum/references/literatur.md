# Studi Literatur yang Dapat Diverifikasi

Buku ajar diwarisi banyak angkatan pembaca, jadi satu klaim yang keliru akan diulang bertahun-tahun. Karena itu, setiap pernyataan faktual di naskah harus bisa ditelusuri pembaca ke sumber yang bereputasi, dan Claude sendiri harus sudah membaca sumber itu.

## Sumber yang diterima

Urutan di bawah ini juga urutan prioritas.

1. **Buku teks dan monograf** dari penerbit akademik atau penerbit yang dikenal di bidangnya, misalnya Springer, Wiley, CRC Press/Chapman & Hall, Cambridge University Press, Oxford University Press, Pearson, Cengage, SIAM, O'Reilly (untuk pemrograman), serta penerbit universitas. Utamakan edisi terbaru.
2. **Artikel jurnal bertelaah sejawat** yang bereputasi, misalnya Journal of the American Statistical Association, Journal of the Royal Statistical Society, Biometrika, Annals of Statistics, Journal of Statistical Software, Statistics in Medicine, Journal of Computational and Graphical Statistics, dan jurnal nasional terakreditasi Sinta yang relevan. Untuk metode, kutip artikel yang pertama kali memperkenalkannya bila memungkinkan, ditambah rujukan buku yang lebih mudah dibaca.
3. **Dokumentasi resmi perangkat lunak**: manual R dan CRAN, dokumentasi paket (vignette, laman referensi), dokumentasi Python/NumPy/SciPy/statsmodels/pandas, dokumentasi Julia dan paketnya. Dokumentasi menjadi sumber untuk perilaku fungsi, argumen, dan bawaan (*default*), bukan untuk teori statistik.
4. **Publikasi lembaga resmi**: BPS, badan statistik negara lain, PBB, Bank Dunia, IMF, WHO, untuk data, definisi operasional, dan metodologi resmi.
5. **Prosiding konferensi bereputasi dan pracetak** (arXiv) hanya bila tidak ada padanan yang sudah ditelaah, dan diberi catatan bahwa sumbernya belum atau tidak ditelaah sejawat.

**Tidak diterima sebagai sumber**: blog pribadi, forum tanya jawab, Wikipedia (boleh dipakai untuk menemukan sumber primer, bukan dikutip), salindia kuliah tanpa penerbit, situs agregator, dan teks buatan AI.

## Cara memverifikasi

1. **Identitas sumber.** Cocokkan penulis, tahun, judul, edisi, penerbit/jurnal, volume, halaman, dan DOI/ISBN pada halaman penerbit, halaman DOI (`https://doi.org/...`), atau katalog perpustakaan. Jangan menyusun entri pustaka dari ingatan.
2. **Isi klaim.** Buka teks sumbernya (PDF, halaman web, atau pratinjau buku) dan temukan bagian yang mendukung klaim. Catat lokasinya: bab, subbab, halaman, nomor persamaan, atau nomor teorema.
3. **Rumus.** Salin bentuk rumus persis seperti di sumber, beserta definisi simbolnya. Bila buku ini memakai notasi lain, catat padanannya.
4. **Klaim yang tidak bisa dibuka.** Jika teks sumber tidak dapat diakses, status klaim tetap `BELUM`. Minta pengguna mengunggah sumbernya, cari sumber lain yang dapat diakses, atau jangan pakai klaim itu.
5. **Klaim pengetahuan umum bidang** (mis. "rata-rata sampel adalah penduga tak bias bagi rata-rata populasi") tetap diberi minimal satu rujukan buku teks agar pembaca bisa membaca lebih lanjut, dan bila perlu diturunkan di naskah.
6. **Angka dan data** (statistik resmi, hasil penelitian) dicatat bersama tahun data dan tanggal akses.

Bila tersedia, gunakan alat pencarian web dan pengambil halaman untuk langkah 1–3. Tulis temuan dengan kata-kata sendiri; kutipan langsung dipakai seperlunya dan pendek.

## Buku besar klaim (`naskah/01-literatur.md`)

Gunakan templat `assets/templat-literatur.md`. Bentuknya dua bagian.

**Daftar pustaka** (APA 7 atau gaya lain sesuai brief), dengan kunci sitasi:

```
[casella2002] Casella, G., & Berger, R. L. (2002). Statistical inference (2nd ed.). Duxbury.
```

**Tabel klaim**:

| ID | Klaim (parafrase) | Sumber | Lokasi | Dipakai di | Status |
|---|---|---|---|---|---|
| K-03-01 | Rata-rata sampel merupakan penduga tak bias bagi rata-rata populasi | casella2002 | Bab 5, Teorema 5.2.6 | Bab 3, 3.2 | TERVERIFIKASI |
| K-03-02 | ... | ... | ... | ... | BELUM |

Aturan tabel:

- Satu baris untuk satu klaim. ID berformat `K-<bab>-<urutan>`.
- `TERVERIFIKASI` hanya diberikan setelah lokasi klaim ditemukan di teks sumber yang benar-benar dibuka.
- Contoh lokasi di atas hanya ilustrasi format; lokasi nyata selalu diambil dari sumber yang dibuka.
- Klaim yang ternyata bertentangan dengan sumber diberi status `DIBANTAH` dan dicatat koreksinya.
- Di naskah, setiap sitasi menunjuk kunci pustaka (Quarto: `[@casella2002, hlm. 212]`), dan setiap kunci yang dipakai harus ada di daftar pustaka.

## Gerbang T1

- Setiap bab dalam rancangan punya minimal satu sumber utama berstatus terverifikasi.
- Setiap metode statistik utama punya rujukan teori (buku/artikel) dan, bila diimplementasikan dengan kode, rujukan dokumentasi fungsi yang dipakai.
- Tidak ada entri pustaka yang identitasnya belum dicek.
