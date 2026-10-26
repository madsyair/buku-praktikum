# buku-praktikum

Skill Claude untuk menulis buku ajar, modul praktikum, dan diktat matematika, statistika, sains data, serta komputasi. Teori, rumus beserta penurunannya, metode dan pemodelan statistik, serta kode R/Python/Julia digarap sebagai rangkaian agen yang saling terhubung, dengan gerbang mutu yang dapat dieksekusi dan loop perbaikan. Alurnya dibangun di atas sinergi metode Sokratik dan teknik Feynman, dan naskah berbahasa Indonesia mengikuti EYD V.

## Isi

| Bagian | Isi |
|---|---|
| Alur | Brief → studi literatur terverifikasi → rancangan bab → kerangka paragraf → penulisan → verifikasi kode, rumus, dan klaim → ulasan Sokratik–Feynman → penyuntingan bahasa → perakitan |
| Agen | A0 orkestrator, A1 perencana, A2 peneliti literatur, A2v verifikator klaim, A3 arsitek buku, A4 perancang kerangka, A5 penulis, A6 insinyur kode, A7 verifikator matematis, A8 pembaca Sokratik–Feynman, A9 penyunting bahasa, A10 perakit |
| Pedagogi | Bab sebagai peta pertanyaan, paragraf sebagai rantai tanya-jawab, uji penjelasan ulang oleh pembaca simulasi berkonteks bersih, fitur belajar (pertanyaan pemantik, jelaskan kembali, miskonsepsi) |
| Harness | `init_naskah.py` (folder kerja dan STATE), `cek_gerbang.py` (gerbang G0–G9 dan `laporan-gerbang.md`) |
| Pemeriksa | `jalankan_kode.py` (blok R/Python/Julia), `cek_turunan.py` (langkah penurunan dengan SymPy), `cek_istilah.py` (konsistensi istilah dan padanan KBBI) |
| Kebijakan istilah | Padanan KBBI dipakai selektif, serapan sesuai EYD diutamakan bila lebih populer, istilah asing disertai padanan pada kemunculan pertama; glosarium bawaan 79 istilah |

## Struktur

```
buku-praktikum/               # folder skill (inilah yang dipasang)
├── SKILL.md
├── agents/                   # instruksi per agen
├── references/               # pedagogi, literatur, struktur bab, narasi, istilah, kode, rumus
├── scripts/                  # init_naskah.py, cek_gerbang.py, dan tiga pemeriksa
└── assets/                   # templat artefak, glosarium, _quarto.yml
tests/                        # uji mandiri untuk skrip, dengan proyek contoh
.github/workflows/            # CI dan rilis berkas .skill
```

## Memasang

**Claude.ai / aplikasi Claude**: unduh `buku-praktikum.skill` dari halaman [Releases](https://github.com/madsyair/buku-praktikum/releases/latest), lalu unggah lewat pengaturan skill.

**Claude Code**: salin folder skill ke direktori skill Anda.

```bash
git clone https://github.com/madsyair/buku-praktikum.git
cp -r buku-praktikum/buku-praktikum ~/.claude/skills/
```

Skill ini paling baik dipakai bersama [skill-eyd](https://github.com/madsyair/skill-eyd) dan [humanizer-id](https://github.com/madsyair/humanizer-id).

## Memakai harness secara langsung

```bash
python buku-praktikum/scripts/init_naskah.py --root path/ke/proyek --judul "Judul Buku"
python buku-praktikum/scripts/init_naskah.py --root path/ke/proyek --bab-baru 1
python buku-praktikum/scripts/cek_gerbang.py --root path/ke/proyek
```

## Menjalankan uji

```bash
pip install pytest sympy numpy
python -m pytest -q tests      # uji R ikut berjalan bila Rscript tersedia
```

Pengeksekusi kode Julia belum masuk CI.

## Lisensi

MIT
