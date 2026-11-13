# Kajian model per peran agen (uji banding, 2026-11-12/13)

Dasar tabel **Pilih model per peran** di `agents/a0-orkestrator.md`. Uji banding dilakukan pada proyek buku ajar statistika dengan skill buku-ajar, yang perannya sepadan dengan peran skill ini (reviewer isi dan rumus ≈ A7, A2v, A11v; pembaca pemula ≈ A8; inventaris harness ≈ tugas mekanis A0). Setiap pasangan agen bekerja terpisah pada bahan yang sama dengan instruksi identik.

## Hasil

| Uji | Peran / bahan | Model | Temuan | Token | Waktu | Catatan |
|---|---|---|---|---|---|---|
| 1 | Reviewer isi, bab model Stan | Fable | 1 MAYOR, 7 MINOR | 253 rb | 10,6 mnt | MAYOR identik dengan Opus (dibuktikan dengan CmdStan) |
| 1 | | Opus | 1 MAYOR, 7 MINOR | 273 rb | 11,6 mnt | 3 MINOR sama, masing-masing 4 MINOR unik |
| 2 | Reviewer rumus, bab SBC | Fable | 0 MAYOR, 8 MINOR | 179 rb | 4,3 mnt | Unik: densitas tanpa Jacobian tidak *proper*; tidak menghitung ulang angka Stan |
| 2 | | Opus | 0 MAYOR, 9 MINOR | 182 rb | 4,4 mnt | Unik: syarat *draws* saling bebas (dibantah contoh bab); menghitung ulang SBC, pita, Jacobian, ESS |
| 3 | Pembaca pemula, bab pengantar | Sonnet | 3 MAYOR, 18 MINOR | 125 rb | 2,8 mnt | Tiga masalah inti sama dengan Opus |
| 3 | | Opus | 2 MAYOR, 15 MINOR | 153 rb | 4,0 mnt | Satu temuan tambahan |
| 4 | Inventaris harness (mekanis) | Haiku | 200 temuan rumus, 690 EYD | 212 rb | 2,9 mnt | Angka **tepat** (dicek dengan skrip) |
| 4 | | Sonnet | 192 temuan rumus, 690 EYD | 92 rb | 1,2 mnt | Temuan rumus **salah hitung** 8 |

## Kesimpulan

1. **Fable setara Opus untuk peran reviewer** (isi dan rumus, dua uji): jumlah dan bobot temuan sama, masalah mayor sama, biaya sedikit lebih rendah. Opus lebih konsisten menghitung ulang angka. Di skill ini fable boleh menggantikan opus pada A7, A2v, dan A11v.
2. **Untuk bab penting, dua reviewer dengan model berbeda** (opus dan fable) menangkap lebih banyak, karena setiap uji memberi temuan unik di kedua sisi.
3. **Sonnet cukup untuk pembaca pemula**: masalah inti sama dengan Opus, ±20% lebih hemat token. Dasar A8 = sonnet.
4. **Haiku tepat untuk tugas mekanis berbasis hitungan**, bahkan lebih teliti daripada Sonnet di uji 4, tetapi memakai token lebih banyak. Hasil hitungannya tetap dicek dengan skrip.

**Keterbatasan.** Satu bab per uji; temuan unik belum semuanya diverifikasi kebenarannya. Peran penulis, perancang, insinyur kode, pembuat kunci, dan penyunting belum diuji banding; modelnya ditetapkan dari sifat tugas (lihat alasan per peran di tabel A0).

## Cara memperbarui tabel

Tabel model hanya diubah berdasarkan uji banding pada pekerjaan nyata, bukan dugaan.

1. **Pilih peran dan bahan.** Satu peran, satu bab nyata yang belum diperbaiki untuk temuan peran itu (simpan salinannya agar kedua agen membaca bahan yang sama).
2. **Jalankan dua subagen berkonteks bersih** dengan berkas instruksi peran, masukan, dan format keluaran yang identik; hanya modelnya yang berbeda. Jangan saling memperlihatkan hasil.
3. **Catat per agen**: jumlah temuan MAYOR dan MINOR, token, waktu, serta temuan yang sama dan yang unik. Untuk tugas mekanis, cocokkan setiap angka dengan hasil skrip.
4. **Verifikasi temuan unik** (hitung ulang, buka sumber, jalankan kode). Temuan unik yang salah tidak dihitung sebagai kelebihan.
5. **Putuskan.** Model yang lebih murah dipakai bila masalah mayor sama dan temuan unik sahnya tidak lebih sedikit secara berarti; ulangi minimal pada dua bab sebelum menurunkan model untuk peran verifikator.
6. **Perbarui** tabel di `agents/a0-orkestrator.md`, frontmatter `model` di `claude-agents/buku-praktikum-aN-*.md`, dan tabel hasil di berkas ini (bertanggal), lalu jalankan `python scripts/cek_agen.py` dan uji repo. Proyek yang sudah memasang agen menghapus `.claude/agents/buku-praktikum-*.md` lalu menjalankan ulang `init_naskah.py --pasang-agen` (jangan memakai `--force`, yang juga menimpa artefak `naskah/`).
