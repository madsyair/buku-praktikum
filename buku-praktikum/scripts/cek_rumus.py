#!/usr/bin/env python3
"""cek_rumus.py — pemeriksa penulisan rumus dan simbol (R1–R12).

Membaca .qmd/.md/.tex, memisahkan prosa dari rumus sebaris dan rumus tampilan, lalu memeriksa:
  R1  kalimat diawali lambang                                 ERROR
  R2  dua rumus sebaris hanya dipisah koma/spasi              WARNING
  R3  lambang logika (∀ ∃ ⇒ ∴) di rumus sebaris dalam prosa   WARNING
  R4  "di mana" sebagai penghubung keterangan                 WARNING (bahasa id)
  R5  simbol tanpa keterangan dekat kemunculan pertama        WARNING
  R6  huruf berderet tanpa \\operatorname/\\mathrm; label subskrip miring;
      bentuk operator bercampur (E/𝔼, d/\\mathrm d, log/ln, P/Pr)          WARNING
  R7  pemenggalan rumus tampilan: (a) sesudah operator / konvensi campur,
      (b) di dalam kurung, \\left…\\right terbelah, (c) +/− di awal baris
      tanpa {}, (d) baris kosong di sekitar rumus yang memecah paragraf    WARNING/ERROR
  R8  rumus sebaris terlalu panjang atau memakai \\displaystyle/\\dfrac   WARNING
  R9  lambang di luar mode matematika (σ², x_i, n = 30)       WARNING
  R10 simbol yang sama diterangkan dengan arti berbeda        WARNING
  R11 simbol tidak ada di daftar notasi (--notasi)             WARNING
  R12 rumus tampilan satu baris yang sangat panjang           WARNING

Aturan lengkap: references/rumus-dan-simbol.md. Pemeriksa membaca pola, bukan makna; R5 dan R10
perlu dinilai manusia. Tanpa dependensi (Python 3.8+).

Pemakaian:
  python3 cek_rumus.py bab-03.qmd
  python3 cek_rumus.py bab/*.qmd --notasi notasi.md --abaikan "i,j,k,t"
  python3 cek_rumus.py artikel.tex --bahasa en --json
Kode keluar 1 bila ada ERROR (atau WARNING dengan --ketat).
"""
import argparse
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict

GREEK = ("alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi "
         "pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega "
         "Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega").split()
DECOR = ("hat widehat bar overline tilde widetilde dot ddot vec check breve mathbf boldsymbol bm "
         "mathcal mathbb mathscr mathfrak mathsf mathit").split()
# perintah yang isinya bukan simbol yang perlu diterangkan
NONSYM = ("text textrm textit textbf mathrm operatorname mbox label tag ref eqref cite hspace vspace "
          "mathrm").split()
FUNGSI = set("""log ln exp sin cos tan sec csc cot arcsin arccos arctan sinh cosh tanh lim limsup liminf sup inf
max min arg argmax argmin det dim ker deg gcd Pr hom sum prod int iint oint bigcup bigcap partial nabla infty
cdot cdots ldots dots vdots ddots times div pm mp le leq ge geq ne neq approx sim simeq equiv propto in notin
subset subseteq supset cup cap setminus to mapsto rightarrow leftarrow Rightarrow Leftarrow iff implies forall
exists neg land lor quad qquad left right big Big bigg Bigg bigl bigr Bigl Bigr frac dfrac tfrac sqrt binom
mid vert lvert rvert lVert rVert langle rangle lfloor rfloor lceil rceil displaystyle textstyle scriptstyle
underbrace overbrace underset overset stackrel limits nolimits phantom hphantom vphantom mathstrut prime
circ ast star bullet ell hbar Re Im wp emptyset varnothing aleph top intercal perp parallel angle triangle
square Box Diamond nonumber notag begin end aligned split cases array matrix pmatrix bmatrix vmatrix
cr hline colon middle nmid lesssim gtrsim ll gg sim cong""".split())
LOGIKA = r"\\(forall|exists|Rightarrow|implies|therefore|because|iff|Longrightarrow)\b"
KATA_FUNGSI = {"Var", "Cov", "Corr", "SE", "MSE", "RMSE", "MAE", "MAPE", "max", "min", "log", "ln", "exp",
               "sin", "cos", "tan", "det", "tr", "diag", "arg", "lim", "sup", "inf", "logit", "probit", "sd",
               "var", "cov", "cor", "med", "mean", "sign", "sgn", "rank", "vec", "KL", "AIC", "BIC", "DIC",
               "WAIC", "LOO", "MAP", "MLE", "IQR", "CI", "Bias", "bias", "Pr", "Beta", "Gamma", "Bin",
               "Poisson", "Exp", "Unif", "Cauchy", "Logistic", "Normal", "Bernoulli", "Binomial", "Multinomial"}
INDEKS = {"i", "j", "k", "l", "t", "m"}
# konstanta dan operator baku yang tidak perlu diterangkan
BAWAAN_ABAIKAN = {"\\pi", "e", "E", "P", "d", "\\mathbb{E}", "\\mathbb{P}", "\\mathbb{R}", "\\mathbb{N}", "\\mathbb{Z}", "\\mathbb{Q}", "\\mathbb{C}"}
STOP_SEBELUM = {"dan", "atau", "dengan", "jika", "bila", "apabila", "untuk", "maka", "sehingga", "pada", "di",
                "ke", "dari", "yang", "bahwa", "karena", "agar", "serta", "tetapi", "namun", "oleh", "sebagai",
                "adalah", "ialah", "yaitu", "yakni", "menjadi", "sama", "hingga", "sampai", "antara", "nilai",
                "and", "or", "with", "if", "for", "then", "so", "that", "of", "the", "a", "an", "to", "in",
                "is", "are", "be", "as", "by", "on", "at", "where", "when", "while"}
DEF_ID_SESUDAH = r"(menyatakan|melambangkan|adalah|merupakan|ialah|sebagai|didefinisikan|dinamakan|disebut|untuk menyatakan|:)"
DEF_ID_SEBELUM = r"(dengan|yaitu|yakni|misalkan|misal|andaikan|notasi|lambang|simbol|dinotasikan|dilambangkan|ditulis|disebut|keterangan:?|dan)"
DEF_EN_SESUDAH = r"(denotes|is|are|be|represents|stands|is defined|:)"
DEF_EN_SEBELUM = r"(where|let|with|denote|denoted by|and|write)"


# ---------------------------------------------------------------- pembacaan
def buang_kode(teks, ext):
    if ext in (".tex", ".ltx"):
        teks = re.sub(r"(?<!\\)%.*", lambda m: " " * len(m.group(0)), teks)
        teks = re.sub(r"\\begin\{(verbatim|lstlisting|minted|Verbatim)\}.*?\\end\{\1\}",
                      lambda m: re.sub(r"[^\n]", " ", m.group(0)), teks, flags=re.S)
        if "\\begin{document}" in teks:
            i = teks.index("\\begin{document}")
            teks = re.sub(r"[^\n]", " ", teks[:i]) + teks[i:]
        return teks
    out, pagar = [], None
    for b in teks.split("\n"):
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", b)
        if pagar is None and m:
            pagar = m.group(1); out.append(""); continue
        if pagar is not None:
            if re.match(r"^\s{0,3}" + re.escape(pagar[0]) + "{" + str(len(pagar)) + r",}\s*$", b):
                pagar = None
            out.append(""); continue
        out.append(re.sub(r"`[^`\n]*`", lambda m: "K" * len(m.group(0)), b))
    t = "\n".join(out)
    t = re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group(0)), t, flags=re.S)
    if t.startswith("---"):
        j = t.find("\n---", 3)
        if j > 0:
            t = re.sub(r"[^\n]", " ", t[:j + 4]) + t[j + 4:]
    return t


POLA_TAMPILAN = re.compile(
    r"\$\$(?P<a>.*?)\$\$(?:\s*\{#[^}]*\})?"
    r"|\\\[(?P<b>.*?)\\\]"
    r"|\\begin\{(?P<env>equation|align|gather|multline|eqnarray|displaymath|flalign|alignat)(?P<st>\*?)\}(?P<c>.*?)\\end\{(?P=env)(?P=st)\}",
    re.S)
POLA_SEBARIS = re.compile(r"(?<![\\$])\$(?!\$)(?P<a>[^$\n]+?)(?<!\\)\$(?!\$)|\\\((?P<b>.*?)\\\)", re.S)


def segmen(teks):
    """Daftar (jenis, isi, awal, akhir) berurutan: 'tampilan', 'sebaris'."""
    seg = []
    terpakai = [False] * (len(teks) + 1)
    for m in POLA_TAMPILAN.finditer(teks):
        isi = m.group("a") if m.group("a") is not None else (m.group("b") if m.group("b") is not None else m.group("c"))
        seg.append(("tampilan", isi, m.start(), m.end(), m.group("env") or ""))
        for k in range(m.start(), m.end()):
            terpakai[k] = True
    for m in POLA_SEBARIS.finditer(teks):
        if terpakai[m.start()]:
            continue
        isi = m.group("a") if m.group("a") is not None else m.group("b")
        seg.append(("sebaris", isi, m.start(), m.end(), ""))
    seg.sort(key=lambda s: s[2])
    return seg


def prosa_tanpa_rumus(teks, seg):
    """Teks dengan rumus diganti penanda sepanjang aslinya (posisi tetap)."""
    t = list(teks)
    for jenis, isi, a, b, _ in seg:
        ganti = ("§" if jenis == "sebaris" else "¶")
        for k in range(a, b):
            if t[k] != "\n":
                t[k] = ganti
    return "".join(t)


def baris_ke(teks, pos):
    return teks.count("\n", 0, pos) + 1


# ---------------------------------------------------------------- simbol
def _hapus_isi_perintah(s, nama):
    """Hapus \\nama{...} beserta isinya (kurung kurawal bersarang)."""
    out, i = [], 0
    pola = re.compile(r"\\(" + "|".join(nama) + r")\*?\s*\{")
    while True:
        m = pola.search(s, i)
        if not m:
            out.append(s[i:]); break
        out.append(s[i:m.start()])
        k, d = m.end(), 1
        while k < len(s) and d:
            d += {"{": 1, "}": -1}.get(s[k], 0); k += 1
        out.append(" ")
        i = k
    return "".join(out)


def simbol_dari(isi):
    """Kembalikan daftar kunci simbol dalam rumus, berurutan, tanpa duplikat."""
    s = _hapus_isi_perintah(isi, NONSYM)
    hasil = []
    # simbol berhias: \hat{\beta}, \hat\beta, \mathbf{X}, \bar{x}
    pola = re.compile(r"\\(" + "|".join(DECOR) + r")\s*(?:\{\s*(\\[A-Za-z]+|[A-Za-z])\s*\}|(\\[A-Za-z]+|[A-Za-z]))")
    def ganti(m):
        dasar = m.group(2) or m.group(3)
        if dasar.startswith("\\") and dasar[1:] not in GREEK:
            return " "
        hasil.append((m.start(), "\\" + m.group(1) + "{" + dasar + "}"))
        return " " * len(m.group(0))
    s2 = pola.sub(ganti, s)
    for m in re.finditer(r"\\([A-Za-z]+)", s2):
        if m.group(1) in GREEK:
            hasil.append((m.start(), "\\" + m.group(1)))
    s3 = re.sub(r"\\[A-Za-z]+", lambda m: " " * len(m.group(0)), s2)
    s3 = re.sub(r"[_^]\s*\{[^{}]*\}", lambda m: " " * len(m.group(0)), s3)   # subskrip/superskrip berkurung
    s3 = re.sub(r"[_^]\s*[A-Za-z0-9]", lambda m: " " * len(m.group(0)), s3)  # subskrip satu huruf
    for m in re.finditer(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", s3):
        hasil.append((m.start(), m.group(1)))
    hasil.sort()
    urut = []
    for _, k in hasil:
        if k not in urut:
            urut.append(k)
    return urut


def tampil(k):
    return k


# ---------------------------------------------------------------- pemeriksaan
class Laporan:
    def __init__(self):
        self.temuan = []

    def add(self, berkas, baris, kode, tingkat, apa, saran):
        self.temuan.append(dict(berkas=berkas, baris=baris, kode=kode, tingkat=tingkat, temuan=apa, saran=saran))


def kalimat_awal(prosa, pos):
    """True bila posisi pos adalah awal kalimat (awal paragraf/butir atau sesudah . ! ?)."""
    sebelum = prosa[:pos]
    j = len(sebelum) - 1
    while j >= 0 and sebelum[j] in " \t*_":
        j -= 1
    if j < 0:
        return True
    c = sebelum[j]
    if c == "\n":
        # awal baris: awal paragraf bila baris sebelumnya kosong, atau butir daftar
        return True
    if c in ".!?":
        # bukan singkatan pendek (mis. "dkk.", "hlm.")
        kata = re.search(r"(\S+)$", sebelum[:j + 1])
        if kata and re.match(r"^(dkk|hlm|No|Jl|Dr|dr|Prof|S\.\w+|M\.\w+|vs|cf|e\.g|i\.e|al|Fig|Eq)\.$", kata.group(1)):
            return False
        return True
    if c in "-+" and re.search(r"(^|\n)\s*[-+*]\s*$", sebelum):
        return True
    if re.search(r"(^|\n)\s*\d+[.)]\s*$", sebelum):
        return True
    return False


def periksa_berkas(path, bahasa, lap, abaikan, simbol_global, ext=None):
    mentah = open(path, encoding="utf-8").read()
    ext = ext or os.path.splitext(path)[1].lower()
    teks = buang_kode(mentah, ext)
    seg = segmen(teks)
    prosa = prosa_tanpa_rumus(teks, seg)
    nama = os.path.basename(path)

    # ---- R1, R2, R3, R8 (rumus sebaris)
    for idx, (jenis, isi, a, b, env) in enumerate(seg):
        if jenis != "sebaris":
            continue
        br = baris_ke(teks, a)
        baris_prosa = prosa[prosa.rfind("\n", 0, a) + 1:prosa.find("\n", a) if prosa.find("\n", a) >= 0 else len(prosa)]
        if baris_prosa.lstrip().startswith(("|", "#", ":", "<")):
            pass
        elif kalimat_awal(prosa, a):
            butir = bool(re.search(r"(^|\n)\s*([-+*]|\d+[.)])\s*$", prosa[:a]))
            lap.add(nama, br, "R1", "WARNING" if butir else "ERROR", "$" + isi.strip()[:30] + "$ di awal " + ("butir" if butir else "kalimat"),
                    "awali dengan kata benda: 'Parameter $\\beta$ ...' / 'The parameter ...'")
        # R2: rumus berikutnya dipisah hanya oleh koma/spasi dan salah satunya relasi
        if idx + 1 < len(seg) and seg[idx + 1][0] == "sebaris":
            antara = teks[b:seg[idx + 1][2]]
            if re.fullmatch(r"\s*,?\s*", antara):
                isi2 = seg[idx + 1][1]
                if re.search(r"[=<>]|\\(le|ge|leq|geq|ne|neq|in|approx|sim)\b", isi + isi2):
                    lap.add(nama, br, "R2", "WARNING", f"${isi.strip()[:20]}${antara}${isi2.strip()[:20]}$",
                            "pisahkan dengan kata: 'untuk $S_q$ dengan $q<p$' / 'where'")
        if re.search(LOGIKA, isi):
            lap.add(nama, br, "R3", "WARNING", "$" + isi.strip()[:40] + "$", "ganti lambang logika dengan kata (untuk setiap, ada, maka)")
        polos = re.sub(r"\\[A-Za-z]+|[{}\s]", "", isi)
        if len(polos) > 45 or re.search(r"\\(displaystyle|dfrac)\b", isi) or (re.search(r"\\(sum|prod|int)\b", isi) and "\\frac" in isi):
            lap.add(nama, br, "R8", "WARNING", "$" + isi.strip()[:50] + "$",
                    "rumus sebaris panjang/bertingkat → jadikan rumus tampilan (TeX memenggal sebaris di sembarang operator)")

    # ---- R4: di mana
    if bahasa == "id":
        for m in re.finditer(r"(?:¶[^\S\n]*\n?\s*|,\s*)di mana\b", prosa):
            lap.add(nama, baris_ke(teks, m.start()), "R4", "WARNING", "di mana", "pakai 'dengan' untuk keterangan simbol")

    # ---- R6: huruf berderet, label subskrip miring, bentuk campur
    bentuk = defaultdict(set)
    for jenis, isi, a, b, env in seg:
        br = baris_ke(teks, a)
        s = _hapus_isi_perintah(isi, ["text", "textrm", "textit", "textbf", "mathrm", "operatorname", "mbox", "label", "tag", "ref", "eqref", "mathsf", "mathtt"])
        s = re.sub(r"\\[A-Za-z]+", " ", s)
        for m in re.finditer(r"(?<![A-Za-z])([A-Za-z]{2,})(?![A-Za-z])", s):
            w = m.group(1)
            if w in KATA_FUNGSI:
                lap.add(nama, br, "R6", "WARNING", w, f"tulis tegak: \\operatorname{{{w}}} / \\mathrm{{{w}}} (atau \\{w} bila perintah baku)")
        for m in re.finditer(r"[_^]\s*\{\s*([A-Za-z]{2,})\s*\}", _hapus_isi_perintah(isi, ["text", "mathrm", "operatorname", "mbox", "textrm"])):
            if not re.fullmatch(r"(ij|ik|jk|kl|it|jt|nk|mn)", m.group(1)):
                lap.add(nama, br, "R6", "WARNING", "_{" + m.group(1) + "}", f"label subskrip tegak: _{{\\mathrm{{{m.group(1)}}}}}")
        if re.search(r"\\mathbb\{E\}", isi): bentuk["ekspektasi"].add("\\mathbb{E}")
        if re.search(r"\\(mathrm|operatorname)\{E\}", isi): bentuk["ekspektasi"].add("\\mathrm{E}")
        if re.search(r"(?<![\\A-Za-z{])E\s*(\[|\(|\\left|\\bigl|\\Big)", isi): bentuk["ekspektasi"].add("E (miring)")
        if re.search(r"\\mathrm\{d\}\s*[A-Za-z\\]", isi): bentuk["diferensial"].add("\\mathrm{d}")
        if re.search(r"\\int.*?(?:\\[,;!]|\s)d[A-Za-z]\b|\\frac\{d\}\{d", isi, flags=re.S): bentuk["diferensial"].add("d (miring)")
        if re.search(r"\\ln\b", isi): bentuk["logaritma natural"].add("\\ln")
        if re.search(r"\\log(?!_)\b", isi): bentuk["logaritma natural"].add("\\log")
        if re.search(r"\\Pr\b", isi): bentuk["peluang"].add("\\Pr")
        if re.search(r"\\mathbb\{P\}", isi): bentuk["peluang"].add("\\mathbb{P}")
        if re.search(r"(?<![\\A-Za-z{])P\s*(\(|\\left|\\bigl)", isi): bentuk["peluang"].add("P")
        if re.search(r"\\mathbf\{[a-z]\}", isi): bentuk["vektor tebal"].add("\\mathbf")
        if re.search(r"\\boldsymbol\{[a-z]\}", isi): bentuk["vektor tebal"].add("\\boldsymbol (Latin)")
    for k, v in bentuk.items():
        if len(v) > 1:
            lap.add(nama, 0, "R6", "WARNING", f"{k}: " + " / ".join(sorted(v)), "pilih satu bentuk untuk seluruh naskah")

    # ---- R7, R12 (rumus tampilan)
    konvensi = set()
    for jenis, isi, a, b, env in seg:
        if jenis != "tampilan":
            continue
        br = baris_ke(teks, a)
        baris = [x for x in re.split(r"\\\\(?:\[[^\]]*\])?", isi)]
        if len(baris) > 1:
            for k in range(len(baris) - 1):
                kiri = re.sub(r"\\(nonumber|notag)\b|\\label\{[^}]*\}|\s|&", "", baris[k])
                kanan = re.sub(r"^\s*&?\s*(\\quad|\\qquad|\\phantom\{[^}]*\}|\{\}|\\;|\\,|\\hspace\{[^}]*\})*\s*", "", baris[k + 1])
                akhir_op = re.search(r"(\+|-|=|\\times|\\cdot|<|>|\\le(q)?|\\ge(q)?|\\approx)$", kiri)
                awal_op = re.match(r"(\+|-|=|\\times|\\cdot|<|>|\\le(q)?|\\ge(q)?|\\approx)", kanan.strip())
                if akhir_op and awal_op:
                    konvensi.add("ulang")
                elif akhir_op:
                    konvensi.add("sesudah")
                    lap.add(nama, br + baris[k].count("\n"), "R7a", "WARNING", "…" + kiri[-25:] + " \\\\",
                            "penggal SEBELUM operator: operator mengawali baris lanjutan (Knuth/AMS)")
                elif awal_op:
                    konvensi.add("sebelum")
                # R7b: kedalaman kurung di titik penggal
                pre = "\\\\".join(baris[:k + 1])
                pre_b = re.sub(r"\\[{}]", lambda m: "(" if m.group(0) == "\\{" else ")", pre)
                pre_b = re.sub(r"\\(left|bigl|Bigl|biggl|Biggl)\s*[.([{|]|\\lbrace|\\langle", "(", pre_b)
                pre_b = re.sub(r"\\(right|bigr|Bigr|biggr|Biggr)\s*[.)\]}|]|\\rbrace|\\rangle", ")", pre_b)
                dalam = pre_b.count("(") + pre_b.count("[") - pre_b.count(")") - pre_b.count("]")
                if len(re.findall(r"\\left\b", pre)) != len(re.findall(r"\\right\b", pre)):
                    lap.add(nama, br, "R7b", "ERROR", "\\left … \\right terbelah antarbaris",
                            "pakai \\bigl( … \\bigr) berukuran tetap di setiap baris")
                elif dalam > 0:
                    lap.add(nama, br, "R7b", "WARNING", "penggal di dalam kurung (kedalaman %d)" % dalam,
                            "penggal di tingkat terluar, atau definisikan simbol bantu")
                if re.match(r"^\s*&\s*[+-]", baris[k + 1]):
                    lap.add(nama, br, "R7c", "WARNING", baris[k + 1].strip()[:30],
                            "beri {} dan jarak: '&\\quad {}+ c' agar + berspasi operator biner")
        else:
            polos = re.sub(r"\\(label|tag)\{[^}]*\}|\\[A-Za-z]+|[{}\s&]", "", isi)
            if len(polos) > 110:
                lap.add(nama, br, "R12", "WARNING", isi.strip()[:50] + "…",
                        f"rumus tampilan satu baris ±{len(polos)} lambang; berisiko melewati tepi → sederhanakan atau penggal")
        # R7d: baris kosong di sekitar rumus tampilan
        ses = teks[b:]
        ms = re.match(r"[ \t]*\n((?:[ \t]*\n)+)[ \t]*([^\n]*)", ses)
        if ms and ms.group(2).strip():
            nxt = ms.group(2).strip()
            if re.match(r"[a-z]", nxt) and not nxt.startswith(("\\noindent",)):
                lap.add(nama, baris_ke(teks, b), "R7d", "WARNING", "baris kosong sesudah rumus, lalu '" + nxt[:25] + "'",
                        "kalimat berlanjut: hapus baris kosong agar lanjutan tidak diindentasi")
        seb = teks[:a]
        mb = re.search(r"([^\n]*\S)[ \t]*\n(?:[ \t]*\n)+[ \t]*$", seb)
        if mb and re.search(r"[A-Za-z,]$", mb.group(1).rstrip()) and not mb.group(1).lstrip().startswith(("#", "\\", ":", "|")):
            lap.add(nama, br, "R7d", "WARNING", "…" + mb.group(1)[-25:] + " ↵↵ rumus",
                    "baris kosong sebelum rumus memutus kalimat; tempelkan rumus pada kalimat pengantar")
    if {"sebelum", "sesudah"} <= konvensi or ("ulang" in konvensi and len(konvensi) > 1):
        lap.add(nama, 0, "R7a", "WARNING", "konvensi pemenggalan bercampur: " + ", ".join(sorted(konvensi)),
                "satu konvensi untuk seluruh naskah (bawaan: sebelum operator, tanpa pengulangan)")

    # ---- R9: lambang di luar mode matematika
    for m in re.finditer(r"[α-ωΑ-Ω](?:[²³¹⁰-⁹]|_)?|(?<![\w/.\-])[a-zA-Z]_[a-zA-Z0-9]\b|(?<![\w$§.,/])[a-zA-Z]\s?[=<>≤≥]\s?-?\d", prosa):
        posb = prosa.rfind("\n", 0, m.start()) + 1
        if prosa[posb:posb + 1] in "|#" or "http" in prosa[max(0, m.start() - 30):m.start()]:
            continue
        lap.add(nama, baris_ke(teks, m.start()), "R9", "WARNING", m.group(0), "tulis dalam mode matematika: $...$")

    # ---- R5, R10: keterangan simbol
    kunci_def = DEF_ID_SESUDAH if bahasa == "id" else DEF_EN_SESUDAH
    kunci_seb = DEF_ID_SEBELUM if bahasa == "id" else DEF_EN_SEBELUM
    paragraf_batas = [m.start() for m in re.finditer(r"\n[ \t]*\n", prosa)] + [len(prosa)]

    def ujung_paragraf(pos, tambah=1):
        """Akhir paragraf ke-(tambah) mulai dari pos."""
        n = 0
        for p in paragraf_batas:
            if p > pos:
                n += 1
                if n >= tambah:
                    return p
        return len(prosa)

    for idx, (jenis, isi, a, b, env) in enumerate(seg):
        sim = simbol_dari(isi)
        # sisi kiri definisi (x = ..., x := ..., x \sim ...) dianggap mendefinisikan
        kiri = re.split(r"(?<![<>!:])=|:=|\\coloneqq|\\equiv|\\sim\b|\\overset", isi, maxsplit=1)
        didef_kiri = set(simbol_dari(kiri[0])) if len(kiri) > 1 and len(simbol_dari(kiri[0])) <= 2 else set()
        for s in sim:
            if s in abaikan or (len(s) == 1 and s in INDEKS):
                continue
            g = simbol_global.setdefault(s, dict(pertama=None, terdef=False, arti=[], berkas=nama))
            # cari definisi dalam jendela: kalimat yang memuat rumus ini, paragraf ini, dan paragraf berikutnya
            awal = max(0, prosa.rfind("\n\n", 0, a))
            akhir = ujung_paragraf(b, 2 if jenis == "tampilan" else 1)
            jendela_seg = [x for x in seg if awal <= x[2] < akhir]
            arti = None
            for x in jendela_seg:
                if s not in simbol_dari(x[1]) or x[0] != "sebaris":
                    continue
                tunggal = simbol_dari(x[1]) == [s] and not re.search(r"[=<>]|\\(le|ge|leq|geq|sim|in|approx)\b", x[1])
                if not tunggal:
                    continue
                ses = prosa[x[3]:x[3] + 90]
                seb = prosa[max(0, x[2] - 60):x[2]]
                m1 = re.match(r"\s*" + kunci_def + r"\s+(?P<arti>[^.,;§¶\n]{2,60})", ses)
                m2 = re.search(r"\b" + kunci_seb + r"\s*$", seb, flags=re.I)
                m4 = re.match(r"\s*\((?P<arti>[^)§]{3,50})\)", ses)
                kata = re.findall(r"[A-Za-z][\w-]*", seb)
                if m1:
                    arti = m1.group("arti").strip(); break
                if m4:
                    arti = m4.group("arti").strip(); break
                if m2:
                    mm = re.match(r"\s*(?:" + kunci_def + r"\s+)?(?P<arti>[^.,;§¶\n]{2,60})", ses)
                    if mm and re.match(r"\s*[a-z*_]", ses):
                        arti = mm.group("arti").strip(); break
                if kata and kata[-1].lower() not in STOP_SEBELUM and len(kata[-1]) >= 3 and re.search(r"[A-Za-z][\w-]*\s*$", seb):
                    dua = kata[-2:] if len(kata) >= 2 and kata[-2].lower() not in STOP_SEBELUM else kata[-1:]
                    arti = " ".join(dua); break
            if arti is None and s in didef_kiri:
                arti = "(didefinisikan oleh rumus)"
            if arti:
                g["terdef"] = True
                g["arti"].append((nama, baris_ke(teks, a), arti))
            if g["pertama"] is None:
                g["pertama"] = (nama, baris_ke(teks, a))
                g["terdef_dekat"] = bool(arti)
    return lap


def normal_arti(a):
    a = a.lower()
    a = re.sub(r"[*_`]|\(.*?\)", " ", a)
    w = [x for x in re.findall(r"[a-z\-]+", a) if x not in STOP_SEBELUM and x not in ("menyatakan", "adalah", "merupakan", "denotes", "is", "the")]
    return " ".join(w[:3])


def baca_notasi(path):
    s = set()
    for b in open(path, encoding="utf-8"):
        if b.startswith("|") and not b.startswith("|---"):
            sel = b.strip().strip("|").split("|")[0]
            for m in re.finditer(r"\$([^$]+)\$", sel):
                for k in simbol_dari(m.group(1)):
                    s.add(k)
    return s


def evaluasi_simbol(lap, simbol, notasi=None):
    """R5, R10, R11 dari kumpulan simbol semua berkas (dipanggil sesudah periksa_berkas)."""
    for s, g in simbol.items():
        if notasi is not None and s not in notasi:
            lap.add(g["pertama"][0], g["pertama"][1], "R11", "WARNING", s, "tambahkan ke daftar notasi")
            continue
        if notasi is not None:
            pass
        elif not g.get("terdef_dekat"):
            lanjut = " (keterangan baru ada di " + "; ".join(f"{x[0]}:{x[1]}" for x in g["arti"][:2]) + ")" if g["arti"] else ""
            lap.add(g["pertama"][0], g["pertama"][1], "R5", "WARNING", s,
                    "terangkan simbol pada kemunculan pertama: 'dengan $%s$ menyatakan …'%s" % (s, lanjut))
        himp = [(x, set(normal_arti(x[2]).split())) for x in g["arti"] if not x[2].startswith("(") and normal_arti(x[2])]
        beda = [(p, q) for i_, p in enumerate(himp) for q in himp[i_ + 1:] if not (p[1] & q[1])]
        if beda:
            p_, q_ = beda[0]
            lap.add(g["pertama"][0], g["pertama"][1], "R10", "WARNING", s,
                    f"diterangkan dengan arti berbeda: {p_[0][0]}:{p_[0][1]} '{p_[0][2][:30]}' | {q_[0][0]}:{q_[0][1]} '{q_[0][2][:30]}' — satu simbol, satu arti")


def periksa(berkas, bahasa="id", abaikan=(), notasi=None):
    """API untuk harness: kembalikan daftar temuan."""
    lap = Laporan(); simbol = OrderedDict()
    ab = set(abaikan) | BAWAAN_ABAIKAN
    for p in berkas:
        periksa_berkas(str(p), bahasa, lap, ab, simbol)
    evaluasi_simbol(lap, simbol, baca_notasi(notasi) if notasi else None)
    lap.temuan.sort(key=lambda t: (t["berkas"], t["baris"], t["kode"]))
    return lap.temuan, len(simbol)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("berkas", nargs="+")
    ap.add_argument("--bahasa", choices=["id", "en"], default="id")
    ap.add_argument("--notasi", help="berkas daftar notasi (tabel Markdown; kolom pertama berisi $simbol$)")
    ap.add_argument("--abaikan", default="", help="simbol yang tidak perlu diterangkan, dipisah koma (mis. 'e,\\pi,n')")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ketat", action="store_true", help="WARNING juga membuat kode keluar 1")
    a = ap.parse_args()
    abaikan = {x.strip() for x in a.abaikan.split(",") if x.strip()} | BAWAAN_ABAIKAN
    lap = Laporan()
    simbol = OrderedDict()
    for p in a.berkas:
        periksa_berkas(p, a.bahasa, lap, abaikan, simbol)
    evaluasi_simbol(lap, simbol, baca_notasi(a.notasi) if a.notasi else None)
    lap.temuan.sort(key=lambda t: (t["berkas"], t["baris"], t["kode"]))
    n_err = sum(t["tingkat"] == "ERROR" for t in lap.temuan)
    n_war = len(lap.temuan) - n_err
    if a.json:
        print(json.dumps(dict(error=n_err, warning=n_war, simbol=len(simbol), temuan=lap.temuan), ensure_ascii=False, indent=1))
    else:
        print(f"== cek_rumus.py — {len(a.berkas)} berkas, {len(simbol)} simbol ==")
        print(f"ERROR: {n_err}   WARNING: {n_war}")
        for t in lap.temuan:
            print(f"[{t['tingkat']:7s}] {t['berkas']}:{t['baris']:<5} {t['kode']:4s} \"{t['temuan']}\" → {t['saran']}")
    return 1 if (n_err or (a.ketat and n_war)) else 0


if __name__ == "__main__":
    sys.exit(main())
