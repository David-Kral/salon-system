"""Vygeneruje MAILY-ZBYTEK.md a MAILY-ZBYTEK.txt — vsechny zbyle leady
(sloupec B prazdny, rating 7, radek nebyl v zadne predchozi davce).

Textove pooly se beru z gen-maily-243-300.py, aby ton sedel s predchozimi
davkami. Vsechny tyhle ordinace web NEMAJI a v tabulce u nich neni e-mail,
takze se pouzivaji jen "nemate web" uvody a KOMU zustava prazdne.

Spusteni:  python gen-maily-zbytek.py
"""

import importlib.util
import json
import re

spec = importlib.util.spec_from_file_location("mg243", "gen-maily-243-300.py")
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
BATCH = json.load(open("davka-zbytek.json", encoding="utf-8"))


def parts(i, e):
    return mg.subject_for(i, e["nazev"]), [
        mg.OPENERS[(i * 3) % len(mg.OPENERS)],
        mg.MIDDLES[(i * 5) % len(mg.MIDDLES)].format(name=e["nazev"]),
        "__URL__",
        mg.FORM[(i * 3) % len(mg.FORM)],
        mg.ATTACH[(i * 7) % len(mg.ATTACH)],
        mg.CLOSERS[(i * 11) % len(mg.CLOSERS)],
    ]


HEAD_MD = [
    f"# MAILY — zbytek ({len(BATCH)} ordinací, šablona `ukazka-1`)", "",
    "Všechny zbylé řádky Google Sheetu, které **nemají web** (sloupec B je",
    "prázdný), mají **rating 7** a **nebyly v žádné předchozí dávce**.",
    "Jsou to řádky **56–194** a **451–634** — dávky 195–242, 243–300 a",
    "301–450 už jsou hotové zvlášť.", "",
    "U každého mailu je číslo řádku v tabulce.", "",
    "**Šablona:** všechny ukázky běží na `ukazka-1` (Dentaline styl).", "",
    "**Komu:** je prázdné — u těchto řádků v tabulce žádné e-maily nejsou.", "",
    "Vynechané řádky (bez jména, laboratoře, zubní technici, pohotovost,",
    "komora, nebo už ukázku mají) jsou vypsané v `davka-zbytek-vynechane.txt`.", "",
    "---", "",
]

HEAD_TXT = [
    f"MAILY — zbytek ({len(BATCH)} leadu bez webu, rating 7)",
    "=" * 70, "",
    "Vsechny zbyle radky tabulky bez webu s ratingem 7, ktere jeste nebyly",
    "v zadne davce — radky 56-194 a 451-634. Davky 195-242, 243-300",
    "a 301-450 jsou hotove zvlast.", "",
    "U kazdeho mailu je cislo radku v tabulce.", "",
    "Kazdy odstavec je jeden radek — po vlozeni do mailu se odstavce",
    "nerozsypou a netreba nic prerovnavat.", "",
    "Adresata si vyplnte v mailovem klientovi; v tabulce u techto radku",
    "zadne e-maily nejsou.", "",
    "SABLONA: vsechny ukazky bezi na ukazka-1 (Dentaline styl).", "",
    "Odstavec o rezervaci ma KAZDY mail. Formular na ukazce:",
    "  1) Novy pacient / Stavajici pacient",
    "  2) Preferovany termin (od-do) + preferovany cas",
    "  3) Jmeno a prijmeni, telefon, e-mail, poznamka", "",
    "Vynechane radky (bez jmena, laboratore, technici, pohotovost, komora,",
    "nebo uz ukazku maji) jsou v davka-zbytek-vynechane.txt.", "",
]

md = list(HEAD_MD)
for i, e in enumerate(BATCH):
    subject, blocks = parts(i, e)
    url = MAN[e["slug"]]["url"]
    md.append(f"## {i + 1}. {e['nazev']}")
    md.append("")
    md.append(f"*řádek {e['radek']} · šablona `{e['sablona']}`*")
    md.append("")
    md.append("```")
    md.append("Komu:")
    md.append(f"Předmět: {subject}")
    md.append("")
    md.append("Dobrý den,")
    md.append("")
    for block in blocks:
        md.append(url if block == "__URL__" else block)
        md.append("")
    md.extend(mg.SIGNATURE)
    md.append("```")
    md.append("")

open("MAILY-ZBYTEK.md", "w", encoding="utf-8").write("\n".join(md) + "\n")

txt = list(HEAD_TXT)
for i, e in enumerate(BATCH):
    subject, blocks = parts(i, e)
    txt.append("")
    txt.append("=" * 70)
    txt.append(f"{i + 1}. {e['nazev']}")
    txt.append(f"   radek {e['radek']}")
    txt.append("=" * 70)
    txt.append("")
    txt.append("PREDMET ↓")
    txt.append(subject)
    txt.append("")
    txt.append("Dobrý den,")
    txt.append("")
    for block in blocks:
        txt.append(MAN[e["slug"]]["url"] if block == "__URL__" else mg.unwrap(block))
        txt.append("")
    txt.extend(mg.SIGNATURE)
    txt.append("")

open("MAILY-ZBYTEK.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")

# ── kontroly ────────────────────────────────────────────────────────────
body = open("MAILY-ZBYTEK.txt", encoding="utf-8").read()
lines = body.split("\n")
starts = [k for k, ln in enumerate(lines) if re.match(r"^\d+\. \S", ln)]
bodies = ["\n".join(lines[k:(starts[n + 1] if n + 1 < len(starts) else len(lines))])
          for n, k in enumerate(starts)]

problems = []
if len(bodies) != len(BATCH):
    problems.append(f"rozdeleno {len(bodies)} mailu, ocekavano {len(BATCH)}")
for k, b in enumerate(bodies, start=1):
    for what, ok in (("predmet", "PREDMET ↓" in b),
                     ("radek", re.search(r"^   radek \d+$", b, re.M)),
                     ("odkaz", "https://david-kral.github.io/salon-system/ordinace/" in b),
                     ("rezervace", re.search(r"rezerva|objedn", b, re.I)),
                     ("podpis", "fitego.cz" in b)):
        if not ok:
            problems.append(f"mail {k}: chybi {what}")
for slug in ("Dentaline", "DomiDent"):
    if any(slug in b for b in bodies):
        problems.append(f"v textu mailu zbyl '{slug}'")

print(f"OK — MAILY-ZBYTEK.md + .txt, {len(BATCH)} mailu")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
