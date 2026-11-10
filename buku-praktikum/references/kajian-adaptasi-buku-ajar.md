# Kajian Adaptasi dari Skill buku-ajar

Skill `buku-ajar` lahir dari skill ini, lalu dimatangkan saat dipakai menulis seri buku statistika Bayesian (tiga buku induk, tiga buku kunci, ±1.200 klaim terverifikasi). Kajian ini, yang disusun pada 10 November 2026, memeriksa bagian buku-ajar yang layak dibawa kembali ke `buku-praktikum`. Batasnya: skill ini tetap **ringan** untuk modul praktikum dan buku tunggal, sehingga yang diambil adalah aturan yang murah ditegakkan dan sering dilanggar, bukan seluruh perangkat seri buku.

Status:
- **Diterapkan**: sudah masuk skill ini (berkas, gerbang, dan uji disebut).
- **Diusulkan**: perlu keputusan pemilik skill karena menambah peran, tahap, atau ketergantungan.
- **Tidak diadaptasi**: hanya bermanfaat untuk seri buku atau tata letak cetak berat.

## 1. Diterapkan

| Aspek | Di buku-ajar | Kekurangan buku-praktikum sebelumnya | Adaptasi | Tempat |
|---|---|---|---|---|
| Rumus dan simbol | `rumus-dan-simbol.md`, `cek_rumus.py`, G-RUMUS | Simbol wajib dijelaskan, tetapi tidak diperiksa. Pemenggalan rumus, kalimat diawali lambang, dan konsistensi simbol tidak diatur. Templat menyisipkan baris kosong sesudah rumus sehingga lanjutan *dengan …* terindentasi | Rujukan yang sama; G6 menjalankan `cek_rumus.py` (ERROR menggagalkan, WARNING untuk A7); templat dibetulkan | `references/rumus-dan-simbol.md`, `scripts/cek_rumus.py`, `cek_gerbang.py` G6, `assets/templat-bab.qmd` |
| Nama teknik pengajaran | Label internal; dilarang di naskah (G-LARANGAN) | Templat mencetak subjudul **"Pertanyaan Sokratik"** di bab | Subjudul menjadi *Pertanyaan untuk direnungkan*; G4 menolak "Sokratik", "Socrates", dan "Feynman" di bab (pola dapat diubah lewat `larangan`) | `SKILL.md`, templat, `pedagogi-sokratik-feynman.md`, G4 |
| Struktur bab | Pengantar studi kasus/cerita, subbab ringkas, Rangkuman (G-STRUKTUR) | Ada pembuka dan rangkuman di anatomi, tetapi tidak diperiksa | G4 memeriksa pengantar ≥ `pengantar_min_kata` (bawaan 80) yang tidak dibuka "Bab ini …", setiap bagian ≤ `subbab_maks_kata` (800), dan `## Rangkuman` | `struktur-bab.md`, templat, G4, `init_naskah.py` |
| Angka dari kode | G-ANGKA: angka hasil hitung di prosa wajib dari R inline | Angka interpretasi disalin manual dari keluaran (penanda `[[...]]`), sehingga bisa berbeda dari keluaran setelah kode diubah | Di Quarto, angka ditulis dengan kode inline; G4 menolak desimal/persen/ribuan yang diketik bila `angka_inline` aktif (aktif untuk proyek baru; proyek lama tidak berubah). Pengecualian lewat `angka_tetap` | `kode.md`, `a5-penulis.md`, G4 |
| Subjudul | Frasa, bukan kalimat tanya (G-JUDUL) | Tidak diatur | G4 menolak subjudul bertanda tanya | G4 |
| "persamaan" huruf kecil | G-PERSAMAAN | Tidak diatur | G4 menolak *Persamaan* berkapital di tengah kalimat | G4 |
| Lebar kode | 72 (R) / 79 (Python) untuk B5 | Tidak diatur, sehingga kode bisa terpotong di PDF | `lebar_kode_maks` (bawaan proyek baru 80) | G4, `init_naskah.py` |
| Status data | Riil → sintetis paket → simulasi, status disebut, batasan di prakata | Hanya "sertakan sumber dan lisensi" | Status data disebut saat data diperkenalkan; batasan di prakata | `kode.md` |
| Perbaikan temuan pembaca | Perbaikan dikerjakan agen lain yang memeriksa temuan dulu; "tidak diterapkan" wajib berbukti | A5 mencentang temuan A8 tanpa kewajiban memeriksa | A5 memeriksa setiap temuan isi dan menulis *diperbaiki* (lokasi) atau *tidak diterapkan* (bukti); A8 memverifikasi | `a0-orkestrator.md` |
| Uji pemeriksa | Fikstur gagal/lulus per gerbang | Ada `tests/test_skrip.py` | Uji baru untuk `cek_rumus.py` dan aturan G4 hasil adaptasi; bab contoh di fikstur dilengkapi pengantar dan rangkuman | `tests/test_skrip.py`, `tests/fixtures/` |

## 2. Diusulkan (perlu keputusan)

| No. | Aspek di buku-ajar | Manfaat untuk praktikum | Biaya | Rekomendasi |
|---|---|---|---|---|
| U1 | **Kunci jawaban berubrik** (peran 13–14, `kunci-jawaban.md`): pembahasan, jawaban akhir, rubrik 10 poin, temuan soal dikembalikan ke soal induk | Tugas praktikum lebih mudah dinilai asisten; soal yang ambigu ketahuan sebelum dipakai di kelas | Satu agen (A11) dan satu gerbang | **Setuju**. Praktikum hampir selalu dinilai, dan menurunkan rubrik dari tugas murah bila dikerjakan per bab |
| U2 | **Tahap gaya buku ajar** (peran 22–23, `gaya-buku-ajar.md`): tulis ulang komunikatif dengan *Anda/kita*, semi-formal, istilah dijelaskan, sitasi seperlunya ke *Bacaan lanjut* | Modul yang padat sitasi selama penulisan menjadi enak dibaca | Dua peran dan gerbang G-GAYA-AJAR | Setuju untuk mode `buku`; tidak perlu untuk modul satu pertemuan |
| U3 | **Registri klaim berkutipan verbatim** (G-REFERENSI, `referensi.py`) | Klaim dapat dicocokkan ulang otomatis ke teks sumber | Format buku besar berubah dari tabel parafrase ke JSON; perlu salinan teks sumber | Tunda. Buku besar klaim + A2v cukup untuk buku tunggal |
| U4 | **Editor penerbitan** (peran 24) dan **penelaah pakar buku ajar** (21, Permendikbudristek 22/2022) | Kelayakan dan kesiapan terbit buku yang akan diajukan ke penerbit atau angka kredit | Dua peran di akhir buku | Setuju bila buku akan diterbitkan; lewati untuk modul internal |
| U5 | **Keputusan penulis → gerbang + fikstur → audit semua bab** (loop D, `KEPUTUSAN-RANCANGAN.md`, `REVISI.md`) | Keputusan gaya tidak lupa diterapkan ke bab lama | Disiplin pencatatan | Setuju (murah): setiap keputusan gaya yang dapat diperiksa mesin ditambahkan ke `gerbang.json` disertai satu uji |
| U6 | **Pelajaran proyek** (`pelajaran-proyek.md`): kesalahan berulang dan pencegahannya | Mencegah kesalahan yang sama terulang | Pemeliharaan berkas | Setuju: salin butir yang relevan untuk praktikum (klaim perbandingan dikunci `stopifnot`, narasi gambar dihitung, pembulatan tabel) |

## 3. Tidak diadaptasi

| Aspek | Alasan |
|---|---|
| Buku multidisiplin (penulis ahli bidang + pemadu, reviewer ahli 16–20) | Modul praktikum biasanya satu disiplin dan satu penulis |
| Seri buku (peta "satu topik, satu pemilik", kotak "Ingat dari Buku N", jembatan istilah antarbuku) | Hanya bermanfaat untuk seri |
| Tipografi B5 Libertinus, PDF bertag (G-TAG), G-LOG, G-TEPI, G-PENGGALAN pasca-render | Butuh LuaLaTeX dan pipa render berat; modul praktikum cukup dengan render Quarto bawaan. Pemenggalan kata tetap dapat diperiksa dengan skill eyd |
| R menghitung, Python menggambar (G-PYTHON, `gaya_gambar.py`) | Keputusan khusus seri; modul praktikum memakai satu bahasa per modul |

## 4. Catatan untuk pemeliharaan

- Pemeriksa yang diadaptasi diberi kunci konfigurasi di `gerbang.json` sehingga dapat diatur per proyek. Larangan nama teknik, subjudul bukan tanya, *persamaan* huruf kecil, dan struktur bab (`periksa_struktur`) aktif untuk semua proyek, termasuk proyek lama, jadi bab lama mungkin perlu dilengkapi pengantar dan rangkuman. `angka_inline` dan `lebar_kode_maks` hanya aktif bila kuncinya ada; `init_naskah.py` menuliskannya untuk proyek baru.
- `cek_rumus.py` dan `rumus-dan-simbol.md` adalah salinan yang sama dengan yang ada di skill `buku-ajar` dan `math-article`. Perubahan di satu tempat perlu disalin ke dua tempat lainnya.
