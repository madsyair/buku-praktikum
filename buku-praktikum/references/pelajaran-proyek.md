# Pelajaran dari proyek buku ajar

Subset yang relevan untuk modul praktikum dari `references/pelajaran-proyek.md` skill buku-ajar (temuan peninjau independen pada seri statistika Bayesian, November 2026). Penulis (A5) membaca berkas ini sebelum menulis bab; A6, A7, A8, dan A11v memakainya sebagai daftar buru.

## 1. Narasi tidak cocok dengan keluaran atau gambar

*Gejala*: prosa menyebut kelompok "terlebar" atau "naik", padahal gambar atau tabel menunjukkan sebaliknya, atau skala yang dibaca berbeda (log vs asli).

*Pencegahan*: setiap ciri keluaran yang disebut di prosa (urutan, terbesar, arah) dihitung dari data yang sama lewat kode inline; bila menjadi dasar kalimat tetap, kunci dengan `stopifnot()`. A8 membuka hasil render, bukan hanya `.qmd`.

## 2. Ambang tipis

*Gejala*: kalimat bersyarat "turun cukup jauh" lolos dengan selisih 0,0002; "interval tidak memuat nol" dengan batas bawah 0,0007.

*Pencegahan*: ambang jauh dari nilai (beberapa galat baku), atau tiga cabang (jelas di atas, jelas di bawah, di sekitar ambang); hindari kata sifat penilai tanpa ukuran. A6 mencetak margin setiap kalimat bersyarat.

## 3. Klaim "sama" atau "tidak satu pun" tanpa penguncian

*Pencegahan*: uji persis (`== 0`, `all.equal(…, tolerance =)`) dan `stopifnot()` di chunk tersembunyi; kata "sama" hanya untuk kesamaan dalam toleransi yang disebut.

## 4. Label kategori dan arti peubah tidak sesuai dokumentasi

*Pencegahan*: label kategori, satuan, dan arti peubah diambil dari dokumentasi data atau paket, dicetak dari data (bukan diketik), dan dipakai sama persis di prosa, tabel, gambar, tugas, dan kunci.

## 5. Penjelasan mekanisme yang keliru walau angkanya benar

*Pencegahan*: setiap "karena" yang menjelaskan hasil numerik diuji A7 dengan simulasi pembanding kecil; syarat (data terpusat, ukuran sampel) disebut.

## 6. Notasi dan pembulatan tidak konsisten

*Pencegahan*: satu fungsi pemformat angka dengan digit yang sama untuk besaran yang sama; tanpa `paste()` angka mentah (desimal bertitik di prosa); notasi diperiksa lintas bab sebelum dipilih (grep simbol calon di semua bab, rumus, kode, tugas, dan kunci; `cek_rumus.py` R10).

## 7. Tugas yang tidak dapat dijawab pasti

*Pencegahan*: A4 menulis untuk setiap tugas hitungan: data, parameter, *seed*, kriteria, dan bentuk jawaban. Bila `kunci_jawaban` aktif, A11 menjawab semua tugas dan mencatat temuan soal (`kunci-jawaban.md`).

## 8. Pengulangan dan panjang

*Pencegahan*: definisi tidak diulang di kotak, prosa, dan rangkuman; kode pembantu disembunyikan dan dirujuk ke lampiran; pemangkasan hanya untuk kalimat mubazir, **bukan** penjelasan, contoh, atau langkah penurunan.

## 9. Nama teknik pengajaran bocor ke naskah

*Pencegahan*: G4 (`larangan`) pada semua bab dan kunci; brief menyebut gaya dengan deskripsi ("pertanyaan wajar pembaca"), bukan nama teknik.

## 10. Audit tanpa isolasi konteks melewatkan kesalahan

*Gejala*: setelah putaran "audit dan perbaikan" oleh agen penulis sendiri, pembaca independen masih menemukan banyak kesalahan isi; sebagian temuan pembaca juga keliru dan baru tampak setelah dihitung ulang.

*Pencegahan*: A2v, A8, A11v, dan A14 selalu subagen berkonteks bersih. Temuan diperbaiki oleh agen lain yang lebih dulu memeriksanya (hitung ulang, buka sumber) dan menulis "tidak diterapkan" beserta bukti bila temuan keliru (`agents/a0-orkestrator.md`).

## 11. Istilah atau simbol dipakai sebelum didefinisikan

*Pencegahan*: setiap istilah dan simbol didefinisikan sebelum dipakai atau dirujuk ke tempat definisinya yang benar; intisari kotak penurunan yang dipakai teks inti ditulis satu atau dua kalimat di teks inti; matriks tujuan → tugas di kerangka.

## 12. Konflik kepentingan penulis paket

*Pencegahan*: bila buku memakai paket yang dibuat atau dipelihara penulis buku, tulis satu kalimat pengungkapan di tempat paket pertama dipakai, dan pastikan jalur alternatif tetap lengkap.

## 13. Keputusan yang hilang antarsesi

*Gejala*: keputusan istilah, sapaan, atau notasi dibuat di tengah percakapan lalu dilanggar bab berikutnya.

*Pencegahan*: catat setiap keputusan di `naskah/KEPUTUSAN.md` (tanggal, keputusan, alasan); keputusan istilah yang menolak suatu bentuk juga ditambahkan ke `istilah_terlarang` di `gerbang.json` agar G4 menegakkannya; bab yang sudah lolos diaudit ulang (A0, loop keputusan).
