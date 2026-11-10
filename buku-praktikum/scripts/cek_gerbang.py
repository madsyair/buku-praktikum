#!/usr/bin/env python3
"""Menjalankan gerbang mutu G0–G9 atas artefak di folder naskah/.

Gerbang buku : G0 brief, G1 literatur, G2 rancangan, G9 perakitan
Gerbang bab  : G3 kerangka, G4 draf, G5 kode, G6 rumus, G7 ulasan Sokratik–Feynman, G8 bahasa,
               GG gaya buku ajar (bila "tahap_gaya"), GK kunci jawaban (bila "kunci_jawaban")

Contoh:
    python cek_gerbang.py --root .                     # semua gerbang yang artefaknya sudah ada
    python cek_gerbang.py --root . --gerbang G1 G2
    python cek_gerbang.py --root . --bab 3 --gerbang G3 G4 G5
    python cek_gerbang.py --root . --bab 3 --lewati-perintah   # hanya periksa artefak, tanpa menjalankan skrip

Hasil ditulis ke naskah/harness/laporan-gerbang.md.
Kode keluar: 0 = tidak ada gerbang GAGAL; 1 = ada yang GAGAL; 3 = gerbang yang diminta dengan --gerbang
dilewati (artefak belum ada atau --lewati-perintah). LEWATI tidak sama dengan LOLOS.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK_GATES = ["G0", "G1", "G2"]
CHAPTER_GATES = ["G3", "G4", "G5", "G6", "G7", "G8", "GG", "GK"]
TITLES = {"G0": "Brief", "G1": "Literatur", "G2": "Rancangan", "G3": "Kerangka", "G4": "Draf",
          "G5": "Kode", "G6": "Rumus", "G7": "Ulasan Sokratik–Feynman", "G8": "Bahasa", "G9": "Perakitan",
          "GG": "Gaya buku ajar", "GK": "Kunci jawaban"}


@dataclass
class Gate:
    gate: str
    scope: str
    checks: list[tuple[str, bool, str]] = field(default_factory=list)
    skipped: str = ""

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append((name, ok, detail))

    @property
    def passed(self) -> bool:
        return not self.skipped and all(ok for _, ok, _ in self.checks)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------------------ pembaca artefak
def brief_rows(text: str) -> dict[str, str]:
    rows = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", line)
        if m and not set(m.group(1)) <= set("-: ") and m.group(1) != "Butir":
            rows[m.group(1).rstrip("*").strip().lower()] = m.group(2).strip()
    return rows


def pustaka_keys(lit: str) -> set[str]:
    return set(re.findall(r"^\s*-\s*\[([A-Za-z0-9_:.-]+)\]\s+\S", lit, flags=re.M)) - {"kunci"}


def claims(lit: str) -> dict[str, str]:
    out = {}
    for line in lit.splitlines():
        m = re.match(r"^\|\s*(K-[\w-]+)\s*\|(.*)\|\s*$", line)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            out[m.group(1)] = cells[-1].upper() if cells else ""
    return out


def chapters(ranc: str) -> dict[str, str]:
    """Kembalikan {nomor_dua_digit: isi_bagian} dari '## Bab N — judul'."""
    parts = re.split(r"^##\s+Bab\s+(\d+)\b.*$", ranc, flags=re.M)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        out[f"{int(parts[i]):02d}"] = parts[i + 1]
    return out


def field_value(section: str, label: str) -> str:
    m = re.search(r"^[ \t]*-[ \t]*\*\*" + re.escape(label) + r"\*\*[ \t]*:[ \t]*(.*)$", section, flags=re.M | re.I)
    return m.group(1).strip() if m else ""


def list_after(section: str, label: str, item: str) -> list[str]:
    m = re.search(r"^[ \t]*-[ \t]*\*\*" + re.escape(label) + r"\*\*[ \t]*:[ \t]*$", section, flags=re.M | re.I)
    if not m:
        return []
    items = []
    for line in section[m.end():].splitlines()[1:]:
        if re.match(r"^\s*-\s*\*\*", line):
            break
        mm = re.match(item, line)
        if mm and mm.group(1).strip():
            items.append(mm.group(1).strip())
    return items


def table_rows_after(text: str, heading: str) -> int:
    """Jumlah baris data berisi (bukan judul/pemisah) pada tabel pertama setelah judul tertentu."""
    i = text.find(heading)
    if i < 0:
        return 0
    rows = []
    for line in text[i + len(heading):].splitlines()[1:]:
        if line.startswith("#"):
            break
        if line.strip().startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    data = [r for r in rows[2:] if r and r[0] and not set(r[0]) <= set("-: ")]
    return len(data)


def kerangka_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if re.match(r"^\|\s*P[\w.<>-]*\d", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def code_blocks(text: str) -> list[tuple[int, int, str, bool]]:
    """(baris_mulai, baris_selesai, bahasa, dijalankan) untuk blok r/python/julia."""
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        fence, info, start = m.group(1), m.group(2), i
        j = i + 1
        close = re.compile(r"^\s{0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$")
        while j < len(lines) and not close.match(lines[j]):
            j += 1
        lang = re.match(r"^\{?\s*\.?([A-Za-z0-9]+)", info)
        lang = lang.group(1).lower() if lang else ""
        body = "\n".join(lines[start + 1:j])
        if lang in ("r", "python", "py", "julia", "jl"):
            run = not re.search(r"#\|\s*eval\s*:\s*false|^\s*#\s*tidak-dijalankan", body, flags=re.I | re.M)
            out.append((start, j, lang, run))
        i = j + 1
    return out


def citations(text: str) -> set[str]:
    keys = set()
    for m in re.finditer(r"(?<![\w.])@([A-Za-z0-9_][A-Za-z0-9_:.-]*[A-Za-z0-9_])", text):
        k = m.group(1)
        if re.match(r"^(eq|fig|tbl|sec|thm|lem|cor|prp|cnj|def|exm|exr|prf|rem)-", k):
            continue
        keys.add(k)
    return keys


def strip_code(text: str) -> str:
    out, fence = [], None
    for line in text.splitlines():
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is None and m:
            fence = m.group(1)
            out.append("")
            continue
        if fence is not None:
            if re.match(r"^\s{0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


def run(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, f"melewati batas waktu {timeout} detik"
    except FileNotFoundError as e:
        return 127, str(e)


def tail(s: str, n: int = 3) -> str:
    lines = [l for l in s.splitlines() if l.strip()]
    return " | ".join(lines[-n:])[:300]


# ------------------------------------------------------------------ gerbang buku
def g0(n: Path, cfg: dict) -> Gate:
    g = Gate("G0", "buku")
    text = read(n / "00-brief.md")
    if not text:
        g.skipped = "00-brief.md belum ada"
        return g
    rows = brief_rows(text)
    for b in ("jenis", "pembaca sasaran", "bahasa naskah", "register", "perangkat lunak", "format keluaran", "fitur belajar"):
        g.add(f"Butir '{b}' terisi", bool(rows.get(b)), "" if rows.get(b) else "kosong")
    return g


def g1(n: Path, cfg: dict) -> Gate:
    g = Gate("G1", "buku")
    lit = read(n / "01-literatur.md")
    if not lit:
        g.skipped = "01-literatur.md belum ada"
        return g
    keys, cl = pustaka_keys(lit), claims(lit)
    g.add("Daftar pustaka berisi entri", bool(keys), f"{len(keys)} entri")
    g.add("Tabel klaim berisi klaim", bool(cl), f"{len(cl)} klaim")
    pending = [k for k, s in cl.items() if s in ("DIUSULKAN", "")]
    g.add("Tidak ada klaim DIUSULKAN tersisa (semua sudah dicek A2v)", not pending, ", ".join(pending[:8]))
    ver = [k for k, s in cl.items() if s == "TERVERIFIKASI"]
    g.add("Ada klaim TERVERIFIKASI", bool(ver), f"{len(ver)} terverifikasi")
    ranc = read(n / "02-rancangan.md")
    chs = chapters(ranc)
    if chs:
        missing = [c for c, sec in chs.items()
                   if not (set(re.findall(r"\[([A-Za-z0-9_:.-]+)\]", field_value(sec, "Sumber utama"))) & keys)]
        g.add("Setiap bab di rancangan punya sumber utama di daftar pustaka", not missing, "bab " + ", ".join(missing) if missing else "")
    return g


def g2(n: Path, cfg: dict) -> Gate:
    g = Gate("G2", "buku")
    ranc = read(n / "02-rancangan.md")
    if not ranc:
        g.skipped = "02-rancangan.md belum ada"
        return g
    chs = chapters(ranc)
    g.add("Rancangan memuat bab", bool(chs), f"{len(chs)} bab")
    keys = pustaka_keys(read(n / "01-literatur.md"))
    min_tp = int(cfg.get("min_tujuan_pembelajaran", 3))
    for c, sec in chs.items():
        errs = []
        if not field_value(sec, "Pertanyaan pemandu"):
            errs.append("pertanyaan pemandu kosong")
        if not field_value(sec, "Penjelasan Feynman bab"):
            errs.append("penjelasan Feynman bab kosong")
        tp = list_after(sec, "Tujuan pembelajaran", r"^\s*\d+\.\s*(.*)$")
        if len(tp) < min_tp:
            errs.append(f"tujuan pembelajaran {len(tp)} < {min_tp}")
        sb = list_after(sec, "Subbab", r"^\s*-\s*(\d+\.\d+.*)$")
        if not sb:
            errs.append("subbab kosong")
        src = set(re.findall(r"\[([A-Za-z0-9_:.-]+)\]", field_value(sec, "Sumber utama"))) - {"kunci"}
        if not src:
            errs.append("sumber utama kosong")
        elif keys and not src <= keys:
            errs.append("kunci tidak ada di pustaka: " + ", ".join(sorted(src - keys)))
        g.add(f"Bab {c} lengkap", not errs, "; ".join(errs))
    g.add("Glosarium buku ada", (n / "glosarium.csv").exists())
    g.add("Notasi ditetapkan", table_rows_after(ranc, "## Notasi") > 0, "tabel notasi masih kosong")
    state = read(n / "harness" / "STATE.md")
    g.add("Persetujuan pengguna atas rancangan dicatat di STATE.md",
          bool(re.search(r"rancangan.*\|\s*(ya|disetujui)\s*\|", state, flags=re.I)),
          "tambahkan baris keputusan 'rancangan ... | ya |' di tabel Keputusan")
    return g


# ------------------------------------------------------------------ gerbang bab
def g3(n: Path, b: str, cfg: dict) -> Gate:
    g = Gate("G3", f"bab {b}")
    k = read(n / "03-kerangka" / f"bab-{b}.md")
    if not k:
        g.skipped = f"03-kerangka/bab-{b}.md belum ada"
        return g
    rows = kerangka_rows(k)
    g.add("Kerangka berisi baris paragraf", bool(rows), f"{len(rows)} paragraf")
    bad = []
    for idx, r in enumerate(rows):
        r = (r + [""] * 6)[:6]
        pid, q, fungsi, gagasan, _, trans = r
        miss = [nm for nm, v in (("pertanyaan", q), ("fungsi", fungsi), ("gagasan", gagasan)) if not v]
        if not trans and idx != len(rows) - 1:
            miss.append("transisi")
        if miss:
            bad.append(f"{pid}: {', '.join(miss)}")
    g.add("Setiap paragraf punya pertanyaan, fungsi, gagasan, dan transisi", not bad, "; ".join(bad[:6]))
    subs = re.findall(r"^##\s+\d+\.\d+.*$", k, flags=re.M)
    feyn = re.findall(r"^\*\*Penjelasan Feynman subbab\*\*[ \t]*:[ \t]*(\S.*)$", k, flags=re.M)
    g.add("Setiap subbab punya penjelasan Feynman", len(feyn) >= len(subs) > 0, f"{len(feyn)} dari {len(subs)} subbab")
    cl = claims(read(n / "01-literatur.md"))
    ids = set(re.findall(r"\bK-\d+-\d+\b", k))
    notver = sorted(i for i in ids if cl.get(i) != "TERVERIFIKASI")
    g.add("Setiap ID klaim yang dirujuk berstatus TERVERIFIKASI", not notver, ", ".join(notver[:8]))
    return g


LARANGAN_BAWAAN = [r"\bsokrat\w*|\bsocrat\w*|\bsokrates\b|\bsocrates\b", r"\bfeynman\b"]
POLA_ANGKA = [("desimal", r"(?<![\w.,])\d+,\d+(?![\w,])"),
              ("persen", r"(?<![\w.,])\d+(?:,\d+)?\s?(?:%|persen\b)"),
              ("ribuan", r"(?<![\w.,])\d{1,3}(?:\.\d{3})+(?![\w.])")]


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Baris prosa (di luar blok kode, YAML, dan rumus tampilan) dengan nomornya."""
    out, in_math = [], False
    body = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), strip_code(text), flags=re.S)
    lines = body.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        start = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) + 1
    for i in range(start, len(lines)):
        l = lines[i]
        if l.strip().startswith("$$"):
            in_math = not (l.strip().count("$$") == 2) and not in_math
            continue
        if not in_math:
            out.append((i + 1, l))
    return out


def clean_prose(l: str) -> str:
    l = re.sub(r"<!--.*?-->", " ", l)
    l = re.sub(r"`r [^`]*`", " ", l)
    l = re.sub(r"`[^`]*`", " ", l)
    l = re.sub(r"\$[^$]*\$", " ", l)
    l = re.sub(r"\{[#.][^}]*\}", " ", l)
    l = re.sub(r"\[@[^\]]*\]|@\w[\w:-]*", " ", l)
    return l


def structure_problems(text: str, cfg: dict) -> list[str]:
    """Pengantar bab, subbab ringkas, rangkuman (diadaptasi dari skill buku-ajar, G-STRUKTUR)."""
    sections, cur = [], ["(pengantar)", 0, []]
    for no, l in prose_lines(text):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*(\{[^}]*\})?\s*$", l)
        if m:
            sections.append(cur)
            cur = [m.group(2).strip(), len(m.group(1)), []]
            continue
        cur[2].append(clean_prose(l))
    sections.append(cur)
    words = lambda ls: len(re.findall(r"[A-Za-zÀ-ÿ][\w'-]*", re.sub(r":::[^\n]*", " ", "\n".join(ls))))
    out = []
    intro = words(sections[0][2])
    # pengantar = prosa sebelum judul pertama (judul bab ada di YAML 'title')
    if intro < int(cfg.get("pengantar_min_kata", 80)):
        out.append(f"pengantar bab {intro} kata (< {cfg.get('pengantar_min_kata', 80)}); buka dengan studi kasus nyata atau cerita pendek")
    first = " ".join(" ".join(sections[0][2]).split()[:4]).lower()
    if re.match(r"^(bab|modul) ini\b|^(pada|dalam) (bab|modul) ini\b", first):
        out.append("pengantar dibuka komentar meta ('Bab ini …')")
    for title, lvl, ls in sections[1:]:
        w = words(ls)
        if w > int(cfg.get("subbab_maks_kata", 800)) and not re.match(r"(?i)(tugas|latihan|bacaan lanjut|lampiran)", title):
            out.append(f"bagian '{title[:40]}' {w} kata (> {cfg.get('subbab_maks_kata', 800)}); pecah per konsep")
    if not any(re.match(r"(?i)^(rangkuman|ringkasan)\b", s[0]) for s in sections if s[1] == 2):
        out.append("tidak ada subbab '## Rangkuman' di akhir bab")
    return out


def g4(n: Path, b: str, cfg: dict) -> Gate:
    g = Gate("G4", f"bab {b}")
    path = n / "bab" / f"bab-{b}.qmd"
    text = read(path)
    if not text:
        g.skipped = f"bab/bab-{b}.qmd belum ada"
        return g
    keys = pustaka_keys(read(n / "01-literatur.md"))
    cites = citations(strip_code(text)) - {"kunci"}
    unknown = sorted(cites - keys)
    g.add("Setiap sitasi ada di daftar pustaka", not unknown, ", ".join(unknown[:8]))
    g.add("Naskah memuat sitasi", bool(cites), "" if cites else "tidak ada sitasi sama sekali")
    lines = text.splitlines()
    min_words = int(cfg.get("min_kata_penjelasan_kode", 8))
    lonely = []
    blocks = code_blocks(text)
    for k_, (s, e, lang, runs) in enumerate(blocks):
        if not runs:
            continue
        nxt = blocks[k_ + 1][0] if k_ + 1 < len(blocks) else len(lines)
        heading = next((i for i in range(e + 1, nxt) if lines[i].startswith("#")), nxt)
        prose = [l for l in lines[e + 1:heading] if l.strip() and not l.lstrip().startswith((":::", "|", "<!--"))]
        if len(" ".join(prose).split()) < min_words:
            lonely.append(f"baris {s + 1}")
    g.add("Setiap blok kode yang dijalankan diikuti penjelasan", not lonely, ", ".join(lonely[:8]))
    ph = [i + 1 for i, l in enumerate(lines) if "[[" in l and "]]" in l]
    g.add("Tidak ada penanda [[...]] tersisa", not ph, "baris " + ", ".join(map(str, ph[:8])) if ph else "")
    k = read(n / "03-kerangka" / f"bab-{b}.md")
    if k:
        subs = [re.sub(r"^##\s+\d+(\.\d+)+\s*", "", s).strip() for s in re.findall(r"^##\s+\d+\.\d+.*$", k, flags=re.M)]
        heads = {re.sub(r"\{.*?\}", "", h).strip().lower() for h in re.findall(r"^#{2,4}\s+(.*)$", text, flags=re.M)}
        missing = [s for s in subs if s and s.lower() not in heads and not s.startswith("<")]
        g.add("Setiap subbab di kerangka ada di naskah", not missing, "; ".join(missing[:6]))
    # --- aturan yang diadaptasi dari skill buku-ajar (lihat references/kajian-adaptasi-buku-ajar.md)
    prose = prose_lines(text)
    larangan = cfg.get("larangan", LARANGAN_BAWAAN)
    hit = [f"baris {no}: {m.group(0)}" for no, l in prose for pola in larangan
           for m in re.finditer(pola, clean_prose(l), flags=re.I)]
    g.add("Nama teknik pengajaran tidak ditulis di naskah", not hit, "; ".join(hit[:6]))
    ask = [f"baris {no}" for no, l in prose if re.match(r"^#{1,6}\s", l) and "?" in re.sub(r"\{[^}]*\}\s*$", "", l)]
    g.add("Subjudul berupa frasa, bukan kalimat tanya", not ask, ", ".join(ask[:6]))
    eqcap = [f"baris {no}" for no, l in prose if re.search(r"(?:[^.!?\s#>*-])\s+Persamaan\b", clean_prose(l))]
    g.add("Kata 'persamaan' huruf kecil di tengah kalimat", not eqcap, ", ".join(eqcap[:6]))
    salah = [f"baris {no}: '{m.group(0)}' → {d.get('saran', '')}" for no, l in prose for d in cfg.get("istilah_terlarang", [])
             for m in re.finditer(d["pola"], clean_prose(l), flags=re.I)]
    g.add("Istilah yang sudah diputuskan (istilah_terlarang di gerbang.json)", not salah, "; ".join(salah[:6]))
    if cfg.get("periksa_struktur", True):
        sp = structure_problems(text, cfg)
        g.add("Struktur bab: pengantar menarik, subbab ringkas, rangkuman", not sp, "; ".join(sp[:6]))
    if cfg.get("angka_inline"):
        izin = set(cfg.get("angka_tetap", []))
        typed = [f"baris {no}: {j} '{m.group(0).strip()}'" for no, l in prose for j, pola in POLA_ANGKA
                 for m in re.finditer(pola, clean_prose(l)) if m.group(0).strip() not in izin]
        g.add("Angka hasil hitung di prosa berasal dari kode inline (`r ...`)", not typed, "; ".join(typed[:8]))
    if cfg.get("lebar_kode_maks"):
        wide = [f"baris {i + 1}" for s, e, lang, _ in blocks for i in range(s + 1, e)
                if len(lines[i]) > int(cfg["lebar_kode_maks"]) and not lines[i].lstrip().startswith("#|")]
        g.add(f"Baris kode ≤ {cfg['lebar_kode_maks']} karakter", not wide, ", ".join(wide[:8]))
    rows = brief_rows(read(n / "00-brief.md"))
    if rows.get("fitur belajar", "").lower().startswith("ya"):
        plain = strip_code(text).lower()
        miss = [f for f in cfg.get("fitur_belajar_penanda", []) if f.lower() not in plain]
        g.add("Fitur belajar ada di bab", not miss, "belum ada: " + ", ".join(miss) if miss else "")
    return g


def g5(n: Path, b: str, cfg: dict, skip: bool) -> Gate:
    g = Gate("G5", f"bab {b}")
    path = n / "bab" / f"bab-{b}.qmd"
    if not path.exists():
        g.skipped = f"bab/bab-{b}.qmd belum ada"
        return g
    if skip:
        g.skipped = "--lewati-perintah"
        return g
    rep = n / "laporan" / f"kode-bab-{b}.md"
    code, out = run([sys.executable, str(HERE / "jalankan_kode.py"), str(path), "--laporan", str(rep),
                     "--batas-waktu", str(cfg.get("batas_waktu_kode", 900))], n, int(cfg.get("batas_waktu_kode", 900)) * 3 + 60)
    if code == 2 and cfg.get("izinkan_kode_tidak_dijalankan"):
        g.add("Semua blok berhasil (sebagian tidak dijalankan, diizinkan gerbang.json)", True, tail(out))
    else:
        g.add("Semua blok kode berjalan tanpa galat tak terduga", code == 0, tail(out))
    return g


def g6(n: Path, b: str, cfg: dict, skip: bool) -> Gate:
    g = Gate("G6", f"bab {b}")
    bab = n / "bab" / f"bab-{b}.qmd"
    if bab.exists():
        sys.path.insert(0, str(HERE))
        import cek_rumus
        temuan, _ = cek_rumus.periksa([bab], "id", cfg.get("rumus_abaikan", []))
        err = [t for t in temuan if t["tingkat"] == "ERROR"]
        war = [t for t in temuan if t["tingkat"] != "ERROR"]
        fmt = lambda t: f"baris {t['baris']} {t['kode']}: {t['temuan']}"
        g.add(f"cek_rumus.py: tidak ada ERROR penulisan rumus ({len(war)} WARNING untuk A7, lihat references/rumus-dan-simbol.md)",
              not err, "; ".join(fmt(t) for t in (err or war)[:6]))
    files = sorted((n / "turunan").glob(f"bab-{b}-*.txt"))
    if not files:
        g.add("Tidak ada penurunan yang perlu diperiksa", True, "tidak ada berkas turunan untuk bab ini")
        return g
    if skip:
        g.skipped = "--lewati-perintah"
        return g
    rep = n / "laporan" / f"rumus-bab-{b}-otomatis.md"
    code, out = run([sys.executable, str(HERE / "cek_turunan.py"), *map(str, files), "--laporan", str(rep), "--json"], n, 600)
    g.add("cek_turunan.py: tidak ada langkah GAGAL atau GALAT-SINTAKS", code == 0, tail(read(rep), 1))
    try:
        data = json.loads(out[out.index("["):]) if "[" in out else []
    except ValueError:
        data = []
    need = [e for r in data for e in r.get("langkah", []) if e.get("status") in ("MANUAL", "NUMERIK-OK", "TIDAK-DAPAT-DIPERIKSA")]
    if need:
        notes = read(n / "laporan" / f"rumus-bab-{b}.md")
        ok = "## Catatan pemeriksaan" in notes
        g.add(f"Catatan pemeriksaan untuk {len(need)} langkah manual/numerik ada di laporan/rumus-bab-{b}.md", ok,
              "" if ok else "tambahkan bagian '## Catatan pemeriksaan'")
    return g


def g7(n: Path, b: str, cfg: dict) -> Gate:
    g = Gate("G7", f"bab {b}")
    text = read(n / "ulasan" / f"bab-{b}.md")
    if not text:
        g.skipped = f"ulasan/bab-{b}.md belum ada"
        return g
    verdicts = re.findall(r"Putusan:\s*(LOLOS|REVISI)\b", text)
    g.add("Putusan terakhir LOLOS", bool(verdicts) and verdicts[-1] == "LOLOS", verdicts[-1] if verdicts else "belum ada putusan")
    open_major = re.findall(r"^\s*-\s*\[\s\]\s*\[mayor\].*$", text, flags=re.M | re.I)
    g.add("Tidak ada temuan mayor yang terbuka", not open_major, "; ".join(t.strip()[:60] for t in open_major[:3]))
    return g


def g8(n: Path, b: str, cfg: dict, skip: bool) -> Gate:
    g = Gate("G8", f"bab {b}")
    path = n / "bab" / f"bab-{b}.qmd"
    if not path.exists():
        g.skipped = f"bab/bab-{b}.qmd belum ada"
        return g
    if skip:
        g.skipped = "--lewati-perintah"
        return g
    eyd = cfg.get("eyd_periksa")
    if eyd and Path(eyd).exists():
        code, out = run([sys.executable, eyd, str(path), "--ragam", cfg.get("eyd_ragam", "ilmiah"), "--json"], n, 600)
        try:
            summ = json.loads(out).get("ringkasan", {})
            det = f"ERROR {summ.get('error')}, WARNING {summ.get('warning')}"
        except ValueError:
            det = tail(out)
        g.add("periksa.py EYD: 0 ERROR", code == 0, det)
    else:
        g.add("periksa.py EYD tersedia", False, "isi 'eyd_periksa' di harness/gerbang.json, atau catat di laporan bahasa bahwa skill eyd tidak tersedia lalu set ke \"tidak-tersedia\"") \
            if eyd != "tidak-tersedia" else g.add("periksa.py EYD dicatat tidak tersedia", True, "")
    gl = n / "glosarium.csv"
    code, out = run([sys.executable, str(HERE / "cek_istilah.py"), str(path), "--glosarium", str(gl)], n, 300)
    g.add("cek_istilah.py: tidak ada temuan K1–K3", code == 0, tail(out, 1))
    g.add("Laporan bahasa ada", (n / "laporan" / f"bahasa-bab-{b}.md").exists())
    return g


def sentences(par: str) -> list[str]:
    par = re.sub(r"\b(dll|dsb|dst|dkk|hlm|No|Dr|dr|Prof|Jl|S\.\w+|M\.\w+)\.", r"\1§", par)
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(*])", par.strip()) if s.strip()]


def gg(n: Path, b: str, cfg: dict) -> Gate:
    """Tahap gaya buku ajar (diadaptasi dari buku-ajar, references/gaya-buku-ajar.md)."""
    g = Gate("GG", f"bab {b}")
    if not cfg.get("tahap_gaya"):
        g.add("Tahap gaya tidak diaktifkan (tahap_gaya di gerbang.json)", True)
        return g
    text = read(n / "bab" / f"bab-{b}.qmd")
    if not text:
        g.skipped = f"bab/bab-{b}.qmd belum ada"
        return g
    rev = read(n / "ulasan" / f"gaya-bab-{b}.md")
    rev_isi = re.sub(r"<!--.*?-->", "", rev, flags=re.S)
    g.add("Telaah gaya A12 ada dan ditindaklanjuti A13 (## Tindak lanjut)",
          bool(re.search(r"^##\s+Tindak lanjut", rev_isi, flags=re.M)),
          "" if rev else f"ulasan/gaya-bab-{b}.md belum ada")
    body, skip, cites = [], False, 0
    for _, l in prose_lines(text):
        h = re.match(r"^#{1,6}\s+(.*)$", l)
        if h:
            skip = bool(re.match(r"(?i)(bacaan lanjut|tugas|latihan|pertanyaan diskusi|jelaskan kembali)", h.group(1)))
            continue
        if skip or l.lstrip().startswith((":::", "|")):
            continue
        cites += len(re.findall(r"\[@[^\]]*\]", l)) + len(re.findall(r"(?<![\[\w`])@(?!fig-|tbl-|eq-|sec-)\w[\w:-]*", l))
        body.append(clean_prose(l))
    plain = "\n".join(body)
    words = len(re.findall(r"[A-Za-zÀ-ÿ][\w'-]*", plain)) or 1
    sents = [len(re.findall(r"[A-Za-zÀ-ÿ0-9][\w'-]*", s)) for p in re.split(r"\n\s*\n", plain) for s in sentences(" ".join(p.split()))]
    sents = [x for x in sents if x >= 3]
    mode = cfg.get("sapaan", "kita")
    pola = {"kita": r"\b[Kk]ita\b", "Anda": r"\bAnda\b"}.get(mode, r"\bAnda\b|\b[Kk]ita\b")
    per = 1000 * len(re.findall(pola, plain)) / words
    g.add(f"Sapaan {mode} ≥ {cfg.get('sapaan_per_1000_kata_min', 3)} per 1.000 kata", per >= cfg.get("sapaan_per_1000_kata_min", 3), f"{per:.1f}")
    if mode == "kita":
        anda = len(re.findall(r"\bAnda\b", plain))
        g.add("Tanpa 'Anda' di prosa (sapaan buku: kita)", anda == 0, f"{anda}×" if anda else "")
    if sents:
        mean = sum(sents) / len(sents)
        g.add(f"Rata-rata kalimat ≤ {cfg.get('rerata_kata_kalimat_maks', 20)} kata", mean <= cfg.get("rerata_kata_kalimat_maks", 20), f"{mean:.1f}")
    dens = 1000 * cites / words
    g.add(f"Sitasi ≤ {cfg.get('sitasi_per_1000_kata_maks', 4)} per 1.000 kata prosa isi (sisanya di Bacaan lanjut)",
          dens <= cfg.get("sitasi_per_1000_kata_maks", 4), f"{dens:.1f}")
    return g


def gk(n: Path, b: str, cfg: dict) -> Gate:
    """Kunci jawaban berubrik untuk tugas praktikum (diadaptasi dari buku-ajar, references/kunci-jawaban.md)."""
    g = Gate("GK", f"bab {b}")
    if not cfg.get("kunci_jawaban"):
        g.add("Kunci jawaban tidak diaktifkan (kunci_jawaban di gerbang.json)", True)
        return g
    bab = read(n / "bab" / f"bab-{b}.qmd")
    kunci = read(n / "kunci" / f"bab-{b}.qmd")
    if not bab or not kunci:
        g.skipped = f"bab/bab-{b}.qmd atau kunci/bab-{b}.qmd belum ada"
        return g
    sec = re.search(r"^##\s+(Tugas praktikum|Latihan)\b.*?$(.*?)(?=^##\s|\Z)", strip_code(bab), flags=re.M | re.S | re.I)
    n_tugas = len(re.findall(r"^\s*\d+\.\s", sec.group(2), flags=re.M)) if sec else 0
    items = re.split(r"^###\s+(?:Tugas|Latihan)\s+(\d+)\b.*$", kunci, flags=re.M)
    blocks = {items[i]: items[i + 1] for i in range(1, len(items) - 1, 2)}
    g.add(f"Setiap tugas di bab punya kunci ({n_tugas} tugas, {len(blocks)} kunci)", n_tugas > 0 and len(blocks) == n_tugas,
          "" if sec else "subbab '## Tugas praktikum' tidak ditemukan di bab")
    no_ans = [k for k, v in blocks.items() if not re.search(r"^>\s*\*\*Jawaban akhir:\*\*", v, flags=re.M)]
    g.add("Setiap kunci memuat '> **Jawaban akhir:**'", not no_ans, "tugas " + ", ".join(no_ans) if no_ans else "")
    bad = []
    for k, v in blocks.items():
        m = re.search(r"skor\s*(?:<-|=)\s*c\(([^)]*)\)", v)
        if m:
            total = sum(float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", m.group(1)))
        else:
            rows = [r for r in v.splitlines() if r.startswith("|") and not r.startswith("|-") and not re.search(r"(?i)\|\s*skor\s*\|", r)]
            total = sum(float(c.strip()) for r in rows for c in [r.strip().strip("|").split("|")[-1]] if re.fullmatch(r"\s*\d+(\.\d+)?\s*", c))
        if abs(total - 10) > 1e-9:
            bad.append(f"tugas {k}: {total:g}")
    g.add("Rubrik setiap tugas berjumlah 10 poin", not bad, "; ".join(bad))
    temuan = read(n / "kunci" / "temuan-soal.md")
    terbuka = [l.strip()[:60] for l in temuan.splitlines() if l.startswith("|") and f"| {int(b)} |" in l and "Diterapkan" not in l and "Diputuskan" not in l]
    g.add("Temuan soal bab ini sudah Diterapkan/Diputuskan", not terbuka, "; ".join(terbuka[:3]))
    return g


def g9(n: Path, cfg: dict, chapter_results: dict) -> Gate:
    g = Gate("G9", "buku")
    chs = list(chapters(read(n / "02-rancangan.md")))
    g.add("Rancangan memuat bab", bool(chs))
    for c in chs:
        res = chapter_results.get(c, {})
        failed = [k for k in CHAPTER_GATES if k not in res or not res[k].passed]
        g.add(f"Bab {c} lolos G3–G8, GG, GK", not failed, "belum: " + ", ".join(failed) if failed else "")
    if cfg.get("terbit"):
        ed = read(n / "ulasan" / "editor-penerbitan.md")
        ok = bool(re.search(r"Keputusan:\s*\**\s*siap terbit", ed, flags=re.I))
        g.add("Editor penerbitan (A14) memutuskan siap terbit (terbit: true)", ok, "" if ed else "ulasan/editor-penerbitan.md belum ada")
    fmt = brief_rows(read(n / "00-brief.md")).get("format keluaran", "").lower()
    if "quarto" in fmt or not fmt:
        g.add("_quarto.yml ada", (n / "_quarto.yml").exists())
    return g


# ------------------------------------------------------------------ utama
def to_md(results: list[Gate]) -> str:
    out = ["# Laporan Gerbang", ""]
    out += ["| Gerbang | Cakupan | Hasil |", "|---|---|---|"]
    for r in results:
        st = "LEWATI" if r.skipped else ("LOLOS" if r.passed else "GAGAL")
        out.append(f"| {r.gate} {TITLES[r.gate]} | {r.scope} | {st} |")
    out.append("")
    for r in results:
        out.append(f"## {r.gate} {TITLES[r.gate]} — {r.scope}")
        if r.skipped:
            out.append(f"- dilewati: {r.skipped}")
        for name, ok, det in r.checks:
            out.append(f"- {'✓' if ok else '✗'} {name}" + (f" — {det}" if det else ""))
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--gerbang", nargs="*", choices=BOOK_GATES + CHAPTER_GATES + ["G9"])
    ap.add_argument("--bab", nargs="*", type=int, help="nomor bab untuk gerbang G3–G8 (bawaan: semua bab di rancangan)")
    ap.add_argument("--lewati-perintah", action="store_true", help="jangan jalankan skrip kode/rumus/bahasa")
    a = ap.parse_args()
    n = a.root / "naskah"
    if not n.exists():
        print("folder naskah/ tidak ditemukan; jalankan init_naskah.py dulu", file=sys.stderr)
        return 1
    cfg = json.loads(read(n / "harness" / "gerbang.json") or "{}")
    want = a.gerbang or BOOK_GATES + CHAPTER_GATES + ["G9"]
    results: list[Gate] = []
    book = {"G0": g0, "G1": g1, "G2": g2}
    for gname in BOOK_GATES:
        if gname in want:
            results.append(book[gname](n, cfg))
    bab_list = [f"{x:02d}" for x in a.bab] if a.bab else sorted(chapters(read(n / "02-rancangan.md")))
    chapter_results: dict[str, dict[str, Gate]] = {}
    need_ch = [x for x in CHAPTER_GATES if x in want] or (CHAPTER_GATES if "G9" in want else [])
    for b in bab_list:
        chapter_results[b] = {}
        for gname in need_ch:
            if gname == "G3":
                r = g3(n, b, cfg)
            elif gname == "G4":
                r = g4(n, b, cfg)
            elif gname == "G5":
                r = g5(n, b, cfg, a.lewati_perintah)
            elif gname == "G6":
                r = g6(n, b, cfg, a.lewati_perintah)
            elif gname == "G7":
                r = g7(n, b, cfg)
            elif gname == "GG":
                r = gg(n, b, cfg)
            elif gname == "GK":
                r = gk(n, b, cfg)
            else:
                r = g8(n, b, cfg, a.lewati_perintah)
            chapter_results[b][gname] = r
            if gname in want:
                results.append(r)
    if "G9" in want:
        results.append(g9(n, cfg, chapter_results))
    md = to_md(results)
    (n / "harness").mkdir(parents=True, exist_ok=True)
    (n / "harness" / "laporan-gerbang.md").write_text(md + "\n", encoding="utf-8")
    for r in results:
        st = "LEWATI" if r.skipped else ("LOLOS " if r.passed else "GAGAL ")
        print(f"{r.gate} {st} {TITLES[r.gate]} ({r.scope})" + (f" — {r.skipped}" if r.skipped else ""))
        for name, ok, det in r.checks:
            if not ok:
                print(f"    ✗ {name}" + (f": {det}" if det else ""))
    print(f"\nLaporan: {n / 'harness' / 'laporan-gerbang.md'}")
    if any(not r.skipped and not r.passed for r in results):
        return 1
    if a.gerbang and any(r.skipped for r in results):
        return 3  # gerbang yang diminta dilewati: artefaknya belum ada atau perintah dilewati
    return 0


if __name__ == "__main__":
    sys.exit(main())
