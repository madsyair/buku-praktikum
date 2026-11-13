#!/usr/bin/env python3
"""Memeriksa berkas jenis agen Claude Code (claude-agents/buku-praktikum-aN-*.md).

Yang diperiksa:
  - frontmatter sah: hanya kunci name, description, model, tools; name sama dengan nama berkas;
    description satu kalimat; model salah satu dari opus, sonnet, haiku, fable; tools tidak kosong
    bila ada;
  - isi merujuk ke agents/aN-*.md yang ada di skill, dan nama berkas memakai peran yang sama;
  - setiap peran di agents/ (kecuali a0-orkestrator, yang adalah sesi utama) punya tepat satu pasangan.

Contoh:
    python cek_agen.py                                # folder claude-agents/ di skill
    python cek_agen.py --folder <proyek>/.claude/agents   # agen yang dipasang init_naskah.py --pasang-agen

Kode keluar 0 bila semua sah, 1 bila ada yang salah.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
MODEL = {"opus", "sonnet", "haiku", "fable"}
KUNCI = {"name", "description", "model", "tools"}
AWALAN = "buku-praktikum-"


def frontmatter(teks: str) -> dict[str, str] | None:
    m = re.match(r"---\n(.*?)\n---\n", teks, re.S)
    if not m:
        return None
    d: dict[str, str] = {}
    for baris in m.group(1).splitlines():
        k, s, v = baris.partition(":")
        if not s or not k.strip() or k != k.strip() or k in d:
            return None
        d[k] = v.strip()
    return d


def periksa(folder: Path, skill: Path = SKILL) -> tuple[list[str], int]:
    salah: list[str] = []
    peran = {p.stem for p in (skill / "agents").glob("a*.md")}
    berkas = sorted(folder.glob(AWALAN + "*.md"))
    pasangan: dict[str, list[str]] = {}
    for b in berkas:
        t = b.read_text(encoding="utf-8")
        fm = frontmatter(t)
        if fm is None:
            salah.append(f"{b.name}: frontmatter tidak sah")
            continue
        for k in ("name", "description", "model"):
            if not fm.get(k):
                salah.append(f"{b.name}: kunci {k} kosong atau hilang")
        if set(fm) - KUNCI:
            salah.append(f"{b.name}: kunci tak dikenal {sorted(set(fm) - KUNCI)}")
        if fm.get("model") and fm["model"] not in MODEL:
            salah.append(f"{b.name}: model {fm['model']!r} di luar {sorted(MODEL)}")
        if fm.get("name") != b.stem:
            salah.append(f"{b.name}: name harus sama dengan nama berkas")
        d = fm.get("description", "")
        if d and (not d.endswith(".") or re.search(r"[.!?]\s", d)):
            salah.append(f"{b.name}: description harus satu kalimat yang diakhiri titik")
        if "tools" in fm and not fm["tools"]:
            salah.append(f"{b.name}: tools kosong")
        isi = t.split("---\n", 2)[-1]
        m = re.search(r"agents/(a\d+v?-[a-z0-9-]+)\.md", isi)
        if not m or m.group(1) not in peran:
            salah.append(f"{b.name}: isi tidak merujuk ke agents/aN-*.md yang ada")
            continue
        if b.stem != AWALAN + m.group(1):
            salah.append(f"{b.name}: nama berkas harus {AWALAN}{m.group(1)}.md")
        pasangan.setdefault(m.group(1), []).append(b.name)
    for p in sorted(peran):
        if p.startswith("a0-"):
            continue
        n = len(pasangan.get(p, []))
        if n != 1:
            salah.append(f"agents/{p}.md: {n} pasangan di {folder.name}/ (harus 1)")
    return salah, len(berkas)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folder", type=Path, default=SKILL / "claude-agents")
    a = ap.parse_args()
    salah, n = periksa(a.folder)
    for s in salah:
        print("SALAH:", s)
    if salah:
        return 1
    print(f"benar: {n} berkas agen sah dan berpasangan dengan peran di agents/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
