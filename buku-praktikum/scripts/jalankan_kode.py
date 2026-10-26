#!/usr/bin/env python3
"""Menjalankan semua blok kode R, Python, dan Julia dalam naskah Markdown/Quarto/R Markdown.

Blok dijalankan berurutan dalam satu sesi per bahasa untuk setiap berkas (seperti Quarto),
dengan direktori kerja = folder berkas naskah. Hasilnya berupa laporan per blok.

Contoh:
    python jalankan_kode.py naskah/bab/bab-03.qmd --laporan naskah/laporan/kode-bab-03.md
    python jalankan_kode.py naskah/bab/*.qmd --json

Penanda pada baris awal blok:
    #| eval: false        -> blok tidak dijalankan
    # tidak-dijalankan     -> blok tidak dijalankan
    #| error: true        -> galat di blok ini memang diharapkan

Kode keluar: 0 = semua blok yang dijalankan berhasil; 1 = ada galat tak terduga;
2 = tidak ada galat, tetapi ada blok yang tidak dapat dijalankan karena interpreter tidak tersedia.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path

LANG_ALIASES = {
    "r": "r",
    "python": "python", "py": "python", "python3": "python",
    "julia": "julia", "jl": "julia",
}
EXT = {"r": ".R", "python": ".py", "julia": ".jl"}

FENCE_OPEN = re.compile(r"^(?P<indent>\s{0,3})(?P<fence>`{3,}|~{3,})\s*(?P<info>.*)$")


@dataclass
class Block:
    file: str
    index: int
    line: int
    lang: str
    code: str
    eval: bool = True
    expect_error: bool = False
    status: str = "BELUM"
    output: str = ""
    warnings: list[str] = field(default_factory=list)
    error: str = ""


def parse_info(info: str) -> str | None:
    """Ambil nama bahasa dari info string: '{r}', '{r label}', 'r', '{python, echo=FALSE}'."""
    info = info.strip()
    if not info:
        return None
    m = re.match(r"^\{\s*\.?([A-Za-z0-9_+-]+)", info) or re.match(r"^\.?([A-Za-z0-9_+-]+)", info)
    if not m:
        return None
    return LANG_ALIASES.get(m.group(1).lower())


def extract_blocks(path: Path) -> list[Block]:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        m = FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        fence = m.group("fence")
        lang = parse_info(m.group("info"))
        start = i
        body: list[str] = []
        i += 1
        close = re.compile(r"^\s{0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$")
        while i < len(lines) and not close.match(lines[i]):
            body.append(lines[i])
            i += 1
        i += 1  # lewati pagar penutup
        if lang is None:
            continue  # blok bahasa lain (bash, markdown, latex) atau blok bersarang di dalamnya
        b = Block(file=str(path), index=len(blocks) + 1, line=start + 1, lang=lang, code="\n".join(body))
        head = [l.strip() for l in body[:15]]
        for l in head:
            if re.match(r"^#\|\s*eval\s*:\s*false\b", l, re.I):
                b.eval = False
            if re.match(r"^#\|\s*error\s*:\s*true\b", l, re.I):
                b.expect_error = True
        first_code = next((l for l in head if l and not l.startswith("#|")), "")
        if re.match(r"^#\s*tidak-dijalankan\b", first_code, re.I):
            b.eval = False
        # opsi gaya knitr di info string: {r, eval=FALSE}
        info = m.group("info")
        if re.search(r"eval\s*=\s*(FALSE|F)\b", info):
            b.eval = False
        if re.search(r"error\s*=\s*(TRUE|T)\b", info):
            b.expect_error = True
        if not b.eval:
            b.status = "DILEWATI"
        blocks.append(b)
    return blocks


DRIVER_R = r'''
args <- commandArgs(trailingOnly = TRUE)
options(device = function(...) grDevices::pdf(file = tempfile(fileext = ".pdf")), width = 90)
for (f in args) {
  cat("\n@@MULAI ", basename(f), "@@\n", sep = "")
  res <- tryCatch({
    withCallingHandlers(
      source(f, echo = FALSE, print.eval = TRUE, local = globalenv()),
      warning = function(w) {
        cat("\n@@PERINGATAN@@ ", gsub("\n", " ", conditionMessage(w)), "\n", sep = "")
        invokeRestart("muffleWarning")
      })
    "OK"
  }, error = function(e) {
    cat("\n@@GALAT@@ ", gsub("\n", " ", conditionMessage(e)), "\n", sep = "")
    "GALAT"
  })
  cat("\n@@SELESAI ", basename(f), " ", res, "@@\n", sep = "")
}
'''

DRIVER_PY = r'''
import ast, sys, traceback, warnings, os
os.environ.setdefault("MPLBACKEND", "Agg")
ns = {"__name__": "__main__"}
def _warn(message, category, filename, lineno, file=None, line=None):
    print("\n@@PERINGATAN@@ " + category.__name__ + ": " + str(message).replace("\n", " "), flush=True)
warnings.showwarning = _warn
for f in sys.argv[1:]:
    name = os.path.basename(f)
    print("\n@@MULAI " + name + "@@", flush=True)
    status = "OK"
    try:
        src = open(f, encoding="utf-8").read()
        tree = ast.parse(src, filename=f)
        last = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last = ast.Expression(tree.body.pop().value)
        exec(compile(tree, f, "exec"), ns)
        if last is not None:
            val = eval(compile(last, f, "eval"), ns)
            if val is not None:
                print(repr(val))
    except BaseException as e:
        msg = "".join(traceback.format_exception_only(type(e), e)).strip().replace("\n", " ")
        print("\n@@GALAT@@ " + msg, flush=True)
        status = "GALAT"
    sys.stdout.flush()
    print("\n@@SELESAI " + name + " " + status + "@@", flush=True)
'''

DRIVER_JL = r'''
for f in ARGS
    name = basename(f)
    println("\n@@MULAI ", name, "@@")
    status = "OK"
    try
        v = Base.include(Main, f)
        if v !== nothing
            show(stdout, MIME"text/plain"(), v)
            println()
        end
    catch e
        msg = replace(sprint(showerror, e), "\n" => " ")
        println("\n@@GALAT@@ ", msg)
        status = "GALAT"
    end
    flush(stdout)
    println("\n@@SELESAI ", name, " ", status, "@@")
end
'''


def interpreter(lang: str) -> list[str] | None:
    if lang == "r":
        exe = shutil.which("Rscript")
        return [exe, "--vanilla"] if exe else None
    if lang == "python":
        return [sys.executable, "-u"]
    if lang == "julia":
        exe = shutil.which("julia")
        return [exe, "--startup-file=no"] if exe else None
    return None


def version(lang: str) -> str:
    cmd = {"r": ["Rscript", "--version"], "python": [sys.executable, "--version"], "julia": ["julia", "--version"]}[lang]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (p.stdout + p.stderr).strip().splitlines()[0]
    except Exception:
        return "tidak tersedia"


def run_language(blocks: list[Block], lang: str, workdir: Path, timeout: int) -> None:
    todo = [b for b in blocks if b.lang == lang and b.eval]
    if not todo:
        return
    cmd = interpreter(lang)
    if cmd is None:
        for b in todo:
            b.status = "TIDAK DIJALANKAN"
            b.error = f"interpreter {lang} tidak ditemukan"
        return
    with tempfile.TemporaryDirectory(prefix="jalankan-kode-") as tmp:
        tmpd = Path(tmp)
        names = {}
        for b in todo:
            fn = tmpd / f"blok{b.index:03d}{EXT[lang]}"
            fn.write_text(b.code + "\n", encoding="utf-8")
            names[fn.name] = b
        drv = tmpd / f"_driver{EXT[lang]}"
        drv.write_text({"r": DRIVER_R, "python": DRIVER_PY, "julia": DRIVER_JL}[lang], encoding="utf-8")
        files = [str(tmpd / n) for n in names]
        env = dict(os.environ, MPLBACKEND="Agg")
        try:
            p = subprocess.run(cmd + [str(drv)] + files, cwd=workdir, capture_output=True,
                               text=True, timeout=timeout, env=env)
            out = p.stdout + ("\n" + p.stderr if p.stderr.strip() else "")
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or "") if isinstance(e.stdout, str) else ""
            out += f"\n@@BATAS-WAKTU@@ {timeout} detik"
        current: Block | None = None
        buf: list[str] = []
        for line in out.splitlines():
            m = re.match(r"^@@MULAI (\S+)@@$", line)
            if m:
                current = names.get(m.group(1))
                buf = []
                continue
            m = re.match(r"^@@SELESAI (\S+) (OK|GALAT)@@$", line)
            if m and current is not None:
                current.output = "\n".join(buf).strip("\n")
                if m.group(2) == "OK":
                    current.status = "GAGAL (galat diharapkan tidak muncul)" if current.expect_error else "OK"
                else:
                    current.status = "GALAT DIHARAPKAN" if current.expect_error else "GALAT"
                current = None
                continue
            if current is None:
                continue
            if line.startswith("@@PERINGATAN@@"):
                current.warnings.append(line.removeprefix("@@PERINGATAN@@").strip())
            elif line.startswith("@@GALAT@@"):
                current.error = line.removeprefix("@@GALAT@@").strip()
            else:
                buf.append(line)
        for b in todo:
            if b.status == "BELUM":
                b.status = "TIDAK SELESAI"
                b.error = b.error or "proses berhenti sebelum blok ini selesai (lihat galat blok sebelumnya atau batas waktu)"
                if current is b:
                    b.output = "\n".join(buf).strip("\n")
        tail = [l for l in out.splitlines() if l.startswith("@@BATAS-WAKTU@@")]
        if tail:
            for b in todo:
                if b.status == "TIDAK SELESAI":
                    b.error = "melewati batas waktu " + str(timeout) + " detik"


def truncate(text: str, n: int) -> str:
    lines = text.splitlines()
    if len(lines) <= n:
        return text
    return "\n".join(lines[:n]) + f"\n... [{len(lines) - n} baris lagi dipotong di laporan]"


def report_md(results: dict, max_lines: int) -> str:
    out = ["# Laporan Eksekusi Kode", ""]
    out.append("## Lingkungan")
    out.append("")
    for lang, v in results["versi"].items():
        out.append(f"- {lang}: {v}")
    out.append("")
    for f, blocks in results["berkas"].items():
        out.append(f"## {f}")
        out.append("")
        out.append("| Blok | Baris | Bahasa | Status | Peringatan | Galat |")
        out.append("|---|---|---|---|---|---|")
        for b in blocks:
            err = b["error"].replace("|", "\\|")[:120]
            out.append(f"| {b['index']} | {b['line']} | {b['lang']} | {b['status']} | {len(b['warnings'])} | {err} |")
        out.append("")
        for b in blocks:
            if b["status"] == "DILEWATI":
                continue
            out.append(f"### Blok {b['index']} (baris {b['line']}, {b['lang']}) — {b['status']}")
            out.append("")
            if b["output"]:
                out.append("```text")
                out.append(truncate(b["output"], max_lines))
                out.append("```")
            else:
                out.append("_(tidak ada keluaran teks)_")
            for w in b["warnings"]:
                out.append(f"- Peringatan: {w}")
            if b["error"]:
                out.append(f"- Galat: {b['error']}")
            out.append("")
    s = results["ringkasan"]
    out.append("## Ringkasan")
    out.append("")
    out.append(f"OK {s['ok']}, galat {s['galat']}, galat diharapkan {s['galat_diharapkan']}, "
               f"tidak dijalankan/tidak selesai {s['tidak_dijalankan']}, dilewati {s['dilewati']}, "
               f"blok berperingatan {s['berperingatan']}.")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("berkas", nargs="+", type=Path)
    ap.add_argument("--laporan", type=Path, help="tulis laporan Markdown ke berkas ini")
    ap.add_argument("--json", action="store_true", help="cetak hasil dalam JSON")
    ap.add_argument("--bahasa", nargs="*", choices=["r", "python", "julia"], help="hanya jalankan bahasa ini")
    ap.add_argument("--batas-waktu", type=int, default=900, help="detik per bahasa per berkas (bawaan 900)")
    ap.add_argument("--maks-baris", type=int, default=40, help="baris keluaran per blok di laporan")
    a = ap.parse_args()

    results = {"versi": {}, "berkas": {}, "ringkasan": {}}
    used = set()
    for path in a.berkas:
        if not path.exists():
            print(f"berkas tidak ditemukan: {path}", file=sys.stderr)
            return 1
        blocks = extract_blocks(path)
        if a.bahasa:
            for b in blocks:
                if b.lang not in a.bahasa and b.eval:
                    b.eval, b.status = False, "DILEWATI"
        for lang in ("r", "python", "julia"):
            if any(b.lang == lang and b.eval for b in blocks):
                used.add(lang)
                run_language(blocks, lang, path.resolve().parent, a.batas_waktu)
        results["berkas"][str(path)] = [asdict(b) for b in blocks]
    for lang in sorted(used):
        results["versi"][lang] = version(lang) if interpreter(lang) else "tidak tersedia"

    allb = [b for bs in results["berkas"].values() for b in bs]
    s = {
        "ok": sum(b["status"] == "OK" for b in allb),
        "galat": sum(b["status"] == "GALAT" or b["status"].startswith("GAGAL") for b in allb),
        "galat_diharapkan": sum(b["status"] == "GALAT DIHARAPKAN" for b in allb),
        "tidak_dijalankan": sum(b["status"] in ("TIDAK DIJALANKAN", "TIDAK SELESAI") for b in allb),
        "dilewati": sum(b["status"] == "DILEWATI" for b in allb),
        "berperingatan": sum(bool(b["warnings"]) for b in allb),
    }
    results["ringkasan"] = s

    md = report_md(results, a.maks_baris)
    if a.laporan:
        a.laporan.parent.mkdir(parents=True, exist_ok=True)
        a.laporan.write_text(md, encoding="utf-8")
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(md if not a.laporan else md.split("## Ringkasan")[-1].strip())
        if a.laporan:
            print(f"Laporan: {a.laporan}")
    galat_selesai = sum(b["status"] == "TIDAK SELESAI" for b in allb)
    if s["galat"] or galat_selesai:
        return 1
    if s["tidak_dijalankan"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
