# Gaya buku ajar: tahap gaya akhir

Diadaptasi dari skill buku-ajar (`references/gaya-buku-ajar.md`). Aktif bila `"tahap_gaya": true` di `naskah/harness/gerbang.json` (dianjurkan untuk mode `buku`). Tahap ini berjalan **sesudah G8** suatu bab. Selama A2–A8, naskah boleh padat sitasi agar setiap pernyataan punya dasar yang dapat diperiksa. Pada tahap ini A12 menulis ulang bab agar bergaya buku ajar, dan A13 (agen lain) memeriksa lalu menerapkannya. Gerbang: **GG**.

## 1. Komunikatif dan interaktif

- **Sapaan *kita*** (bawaan `"sapaan": "kita"`). Penulis dan pembaca mengerjakan langkahnya bersama: *kita hitung*, *kita lihat keluarannya*. Kata *Anda* tidak dipakai di prosa; perintah di tugas ditulis tanpa kata ganti (*Hitunglah …*, *Bandingkan …*). Sapaan lain boleh dipilih dengan mengubah `sapaan` dan mencatatnya di `KEPUTUSAN.md`.
  - ✗ *Rata-rata sampel dihitung dengan menjumlahkan semua pengamatan.* → ✓ *Untuk mendapatkan rata-rata, kita jumlahkan semua pengamatan, lalu bagi dengan banyaknya.*
- **Pertanyaan yang mengajak berpikir** di tempat pembaca biasanya ragu, langsung dijawab atau dijadikan aktivitas singkat. Subjudul tetap berupa frasa (G4).
- **Kalimat aktif** lebih dulu; pasif bila pelakunya tidak penting.
- **Tanpa komentar meta**: hindari *Mari kita lihat …*, *Pada bab ini kita akan …*. Langsung kerjakan: *Kita hitung rata-ratanya.*

## 2. Semi-formal

- Kosakata baku EYD V, istilah sesuai `glosarium.csv` dan `KEPUTUSAN.md`.
- Satu gagasan per kalimat; rata-rata ±12–20 kata, tidak ada kalimat lebih dari 35 kata. Paragraf 2–6 kalimat.
- Contoh dekat dengan pembaca (konteks Indonesia, angka masuk akal, status data disebut).

## 3. Penjelasan istilah

Setiap istilah teknis atau asing dijelaskan pada kemunculan pertama di bab (arti sehari-hari, lalu contoh singkat), dicetak miring bila asing, dan masuk `glosarium.csv` dengan arti yang sama. Satu istilah baru per kalimat. Simbol mengikuti `rumus-dan-simbol.md`.

## 4. Rujukan seperlunya

Tujuannya menghapus sitasi dari prosa, **bukan menghapus dasar**: klaim tetap tercatat di `01-literatur.md`.

| Jenis kalimat | Keputusan |
|---|---|
| Kutipan langsung, angka atau data dari sumber lain, tabel/gambar yang diadaptasi | pertahankan |
| Hasil yang khas satu sumber, masih diperdebatkan, atau baru | pertahankan |
| Nama metode atau teorema yang dinamai orang, kemunculan pertama | pertahankan sekali |
| Pengetahuan baku yang ada di banyak buku teks | hapus dari prosa; sumbernya ke *Bacaan lanjut* |
| Beberapa sitasi untuk satu klaim | sisakan satu; sisanya ke *Bacaan lanjut* |
| Sitasi yang hanya menambah wibawa | hapus beserta frasanya |

Klaim yang sitasinya dipindah diberi catatan `tampil: bacaan-lanjut` di buku besar klaim. Kepadatan sasaran `sitasi_per_1000_kata_maks` (bawaan 4) dihitung pada prosa isi, di luar *Bacaan lanjut*, tugas, dan pertanyaan diskusi.

## 5. Struktur bab

Pengantar berupa studi kasus nyata atau cerita pendek, subbab ringkas, dan `## Rangkuman` di akhir (G4 sudah memeriksanya; `struktur-bab.md`). A12 menilai apakah pengantar benar-benar menarik dan dirujuk lagi di contoh terbimbing atau rangkuman.

## 6. Ukuran (GG)

| Ukuran | Kunci `gerbang.json` (bawaan) |
|---|---|
| Telaah A12 ada dan berisi `## Tindak lanjut` dari A13 | — |
| Sapaan per 1.000 kata prosa | `sapaan_per_1000_kata_min` (3) |
| Kata *Anda* bila sapaan *kita* | 0 |
| Rata-rata panjang kalimat | `rerata_kata_kalimat_maks` (20) |
| Sitasi per 1.000 kata prosa isi | `sitasi_per_1000_kata_maks` (4) |

## 7. Daftar periksa A12 dan A13

- [ ] Pengantar menarik, berakhir pada pertanyaan bab, dan dirujuk lagi.
- [ ] Sapaan *kita*, tanpa *Anda*, tanpa komentar meta; kalimat aktif.
- [ ] Kalimat pendek dan mengalir; paragraf 2–6 kalimat.
- [ ] Setiap istilah dijelaskan pada kemunculan pertama dan ada di glosarium.
- [ ] Sitasi tersisa hanya jenis yang dipertahankan; sisanya di *Bacaan lanjut*.
- [ ] Kode, keluaran, angka inline, dan rumus tidak berubah; G4–G8 tetap lolos.
