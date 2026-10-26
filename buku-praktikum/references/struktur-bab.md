# Struktur Buku, Bab, dan Kerangka Paragraf

## Merancang urutan bab

Urutan bab mengikuti cara pembaca membangun pemahaman, bukan urutan daftar isi buku sumber.

- **Dari konsep ke penerapan.** Bab awal meletakkan bahasa bersama (notasi, perangkat lunak, data); bab tengah membangun metode; bab akhir memadukan metode pada kasus utuh.
- **Prasyarat eksplisit.** Setiap konsep dipakai setelah diperkenalkan. Tulis prasyarat setiap bab di rancangan; bila satu bab memakai konsep dari bab yang lebih belakang, urutannya salah.
- **Satu benang merah.** Untuk modul praktikum, pakai satu atau dua dataset yang muncul berulang di beberapa bab. Pembaca tidak perlu mengenal data baru setiap kali dan bisa melihat satu masalah dari banyak sudut.
- **Ukuran bab seimbang.** Bab yang terlalu gemuk dipecah; bab yang terlalu tipis digabung atau dijadikan subbab.
- Untuk modul praktikum yang dipakai per pertemuan, satu bab biasanya setara dengan satu pertemuan praktikum (90–150 menit).

## Anatomi bab

### Buku teori atau buku ajar

1. **Pembuka** — satu atau dua paragraf yang menghubungkan bab ini dengan bab sebelumnya dan menyodorkan masalah yang akan dijawab. Di sini gaya bercerita paling berguna: kasus nyata, pertanyaan yang biasa muncul di lapangan, atau kisah singkat lahirnya metode.
2. **Tujuan pembelajaran** — 3–5 butir yang dapat diukur ("menurunkan penduga kuadrat terkecil", bukan "memahami regresi").
3. **Isi** — subbab yang masing-masing bergerak dari intuisi → definisi → rumus → penurunan (bila membantu) → contoh → catatan batasan atau asumsi.
4. **Rangkuman** — beberapa kalimat yang menyatakan kembali gagasan inti dengan kata lain, bukan menyalin kalimat dari isi.
5. **Latihan** — bertingkat dari soal hitung, soal konsep, sampai soal penerapan dengan data.
6. **Bacaan lanjut** — dua sampai lima rujukan dengan satu kalimat alasan untuk masing-masing.

### Modul praktikum

1. **Pembuka dan tujuan praktikum.**
2. **Ringkasan teori** — cukup untuk mengerjakan praktikum, dengan rujukan ke bab teori atau buku acuan untuk pendalaman. Rumus kunci tetap ditulis lengkap.
3. **Persiapan** — paket yang dibutuhkan, cara memasangnya, dataset dan cara memuatnya, serta versi perangkat lunak yang dipakai saat menulis.
4. **Contoh terbimbing** — satu atau beberapa kasus yang dikerjakan langkah demi langkah. Setiap langkah mengikuti pola kode di `kode.md`. Bila memungkinkan, mulai dengan contoh kecil yang bisa dihitung manual, lalu cocokkan dengan keluaran perangkat lunak.
5. **Tugas praktikum** — kasus serupa yang dikerjakan pembaca sendiri, dengan petunjuk secukupnya dan hasil yang dapat dicek (mis. "koefisien kemiringan seharusnya sekitar 0,8").
6. **Pertanyaan diskusi** — tentang interpretasi, asumsi, dan apa yang terjadi bila asumsi dilanggar.
7. **Rangkuman dan kesalahan umum** — galat yang sering muncul saat menjalankan kode atau menafsirkan hasil.

Kotak khusus (*callout* di Quarto) dipakai hemat: **Catatan** untuk informasi tambahan, **Perhatian** untuk jebakan, **Tips** untuk jalan pintas praktis. Lebih dari dua kotak per subbab membuat bacaan terputus-putus.

## Rancangan bab (`naskah/02-rancangan.md`)

Gunakan `assets/templat-rancangan.md`. Untuk setiap bab tuliskan:

- judul bab dan satu kalimat pertanyaan yang dijawab bab ini;
- tujuan pembelajaran;
- prasyarat;
- subbab bernomor (mis. 3.1, 3.2, 3.2.1);
- rumus, metode, dan model utama;
- contoh, dataset, dan bahasa pemrograman;
- sumber utama (kunci pustaka dari T1).

Di akhir rancangan, tulis peta ketergantungan singkat antarbab dan daftar dataset.

## Kerangka paragraf (`naskah/03-kerangka/bab-XX.md`)

Kerangka paragraf adalah alat utama agar narasi mengalir. Untuk setiap paragraf tulis satu baris:

```
P3.2-4 | fungsi: menurunkan | gagasan: varians rata-rata sampel mengecil sebanding 1/n
       | bahan: rumus F-3.2, turunan/bab-03-varians.txt, K-03-04
       | transisi → P3.2-5: "karena mengecil, wajar bertanya seberapa cepat..." (kaitan sebab-akibat)
```

Fungsi paragraf yang lazim: **membuka**, **memotivasi**, **mendefinisikan**, **menjelaskan**, **menurunkan**, **mencontohkan**, **mengantar kode**, **menafsirkan**, **membandingkan**, **memperingatkan**, **merangkum**, **menjembatani**.

Uji kerangka sebelum menulis:

1. Baca semua baris *gagasan* dari atas ke bawah. Hasilnya harus berupa alur argumen yang utuh tanpa lompatan.
2. Setiap paragraf punya satu gagasan pokok. Dua gagasan berarti dua paragraf.
3. Setiap transisi menyebut jenis kaitannya (sebab-akibat, pertentangan, penambahan, contoh, urutan waktu, umum-khusus). Jika tidak ada kaitan yang masuk akal, mungkin ada paragraf yang hilang atau urutannya keliru.
4. Setiap paragraf berisi klaim faktual menunjuk ID klaim dari buku besar.
5. Tandai paragraf yang cocok diberi cerita atau kasus nyata dengan `[cerita]`.
