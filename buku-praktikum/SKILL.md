---
name: buku-praktikum
description: Alur multi-agen untuk menulis buku ajar, modul praktikum, diktat, atau bahan ajar matematika, statistika, sains data, dan komputasi yang memadukan teori, rumus beserta penurunannya, metode dan pemodelan statistik, serta kode R/Python/Julia yang benar-benar dijalankan, dijelaskan, dan diinterpretasikan. Memakai sinergi metode Sokratik dan teknik Feynman, studi literatur terverifikasi, gerbang mutu yang dapat dieksekusi, dan loop perbaikan; naskah Indonesia mengikuti EYD V. Gunakan setiap kali pengguna minta "buat buku", "modul praktikum", "buku ajar", "diktat", "bahan ajar", "handout", "lab manual", "tutorial statistik", atau menulis/menyunting/mengaudit satu bab buku teknis, meskipun tidak menyebut skill ini.
---

# Menulis Buku dan Modul Praktikum (multi-agen, terverifikasi)

Skill ini mengatur penulisan buku atau modul yang menggabungkan teori, rumus, metode, pemodelan statistik, dan penerapannya lewat kode, sebagai **rangkaian agen yang saling terhubung**. Setiap tahap dikerjakan satu agen dengan kontrak masukan dan keluaran yang jelas. Gerbang mutu yang dapat dieksekusi memisahkan tahap-tahap itu, dan loop umpan balik memperbaiki artefak sampai gerbangnya lolos atau masalahnya dinaikkan kepada pengguna.

Tiga janji yang dijaga:

1. **Benar.** Setiap pernyataan faktual dapat dilacak ke literatur bereputasi yang benar-benar dibuka; setiap penurunan rumus dapat diperiksa langkah demi langkah; setiap kode benar-benar berjalan dan keluarannya asli.
2. **Dipahami.** Rantai pertanyaan Sokratik menyusun alur, dan uji Feynman memastikan setiap subbab bisa dijelaskan ulang secara sederhana oleh pembaca sasaran.
3. **Terbaca seperti tulisan manusia.** Kalimat efektif dan hemat, paragraf koheren, narasi mengalir, sesuai EYD V, dengan kebijakan istilah yang selektif.

## Sinergi Sokratik–Feynman

Rinciannya di `references/pedagogi-sokratik-feynman.md`. Intinya, pertanyaan Sokratik **menghasilkan** tuntutan penjelasan, sedangkan teknik Feynman **menguji** apakah penjelasan itu dipahami. Siklus ini diterapkan pada tiga lapis:

- **Penulis**: konsep inti harus bisa dijelaskan dalam lima kalimat sederhana sebelum bab dirancang (A2, A3); bila tidak bisa, literaturnya belum cukup.
- **Naskah**: bab disusun sebagai peta pertanyaan (A3), dan setiap paragraf menjawab satu pertanyaan yang lahir dari paragraf sebelumnya (A4). Inilah mesin utama narasi yang mengalir.
- **Pembaca**: pertanyaan pemantik, pertanyaan untuk direnungkan setelah keluaran kode, latihan *jelaskan kembali*, dan miskonsepsi umum (A5); naskah diuji oleh pembaca simulasi berkonteks bersih (A8).

**Label internal.** "Sokratik" dan "Feynman" adalah nama kerja skill. Nama itu tidak pernah ditulis di naskah buku (judul, subjudul, kotak, latihan); tekniknya bekerja tanpa label. Gerbang G4 menolaknya (`larangan` di `gerbang.json`).

## Agen dan kontraknya

Setiap agen punya berkas instruksi di `agents/`. Baca berkas agen sebelum menjalankan tahapnya. Semua artefak tinggal di folder `naskah/` di akar proyek.

| Agen | Berkas | Keluaran | Gerbang |
|---|---|---|---|
| A0 Orkestrator | `agents/a0-orkestrator.md` | `naskah/harness/STATE.md`, rute, eskalasi | — |
| A1 Perencana | `agents/a1-perencana.md` | `00-brief.md` | G0 |
| A2 Peneliti Literatur | `agents/a2-peneliti-literatur.md` | `01-literatur.md` (pustaka, klaim, penjelasan konsep inti) | G1 |
| A2v Verifikator Klaim | `agents/a2v-verifikator-klaim.md` | status klaim di `01-literatur.md` | G1 |
| A3 Arsitek Buku | `agents/a3-arsitek-buku.md` | `02-rancangan.md` (peta pertanyaan), `glosarium.csv`, notasi | G2 |
| A4 Perancang Kerangka | `agents/a4-perancang-kerangka.md` | `03-kerangka/bab-XX.md` (rantai pertanyaan per paragraf) | G3 |
| A5 Penulis | `agents/a5-penulis.md` | `bab/bab-XX.qmd`, `turunan/bab-XX-*.txt` | G4 |
| A6 Insinyur Kode | `agents/a6-insinyur-kode.md` | `laporan/kode-bab-XX.md` | G5 |
| A7 Verifikator Matematis | `agents/a7-verifikator-matematis.md` | `laporan/rumus-bab-XX.md` | G6 |
| A8 Pembaca Sokratik–Feynman | `agents/a8-pembaca-sokratik-feynman.md` | `ulasan/bab-XX.md` | G7 |
| A9 Penyunting Bahasa | `agents/a9-penyunting-bahasa.md` | bab tersunting, `laporan/bahasa-bab-XX.md` | G8 |
| A10 Perakit | `agents/a10-perakit.md` | proyek buku dan hasil render | G9 |
| A11 Pembuat Kunci *(bila `kunci_jawaban`)* | `agents/a11-pembuat-kunci.md` | `kunci/bab-XX.qmd`, `kunci/temuan-soal.md` | GK |
| A11v Pemeriksa Kunci | `agents/a11v-pemeriksa-kunci.md` | `ulasan/kunci-bab-XX.md` | GK |
| A12 Penyunting Gaya Buku Ajar *(bila `tahap_gaya`)* | `agents/a12-penyunting-gaya.md` | `gaya/bab-XX.qmd`, `ulasan/gaya-bab-XX.md` | GG |
| A13 Penerap Revisi Gaya | `agents/a13-penerap-revisi-gaya.md` | bab hasil penerapan, `## Tindak lanjut` | GG |
| A14 Editor Penerbitan *(bila `terbit`)* | `agents/a14-editor-penerbitan.md` | `ulasan/editor-penerbitan.md` | G9 |

**Pemisahan peran disengaja.** A2v, A8, A11v, A12, dan A14 bekerja dengan **konteks bersih**: mereka hanya membaca artefak dari berkas, tidak melihat penalaran agen yang membuatnya, supaya pekerjaan tidak menilai dirinya sendiri. Bila alat subagen (Agent/Task) tersedia, jalankan setiap agen sebagai subagen, dan agen berkonteks bersih selalu sebagai subagen baru. A13 harus agen yang berbeda dari A12, dan A11v berbeda dari A11. Bila tidak tersedia, jalankan peran secara berurutan dalam satu konteks, baca ulang artefak dari berkas untuk A2v dan A8, lalu sebutkan kepada pengguna bahwa ulasan dilakukan tanpa isolasi konteks.

**Model per peran.** Setiap peran punya model bawaan: opus untuk perencanaan, penulisan, verifikasi, dan kunci; sonnet untuk pembaca dan penyuntingan berpola; haiku untuk tugas mekanis; fable boleh menggantikan opus pada A7, A2v, dan A11v. Tabel dan aturan naik/turun satu tingkat ada di `agents/a0-orkestrator.md` (Pilih model per peran), dasarnya di `references/kajian-model.md`. Agar modelnya otomatis, `init_naskah.py --pasang-agen` menyalin `claude-agents/buku-praktikum-aN-*.md` ke `<proyek>/.claude/agents/` sebagai jenis agen Claude Code (bawaan: tidak dipasang); tiap berkas hanya merujuk ke `agents/aN-*.md`.

## Mode

Pilih mode di awal agar biaya proses sepadan dengan pekerjaannya, lalu catat di `STATE.md`.

| Mode | Kapan | Agen |
|---|---|---|
| `buku` | Buku atau modul baru | A1–A10; A12–A13 bila `tahap_gaya` (dianjurkan); A11 bila `kunci_jawaban`; A14 bila `terbit` |
| `bab` | Menambah satu bab ke buku yang ada | A3 (delta), A4–A9 |
| `sunting` | Memperbaiki naskah yang sudah ada | A6, A7, A8, A9, dan A2v untuk klaim yang diragukan |
| `audit` | Memeriksa buku jadi tanpa mengubahnya | A2v, A6, A7, A8, A9; hasilnya laporan temuan |

Untuk permintaan sangat kecil (satu paragraf, satu contoh kode), tidak perlu harness penuh: tulis sesuai berkas rujukan, jalankan kodenya, periksa rumusnya, dan jalankan pemeriksa EYD serta istilah.

## Alur

```
Fase buku : A1 ─G0→ A2 ⇄ A2v ─G1→ A3 ─G2→ [persetujuan pengguna]
Fase bab  : A4 ─G3→ A5 ─G4→ A6 ⇄ A5 ─G5→ A7 ⇄ A5 ─G6→ A8 ⇄ A5 (⇄ A2) ─G7→ A9 ─G8→
            [A12 → A13 ─GG→]  [A11 ⇄ A11v ─GK→]  bab berikutnya
Fase rakit: A10 → [A14] ─G9→ buku
```

Untuk buku panjang, tunjukkan kerangka bab pertama kepada pengguna sebelum A5 menulis, agar gaya dan kedalaman disepakati lebih awal.

Tahap dalam kurung siku bersifat pilihan dan diaktifkan di `gerbang.json`:

- `"tahap_gaya": true`: setelah G8, A12 menulis ulang bab ke gaya buku ajar (sapaan *kita*, semi-formal, istilah dijelaskan, sitasi seperlunya ke *Bacaan lanjut*) dan A13 memeriksa lalu menerapkannya (`references/gaya-buku-ajar.md`).
- `"kunci_jawaban": true`: A11 menulis kunci berubrik untuk setiap tugas praktikum dan A11v memeriksanya secara mandiri (`references/kunci-jawaban.md`).
- `"terbit": true`: A14 menelaah buku utuh sebelum G9 (`agents/a14-editor-penerbitan.md`).

**Keputusan penulis** (istilah, sapaan, notasi) dicatat di `naskah/KEPUTUSAN.md`. Keputusan yang dapat diperiksa mesin ditambahkan ke `gerbang.json` (mis. `istilah_terlarang`) disertai satu uji, lalu A0 mengaudit ulang bab yang sudah lolos.

## Harness: state, gerbang, dan loop

**Inisialisasi** (sekali per proyek, lalu sekali per bab):

```bash
python <skill-dir>/scripts/init_naskah.py --root <proyek> --judul "<judul>"
python <skill-dir>/scripts/init_naskah.py --root <proyek> --bab-baru 1
python <skill-dir>/scripts/init_naskah.py --root <proyek> --pasang-agen   # opsional: peran sebagai agen Claude Code
```

Skrip membuat `naskah/` beserta templat artefak, `harness/STATE.md`, `harness/gerbang.json` (mencari lokasi pemeriksa EYD secara otomatis), glosarium bawaan, dan `_quarto.yml`. Berkas yang sudah ada tidak ditimpa tanpa `--force`.

**Gerbang** dijalankan dengan:

```bash
python <skill-dir>/scripts/cek_gerbang.py --root <proyek> [--gerbang G3 G4] [--bab 1] [--lewati-perintah]
```

Skrip memeriksa artefak dan menjalankan pemeriksa kode, rumus, EYD, dan istilah, lalu menulis `naskah/harness/laporan-gerbang.md`. Kode keluar 0 berarti tidak ada gerbang yang gagal. Status LEWATI (artefak belum ada) tidak sama dengan LOLOS. Jangan menyatakan suatu tahap selesai bila gerbangnya belum lolos.

| Gerbang | Lolos bila |
|---|---|
| G0 Brief | Butir wajib terisi, termasuk pembaca sasaran, perangkat lunak, format, dan fitur belajar |
| G1 Literatur | Ada pustaka dan klaim; tidak ada klaim `DIUSULKAN` tersisa; setiap bab punya sumber utama di pustaka |
| G2 Rancangan | Setiap bab punya pertanyaan pemandu, penjelasan Feynman, minimal tiga tujuan, subbab, dan sumber; notasi dan glosarium ditetapkan; persetujuan pengguna dicatat |
| G3 Kerangka | Setiap paragraf punya pertanyaan, fungsi, gagasan pokok, dan transisi; setiap subbab punya penjelasan Feynman; ID klaim yang dirujuk terverifikasi |
| G4 Draf | Sitasi ada di pustaka; istilah yang sudah diputuskan (`istilah_terlarang`) tidak muncul; setiap blok kode diikuti penjelasan; subbab kerangka ada di naskah; tidak ada penanda `[[...]]`; fitur belajar ada bila diaktifkan; tanpa nama teknik pengajaran; subjudul bukan kalimat tanya; *persamaan* huruf kecil di tengah kalimat; **struktur bab** (pengantar berupa studi kasus/cerita ≥ `pengantar_min_kata`, subbab ≤ `subbab_maks_kata`, `## Rangkuman`); bila diaktifkan di `gerbang.json`: angka hasil hitung dari kode inline (`angka_inline`), lebar baris kode (`lebar_kode_maks`) |
| G5 Kode | `jalankan_kode.py` keluar 0 |
| G6 Rumus | `cek_rumus.py` tanpa ERROR (penulisan rumus dan simbol; WARNING untuk A7); `cek_turunan.py` keluar 0; langkah manual dan numerik punya catatan pemeriksaan |
| G7 Ulasan | Putusan terakhir A8 `LOLOS`; tidak ada temuan mayor terbuka |
| G8 Bahasa | Pemeriksa EYD 0 ERROR; `cek_istilah.py` keluar 0; laporan bahasa ada |
| GG Gaya buku ajar *(bila `tahap_gaya`)* | Telaah A12 ada dan berisi `## Tindak lanjut` dari A13; sapaan *kita* ≥ 3 per 1.000 kata, tanpa *Anda*; rata-rata kalimat ≤ 20 kata; sitasi ≤ 4 per 1.000 kata prosa isi |
| GK Kunci jawaban *(bila `kunci_jawaban`)* | Setiap butir `## Tugas praktikum` punya `### Tugas N` di kunci; setiap kunci memuat `> **Jawaban akhir:**`; rubrik berjumlah 10; tidak ada temuan soal terbuka untuk bab ini |
| G9 Perakitan | Semua bab lolos G3–G8 (dan GG, GK bila aktif); berkas proyek lengkap; bila `terbit`, A14 memutuskan *siap terbit* |

**Loop** yang dikendalikan A0 (rincian dan anggaran di `agents/a0-orkestrator.md`):

- **Literatur** (A2 ⇄ A2v, maks. 3 putaran): usul klaim → verifikasi independen → perbaiki atau cari sumber lain.
- **Kode** (A6 ⇄ A5, maks. 4): jalankan → perbaiki → jalankan ulang; angka di interpretasi diisi dari keluaran asli.
- **Rumus** (A7 ⇄ A5, maks. 3): periksa simbolik/numerik → perbaiki langkah → periksa ulang.
- **Sokratik–Feynman** (A8 ⇄ A5, maks. 3): uji penjelasan ulang dan pertanyaan Sokratik → tutup celah → ulas ulang; celah yang berupa kekurangan sumber diteruskan ke A2.
- **Bahasa** (A9, maks. 4): loop `periksa.py` EYD sampai 0 ERROR, lalu pemeriksa istilah dan `humanizer-id`.
- **Gaya** (A12 → A13, maks. 4 putaran penerapan): telaah dan tulis ulang → periksa dan terapkan → G4–G8 dan GG.
- **Kunci** (A11 ⇄ A11v, maks. 3): tulis kunci → hitung ulang mandiri → perbaiki; temuan soal kembali ke A5.
- **Penerbitan** (A14 → A13/A9 → A10, maks. 2): telaah buku utuh → perbaikan mekanis → render ulang.
- **Keputusan** (A0): keputusan baru → `KEPUTUSAN.md` + `gerbang.json` + uji → audit ulang semua bab yang sudah lolos.
- **Bab** (A0): setelah G3–G8 (dan GG, GK bila aktif) lolos untuk satu bab, lanjut ke bab berikutnya.

Setiap putaran dicatat di `STATE.md`. Jika anggaran putaran habis, perbaikan terus membuka temuan baru, atau ada keputusan yang tidak dapat dibatalkan dan masuk akal ke dua arah, berhenti dan tanyakan pengguna. Perubahan pada bab yang sudah lolos membuka kembali gerbang yang terdampak.

## Berkas rujukan

| Berkas | Isi | Dibaca oleh |
|---|---|---|
| `references/pedagogi-sokratik-feynman.md` | Kajian sinergi, penerapan tiga lapis, risiko dan pengaman, sumber | A3, A4, A5, A8 |
| `references/literatur.md` | Kriteria sumber bereputasi, cara verifikasi, format buku besar klaim | A2, A2v |
| `references/struktur-bab.md` | Anatomi bab teori dan modul praktikum, rancangan bab, kerangka paragraf | A3, A4 |
| `references/gaya-narasi.md` | Narasi mengalir, koherensi, gaya bercerita, register akademik yang mudah dipahami | A4, A5, A9 |
| `references/istilah.md` | Kebijakan istilah (padanan KBBI selektif, serapan, istilah asing) dan istilah khas bidang | A3, A5, A9 |
| `references/kode.md` | Pola contoh kode, lingkungan dan reprodusibilitas, interpretasi keluaran | A5, A6 |
| `references/rumus.md` | Penurunan langkah demi langkah, format berkas turunan, verifikasi | A5, A7 |
| `references/rumus-dan-simbol.md` | Rumus sebagai bagian kalimat, tipografi ISO 80000-2, pemenggalan rumus, keterangan dan konsistensi simbol (R1–R12) | A3, A5, A7, A9 |
| `references/gaya-buku-ajar.md` | Tahap gaya akhir: sapaan *kita*, semi-formal, istilah, rujukan seperlunya, ukuran GG | A12, A13, A14 |
| `references/kunci-jawaban.md` | Kunci berubrik, temuan soal, pemeriksaan independen, GK | A11, A11v |
| `references/pelajaran-proyek.md` | Kesalahan berulang dari proyek buku ajar dan pencegahannya | A4, A5, A6, A7, A8, A11v |
| `references/kajian-model.md` | Uji banding model per peran dan cara memperbarui tabel model | A0, pemelihara skill |
| `references/kajian-adaptasi-buku-ajar.md` | Kajian bagian skill buku-ajar yang diadaptasi ke skill ini (diterapkan dan diusulkan) | A0, pemelihara skill |

Templat ada di `assets/` (brief, literatur, rancangan, kerangka bab, bab Quarto, ulasan, ulasan gaya, kunci bab, temuan soal, KEPUTUSAN, STATE, `_quarto.yml`, `glosarium.csv`).

## Skrip

| Skrip | Fungsi |
|---|---|
| `scripts/init_naskah.py` | Menyiapkan folder kerja dan berkas per bab; `--pasang-agen` memasang peran sebagai agen Claude Code |
| `scripts/cek_gerbang.py` | Menjalankan gerbang G0–G9, GG, dan GK |
| `scripts/jalankan_kode.py` | Menjalankan blok R/Python/Julia berurutan per sesi, mencatat versi, galat, dan peringatan |
| `scripts/cek_rumus.py` | Memeriksa penulisan rumus dan simbol: kalimat diawali lambang, simbol tanpa keterangan, arti ganda, pemenggalan rumus, operator miring (dipanggil G6) |
| `scripts/cek_turunan.py` | Memeriksa setiap langkah penurunan dengan SymPy: simbolik, titik acak, dan titik pembantah |
| `scripts/cek_agen.py` | Memeriksa `claude-agents/` (atau `--folder <proyek>/.claude/agents`): frontmatter sah, model ∈ {opus, sonnet, haiku, fable}, setiap peran punya tepat satu pasangan |
| `scripts/cek_istilah.py` | Memeriksa konsistensi istilah, padanan pada kemunculan pertama, dan huruf miring istilah asing |

Bila interpreter atau paket belum terpasang, pasang dulu (`pip install sympy`, `apt-get install r-base`, `install.packages`). Bila tetap tidak bisa, katakan terus terang kepada pengguna bagian mana yang belum dijalankan; jangan menulis keluaran atau hasil pemeriksaan karangan.

## Skill lain yang dipakai bersama

- **`eyd`**: wajib untuk naskah berbahasa Indonesia; A9 menjalankan loop `periksa.py`-nya. Kebijakan istilah di skill ini melengkapi `istilah-dan-kbbi.md` milik `eyd`.
- **`humanizer-id`**: dipakai A9 untuk membuang pola tulisan mesin tanpa mengubah fakta.
- Skill riset (mis. `deep-research` atau plugin riset akademik) boleh dipakai A2 untuk pencarian yang sangat luas, asalkan hasilnya tetap masuk buku besar klaim dan diverifikasi A2v.

Bila `eyd` atau `humanizer-id` tidak tersedia, terapkan ringkasan aturannya di `references/gaya-narasi.md` dan `references/istilah.md`, set `"eyd_periksa": "tidak-tersedia"` di `gerbang.json`, dan sampaikan kepada pengguna bahwa pemeriksaan otomatis EYD tidak dijalankan.

## Melapor kepada pengguna

Di akhir setiap fase atau bab, laporkan singkat: apa yang selesai, tabel status gerbang (dari `laporan-gerbang.md`), blok kode yang berjalan/gagal/belum dijalankan, penurunan yang lolos atau masih manual, klaim tanpa sumber terverifikasi, temuan Sokratik–Feynman yang masih terbuka, keputusan yang menunggu persetujuan, dan langkah berikutnya. Jangan menyembunyikan bagian yang belum terverifikasi.
