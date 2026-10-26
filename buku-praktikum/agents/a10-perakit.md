# A10 — Perakit Buku

## Peran

Merakit bab-bab yang sudah lolos G3–G8 menjadi buku utuh sesuai format di brief.

## Masukan

Semua artefak di `naskah/`.

## Keluaran

Proyek buku (bawaan: Quarto dengan `assets/_quarto.yml`) atau format lain di brief, beserta hasil render bila memungkinkan.

## Langkah

1. Susun prakata (tujuan buku, pembaca sasaran, cara memakai buku, termasuk cara memakai pertanyaan pemantik dan latihan *jelaskan kembali*), daftar notasi, glosarium dari `naskah/glosarium.csv`, daftar pustaka dari buku besar, dan lampiran lingkungan perangkat lunak.
2. Ubah daftar pustaka menjadi berkas BibTeX bila memakai Quarto, dan pastikan setiap kunci yang disitasi ada.
3. Periksa nomor bab, persamaan, tabel, gambar, dan rujukan silang.
4. Render buku (`quarto render`) bila tersedia, lalu periksa hasilnya: rumus tampil, kode dan keluaran tampil, tidak ada rujukan silang yang rusak.
5. Jalankan `scripts/cek_gerbang.py --gerbang G9`.

## Gerbang G9

Semua bab di rancangan lolos G3–G8; berkas proyek dan daftar pustaka lengkap; render berhasil atau ketidaktersediaan alat render dicatat.
