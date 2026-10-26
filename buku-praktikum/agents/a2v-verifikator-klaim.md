# A2v — Verifikator Klaim (konteks bersih)

## Peran

Memeriksa secara independen bahwa setiap klaim dan entri pustaka benar-benar didukung sumbernya. A2v tidak melihat penalaran A2; ia hanya membaca `naskah/01-literatur.md` dan sumber aslinya.

## Masukan

`naskah/01-literatur.md`; pada mode `sunting` dan `audit` juga sitasi di naskah bab.

## Keluaran

Status akhir di kolom *Status* tabel klaim (`TERVERIFIKASI`, `BELUM`, atau `DIBANTAH` beserta koreksinya) dan bagian *Catatan verifikasi* di akhir buku besar.

## Daftar periksa (setiap klaim)

1. Buka sumbernya sendiri (halaman penerbit, DOI, PDF, dokumentasi). Jangan memercayai lokasi yang ditulis A2 tanpa membukanya.
2. Identitas pustaka cocok: penulis, tahun, judul, edisi, penerbit/jurnal, volume, halaman, DOI/ISBN.
3. Lokasi yang dicatat memang memuat klaim itu.
4. Parafrase tidak mengubah makna: syarat, asumsi, dan batasan klaim tidak hilang. Klaim yang dilebih-lebihkan dikembalikan ke kekuatan aslinya.
5. Rumus yang dicatat sama dengan sumber, termasuk definisi simbolnya.
6. Penjelasan Feynman konsep inti tidak bertentangan dengan definisi formal di sumber. Analogi yang menyesatkan ditandai.
7. Sumber memenuhi kriteria reputasi di `references/literatur.md`.

## Gerbang G1

Setiap bab yang direncanakan punya minimal satu sumber utama dengan klaim berstatus `TERVERIFIKASI`; tidak ada klaim `DIUSULKAN` yang tersisa; tidak ada klaim `DIBANTAH` yang masih dipakai.
