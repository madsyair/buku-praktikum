# Rumus dan Penurunan Langkah demi Langkah

## Menulis rumus

- Tulis rumus dalam LaTeX: `$...$` untuk rumus dalam baris, `$$...$$` untuk rumus terpisah. Rumus penting diberi nomor dan label agar bisa dirujuk (Quarto: `$$ ... $$ {#eq-varians}`, dirujuk dengan `@eq-varians`).
- **Notasi ditetapkan sekali di T2** dan dipakai konsisten: huruf kapital untuk variabel acak ($X$), huruf kecil untuk nilai amatan ($x$), huruf Yunani untuk parameter ($\mu, \sigma^2, \beta$), topi untuk estimator ($\hat\beta$), garis atas untuk rata-rata sampel ($\bar{x}$), huruf tebal untuk vektor dan matriks ($\mathbf{y}, \mathbf{X}$). Catat di daftar notasi pada awal buku.
- Setiap simbol dijelaskan saat pertama muncul, tepat setelah rumusnya: "dengan $n$ menyatakan ukuran sampel dan $x_i$ nilai amatan ke-$i$."
- Rumus adalah bagian kalimat. Tanda baca setelah rumus mengikuti struktur kalimatnya, dan kalimat sebelum rumus tidak diakhiri titik dua bila rumus melanjutkan kalimat.
- Fungsi baku ditulis tegak: `\log`, `\exp`, `\operatorname{Var}`, `\operatorname{E}`; operator khusus seperti $\operatorname{Cov}$ didefinisikan sekali.
- Bila notasi berbeda dengan sumber utama, sebutkan padanannya sekali agar pembaca tidak bingung saat membaca sumber itu.

## Kapan rumus diturunkan

Turunkan rumus bila penurunan **membantu pemahaman**: menunjukkan dari mana sebuah faktor muncul (mis. pembagi $n-1$ pada varians sampel), menghubungkan dua rumus yang tampak berbeda, atau melatih teknik yang akan dipakai lagi. Untuk hasil yang penurunannya panjang dan tidak menambah pemahaman, nyatakan hasilnya, beri sitasi lokasi buktinya, lalu jelaskan intuisinya. Penurunan yang sangat panjang dipindahkan ke lampiran bab.

## Aturan penurunan langkah demi langkah

1. **Nyatakan tujuan dan asumsi** di awal: apa yang akan ditunjukkan dan dengan syarat apa (mis. $X_1, \dots, X_n$ saling bebas dan berdistribusi identik dengan varians $\sigma^2$).
2. **Satu langkah, satu operasi.** Setiap baris hanya melakukan satu manipulasi: menjabarkan kuadrat, memakai sifat linear ekspektasi, mengganti definisi, menyederhanakan. Jangan menggabungkan dua operasi yang tidak jelas dalam satu baris.
3. **Beri alasan setiap langkah** di sisi kanan atau di bawahnya: nama sifat, definisi, asumsi, atau nomor rumus yang dipakai.

   ```latex
   \begin{aligned}
   \operatorname{Var}(\bar X)
     &= \operatorname{Var}\Big(\tfrac{1}{n}\textstyle\sum_{i=1}^n X_i\Big)
       && \text{definisi } \bar X \\
     &= \tfrac{1}{n^2}\operatorname{Var}\Big(\textstyle\sum_{i=1}^n X_i\Big)
       && \operatorname{Var}(aY) = a^2\operatorname{Var}(Y) \\
     &= \tfrac{1}{n^2}\textstyle\sum_{i=1}^n \operatorname{Var}(X_i)
       && X_i \text{ saling bebas} \\
     &= \tfrac{1}{n^2}\, n\sigma^2 = \tfrac{\sigma^2}{n}
       && \operatorname{Var}(X_i) = \sigma^2
   \end{aligned}
   ```

4. **Tunjukkan langkah aljabar yang biasa membuat pembaca tersandung** (penjabaran kuadrat, penukaran urutan penjumlahan, penambahan dan pengurangan suku yang sama), meskipun tampak sepele bagi penulis.
5. **Tutup dengan makna**: setelah hasil diperoleh, satu atau dua kalimat tentang artinya ("varians rata-rata sampel mengecil sebanding $1/n$, sehingga menggandakan ukuran sampel tidak menggandakan presisi").
6. **Periksa dengan contoh angka**: bila memungkinkan, sertakan contoh numerik kecil atau simulasi yang memperlihatkan hasil penurunan berlaku.

## Verifikasi penurunan

Setiap penurunan di naskah juga disimpan dalam bentuk yang bisa diperiksa mesin di `naskah/turunan/<bab>-<nama>.txt`, lalu diperiksa dengan `scripts/cek_turunan.py`.

### Format berkas turunan

```text
# judul: Penjabaran jumlah kuadrat simpangan
# rujukan: rumus (3.4), Subbab 3.2
simbol: mu, a, b: real
simbol: n: integer, positive
indeks: x
langkah: Sum((x[i] - mu)**2, (i, 1, n))
langkah: Sum(x[i]**2 - 2*mu*x[i] + mu**2, (i, 1, n))      | jabarkan kuadrat
langkah: Sum(x[i]**2, (i, 1, n)) - 2*mu*Sum(x[i], (i, 1, n)) + n*mu**2   | sifat linear penjumlahan
manual: E[X^2] = Var(X) + (E[X])^2                         | definisi varians; diperiksa lewat simulasi
```

- `simbol:` mendeklarasikan simbol beserta sifatnya (`real`, `positive`, `integer`, `nonnegative`). Simbol tanpa deklarasi dianggap kompleks, sehingga sebaiknya semua dideklarasikan.
- `indeks:` mendeklarasikan barisan berindeks seperti $x_i$ (ditulis `x[i]`); indeks `i`, `j`, `k` disediakan otomatis.
- `langkah:` adalah satu ekspresi SymPy. Setiap langkah harus sama dengan langkah sebelumnya. Teks setelah `|` adalah alasan dan tidak diperiksa.
- `persamaan:` dipakai untuk rantai persamaan berbentuk `kiri = kanan` (mis. saat menyelesaikan persamaan normal). Dua persamaan berurutan dianggap setara bila selisih kiri dan kanannya hanya berbeda faktor pengali sederhana (bilangan atau pangkat parameter, mis. $n$ atau $1/n$) yang tidak memuat besaran yang dicari; faktor yang memuat parameter dilaporkan agar dicek tidak nol. Selain itu, skrip mencari titik yang memenuhi satu persamaan, tetapi tidak memenuhi pasangannya, sehingga langkah yang menambah atau menghilangkan penyelesaian (mis. mengkuadratkan kedua ruas) terdeteksi.
- `tak-diketahui:` menandai besaran yang sedang dicari dalam rantai persamaan (mis. `tak-diketahui: b0, b1`). Faktor pengali yang memuat besaran ini tidak dianggap sah.
- `manual:` adalah langkah yang tidak dapat diperiksa simbolik (operator ekspektasi, peluang, limit, ketaksamaan, integral yang rumit). Skrip tidak memeriksanya, tetapi mencantumkannya di laporan agar diperiksa dengan cara lain.
- Fungsi SymPy yang lazim: `Sum`, `Product`, `exp`, `log`, `sqrt`, `factorial`, `binomial`, `Integral`, `diff`, `Matrix`, `gamma`, `pi`, `oo`.

### Status hasil pemeriksaan

| Status | Arti |
|---|---|
| `SIMBOLIK-OK` | SymPy membuktikan kedua langkah sama |
| `NUMERIK-OK` | Penyederhanaan simbolik tidak berhasil, tetapi kedua langkah bernilai sama pada banyak titik acak (termasuk ukuran $n$ acak untuk penjumlahan). Ini dukungan kuat, bukan bukti; periksa sekali lagi secara manual |
| `GAGAL` | Kedua langkah berbeda pada titik tertentu; titik pembantahnya dilaporkan |
| `MANUAL` | Langkah ditandai manual dan harus diperiksa dengan cara lain |
| `GALAT-SINTAKS` | Ekspresi tidak dapat dibaca SymPy |

Penurunan dinyatakan lolos bila tidak ada `GAGAL` atau `GALAT-SINTAKS`, dan setiap `MANUAL` serta `NUMERIK-OK` sudah diperiksa dengan cara yang dicatat di laporan bab.

### Memeriksa langkah manual

Untuk langkah yang melibatkan ekspektasi, varians, atau peluang, pakai salah satu cara berikut dan catat hasilnya:

- **Simulasi Monte Carlo** dengan *seed* tetap dan ukuran replikasi yang cukup besar; bandingkan nilai simulasi dengan nilai teoretis dan nyatakan galat Monte Carlo-nya.
- **Perhitungan eksak** untuk distribusi diskret kecil (mis. menghitung semua kemungkinan hasil pelemparan dua dadu).
- **Integral numerik** (`integrate()` di R, `scipy.integrate.quad` di Python) untuk densitas kontinu.
- **Rujukan bukti** dari buku teks pada buku besar klaim, bila langkah itu adalah teorema baku.

Kode simulasi yang dipakai untuk memeriksa boleh ikut ditampilkan di buku bila membantu pembaca, dan bila ditampilkan, ia mengikuti pola di `kode.md`.
