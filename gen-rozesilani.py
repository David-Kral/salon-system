"""Vygeneruje ROZESILANI.txt — prehledovy seznam ke kazdemu mailu:
cislo, soubor k otevreni, adresat a predmet. Bez tela zpravy.

Slouzi jako odesilaci checklist: mas na jednom miste, komu to jde, s jakym
predmetem a ktery HTML soubor otevrit.

Cte se z hotovych .txt (KOMU / PREDMET), takze se to nemuze rozejit
s tim, co je v mailech.

Spusteni:  python gen-rozesilani.py
"""

import os
import re

SUSPECT = {
    "222x222@seznam.cz": "over, ze je spravna",
}


def parse(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    starts = [i for i, ln in enumerate(lines) if re.match(r"^\d+\. \S", ln)]
    out = []
    for n, s in enumerate(starts):
        e = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[s:e]
        num, rest = block[0].split(".", 1)
        flags = ""
        m = re.search(r"\s{2,}\[(.+?)\]\s*$", rest)
        if m:
            flags, rest = m.group(1), rest[: m.start()]
        rec = {
            "num": int(num), "nazev": rest.strip(), "flags": flags,
            "covered": any("NEPOSILAT" in x for x in block[:5]),
            "komu": None, "predmet": None, "slug": None,
        }
        for i, ln in enumerate(block):
            t = ln.strip()
            if t == "KOMU ↓":
                rec["komu"] = block[i + 1].strip()
            elif t == "PREDMET ↓":
                rec["predmet"] = block[i + 1].strip()
            elif t.startswith("http") and not rec["slug"]:
                mm = re.search(r"/ordinace/([a-z0-9-]+)/", t)
                if mm:
                    rec["slug"] = mm.group(1)
        out.append(rec)
    return out


def files_in(folder):
    if not os.path.isdir(folder):
        return {}
    idx = {}
    for f in sorted(os.listdir(folder)):
        m = re.match(r"^(\d+)-", f)
        if m:
            idx[int(m.group(1))] = f
    return idx


A = parse("MAILY-195-242.txt")
B = parse("MAILY-DAVKA-B.txt")
fa = files_in(os.path.join("maily-html", "davka-a"))
fb = files_in(os.path.join("maily-html", "davka-b"))

L = []
L.append("ROZESILACI SEZNAM — komu a s jakym predmetem")
L.append("=" * 100)
L.append("")
L.append("Prehled ke kazdemu mailu. Telo zpravy tady neni — to je v HTML")
L.append("souborech (maily-html/davka-a, maily-html/davka-b).")
L.append("")
L.append("Postup u jednoho mailu:")
L.append("  1) otevrit HTML soubor z posledniho sloupce, Ctrl+A, Ctrl+C")
L.append("  2) v Roundcube vlozit do tela (Ctrl+V)")
L.append("  3) zkopirovat KOMU a PREDMET z tohoto seznamu")
L.append("  4) prilozit screenshot hero sekce")
L.append("")

# ── davka B ────────────────────────────────────────────────────────────
send_b = [r for r in B if not r["covered"]]
L.append("=" * 100)
L.append(f"DAVKA B — sablona Dentaline, {len(send_b)} mailu k odeslani")
L.append("=" * 100)
L.append("")
L.append(f"{'#':>3}  {'KOMU':32}  {'PREDMET':46}  SOUBOR")
L.append(f"{'-'*3}  {'-'*32}  {'-'*46}  {'-'*30}")
for r in B:
    if r["covered"]:
        continue
    f = fb.get(r["num"], "")
    L.append(f"{r['num']:>3}  {r['komu'] or '':32}  {r['predmet'] or '':46}  {f}")
    if (r["komu"] or "").lower() in SUSPECT:
        L.append(f"     !! POZOR: {SUSPECT[r['komu'].lower()]}")

skipped = [r for r in B if r["covered"]]
if skipped:
    L.append("")
    L.append("NEPOSILAT (stejna adresa jako jiny mail — pobocka je v nem zminena):")
    for r in skipped:
        L.append(f"  {r['num']:>3}  {r['nazev']}")

L.append("")
L.append("")

# ── davka A ────────────────────────────────────────────────────────────
L.append("=" * 100)
L.append(f"DAVKA A — ordinace bez webu (radky 195-242), {len(A)} mailu")
L.append("=" * 100)
L.append("")
L.append("U teto davky NEJSOU e-mailove adresy — v tabulce u tech radku zadne")
L.append("nebyly. Adresata si dohledas a vyplnis v Roundcube.")
L.append("")
L.append(f"{'#':>3}  {'ORDINACE':42}  {'PREDMET':46}  SOUBOR")
L.append(f"{'-'*3}  {'-'*42}  {'-'*46}  {'-'*30}")
for r in A:
    f = fa.get(r["num"], "")
    nazev = r["nazev"][:42]
    L.append(f"{r['num']:>3}  {nazev:42}  {r['predmet'] or '':46}  {f}")
    if r["flags"]:
        L.append(f"     ({r['flags']})")

L.append("")
L.append("=" * 100)
L.append(f"CELKEM: {len(send_b)} mailu s adresou (davka B) + {len(A)} bez adresy (davka A)"
         f" = {len(send_b) + len(A)}")
L.append("=" * 100)

open("ROZESILANI.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")

# ── kontroly ───────────────────────────────────────────────────────────
problems = []
for r in send_b:
    if not r["komu"]:
        problems.append(f"B#{r['num']}: chybi adresat")
    if not r["predmet"]:
        problems.append(f"B#{r['num']}: chybi predmet")
    if r["num"] not in fb:
        problems.append(f"B#{r['num']}: chybi HTML soubor")
for r in A:
    if not r["predmet"]:
        problems.append(f"A#{r['num']}: chybi predmet")
    if r["num"] not in fa:
        problems.append(f"A#{r['num']}: chybi HTML soubor")

print(f"ROZESILANI.txt — davka B: {len(send_b)} mailu, davka A: {len(A)} mailu")
print(f"   preskoceno v B (duplicitni adresa): {len(skipped)}")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
