#!/usr/bin/env python3
"""Memeriksa penurunan rumus langkah demi langkah dengan SymPy.

Format berkas (lihat references/rumus.md):

    # judul: ...
    simbol: mu, a: real
    simbol: n: integer, positive
    indeks: x, y
    langkah: Sum((x[i] - mu)**2, (i, 1, n))
    langkah: Sum(x[i]**2, (i, 1, n)) - 2*mu*Sum(x[i], (i, 1, n)) + n*mu**2   | alasan
    tak-diketahui: b
    persamaan: 2*b - 4 = 0
    persamaan: b = 2
    manual: E[X^2] = Var(X) + E[X]^2   | diperiksa lewat simulasi

Setiap 'langkah' dibandingkan dengan 'langkah' sebelumnya; setiap 'persamaan' dengan
'persamaan' sebelumnya. Baris 'manual' hanya dicatat.

Kode keluar: 0 = tidak ada GAGAL/GALAT-SINTAKS; 1 = ada.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
except ImportError:  # pragma: no cover
    print("SymPy belum terpasang. Pasang dengan: pip install sympy", file=sys.stderr)
    sys.exit(3)

ASSUMPTIONS = {"real", "positive", "negative", "nonnegative", "nonpositive", "integer", "nonzero"}
TRANSFORMS = standard_transformations


class Derivation:
    def __init__(self) -> None:
        self.ns: dict = {}
        self.int_syms: list[sp.Symbol] = []
        self.indexed: list[sp.IndexedBase] = []
        self.unknowns: list[sp.Symbol] = []
        self.title = ""
        for nm in ("i", "j", "k"):
            self.ns[nm] = sp.Symbol(nm, integer=True)
        # fungsi SymPy yang umum
        for nm in ("Sum", "Product", "exp", "log", "sqrt", "factorial", "binomial", "Integral", "diff",
                   "Matrix", "gamma", "pi", "oo", "Rational", "Abs", "sin", "cos", "tan", "E", "Eq",
                   "integrate", "simplify", "expand", "Piecewise", "beta", "erf", "Derivative", "limit"):
            self.ns[nm] = getattr(sp, nm)
        self.ns["I"] = sp.I

    def declare(self, spec: str) -> None:
        if ":" in spec:
            names, props = spec.split(":", 1)
            props = {p.strip().lower() for p in props.split(",") if p.strip()}
        else:
            names, props = spec, set()
        unknown = props - ASSUMPTIONS
        if unknown:
            raise ValueError(f"sifat simbol tidak dikenal: {', '.join(sorted(unknown))}")
        kw = {p: True for p in props}
        for nm in [n.strip() for n in names.split(",") if n.strip()]:
            s = sp.Symbol(nm, **kw)
            self.ns[nm] = s
            if "integer" in props:
                self.int_syms.append(s)

    def declare_indexed(self, spec: str) -> None:
        for nm in [n.strip() for n in spec.split(",") if n.strip()]:
            b = sp.IndexedBase(nm, real=True)
            self.ns[nm] = b
            self.indexed.append(b)

    def parse(self, text: str):
        return parse_expr(text, local_dict=self.ns, transformations=TRANSFORMS, evaluate=True)


def rand_value(sym: sp.Symbol, rng: random.Random):
    a = sym.assumptions0
    if a.get("integer"):
        lo = 1 if a.get("positive") else (0 if a.get("nonnegative") else -3)
        return rng.randint(lo, 6)
    if a.get("positive"):
        return sp.Rational(rng.randint(1, 400), 100)
    if a.get("negative"):
        return -sp.Rational(rng.randint(1, 400), 100)
    if a.get("nonnegative"):
        return sp.Rational(rng.randint(0, 400), 100)
    return sp.Rational(rng.randint(-400, 400), 100)


def numeric_equal(d: Derivation, a, b, trials: int, rng: random.Random):
    """Bandingkan a dan b pada titik acak. Kembalikan (setara, titik_pembantah)."""
    diff = a - b
    syms = sorted(diff.free_symbols, key=lambda s: s.name)
    ok_trials = 0
    for _ in range(trials * 3):
        if ok_trials >= trials:
            break
        int_first = {s: rand_value(s, rng) for s in syms if isinstance(s, sp.Symbol) and s.assumptions0.get("integer")}
        try:
            ea = a.subs(int_first).doit()
            eb = b.subs(int_first).doit()
            # ganti x[1], x[2], ... dengan angka acak
            idx = {t: sp.Rational(rng.randint(-500, 500), 100) for t in (ea.atoms(sp.Indexed) | eb.atoms(sp.Indexed))}
            ea, eb = ea.subs(idx), eb.subs(idx)
            rest = {s: rand_value(s, rng) for s in (ea.free_symbols | eb.free_symbols) if isinstance(s, sp.Symbol)}
            va = complex(sp.N(ea.subs(rest).doit(), 30))
            vb = complex(sp.N(eb.subs(rest).doit(), 30))
        except (TypeError, ValueError, ZeroDivisionError, ArithmeticError):
            continue
        val = va - vb
        if val != val:  # NaN
            continue
        scale = max(1.0, abs(va), abs(vb))
        if abs(val) > 1e-9 * scale:
            point = {str(k): str(v) for k, v in {**int_first, **rest}.items()}
            point.update({str(k): str(v) for k, v in idx.items()})
            return False, point
        ok_trials += 1
    return ok_trials >= max(3, trials // 2), None


def symbolic_zero(expr) -> bool:
    for f in (lambda e: e, sp.expand, lambda e: sp.expand(e.doit()), sp.simplify,
              lambda e: sp.simplify(sp.expand(e.doit()))):
        try:
            r = f(expr)
            if r == 0:
                return True
        except Exception:
            continue
    return False


def check_pair(d: Derivation, a, b, trials: int, rng: random.Random):
    if symbolic_zero(a - b):
        return "SIMBOLIK-OK", ""
    eq, point = numeric_equal(d, a, b, trials, rng)
    if point is not None:
        return "GAGAL", "titik pembantah: " + ", ".join(f"{k}={v}" for k, v in point.items())
    if eq:
        return "NUMERIK-OK", "sama di titik acak; belum terbukti simbolik"
    return "TIDAK-DAPAT-DIPERIKSA", "evaluasi numerik tidak berhasil"


def _is_monomial(expr) -> bool:
    """Faktor pengali yang aman: hasil kali bilangan dan pangkat simbol tunggal (mis. -n, 2, 1/n)."""
    for f in sp.Mul.make_args(expr):
        base = f.base if isinstance(f, sp.Pow) else f
        if not (base.is_Number or isinstance(base, sp.Symbol)):
            return False
    return True


def _counterexample(d: Derivation, f, g, rng: random.Random, trials: int):
    """Cari titik yang memenuhi f = 0 tetapi tidak memenuhi g = 0."""
    cands = [s for s in d.unknowns if s in f.free_symbols] or sorted(f.free_symbols, key=lambda s: s.name)
    for sym in cands:
        try:
            sols = sp.solve(sp.Eq(f, 0), sym, dict=False)
        except Exception:
            continue
        if not sols:
            continue
        for _ in range(trials):
            for sol in sols:
                others = {s: rand_value(s, rng) for s in (f.free_symbols | g.free_symbols) - {sym}
                          if isinstance(s, sp.Symbol)}
                try:
                    val = sp.N(sp.sympify(sol).subs(others), 30)
                    gv = complex(sp.N(g.subs(others).subs(sym, val), 30))
                except Exception:
                    continue
                if abs(gv) > 1e-9 * max(1.0, abs(complex(val))):
                    pt = {str(k): str(v) for k, v in others.items()}
                    v = complex(val)
                    pt[str(sym)] = f"{v.real:.6g}" if abs(v.imag) < 1e-12 else f"{v:.6g}"
                    return pt
        return None
    return "tidak-terpecahkan"


def check_equations(d: Derivation, prev, cur, trials: int, rng: random.Random):
    pa = sp.expand(prev[0] - prev[1])
    ca = sp.expand(cur[0] - cur[1])
    if symbolic_zero(pa - ca):
        return "SIMBOLIK-OK", ""
    try:
        ratio = sp.factor(sp.cancel(pa / ca))
    except Exception:
        ratio = None
    if ratio is not None and ratio != 0 and not ratio.has(sp.zoo, sp.nan) and _is_monomial(ratio) \
            and not (ratio.free_symbols & set(d.unknowns)):
        if not ratio.free_symbols:
            return "SIMBOLIK-OK", f"setara dengan faktor pengali {ratio}"
        return "SIMBOLIK-OK", f"setara bila faktor {ratio} tidak nol"
    for f, g, arah in ((pa, ca, "langkah sebelumnya"), (ca, pa, "langkah ini")):
        pt = _counterexample(d, f, g, rng, trials)
        if isinstance(pt, dict):
            return "GAGAL", f"titik yang memenuhi {arah} tetapi tidak memenuhi pasangannya: " + \
                ", ".join(f"{k}={v}" for k, v in pt.items())
        if pt == "tidak-terpecahkan":
            return "TIDAK-DAPAT-DIPERIKSA", "persamaan tidak dapat diselesaikan otomatis; periksa manual"
    return "NUMERIK-OK", "himpunan penyelesaian tampak sama di titik acak; belum terbukti simbolik"


def run(path: Path, trials: int, seed: int) -> dict:
    d = Derivation()
    rng = random.Random(seed)
    res = {"berkas": str(path), "judul": "", "langkah": []}
    prev_expr = None
    prev_eq = None
    for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = re.match(r"#\s*judul\s*:\s*(.*)", line, re.I)
            if m:
                res["judul"] = m.group(1)
            continue
        key, _, rest = line.partition(":")
        key = key.strip().lower()
        body, _, reason = rest.partition("|")
        body, reason = body.strip(), reason.strip()
        entry = {"baris": no, "jenis": key, "teks": body, "alasan": reason, "status": "", "catatan": ""}
        try:
            if key == "simbol":
                d.declare(body)
                continue
            if key == "tak-diketahui":
                d.declare(body) if not all(n.strip() in d.ns for n in body.split(":")[0].split(",")) else None
                d.unknowns += [d.ns[n.strip()] for n in body.split(":")[0].split(",") if n.strip()]
                continue
            if key == "indeks":
                d.declare_indexed(body)
                continue
            if key == "manual":
                entry["status"] = "MANUAL"
                entry["catatan"] = "periksa dengan simulasi, perhitungan eksak, atau rujukan bukti"
            elif key == "langkah":
                expr = d.parse(body)
                if prev_expr is None:
                    entry["status"] = "AWAL"
                else:
                    entry["status"], entry["catatan"] = check_pair(d, prev_expr, expr, trials, rng)
                prev_expr = expr
            elif key == "persamaan":
                if body.count("=") != 1:
                    raise ValueError("persamaan harus memuat tepat satu tanda '='")
                lhs, rhs = (d.parse(s) for s in body.split("="))
                if prev_eq is None:
                    entry["status"] = "AWAL"
                else:
                    entry["status"], entry["catatan"] = check_equations(d, prev_eq, (lhs, rhs), trials, rng)
                prev_eq = (lhs, rhs)
            else:
                entry["status"] = "GALAT-SINTAKS"
                entry["catatan"] = f"kata kunci tidak dikenal: '{key}'"
        except Exception as e:  # sintaks atau deklarasi keliru
            entry["status"] = "GALAT-SINTAKS"
            entry["catatan"] = f"{type(e).__name__}: {e}"
        res["langkah"].append(entry)
    return res


def to_md(r: dict) -> str:
    out = [f"## {r['judul'] or r['berkas']}", "", f"Berkas: `{r['berkas']}`", "",
           "| Baris | Jenis | Status | Alasan | Catatan |", "|---|---|---|---|---|"]
    for e in r["langkah"]:
        out.append(f"| {e['baris']} | {e['jenis']} | {e['status']} | {e['alasan']} | {e['catatan']} |".replace("\n", " "))
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("berkas", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--laporan", type=Path)
    ap.add_argument("--uji", type=int, default=12, help="jumlah titik acak untuk uji numerik")
    ap.add_argument("--seed", type=int, default=2025)
    a = ap.parse_args()
    results = [run(p, a.uji, a.seed) for p in a.berkas]
    md = "# Laporan Pemeriksaan Penurunan Rumus\n\n" + "\n".join(to_md(r) for r in results)
    bad = [e for r in results for e in r["langkah"] if e["status"] in ("GAGAL", "GALAT-SINTAKS")]
    todo = [e for r in results for e in r["langkah"] if e["status"] in ("MANUAL", "NUMERIK-OK", "TIDAK-DAPAT-DIPERIKSA")]
    md += f"\n**Ringkasan**: {len(bad)} langkah gagal atau bersintaks salah; {len(todo)} langkah perlu diperiksa dengan cara lain.\n"
    if a.laporan:
        a.laporan.parent.mkdir(parents=True, exist_ok=True)
        a.laporan.write_text(md, encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2) if a.json else md)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
