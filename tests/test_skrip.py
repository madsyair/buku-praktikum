"""Uji mandiri untuk skrip skill buku-praktikum."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "buku-praktikum" / "scripts"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "proyek-contoh"
HAS_R = shutil.which("Rscript") is not None


def run(script: str, *args, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, cwd=cwd, timeout=600)


# ------------------------------------------------------------------ cek_turunan.py
def test_turunan_benar_lolos_simbolik(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text(
        "simbol: mu: real\nsimbol: n: integer, positive\nindeks: x\n"
        "langkah: Sum((x[i] - mu)**2, (i, 1, n))\n"
        "langkah: Sum(x[i]**2, (i, 1, n)) - 2*mu*Sum(x[i], (i, 1, n)) + n*mu**2 | jabarkan\n",
        encoding="utf-8")
    p = run("cek_turunan.py", f, "--json")
    assert p.returncode == 0, p.stdout
    status = [e["status"] for e in json.loads(p.stdout)[0]["langkah"]]
    assert status == ["AWAL", "SIMBOLIK-OK"]


def test_turunan_salah_ditolak_dengan_titik_pembantah(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("simbol: a, b: real\nlangkah: (a + b)**2\nlangkah: a**2 + b**2\n", encoding="utf-8")
    p = run("cek_turunan.py", f, "--json")
    assert p.returncode == 1
    last = json.loads(p.stdout)[0]["langkah"][-1]
    assert last["status"] == "GAGAL" and "titik pembantah" in last["catatan"]


def test_persamaan_mengkuadratkan_menambah_akar(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("simbol: a: real\npersamaan: 2*a - 4 = 0\npersamaan: a = 2\npersamaan: a**2 = 4\n",
                 encoding="utf-8")
    p = run("cek_turunan.py", f, "--json")
    st = [e["status"] for e in json.loads(p.stdout)[0]["langkah"]]
    assert st == ["AWAL", "SIMBOLIK-OK", "GAGAL"]


def test_persamaan_faktor_memuat_besaran_dicari_ditolak(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("simbol: b0, b1, x, y, n: real\ntak-diketahui: b0, b1\n"
                 "persamaan: n*y - n*b0 - n*b1*x = 0\npersamaan: b0 = y + b1*x\n", encoding="utf-8")
    p = run("cek_turunan.py", f, "--json")
    assert json.loads(p.stdout)[0]["langkah"][-1]["status"] == "GAGAL"


def test_manual_dan_sintaks(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("manual: E[X] = mu | definisi\nlangkah: ((\n", encoding="utf-8")
    p = run("cek_turunan.py", f, "--json")
    st = [e["status"] for e in json.loads(p.stdout)[0]["langkah"]]
    assert st == ["MANUAL", "GALAT-SINTAKS"] and p.returncode == 1


# ------------------------------------------------------------------ cek_istilah.py
NASKAH_ISTILAH = """---
title: uji
---
Setiap variabel diamati, lalu peubah lain dihitung. Data diinstall dulu.

Kita memakai *bootstrap*, lalu bootstrap tanpa huruf miring. Struktur disimpan sebagai *array*.
Fungsi *likelihood* (kemungkinan) dipakai. Nilai *varians* dicetak miring. Galat baku (*standard error*)
dihitung, lalu galat (*error*) model diasumsikan normal.

```{r}
sebaran <- 1  # kata di kode tidak diperiksa
```

Rumus $x_{sebaran}$ dan kode `sebaran` juga tidak diperiksa.
"""


def test_istilah_mendeteksi_temuan(tmp_path):
    f = tmp_path / "bab.qmd"
    f.write_text(NASKAH_ISTILAH, encoding="utf-8")
    p = run("cek_istilah.py", f, "--json")
    found = json.loads(p.stdout)
    kode = {(x["kode"], x["pesan"].split("'")[1]) for x in found}
    assert ("K1", "peubah") in kode
    assert ("K3", "bootstrap") in kode
    assert ("K2", "array") in kode
    assert ("K4", "varians") in kode
    assert ("K5", "diinstall") in kode
    assert not any("sebaran" in x["pesan"] for x in found), "kode dan rumus harus diabaikan"
    assert not any(x["kode"] == "K6" and "'galat'" in x["pesan"] for x in found), \
        "galat di dalam 'galat baku' tidak boleh dihitung sebagai kemunculan pertama 'galat'"
    assert p.returncode == 1


def test_istilah_naskah_bersih_lolos(tmp_path):
    f = tmp_path / "bab.qmd"
    f.write_text("Setiap variabel diamati dan rata-rata dihitung. Struktur disimpan sebagai *array* (larik).\n",
                 encoding="utf-8")
    p = run("cek_istilah.py", f)
    assert p.returncode == 0, p.stdout


# ------------------------------------------------------------------ jalankan_kode.py
NASKAH_KODE = """Teks.

```{python}
x = 41
```

```{python}
x + 1
```

```{python}
#| error: true
raise ValueError("diharapkan")
```

```{python}
#| eval: false
import modul_tidak_ada
```

````markdown
```{python}
raise RuntimeError("blok di dalam contoh markdown tidak boleh dijalankan")
```
````
"""


def test_jalankan_kode_python(tmp_path):
    f = tmp_path / "bab.qmd"
    f.write_text(NASKAH_KODE, encoding="utf-8")
    p = run("jalankan_kode.py", f, "--json")
    assert p.returncode == 0, p.stdout
    blocks = json.loads(p.stdout)["berkas"][str(f)]
    assert [b["status"] for b in blocks] == ["OK", "OK", "GALAT DIHARAPKAN", "DILEWATI"]
    assert blocks[1]["output"].strip() == "42", "sesi harus berlanjut antarblok"


def test_jalankan_kode_galat_tak_terduga(tmp_path):
    f = tmp_path / "bab.qmd"
    f.write_text("```{python}\n1/0\n```\n", encoding="utf-8")
    p = run("jalankan_kode.py", f, "--json")
    assert p.returncode == 1
    assert "ZeroDivisionError" in json.loads(p.stdout)["berkas"][str(f)][0]["error"]


@pytest.mark.skipif(not HAS_R, reason="Rscript tidak tersedia")
def test_jalankan_kode_r(tmp_path):
    f = tmp_path / "bab.qmd"
    f.write_text("```{r}\nx <- c(1, 2, 3)\n```\n\n```{r}\nmean(x)\nas.integer('a')\n```\n", encoding="utf-8")
    p = run("jalankan_kode.py", f, "--json")
    blocks = json.loads(p.stdout)["berkas"][str(f)]
    assert p.returncode == 0
    assert "[1] 2" in blocks[1]["output"] and blocks[1]["warnings"]


# ------------------------------------------------------------------ init_naskah.py + cek_gerbang.py
def test_init_dan_gerbang_templat_kosong_gagal(tmp_path):
    p = run("init_naskah.py", "--root", tmp_path, "--judul", "Uji")
    assert p.returncode == 0
    run("init_naskah.py", "--root", tmp_path, "--bab-baru", "1")
    for rel in ("00-brief.md", "01-literatur.md", "02-rancangan.md", "glosarium.csv", "_quarto.yml",
                "harness/STATE.md", "harness/gerbang.json", "03-kerangka/bab-01.md", "bab/bab-01.qmd"):
        assert (tmp_path / "naskah" / rel).exists(), rel
    p = run("cek_gerbang.py", "--root", tmp_path, "--lewati-perintah")
    assert p.returncode == 1
    for g in ("G0 GAGAL", "G1 GAGAL", "G2 GAGAL", "G3 GAGAL"):
        assert g in p.stdout
    assert "pertanyaan pemandu kosong" in p.stdout


def test_init_tidak_menimpa(tmp_path):
    run("init_naskah.py", "--root", tmp_path)
    brief = tmp_path / "naskah" / "00-brief.md"
    brief.write_text("isi pengguna", encoding="utf-8")
    run("init_naskah.py", "--root", tmp_path)
    assert brief.read_text(encoding="utf-8") == "isi pengguna"


def _proyek(tmp_path) -> Path:
    dst = tmp_path / "proyek"
    shutil.copytree(FIXTURE, dst)
    return dst


def test_gerbang_proyek_contoh_lolos(tmp_path):
    proj = _proyek(tmp_path)
    p = run("cek_gerbang.py", "--root", proj, "--gerbang", "G0", "G1", "G2", "G3", "G4", "G6", "G7", "G8")
    assert p.returncode == 0, p.stdout
    assert "GAGAL" not in p.stdout


@pytest.mark.skipif(not HAS_R, reason="Rscript tidak tersedia")
def test_gerbang_kode_proyek_contoh(tmp_path):
    proj = _proyek(tmp_path)
    p = run("cek_gerbang.py", "--root", proj, "--gerbang", "G5")
    assert p.returncode == 0, p.stdout


def test_gerbang_menangkap_kesalahan(tmp_path):
    proj = _proyek(tmp_path)
    n = proj / "naskah"
    bab = n / "bab" / "bab-01.qmd"
    bab.write_text(bab.read_text(encoding="utf-8").replace("[@casella2002]", "[@casella2002; @fiktif2020]")
                   .replace("pengamatan menjadi", "pengamatan dan setiap peubah menjadi"), encoding="utf-8")
    ul = n / "ulasan" / "bab-01.md"
    ul.write_text(ul.read_text(encoding="utf-8").replace("- [x] [mayor]", "- [ ] [mayor]"), encoding="utf-8")
    lit = n / "01-literatur.md"
    lit.write_text(lit.read_text(encoding="utf-8").replace("| TERVERIFIKASI |", "| DIUSULKAN |"), encoding="utf-8")
    with (n / "turunan" / "bab-01-jumlah.txt").open("a", encoding="utf-8") as fh:
        fh.write("langkah: Sum(x[i]**2, (i, 1, n)) + n*mu**2 | salah\n")
    p = run("cek_gerbang.py", "--root", proj, "--gerbang", "G1", "G3", "G4", "G6", "G7", "G8")
    assert p.returncode == 1
    for g in ("G1 GAGAL", "G3 GAGAL", "G4 GAGAL", "G6 GAGAL", "G7 GAGAL", "G8 GAGAL"):
        assert g in p.stdout, g
    assert "fiktif2020" in p.stdout
