#!/usr/bin/env python3
"""Menyiapkan folder kerja (harness) buku: artefak tiap tahap, STATE.md, gerbang.json, glosarium.

Contoh:
    python init_naskah.py --root . --judul "Statistika Area Kecil dengan R"
    python init_naskah.py --root . --bab-baru 3      # siapkan berkas kerangka, bab, dan ulasan untuk bab 3

Skrip aman dijalankan ulang: berkas yang sudah ada tidak ditimpa tanpa --force.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"


def find_eyd() -> str | None:
    """Cari periksa.py milik skill eyd di lokasi skill yang lazim."""
    pats = ["/mnt/skills/*/eyd/scripts/periksa.py", "/mnt/skills/*/*/eyd/scripts/periksa.py",
            str(Path.home() / ".claude/skills/eyd/scripts/periksa.py"),
            str(SKILL.parent / "eyd/scripts/periksa.py"), str(SKILL.parent / "skill-eyd/scripts/periksa.py")]
    for pat in pats:
        if "*" in pat:
            hits = sorted(Path("/").glob(pat.lstrip("/")))
            if hits:
                return str(hits[0])
        elif Path(pat).exists():
            return pat
    return None


def put(src: Path, dst: Path, force: bool, log: list[str], replace: dict | None = None) -> None:
    if dst.exists() and not force:
        log.append(f"{dst}  sudah ada (dilewati)")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    for k, v in (replace or {}).items():
        text = text.replace(k, v)
    dst.write_text(text, encoding="utf-8")
    log.append(f"{dst}  ditulis")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path("."), help="folder proyek; naskah/ dibuat di dalamnya")
    ap.add_argument("--judul", default="Judul Buku")
    ap.add_argument("--bab-baru", type=int, help="siapkan berkas untuk bab bernomor ini")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    n = a.root / "naskah"
    log: list[str] = []
    if a.bab_baru is None:
        for d in ("03-kerangka", "bab", "turunan", "laporan", "ulasan", "harness", "data"):
            (n / d).mkdir(parents=True, exist_ok=True)
        put(ASSETS / "templat-brief.md", n / "00-brief.md", a.force, log, {"| Judul kerja | |": f"| Judul kerja | {a.judul} |"})
        put(ASSETS / "templat-literatur.md", n / "01-literatur.md", a.force, log)
        put(ASSETS / "templat-rancangan.md", n / "02-rancangan.md", a.force, log)
        put(ASSETS / "templat-state.md", n / "harness" / "STATE.md", a.force, log, {"<judul kerja>": a.judul})
        put(ASSETS / "_quarto.yml", n / "_quarto.yml", a.force, log, {'"Judul Buku"': json.dumps(a.judul)})
        g = n / "glosarium.csv"
        if not g.exists() or a.force:
            shutil.copyfile(ASSETS / "glosarium.csv", g)
            log.append(f"{g}  ditulis")
        cfg = n / "harness" / "gerbang.json"
        if not cfg.exists() or a.force:
            eyd = find_eyd()
            cfg.write_text(json.dumps({
                "eyd_periksa": eyd,
                "eyd_ragam": "ilmiah",
                "izinkan_kode_tidak_dijalankan": False,
                "batas_waktu_kode": 900,
                "fitur_belajar_penanda": ["Pertanyaan pemantik", "Jelaskan kembali"],
                "min_tujuan_pembelajaran": 3,
                "min_kata_penjelasan_kode": 8,
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            log.append(f"{cfg}  ditulis (eyd_periksa: {eyd or 'tidak ditemukan; isi jalurnya bila ada'})")
    else:
        b = f"{a.bab_baru:02d}"
        put(ASSETS / "templat-kerangka-bab.md", n / "03-kerangka" / f"bab-{b}.md", a.force, log,
            {"<nomor>": str(a.bab_baru), "<n>": str(a.bab_baru)})
        put(ASSETS / "templat-bab.qmd", n / "bab" / f"bab-{b}.qmd", a.force, log)
        put(ASSETS / "templat-ulasan.md", n / "ulasan" / f"bab-{b}.md", a.force, log, {"<nomor>": str(a.bab_baru)})
    print("\n".join(log))
    print("\nLangkah berikutnya: " + ("A1 mengisi naskah/00-brief.md." if a.bab_baru is None
                                     else f"A4 mengisi naskah/03-kerangka/bab-{a.bab_baru:02d}.md."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
