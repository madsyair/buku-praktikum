# Rumus dan Simbol: Penulisan, Pemenggalan, Keterangan, dan Konsistensi

Berkas ini mengatur rumus dan simbol dalam naskah matematika, statistika, dan komputasi berbahasa Indonesia, baik buku ajar, modul praktikum, maupun artikel. Aturannya disarikan dari sumber berikut:
- Knuth, Larrabee, dan Roberts (1989), *Mathematical Writing*;
- Knuth (1984), *The TeXbook*, hlm. 195;
- ISO 80000-2:2019 tentang tanda dan lambang matematika;
- Halmos (1970), "How to write mathematics";
- pedoman gaya EE364B Stanford (Boyd, Ryu, dan Parikh, 2014);
- petunjuk naskah APS/REVTeX;
- Downes (1997), "Breaking equations", *TUGboat* 18(3);
- EYD V untuk tanda baca dan huruf.

Label pada setiap aturan:
- **[Wajib]**: kesalahan bila dilanggar.
- **[Konvensi]**: pilihan baku skill. Ganti hanya bila gaya selingkung berbeda, lalu terapkan konsisten.

Pemeriksa otomatis `scripts/cek_rumus.py` (dijalankan gerbang G6 oleh `cek_gerbang.py`) menegakkan sebagian besar aturan di bawah. Kode aturannya (R1–R12) dicantumkan di setiap bagian.

---

## 1. Rumus adalah bagian kalimat

1. **[Wajib]** Rumus sebaris (*inline*) dan rumus tampilan (*display*) adalah unsur kalimat. Rumus diberi tanda baca sesuai posisinya: koma bila kalimat berlanjut, titik bila kalimat selesai, dan tanpa tanda baca bila rumus diikuti langsung oleh kata yang melanjutkan kalimat. Uji Knuth: ganti setiap rumus dengan "anu", lalu kalimatnya harus tetap gramatikal.
2. **[Wajib]** Teks lanjutan sesudah rumus tampilan yang kalimatnya belum selesai **tidak diindentasi** dan berhuruf kecil (*dengan n menyatakan ...*). Indentasi dan huruf kapital hanya dipakai bila paragraf baru dimulai; dalam hal itu rumus ditutup titik. Di LaTeX dan Markdown/Quarto, jangan sisipkan baris kosong sebelum atau sesudah rumus bila paragraf berlanjut. (R7d)
3. **[Wajib]** Kalimat sebelum rumus tampilan tidak diakhiri titik dua bila rumus melanjutkan kalimat: *Rata-rata sampel didefinisikan sebagai* ↵ rumus, bukan *didefinisikan sebagai:* ↵ rumus. Titik dua hanya dipakai sesudah pernyataan lengkap (EYD V III.D.1–2).
4. **[Wajib]** Kalimat tidak dimulai dengan lambang. Tulis *Parameter $\beta$ diestimasi ...*, bukan *$\beta$ diestimasi ...*. Ini juga berlaku untuk nomor rujukan rumus di awal kalimat: tulis *Persamaan (2) menunjukkan ...*. (R1)
5. **[Wajib]** Dua rumus berurutan dipisah kata, bukan hanya koma: *untuk $S_q$ dengan $q < p$*, bukan *untuk $S_q$, $q < p$*. Daftar simbol sejenis boleh dipisah koma: *$a$, $b$, dan $c$*. (R2)
6. **[Wajib]** Lambang logika (∀, ∃, ⇒, ∴, ∵) tidak dipakai sebagai pengganti kata di prosa. Tulis *untuk setiap*, *ada*, *maka*, *jadi*. (R3)
7. **[Konvensi]** Penghubung keterangan sesudah rumus adalah *dengan*, bukan *di mana* (EYD; skill eyd). Contohnya *dengan $n$ menyatakan ukuran sampel*. Dalam bahasa Inggris dipakai *where*. (R4)
8. **[Konvensi]** Rumus sebaris dipakai untuk lambang dan relasi pendek. Rumus yang dirujuk, berupa definisi penting, memuat pecahan bertingkat, atau memuat ∑/∏/∫ berbatas ditulis sebagai rumus tampilan. Rumus sebaris yang lebih panjang dari kira-kira separuh baris dipindahkan ke tampilan, karena TeX akan memenggalnya di sembarang operator. (R8)
9. **[Konvensi]** Rumus tampilan diberi nomor hanya bila dirujuk. Kata *persamaan* ditulis huruf kecil di tengah kalimat (*pada persamaan (3.2)*) dan kapital hanya di awal kalimat.

## 2. Tipografi lambang (ISO 80000-2)

| Unsur | Huruf | Contoh | LaTeX |
|---|---|---|---|
| Peubah, parameter, indeks berjalan, fungsi umum | miring | $x$, $\beta$, $x_i$, $f(x)$ | `x`, `\beta`, `x_i` |
| Konstanta matematis tetap | tegak (bila fonta menyediakan) | e, i, π | `\mathrm{e}`, `\mathrm{i}` |
| Operator dan fungsi bermakna tetap | tegak | ln, exp, sin, Var, Cov, E, d pada d*x* | `\ln`, `\exp`, `\operatorname{Var}`, `\mathrm{d}x` |
| Label subskrip/superskrip (bukan peubah) | tegak | $x_{\mathrm{maks}}$, $R^2_{\mathrm{adj}}$, $\theta^{\mathrm{MAP}}$ | `x_{\mathrm{maks}}` |
| Singkatan dan nama ukuran dalam rumus | tegak | SE, RMSE, MSE | `\mathrm{SE}` |
| Vektor dan matriks | tebal (miring untuk huruf Latin) | $\mathbf{x}$, $\boldsymbol{\beta}$, $\mathbf{X}$ | `\mathbf{x}`, `\boldsymbol{\beta}` |
| Satuan | tegak, berspasi dari angka | 5 kg, 25 °C | `5\ \mathrm{kg}` |
| Bilangan desimal | koma desimal di naskah Indonesia | 0,05 | `0{,}05` |

- **[Wajib]** Kata atau singkatan yang terdiri atas beberapa huruf tidak ditulis miring berderet. Bentuk `Var(X)` terbaca sebagai *V·a·r*; tulis `\operatorname{Var}(X)`. Demikian juga `x_{max}` → `x_{\mathrm{maks}}`. (R6)
- **[Wajib]** Satu operator memakai satu bentuk di seluruh naskah. Ekspektasi ditulis salah satu dari `\mathrm{E}`, `\operatorname{E}`, atau `\mathbb{E}`. Peluang ditulis `P`, `\Pr`, atau `\mathbb{P}`. Diferensial `\mathrm{d}x` tidak dicampur dengan `dx`. Logaritma natural `\ln` tidak dicampur dengan `\log` bila buku memutuskan *ln*. (R6)
- **[Wajib]** Lambang di prosa tetap ditulis dalam mode matematika, bukan huruf biasa atau karakter Unicode. Tulis `$n = 30$`, `$\sigma^2$`, `$x_i$`, bukan *n = 30*, *σ²*, atau *x_i*. Hanya dengan cara itu huruf, spasi, dan bentuk lambang sama dengan yang ada di rumus. (R9)

## 3. Pemenggalan rumus

### 3a. Rumus tampilan
1. **Hindari pemenggalan lebih dulu.** Urutan upaya: (a) sederhanakan atau ubah susunan; (b) definisikan lambang bantu untuk subekspresi panjang, misalnya *dengan $A = \dots$*; (c) pakai lebar blok yang tersedia; (d) baru penggal.
2. **[Konvensi]** Penggal **sebelum** relasi atau operator biner, sehingga operator mengawali baris lanjutan (Knuth, *TeXbook*: rumus tampilan selalu dipenggal sebelum operasi dan relasi; konvensi AMS dan APS). Urutan titik penggal: (1) sebelum relasi (=, <, ≤, ≈) dalam rantai kesamaan; (2) sebelum + atau − pada **tingkat terluar**; (3) sebelum × eksplisit. Bila memenggal di perkalian, tuliskan tanda × di awal baris lanjutan. (R7a)
3. **[Wajib]** Jangan memenggal di dalam kurung, pecahan, akar, argumen fungsi, atau batas ∑/∫ selama ada titik penggal di tingkat yang lebih luar. Pasangan `\left ... \right` tidak boleh terbelah antarbaris. Bila terpaksa, pakai `\bigl( ... \bigr)` berukuran tetap di setiap baris. (R7b)
4. **[Konvensi]** Penjajaran: rantai kesamaan dijajarkan pada tanda =, dengan `&=`. Baris lanjutan yang diawali + atau − diletakkan menjorok ke kanan dari tanda = di atasnya (`&\quad {}+ c`), bukan tepat di bawahnya. Tanda `{}` memastikan + diberi spasi operator biner, bukan spasi tanda positif (Downes, 1997). Pada `multline`, baris pertama rata kiri, baris terakhir rata kanan, dan baris tengah di tengah. (R7c)
5. **[Konvensi]** Satu rumus yang dipenggal hanya mendapat **satu nomor** (`split` atau `aligned` di dalam satu `equation`; Quarto: `$$\begin{aligned} ... \end{aligned}$$ {#eq-x}`). `align` memberi nomor pada setiap baris, jadi pakailah hanya untuk deretan persamaan yang berbeda.
6. **[Konvensi]** Tanda baca penutup diletakkan di ujung baris terakhir.
7. **[Konvensi]** Sebagian tradisi tipografi (Rusia, Ceko) **mengulang operator** di akhir baris dan di awal baris berikutnya. Word menyediakan pilihan *Break before*, *Break after*, dan *Duplicate*. Skill ini memakai *penggal sebelum, tanpa pengulangan*. Bila gaya selingkung meminta pengulangan, terapkan di seluruh naskah, jangan dicampur. (R7a)

Contoh:

```latex
\begin{equation}
\begin{split}
\ell(\beta_0, \beta_1)
  &= \sum_{i=1}^{n} \bigl[ y_i \ln \pi_i + (1 - y_i) \ln (1 - \pi_i) \bigr] \\
  &= \sum_{i=1}^{n} y_i (\beta_0 + \beta_1 x_i)
     \\ &\quad {}- \sum_{i=1}^{n} \ln \bigl\{ 1 + \exp(\beta_0 + \beta_1 x_i) \bigr\},
\end{split}
\end{equation}
```

### 3b. Rumus sebaris
- TeX memenggal rumus sebaris **sesudah** relasi atau operator di tingkat terluar (*TeXbook*). Pemenggalan ini sah, tetapi sulit dibaca, jadi rumus sebaris dijaga pendek (aturan 1.8).
- **[Wajib]** Rumus sebaris yang pendek dan utuh maknanya tidak boleh terpenggal, misalnya $n = 30$ atau $p < 0{,}05$. Bungkus dengan kurung kurawal (`${n = 30}$`) atau dorong ke baris berikutnya. Jangan memecah rumus sebaris menjadi dua `$...$` agar muat.
- Pemenggalan kata di sekitar rumus mengikuti EYD (skill eyd, `pemenggalan-kata.md`). Lambang, angka, dan satuan tidak dipisah dari kata pengikatnya: `ukuran~$n$`, `5~kg`.

## 4. Keterangan simbol

1. **[Wajib]** Setiap simbol **diterangkan pada kemunculan pertama**, sedekat mungkin: di kalimat yang sama, tepat sesudah rumus tampilan, atau paling jauh di paragraf yang sama. Bila sengaja ditunda, katakan, misalnya *... matriks $\mathbf{W}$ yang didefinisikan di Subbab 3.2*. (R5)
2. **[Wajib]** Keterangan memuat **arti**, dan bila relevan juga **jenis atau domain** (skalar, vektor $p \times 1$, bilangan bulat positif), **satuan** (ribu rupiah, tahun), dan **rentang indeks** (*$i = 1, \dots, n$*).
3. **Bentuk keterangan** sesudah rumus tampilan:
   - Satu atau dua simbol: dalam kalimat. *... dengan $n$ menyatakan ukuran sampel dan $x_i$ pengeluaran rumah tangga ke-$i$ (ribu rupiah).*
   - Tiga simbol atau lebih: perincian sesudah *dengan* atau *keterangan:*, satu simbol per baris, berurutan sesuai kemunculan dalam rumus. Untuk *Keterangan:*, pernyataan lengkap diikuti titik dua.
   - Kata kerjanya *menyatakan*, *adalah*, atau *merupakan*. Pakai satu pola secara konsisten dalam satu naskah.
4. **[Wajib]** Simbol tidak diterangkan dua kali dengan arti berbeda (lihat §5). Simbol yang sudah diterangkan **diingatkan** bila muncul lagi jauh dari definisinya (bab lain, atau beberapa halaman kemudian): *ukuran sampel $n$*, bukan $n$ saja.
5. **[Konvensi]** Buku dan modul memuat **daftar notasi** (tabel simbol–arti–subbab pertama) di awal atau akhir buku. Daftar ini disusun dari rancangan dan dicocokkan dengan naskah. (R11)
6. **[Wajib]** Simbol di gambar, tabel, dan keterangannya diterangkan di keterangan gambar/tabel atau di teks yang merujuknya. Label sumbu memakai simbol yang sama dengan naskah.
7. **[Konvensi]** Jangan memperkenalkan simbol yang hanya dipakai sekali (Halmos). Tulis saja dengan kata.

## 5. Konsistensi simbol

1. **[Wajib] Satu simbol, satu arti** dalam satu bab, dan sebaiknya dalam satu buku atau seri. Contoh bentrokan yang sering terjadi: $n$ sebagai ukuran sampel dan indeks; $\pi$ sebagai konstanta dan peluang; $e$ sebagai bilangan Euler dan galat; $d$ sebagai diferensial dan parameter; $\alpha$ sebagai taraf nyata dan intersep. Periksa bentrokan sebelum memilih notasi. (R10)
2. **[Wajib] Satu konsep, satu simbol.** Jangan menulis $s^2$ di satu subbab dan $\hat\sigma^2$ di subbab lain untuk besaran yang sama tanpa menyatakan kesamaannya.
3. **[Wajib] Konvensi tanda tetap**: topi ($\hat\theta$) hanya untuk estimator atau nilai estimasi; garis atas ($\bar x$) untuk rata-rata; bintang atau nol ($\theta^\ast$, $\theta_0$) untuk nilai sebenarnya, dengan satu konvensi saja; huruf kapital ($X$) untuk peubah acak dan huruf kecil ($x$) untuk nilai amatan; tebal untuk vektor/matriks. Konvensi ini ditetapkan di rancangan.
4. **[Wajib] Narasi, rumus, tabel, gambar, dan kode memakai nama yang sama.** Bila prosa menyebut *ukuran sampel $n$*, judul kolom tabel juga $n$, label sumbu juga $n$, dan kode memakai nama yang dipetakan sekali secara eksplisit, misalnya *objek `n_sampel` di kode menyimpan $n$*. Keluaran perangkat lunak yang memakai nama lain (`Estimate`, `Std. Error`) dijembatani di interpretasi: *kolom `Estimate` berisi $\hat\beta_j$*.
5. **[Wajib] Bentuk yang sama di sebaris dan tampilan**: `\operatorname{Var}` di keduanya, bukan `Var` di prosa dan `\operatorname{Var}` di rumus. (R6, R9)
6. **[Konvensi] Indeks tetap**: $i$ untuk unit/amatan, $j$ untuk peubah/kolom, $k$ untuk kelompok/iterasi, $t$ untuk waktu. Rentangnya disebut sekali, misalnya $m \times n$ dengan $i = 1, \dots, m$ dan $j = 1, \dots, n$.
7. **[Konvensi] Notasi sumber yang berbeda** disebut padanannya sekali: *Gelman dkk. (2013) menulis $\theta$ untuk ...; di buku ini ...*.
8. **[Konvensi] Parameterisasi distribusi** dinyatakan eksplisit. Contohnya normal dengan ragam ($\mathrm{N}(\mu;\ \sigma^2)$) atau simpangan baku, Gamma dengan laju atau skala, dan Beta dengan parameter bentuk. Pemisah parameter berupa titik koma bila ada koma desimal.

## 6. Daftar periksa rumus dan simbol
- [ ] Setiap rumus terbaca sebagai bagian kalimat; tanda baca sesudahnya benar; lanjutan sesudah rumus tampilan tidak diindentasi.
- [ ] Tidak ada kalimat diawali lambang, dua rumus yang hanya dipisah koma, ∀/∃/⇒ di prosa, atau *di mana*.
- [ ] Peubah miring; operator, fungsi baku, label subskrip, dan singkatan tegak; vektor/matriks tebal; satu bentuk per operator.
- [ ] Rumus panjang disederhanakan atau dipenggal sebelum relasi/operator di tingkat terluar, terjajar pada =, satu nomor per rumus, tanpa `\left`/`\right` terbelah.
- [ ] Setiap simbol diterangkan pada kemunculan pertama (arti, domain, satuan, rentang indeks); diingatkan bila muncul jauh; ada di daftar notasi.
- [ ] Satu simbol satu arti; satu konsep satu simbol; konvensi topi/garis/bintang tetap; narasi, tabel, gambar, dan kode memakai nama yang sama.

## 7. Pemeriksa otomatis

```bash
python3 scripts/cek_rumus.py bab/bab-03.qmd                     # satu bab
python3 scripts/cek_rumus.py bab/*.qmd --notasi notasi.md       # lintas bab + daftar notasi
python3 scripts/cek_rumus.py naskah.tex --bahasa en --json      # artikel berbahasa Inggris
```

| Kode | Memeriksa | Tingkat |
|---|---|---|
| R1 | kalimat diawali lambang | ERROR |
| R2 | dua rumus sebaris hanya dipisah koma/spasi | WARNING |
| R3 | ∀, ∃, ⇒, ∴ di rumus sebaris dalam prosa | WARNING |
| R4 | *di mana* sebagai penghubung keterangan | WARNING |
| R5 | simbol tanpa keterangan di sekitar kemunculan pertama | WARNING |
| R6 | huruf berderet tanpa `\operatorname`/`\mathrm` (Var, SE, *max*); label subskrip miring; bentuk operator campur (E/𝔼, d/d, log/ln, P/Pr) | WARNING |
| R7 | pemenggalan rumus tampilan: (a) sesudah operator atau konvensi campur, (b) di dalam kurung atau `\left`/`\right` terbelah, (c) + atau − di awal baris tanpa `{}`, (d) baris kosong di sekitar rumus | WARNING/ERROR |
| R8 | rumus sebaris terlalu panjang, atau memakai `\displaystyle`/`\dfrac` | WARNING |
| R9 | lambang ditulis di luar mode matematika (σ², *x_i*, *n = 30*) | WARNING |
| R10 | simbol yang sama diterangkan dengan arti berbeda | WARNING |
| R11 | simbol yang tidak ada di daftar notasi (bila `--notasi`) | WARNING |
| R12 | rumus tampilan sangat panjang tanpa pemenggalan (risiko melewati tepi) | WARNING |

Pemeriksa membaca pola, bukan makna. Temuan R5 dan R10 perlu dinilai manusia, karena definisi bisa saja tertulis dalam bentuk yang tidak dikenali. Simbol yang sengaja tidak diterangkan, seperti konstanta umum atau indeks, didaftarkan di `--abaikan`.
