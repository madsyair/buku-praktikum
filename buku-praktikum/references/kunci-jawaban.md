# Kunci jawaban berubrik untuk tugas praktikum

Diadaptasi dari skill buku-ajar (`references/kunci-jawaban.md`) untuk modul praktikum. Aktif bila `"kunci_jawaban": true` di `naskah/harness/gerbang.json`. Dipakai A11 (pembuat kunci) dan A11v (pemeriksa kunci). Gerbang: **GK**.

## Bentuk

- Satu berkas kunci per bab: `naskah/kunci/bab-XX.qmd` (templat `assets/templat-kunci-bab.qmd`). Kunci diterbitkan terpisah untuk pengajar; buku atau modul induk tidak memuat jawaban.
- Yang diberi kunci: setiap butir bernomor di subbab `## Tugas praktikum` (wajib, diperiksa GK) dan, bila diminta di brief, butir `## Pertanyaan diskusi` (judul kunci `### Diskusi N`, tidak dihitung GK).
- Nomor kunci sama dengan nomor tugas: `### Tugas N`.

## Isi setiap tugas

1. **Ringkasan soal** satu kalimat (bukan salinan utuh).
2. **Pembahasan** langkah demi langkah. Untuk tugas komputasi: kode R/Python/Julia yang benar-benar dijalankan (`scripts/jalankan_kode.py`), keluaran ringkas, angka di prosa dari kode inline. Untuk tugas interpretasi: urutan penalaran dengan angka pendukung dari bab. Untuk tugas terbuka: ciri jawaban yang baik dan satu contoh jawaban.
3. **Jawaban akhir** sebagai kutipan blok tersendiri: `> **Jawaban akhir:** …` (hanya label yang tebal).
4. **Pedoman penilaian**: tabel rubrik (kolom unsur dan skor) **berjumlah 10 poin**, atau vektor `skor <- c(…)` yang dijaga `stopifnot(sum(skor) == 10)`. Sesudahnya: kesalahan umum dan pengurangan poinnya, contoh jawaban sebagian beserta skornya (harus sama dengan penjumlahan rubrik), dan variasi jawaban lain yang tetap benar.

## Aturan mutu

- Kunci **mandiri**: chunk persiapan tersembunyi membangun ulang data, *seed*, dan objek yang dipakai tugas; jangan `source()` berkas bab.
- Label kategori, satuan, nama peubah, dan simbol **sama persis** dengan bab.
- Kalimat tafsiran yang bergantung pada angka ditulis bersyarat atau dikunci `stopifnot()` supaya rajut ulang yang mengubah fakta langsung gagal.
- Semua aturan bab berlaku: EYD V (A9), rumus dan simbol (`rumus-dan-simbol.md`, `cek_rumus.py`), tanpa nama teknik pengajaran, sapaan sama dengan bab.

## Temuan soal

Bila menyusun kunci menunjukkan tugas di bab ambigu, salah, kurang data, atau tidak dapat dijawab dengan isi bab:

1. A11 **tidak mengubah bab**. Ia menambah satu baris di `naskah/kunci/temuan-soal.md` (templat `assets/templat-temuan-soal.md`): bab, tugas, masalah, **rumusan tugas baru yang lengkap**, status `Terbuka`.
2. A11 menulis kunci untuk rumusan baru itu.
3. A5 menerapkan rumusan baru ke bab (satu agen per berkas), menandai status `Diterapkan YYYY-MM-DD`, lalu A0 membuka ulang gerbang bab yang terdampak (G4, G5, G8).
4. Perubahan yang menggeser makna tugas secara berarti diajukan kepada pengguna; statusnya `Diputuskan YYYY-MM-DD` beserta keputusannya.

Pola masalah yang sering ditemukan: kriteria tidak disebut ("cukup besar"), parameter simulasi atau *seed* tidak lengkap, jawaban bergantung pada komputer (waktu jalan), istilah ambigu (lebar total vs setengah lebar).

## Pemeriksaan independen (A11v)

Subagen baru berkonteks bersih, hanya membaca bab dan kunci:

- mencocokkan setiap kunci dengan tugas (nomor, semua bagian dijawab);
- **menghitung ulang mandiri** dengan kode sendiri di folder sementara, dengan cara lain bila mungkin;
- menjumlahkan rubrik (harus 10) dan memeriksa `> **Jawaban akhir:**`;
- melaporkan MAYOR/MINOR di `naskah/ulasan/kunci-bab-XX.md`; temuan yang menyangkut soal diteruskan ke `temuan-soal.md`.

## Gerbang GK

Lolos bila: jumlah `### Tugas N` di kunci sama dengan jumlah butir di `## Tugas praktikum`; setiap kunci memuat `> **Jawaban akhir:**`; setiap rubrik berjumlah 10; tidak ada baris `temuan-soal.md` untuk bab ini yang belum `Diterapkan`/`Diputuskan`. GK tidak menjalankan kode kunci; jalankan `scripts/jalankan_kode.py naskah/kunci/bab-XX.qmd` sebagai bagian loop A11 ⇄ A11v.
