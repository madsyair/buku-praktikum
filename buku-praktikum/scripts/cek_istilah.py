#!/usr/bin/env python3
"""Memeriksa konsistensi istilah pada naskah Markdown/Quarto berdasarkan glosarium buku.

Pemeriksaan (blok kode, kode sebaris, rumus, URL, dan sitasi diabaikan):
  K1  bentuk alternatif dipakai padahal glosarium menetapkan bentuk utama (tidak konsisten)
  K2  kemunculan pertama istilah asing tidak disertai padanan KBBI dalam kurung (kolom kurung_pertama)
  K3  istilah asing tidak dimiringkan
  K4  serapan/padanan Indonesia dimiringkan padahal bukan istilah asing
  K5  bentuk campuran tidak baku (diinstall, didownload, ngerun, ...)
  K6  saran: padanan/serapan belum disertai istilah asingnya pada kemunculan pertama

Contoh:
    python cek_istilah.py naskah/bab/bab-03.qmd --glosarium naskah/glosarium.csv
    python cek_istilah.py naskah/bab/*.qmd --glosarium naskah/glosarium.csv --json

Kode keluar: 0 bila tidak ada temuan K1-K3; 1 bila ada.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

DEFAULT_GLOSS = Path(__file__).resolve().parent.parent / "assets" / "glosarium.csv"
SUFFIX = r"(?:-?nya|lah|kah)?"


def blank(m: re.Match) -> str:
    return re.sub(r"[^\n]", " ", m.group(0))


def mask(text: str) -> str:
    """Ganti bagian non-prosa dengan spasi tanpa mengubah posisi dan nomor baris."""
    t = text
    t = re.sub(r"\A---\n.*?\n---\n", blank, t, flags=re.S)                      # YAML
    t = re.sub(r"<!--.*?-->", blank, t, flags=re.S)                               # komentar HTML
    # blok kode berpagar (dengan dukungan pagar bersarang yang lebih panjang)
    out, i, lines = [], 0, t.split("\n")
    fence = None
    for line in lines:
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is None and m:
            fence = m.group(1)
            out.append(" " * len(line))
            continue
        if fence is not None:
            if re.match(r"^\s{0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            out.append(" " * len(line))
            continue
        out.append(line)
    t = "\n".join(out)
    t = re.sub(r"\$\$.*?\$\$", blank, t, flags=re.S)                               # rumus terpisah
    t = re.sub(r"\\begin\{(equation|align|aligned|gather|multline)\*?\}.*?\\end\{\1\*?\}", blank, t, flags=re.S)
    t = re.sub(r"(?<!\\)\$[^$\n]+?(?<!\\)\$", blank, t)                           # rumus sebaris
    t = re.sub(r"`[^`\n]+`", blank, t)                                            # kode sebaris
    t = re.sub(r"\]\([^)]*\)", lambda m: "]" + " " * (len(m.group(0)) - 1), t)  # URL tautan
    t = re.sub(r"https?://\S+", blank, t)
    t = re.sub(r"\[@[^\]]*\]|@(?:eq|fig|tbl|sec|thm|def|exm)-[\w-]+|\{#[^}]*\}", blank, t)
    return t


def italic_spans(t: str) -> list[tuple[int, int]]:
    spans = []
    for pat in (r"(?<![\*\w])\*{1}(?!\*|\s)(.+?)(?<!\s|\*)\*(?![\*\w])",
                r"\*\*\*(.+?)\*\*\*",
                r"(?<![\w_])_(?!_|\s)(.+?)(?<!\s|_)_(?![\w_])",
                r"\\(?:textit|emph)\{([^}]*)\}"):
        for m in re.finditer(pat, t, flags=re.S):
            spans.append((m.start(1), m.end(1)))
    return spans


def inside(pos: int, end: int, spans) -> bool:
    return any(s <= pos and end <= e for s, e in spans)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def term_regex(term: str) -> re.Pattern:
    parts = [re.escape(p) for p in term.split()]
    body = r"[\s*_]+".join(parts)  # izinkan penanda miring di antara kata
    return re.compile(r"(?<![\w-])" + body + SUFFIX + r"(?![\w-])", re.I)


def load_gloss(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    for r in rows:
        r["alternatif"] = [a.strip() for a in (r.get("alternatif") or "").split("|") if a.strip()]
        for k in ("utama", "jenis", "kurung_pertama", "konsep"):
            r[k] = (r.get(k) or "").strip()
    return [r for r in rows if r["utama"]]


HYBRID = re.compile(
    r"(?<![\w-])(?:di|me|meng|men|mem|ter|ber|nge|ng)-?(?:install|instal(?=l)|upload|download|run|running|"
    r"plot|setting|share|update|input|print|copy|paste|save|load|import|export|klik)\w*(?![\w-])",
    re.I)
HYBRID_OK = {"menginstal", "diinstal", "terinstal", "menginput", "diinput", "mengimpor", "diimpor",
             "mengekspor", "diekspor", "mengklik", "diklik", "terklik", "mengunduh", "diunduh"}


def check(path: Path, gloss: list[dict]) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    t = mask(raw)
    spans = italic_spans(t)
    findings = []

    def add(kode, pos, pesan):
        findings.append({"berkas": str(path), "baris": line_of(t, pos), "kode": kode, "pesan": pesan})

    alt_hits: list[tuple[int, int, str]] = []
    # posisi semua istilah utama, untuk membuang kecocokan yang berada di dalam istilah lebih panjang
    all_hits = {g["utama"]: list(term_regex(g["utama"]).finditer(t)) for g in gloss}
    spans_all = [(h.start(), h.end()) for hs in all_hits.values() for h in hs]

    def nested(h) -> bool:
        return any(s0 <= h.start() and h.end() <= e0 and (e0 - s0) > (h.end() - h.start()) for s0, e0 in spans_all)

    for g in gloss:
        hits = [h for h in all_hits[g["utama"]] if not nested(h)]
        # K2: kurung pada kemunculan pertama
        if g["kurung_pertama"] and hits:
            first = hits[0]
            after = t[first.end(): first.end() + 160]
            before = t[max(0, first.start() - 160): first.start()]
            kur = re.escape(g["kurung_pertama"].lower())
            ok_after = re.match(r"^[\s*_]*\(([^)]*)\)", after) and re.search(kur, re.match(r"^[\s*_]*\(([^)]*)\)", after).group(1).lower().replace("*", "").replace("_", ""))
            ok_before = re.search(kur + r"[\s*_]*\([\s*_]*$", before.lower())
            if not (ok_after or ok_before):
                kode = "K2" if g["jenis"] == "asing" else "K6"
                add(kode, first.start(), f"kemunculan pertama '{g['utama']}' belum disertai '({g['kurung_pertama']})'")
        # K3 / K4: huruf miring
        for h in hits:
            it = inside(h.start(), h.end(), spans)
            if g["jenis"] == "asing" and not it:
                add("K3", h.start(), f"istilah asing '{h.group(0).strip('*_')}' sebaiknya dimiringkan")
            if g["jenis"] in ("indonesia", "serapan") and it:
                # miring wajar bila sedang dikutip sebagai istilah di dalam kurung padanan
                ctx = t[max(0, h.start() - 3): h.start()]
                if "(" not in ctx:
                    add("K4", h.start(), f"'{h.group(0).strip('*_')}' adalah {g['jenis']}, tidak perlu dimiringkan")
        # K1: alternatif (dikumpulkan dulu, lalu dipilih yang terpanjang bila tumpang-tindih)
        utama_pos = [(h.start(), h.end()) for h in hits]
        for alt in g["alternatif"]:
            for h in term_regex(alt).finditer(t):
                # abaikan bila berada di dalam kurung tepat setelah bentuk utama
                if any(0 <= h.start() - e <= 80 and "(" in t[e:h.start()] and ")" not in t[e:h.start()]
                       for _, e in utama_pos):
                    continue
                alt_hits.append((h.start(), h.end(), f"'{h.group(0)}' tidak konsisten dengan glosarium; gunakan '{g['utama']}'"))
    for s0, e0, msg in alt_hits:
        if not any((s1 <= s0 and e0 <= e1) and (e1 - s1) > (e0 - s0) for s1, e1, _ in alt_hits):
            add("K1", s0, msg)
    for h in HYBRID.finditer(t):
        if h.group(0).lower() not in HYBRID_OK:
            add("K5", h.start(), f"bentuk campuran '{h.group(0)}'; gunakan padanan Indonesia (mis. memasang, mengunggah, menjalankan)")
    findings.sort(key=lambda f: (f["berkas"], f["baris"], f["kode"]))
    # buang duplikat
    seen, uniq = set(), []
    for f in findings:
        k = (f["berkas"], f["baris"], f["kode"], f["pesan"])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("berkas", nargs="+", type=Path)
    ap.add_argument("--glosarium", type=Path, default=DEFAULT_GLOSS)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    gloss = load_gloss(a.glosarium)
    findings = [f for p in a.berkas for f in check(p, gloss)]
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"[{f['kode']}] {f['berkas']}:{f['baris']}  {f['pesan']}")
        counts = {k: sum(f["kode"] == k for f in findings) for k in ("K1", "K2", "K3", "K4", "K5", "K6")}
        print("Ringkasan: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    return 1 if any(f["kode"] in ("K1", "K2", "K3") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
