"""MAILY-450-634.txt — vyrez davky "zbytek" jen pro radky 450-634.

Texty jsou presne ty same jako v MAILY-ZBYTEK.txt (bere se stejny index
do rotace variant), meni se jen rozsah a hlavicka: misto poradoveho cisla
je nad kazdym mailem primo CISLO RADKU v tabulce.

Spusteni:  python gen-maily-450-634.py
"""

import importlib.util
import json
import re

ROWS = (450, 634)

spec = importlib.util.spec_from_file_location("mg243", "gen-maily-243-300.py")
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
ALL = json.load(open("davka-zbytek.json", encoding="utf-8"))
SEL = [(i, e) for i, e in enumerate(ALL) if ROWS[0] <= e["radek"] <= ROWS[1]]

txt = [f"MAILY — radky {ROWS[0]}-{ROWS[1]} ({len(SEL)} ordinaci bez webu)",
       "=" * 70, "",
       "Nad kazdym mailem je CISLO RADKU z tabulky (ne poradove cislo).", "",
       "Kazdy odstavec je jeden radek — po vlozeni do mailu se nic nerozsype.",
       "Adresata si vyplnte v mailovem klientovi; v tabulce u techto radku",
       "zadne e-maily nejsou.", "",
       "Vsechny ukazky bezi na ukazka-1 (Dentaline styl), rezervacni",
       "formular ma kazdy mail.", "",
       "Texty jsou totozne s MAILY-ZBYTEK.txt — tohle je jen vyrez.", ""]

for i, e in SEL:
    txt.append("")
    txt.append("=" * 70)
    txt.append(f"RADEK {e['radek']} — {e['nazev']}")
    txt.append("=" * 70)
    txt.append("")
    txt.append("PREDMET ↓")
    txt.append(mg.subject_for(i, e["nazev"]))
    txt.append("")
    txt.append("Dobrý den,")
    txt.append("")
    for block in (mg.OPENERS[(i * 3) % len(mg.OPENERS)],
                  mg.MIDDLES[(i * 5) % len(mg.MIDDLES)].format(name=e["nazev"]),
                  "__URL__",
                  mg.FORM[(i * 3) % len(mg.FORM)],
                  mg.ATTACH[(i * 7) % len(mg.ATTACH)],
                  mg.CLOSERS[(i * 11) % len(mg.CLOSERS)]):
        txt.append(MAN[e["slug"]]["url"] if block == "__URL__" else mg.unwrap(block))
        txt.append("")
    txt.extend(mg.SIGNATURE)
    txt.append("")

open("MAILY-450-634.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")

# kontrola: kazdy mail ma cislo radku, odkaz, rezervaci i podpis; texty
# musi sedet na MAILY-ZBYTEK.txt
zbytek = open("MAILY-ZBYTEK.txt", encoding="utf-8").read()
body = open("MAILY-450-634.txt", encoding="utf-8").read()
problems = []
lines = body.split("\n")
starts = [k for k, ln in enumerate(lines) if ln.startswith("RADEK ")]
bloky = {lines[k].split()[1]: "\n".join(
    lines[k:(starts[j + 1] if j + 1 < len(starts) else len(lines))])
    for j, k in enumerate(starts)}
if len(bloky) != len(SEL):
    problems.append(f"rozdeleno {len(bloky)} mailu, ocekavano {len(SEL)}")
for i, e in SEL:
    blok = bloky.get(str(e["radek"]), "")
    if MAN[e["slug"]]["url"] not in blok:
        problems.append(f"r.{e['radek']}: chybi odkaz")
    if not re.search(r"rezerva|objedn", blok, re.I):
        problems.append(f"r.{e['radek']}: chybi rezervace")
    if "fitego.cz" not in blok:
        problems.append(f"r.{e['radek']}: chybi podpis")
    veta = blok.split("Dobrý den,\n\n")[1].split("\n")[0]
    if veta not in zbytek:
        problems.append(f"r.{e['radek']}: text nesedi na MAILY-ZBYTEK.txt")

print(f"OK — MAILY-450-634.txt, {len(SEL)} mailu (radky {SEL[0][1]['radek']}"
      f"-{SEL[-1][1]['radek']})")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
