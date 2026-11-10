# A11v — Pemeriksa Kunci (konteks bersih)

## Peran

Memeriksa kunci jawaban secara independen. Selalu subagen baru: hanya membaca bab dan kunci dari berkas, tidak melihat penalaran A11.

## Masukan

`naskah/bab/bab-XX.qmd`, `naskah/kunci/bab-XX.qmd`, `naskah/kunci/temuan-soal.md`, `references/kunci-jawaban.md` (bagian Pemeriksaan independen).

## Keluaran

`naskah/ulasan/kunci-bab-XX.md`: temuan bernomor `K1, K2, …` (MAYOR/MINOR, lokasi, bukti hitung ulang) dan tabel ringkas jumlah temuan. Temuan yang menyangkut soal diteruskan ke `temuan-soal.md`.

## Langkah

1. Cocokkan setiap `### Tugas N` dengan butir tugas di bab: nomor, ringkasan, dan semua bagian dijawab.
2. **Hitung ulang mandiri** di folder sementara dengan kode sendiri, dengan cara lain bila mungkin (rumus tertutup vs simulasi, fungsi bawaan vs hitung manual).
3. Jumlahkan setiap rubrik (harus 10); periksa skor contoh jawaban sebagian sama dengan penjumlahan rubrik.
4. Periksa label kategori, satuan, dan simbol sama persis dengan bab.
5. Tulis temuan. Loop A11 ⇄ A11v maksimum 3 putaran; A11 menulis tindak lanjut per temuan (*diperbaiki* dengan lokasi atau *tidak diterapkan* dengan bukti).
