# Kebijakan Istilah untuk Buku Matematika, Statistika, dan Komputasi

Kebijakan ini berlaku untuk naskah berbahasa Indonesia. Ia selaras dengan `references/istilah-dan-kbbi.md` pada skill `eyd`, tetapi lebih tegas soal tiga hal: padanan KBBI dipakai secara **selektif**, serapan yang sesuai EYD **diutamakan** bila lebih populer, dan istilah bidang mengikuti **kelaziman bidangnya**.

## Prinsip

1. **EYD V selalu berlaku**: ejaan, huruf kapital, huruf miring, tanda baca, penulisan angka, dan kaidah penyerapan.
2. **Padanan KBBI dipakai bila sudah populer.** Contoh: *unduh, unggah, daring, tautan, pencilan, peluang, simpangan baku*.
3. **Serapan yang sesuai kaidah EYD diutamakan bila lebih populer daripada padanan asli KBBI.** Contoh: *variabel* lebih lazim daripada *peubah*, *estimasi* lebih lazim daripada *pendugaan* di banyak lembaga, *residual* lebih lazim daripada *sisaan*. Serapan ditulis tegak, tanpa padanan dalam kurung.
4. **Bila padanan KBBI tidak populer dan tidak ada serapan yang lazim, pakai istilah asingnya**: dicetak miring, dan pada **kemunculan pertama** disertai padanan KBBI dalam kurung. Selanjutnya, pakai istilah asing itu secara konsisten. Contoh: *bootstrap*; *array* (larik); *bug* (pepijat); *goodness of fit* (kebaikan suai).
5. **Bila istilah asing tidak punya padanan KBBI sama sekali**, jelaskan maknanya dalam petik tunggal atau dalam satu kalimat saat pertama muncul: *seed* 'bilangan awal yang menentukan urutan bilangan acak'.
6. **Istilah bidang mengikuti kelaziman bidang.** Kata yang sama bisa punya istilah berbeda di bidang lain. Pilih istilah yang dipakai dalam buku teks, jurnal, dan publikasi resmi bidang tersebut di Indonesia (lihat bagian *Istilah yang khas bidang*).
7. **Nama diri tidak diterjemahkan dan tidak dimiringkan**: nama perangkat lunak, paket, fungsi, merek, lembaga, dan metode yang sudah menjadi nama (R, Python, Julia, `lm()`, NumPy, BPS, uji Shapiro-Wilk, metode Newton-Raphson, simulasi Monte Carlo).
8. **Satu konsep, satu istilah** di seluruh buku. Konvensi lembaga atau pengguna (mis. lembaga yang memakai *penduga*) mengalahkan glosarium bawaan, asalkan dipakai konsisten.

## Prosedur memilih istilah

Untuk setiap istilah baru, jalankan urutan ini dan catat keputusannya di `naskah/glosarium.csv`.

1. Apakah istilah itu nama diri? Jika ya, pakai apa adanya.
2. Apakah glosarium buku atau konvensi lembaga sudah menetapkannya? Jika ya, ikuti.
3. Apakah bidang (matematika, statistika, atau komputasi) di Indonesia sudah punya istilah mapan? Periksa buku teks berbahasa Indonesia, jurnal nasional, dan publikasi resmi (mis. BPS untuk istilah statistik resmi). Jika ya, pakai istilah itu.
4. Bandingkan kepopuleran tiga calon di kalangan pembaca sasaran: padanan asli KBBI, serapan sesuai EYD, dan istilah asing. Petunjuknya: frekuensi pemakaian di buku teks, jurnal, dan publikasi resmi berbahasa Indonesia; bila perlu, cari contoh pemakaian dengan pencarian web. Pilih yang paling populer. Bila seimbang, pilih padanan atau serapan Indonesia.
5. Periksa ejaan padanan dan serapan di **KBBI Daring** dan **Glosarium Badan Bahasa** sebelum dipakai. Padanan di glosarium bawaan skill ini adalah titik awal, bukan putusan; tandai yang belum dicek.

## Kaidah penyerapan yang sering dipakai

Serapan mengikuti penyesuaian ejaan EYD V. Pola yang sering muncul di bidang ini:

| Pola asing | Serapan | Contoh |
|---|---|---|
| -ics, -ica | -ika | *statistics* → statistika, *mathematics* → matematika |
| -ty | -tas | *variability* → variabilitas, *probability* → probabilitas |
| -ance, -ence | -ans, -ensi | *variance* → varians, *frequency* → frekuensi |
| -tion | -si | *regression* → regresi, *correlation* → korelasi |
| -ive | -if | *descriptive* → deskriptif, *quantitative* → kuantitatif |
| -al (sifat) | -al | *normal, marginal, residual* (tetap) |
| -ysis, -esis | -isis, -esis | *analysis* → analisis (bukan analisa), *hypothesis* → hipotesis (bukan hipotesa) |
| c sebelum a/o/u/konsonan | k | *coefficient* → koefisien, *cluster* → klaster |
| ph, th | f, t | *graph* → graf, *theorem* → teorema |
| x | ks | *axiom* → aksioma, *complex* → kompleks |

Prefiks seperti *non-, multi-, pra-* ditulis serangkai: *nonparametrik, multivariat, prapemrosesan*. Bila diikuti huruf kapital atau angka, pakai tanda hubung: *non-Bayes, pra-2020*.

## Istilah yang khas bidang

- **statistika** (ilmu) dan **statistik** (nilai yang dihitung dari sampel, atau data hasil pengolahan) adalah dua konsep berbeda. "Statistik uji *t*" benar; "ilmu statistik" sebaiknya "statistika".
- **signifikan** (dalam arti uji statistik) jangan dicampur dengan *nyata* dalam satu buku. Pilih satu, lalu konsisten: "tingkat signifikansi 5%" atau "taraf nyata 5%".
- **galat** dalam statistika berarti suku *error* model; dalam komputasi, *pesan galat* berarti pesan *error* program. Bila keduanya muncul dalam satu bab, sebutkan konteksnya.
- **model efek campuran** (*mixed model*) berbeda dengan **model *mixture*** (*mixture model*, model campuran hingga). Jangan menyingkat keduanya menjadi "model campuran" dalam buku yang membahas keduanya.
- **sampel** dalam statistika; kata *contoh* dipakai untuk arti 'ilustrasi'. Hindari *contoh* untuk arti *sample* agar tidak rancu dengan contoh soal.
- **distribusi** dan **sebaran**: pilih satu untuk *distribution*. Glosarium bawaan memakai *distribusi*.
- **peluang** dan **probabilitas** sama-sama lazim. Glosarium bawaan memakai *peluang* untuk konsep dan "P(A)" dibaca "peluang A".
- **fungsi** dalam matematika dan **fungsi** dalam pemrograman memakai kata yang sama. Bila perlu dibedakan, tulis "fungsi R `mean()`" atau "fungsi matematis *f*".
- Nama distribusi dan metode bernama ditulis dengan huruf kapital sesuai nama orangnya: distribusi Poisson, uji Kolmogorov-Smirnov, metode Newton-Raphson. Kata umumnya ditulis kecil: distribusi normal, distribusi binomial.

## Format penulisan

| Jenis | Kemunculan pertama | Selanjutnya |
|---|---|---|
| Padanan populer | padanan saja; boleh disertai istilah asing miring dalam kurung bila pembaca lebih mengenalnya dari literatur asing | padanan |
| Serapan | serapan saja, tegak | serapan |
| Istilah asing | *istilah asing* (padanan KBBI) | *istilah asing* |
| Istilah asing tanpa padanan | *istilah asing* 'makna' atau dijelaskan dalam kalimat | *istilah asing* |
| Singkatan | kepanjangan (SINGKATAN) | SINGKATAN |
| Nama diri | apa adanya | apa adanya |

Ketentuan tambahan:

- Istilah asing selalu miring di prosa. Di dalam blok kode, nama fungsi, dan rumus, tidak dimiringkan secara manual.
- Hindari bentuk campuran tidak baku (*diinstall* → dipasang, *ngerun* → dijalankan, *di-plot-kan* → digambarkan dalam grafik).
- Bila istilah asing terpaksa diberi imbuhan, pakai tanda hubung dan miringkan bagian asingnya: di-*bootstrap*. Lebih baik ubah kalimatnya: "sampel *bootstrap* dibangkitkan ...".
- Angka desimal di prosa memakai koma (0,05; 1,96) dan pemisah ribuan titik (10.000). Di dalam kode dan keluaran, angka tetap seperti yang dicetak perangkat lunak. Saat mengutip angka keluaran di prosa, ubah ke format Indonesia.

## Glosarium bawaan

Glosarium bawaan ada di `assets/glosarium.csv`. Kolomnya dipisah titik koma (jadi isi kolom tidak boleh memuat titik koma):

- `konsep`: istilah Inggris sebagai kunci konsep;
- `utama`: bentuk yang dipakai di naskah;
- `jenis`: `indonesia`, `serapan`, `asing`, atau `nama`;
- `kurung_pertama`: teks yang wajib ada dalam kurung pada kemunculan pertama (untuk jenis `asing`: padanan KBBI; untuk jenis lain: istilah asing bila ingin disertakan; kosong bila tidak perlu);
- `alternatif`: bentuk lain untuk konsep yang sama yang tidak boleh muncul agar istilah konsisten, dipisah tanda `|`;
- `catatan`.

Glosarium ini disusun untuk pembaca akademik Indonesia secara umum dan perlu disesuaikan dengan konvensi lembaga dan pembaca. Salin ke `naskah/glosarium.csv` di T2, ubah sesuai keputusan, lalu pakai sebagai acuan tunggal. Lampirkan versi akhirnya sebagai glosarium di akhir buku.
