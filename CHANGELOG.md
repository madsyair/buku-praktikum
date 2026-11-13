# Changelog

## 0.4.0 (2026-11-13)

Model per peran (keputusan penulis 2026-11-13), mengikuti skema skill buku-ajar dan hasil uji banding.

- **Tabel model per peran** di `agents/a0-orkestrator.md` (bagian *Pilih model per peran*), dengan alasan satu baris per peran: **opus** untuk A1, A3, A4, A5, A6, A7, A2v, A11, A11v; **sonnet** untuk A2, A8, A9, A10, A12, A13, A14; **haiku** untuk tugas mekanis di luar peran (menjalankan dan merangkum gerbang, inventaris, rakit ulang A10 tanpa prakata baru; hasil hitungan tetap dicek skrip); **fable** boleh menggantikan opus pada A7, A2v, dan A11v. A10 bawaannya sonnet, bukan haiku, karena juga menulis prakata.
- Aturan naik atau turun satu tingkat (dicatat di `STATE.md`) dan dua reviewer berbeda model (opus dan fable) untuk bab penting.
- **`claude-agents/`**: 16 berkas `buku-praktikum-aN-nama.md` (A1–A14, termasuk A2v dan A11v) berfrontmatter Claude Code `name`, `description`, `model`, dan `tools` untuk peran pemeriksa yang tidak menyunting naskah (A7, A8, A11v, A12, A14) serta A2v (hanya menyunting status klaim); isinya merujuk ke `agents/aN-*.md`.
- **`init_naskah.py --pasang-agen`** menyalin `claude-agents/` ke `<proyek>/.claude/agents/` (tidak menimpa tanpa `--force`).
- **`scripts/cek_agen.py`**: frontmatter sah, `model` ∈ {opus, sonnet, haiku, fable}, nama sama dengan berkas, setiap peran di `agents/` (kecuali A0) punya tepat satu pasangan.
- **`references/kajian-model.md`**: ringkasan uji banding (fable setara opus untuk reviewer pada dua uji, sonnet cukup untuk pembaca pemula, haiku tepat untuk hitungan mekanis) dan cara memperbarui tabel lewat uji banding.
- Uji baru: frontmatter dan model sah, pasangan setiap peran, kesesuaian tabel A0 dengan frontmatter, model tidak sah ditolak, `--pasang-agen` menyalin dan tidak menimpa.

## 0.3.0 (2026-11-10)

Usulan U1, U2, U4, U5, dan U6 dari kajian adaptasi buku-ajar diterapkan (U3 ditunda).

- **Kunci jawaban berubrik** (U1, `"kunci_jawaban": true`): A11 pembuat kunci, A11v pemeriksa kunci berkonteks bersih, `references/kunci-jawaban.md`, templat kunci bab dan temuan soal, gerbang **GK** (setiap tugas punya kunci, `> **Jawaban akhir:**`, rubrik 10 poin, tanpa temuan soal terbuka).
- **Tahap gaya buku ajar** (U2, `"tahap_gaya": true`): A12 penyunting gaya (tulis ulang ke berkas terpisah) dan A13 penerap revisi (agen lain), `references/gaya-buku-ajar.md`, templat telaah gaya, gerbang **GG** (sapaan *kita*, tanpa *Anda*, rata-rata kalimat, kepadatan sitasi).
- **Editor penerbitan** (U4, `"terbit": true`): A14 menelaah buku utuh; G9 hanya lolos dengan `Keputusan: siap terbit`.
- **Loop keputusan** (U5): `naskah/KEPUTUSAN.md` dibuat `init_naskah.py`; `istilah_terlarang` di `gerbang.json` ditegakkan G4.
- **Pelajaran proyek** (U6): `references/pelajaran-proyek.md`.
- Sapaan buku *kita* di templat bab; glosarium: *small area estimation* → pendugaan area kecil.
- G9 menuntut GG dan GK lolos bila diaktifkan. Uji baru untuk GK, GG, `istilah_terlarang`, `terbit`, dan berkas init.

## 0.2.0 (2026-11-10)

Adaptasi dari skill buku-ajar (kajian lengkap: `buku-praktikum/references/kajian-adaptasi-buku-ajar.md`).

- **Rumus dan simbol**: rujukan `references/rumus-dan-simbol.md` (rumus bagian kalimat, ISO 80000-2, pemenggalan rumus tampilan, keterangan dan konsistensi simbol) dan pemeriksa `scripts/cek_rumus.py` (R1–R12). G6 menjalankannya: ERROR menggagalkan, WARNING ditinjau A7.
- **G4 bertambah**: tanpa nama teknik pengajaran di naskah (templat tidak lagi mencetak "Pertanyaan Sokratik"), subjudul bukan kalimat tanya, *persamaan* huruf kecil, struktur bab (pengantar studi kasus/cerita, subbab ringkas, `## Rangkuman`), serta angka hasil hitung dari kode inline dan lebar baris kode bila diaktifkan di `gerbang.json`.
- **Templat bab**: pengantar berupa kasus/cerita, tanpa baris kosong sesudah rumus tampilan (lanjutan *dengan …* tidak lagi terindentasi), angka interpretasi lewat kode inline.
- **Perbaikan temuan A8** wajib diperiksa dulu dan "tidak diterapkan" harus berbukti; status data disebut saat data diperkenalkan.
- Uji baru untuk `cek_rumus.py` dan aturan G4; bab contoh di fikstur dilengkapi pengantar dan rangkuman.

## 0.1.0 (2026-10-26)

Rilis awal.

- Alur 12 agen (A0–A10, termasuk A2v verifikator klaim dan A8 pembaca Sokratik–Feynman berkonteks bersih) dengan mode `buku`, `bab`, `sunting`, dan `audit`.
- Kajian sinergi metode Sokratik dan teknik Feynman pada tiga lapis (penulis, naskah, pembaca), beserta risiko dan pengamannya.
- Harness: `init_naskah.py` dan `cek_gerbang.py` dengan gerbang G0–G9, `STATE.md`, serta lima loop berbatas (literatur, kode, rumus, Sokratik–Feynman, bahasa).
- Pemeriksa: `jalankan_kode.py` (R/Python/Julia, sesi berlanjut per bahasa), `cek_turunan.py` (SymPy: simbolik, titik acak, titik pembantah, rantai persamaan), `cek_istilah.py` (konsistensi istilah, padanan pada kemunculan pertama, huruf miring, bentuk campuran).
- Kebijakan istilah selektif untuk matematika, statistika, dan komputasi, dengan glosarium bawaan 79 istilah.
- Templat brief, buku besar klaim, rancangan bab, kerangka paragraf, bab Quarto, ulasan, STATE, dan `_quarto.yml` berbahasa Indonesia.
