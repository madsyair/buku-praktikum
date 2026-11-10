# Changelog

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
