"""Vygeneruje MAILY-301-450.md a MAILY-301-450.txt pro davku 301-450.

Textove pooly (predmety, uvody, stredy, odstavec o rezervaci, priloha,
zavery) se beru z gen-maily-243-300.py, aby se ton obou davek nemohl
rozejit. Import ten skript znovu spusti — je idempotentni, jen prepise
MAILY-243-300.md/.txt stejnym obsahem.

Rozdily proti davce 243-300:
  * ctyri ordinace maji v tabulce e-mail -> je predvyplneny v "KOMU",
  * tri maji vlastni web -> text na redesign s konkretnim hackem,
  * HI.Dentistry ma jen facebookovou stranku -> vlastni uvod.

Spusteni:  python gen-maily-301-450.py
"""

import importlib.util
import json
import re

spec = importlib.util.spec_from_file_location("mg243", "gen-maily-243-300.py")
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
BATCH = json.load(open("davka-301-450.json", encoding="utf-8"))

# Web MAJI -> uhel je redesign, ne "nemate web". Hacek je vzdycky neco,
# co si vsimne i laik, ne "verbozni HTML".
HAS_WEB = {
    "tondrova-dent": ("drtondrova.cz",
                      "stránka je poskládaná v Elementoru a táhne s sebou spoustu\n"
                      "kódu navíc — na mobilu se to projeví na rychlosti načítání"),
    "dentry": ("dentry.cz",
               "v sekci Nabízíme se obsah opakuje dvakrát a v novinkách jsou\n"
               "články datované do budoucna — působí to nedodělaně"),
    "clinic-plus": ("clinic-plus.cz",
                    "navigace i tlačítka na objednání jsou v kódu zdvojená, což\n"
                    "stránku zbytečně zpomaluje, hlavně na mobilu"),
}

# Vlastni verze uvodu pro redesign — bez zaverecne vety o proklikavani se
# k objednani, ta sedi jen na DENT company z minule davky.
OPENER_REDESIGN = "našel jsem web vaší ordinace ({web}). Základ tam je, ale {problem}."

# HI.Dentistry ma jen FB stranku — to je konkretnejsi hacek nez obecne
# "nemate web", takze vlastni uvod.
CUSTOM_OPENER = {
    "hi-dentistry": "hledal jsem web HI.Dentistry a našel jsem jen vaši facebookovou\n"
                    "stránku. Ta je fajn pro stávající pacienty, ale kdo vás hledá poprvé,\n"
                    "nenajde ani ceník, ani možnost se objednat.",
}


def parts(i, e):
    name = e["nazev"]
    if e["slug"] in CUSTOM_OPENER:
        opener = CUSTOM_OPENER[e["slug"]]
    elif e["slug"] in HAS_WEB:
        web, problem = HAS_WEB[e["slug"]]
        opener = OPENER_REDESIGN.format(web=web, problem=problem)
    else:
        opener = mg.OPENERS[(i * 3) % len(mg.OPENERS)]
    return mg.subject_for(i, name), [
        opener,
        mg.MIDDLES[(i * 5) % len(mg.MIDDLES)].format(name=name),
        "__URL__",
        mg.FORM[(i * 3) % len(mg.FORM)],
        mg.ATTACH[(i * 7) % len(mg.ATTACH)],
        mg.CLOSERS[(i * 11) % len(mg.CLOSERS)],
    ]


# ── .md verze ───────────────────────────────────────────────────────────
md = ["# MAILY — dávka 301–450 (101 ordinací, šablona `ukazka-1`)", "",
      "Odpovídá řádkům 301–450 Google Sheetu. Vynecháno 49 řádků:", "",
      "- **ř. 414–447** — v tabulce jsou **duplicitní**, jde o stejné ordinace",
      "  jako na řádcích 380–413 (jen 410/411 mají prohozené pořadí). Kdyby se",
      "  neodfiltrovaly, dostala by jedna ordinace dva různé weby a dva maily.",
      "- 15 dalších řádků nemá žádné jméno (adresa, „Ord. praktického lékaře",
      "  stomatologa“, „Стоматология“…), je to laboratoř, neurologie nebo",
      "  lékařka sítě klinik EUC. Seznam vypíše `python gen-davka-301-450.py`.", "",
      "**Šablona:** všech 101 ukázek běží na `ukazka-1` (Dentaline styl).", "",
      "**Komu:** vyplněno u 4 ordinací, které e-mail v tabulce mají",
      "(Tondrová, HI.Dentistry, Dentry, CLINIC+). U zbytku si adresu doplníte.", "",
      "> **Web mají:** ř. 303 (drtondrova.cz), ř. 370 (dentry.cz) a ř. 371",
      "> (clinic-plus.cz) — mají text na redesign. Ř. 352 (HI.Dentistry) má jen",
      "> facebookovou stránku, taky vlastní úvod.", "", "---", ""]

for i, e in enumerate(BATCH):
    subject, blocks = parts(i, e)
    url = MAN[e["slug"]]["url"]
    redesign = e["slug"] in HAS_WEB
    md.append(f"## {i + 1}. {e['nazev']}")
    md.append("")
    md.append(f"*řádek {e['radek']} · šablona `{e['sablona']}`"
              + ("  · **web MÁ — text na redesign**" if redesign else "") + "*")
    md.append("")
    md.append("```")
    md.append(f"Komu: {e['email']}")
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

open("MAILY-301-450.md", "w", encoding="utf-8").write("\n".join(md) + "\n")

# ── .txt verze ──────────────────────────────────────────────────────────
txt = ["MAILY — ordinace bez webu (101 leadu, radky 301-450 Google Sheetu)",
       "=" * 70, "",
       "Navazuje na MAILY-243-300.txt — stejny ton, stejna struktura.", "",
       "Kazdy odstavec je jeden radek — po vlozeni do mailu se odstavce",
       "nerozsypou a netreba nic prerovnavat.", "",
       "POZOR NA TABULKU: radky 414-447 jsou duplicita radku 380-413",
       "(stejne ordinace znovu). Jsou vynechane, jinak by jedna ordinace",
       "dostala dva weby a dva maily. Dalsich 15 radku vynechano — bez",
       "jmena, laborator, neurologie, EUC.", "",
       "KOMU je predvyplnene u 4 ordinaci, ktere e-mail v tabulce maji;",
       "u zbytku si adresu dohledate.", "",
       "Predmety jsou zamerne KRATKE a BEZ jmena adresata — na mobilu",
       "se zobrazi jen ~40 znaku.", "",
       "SABLONA: vsech 101 ukazek bezi na ukazka-1 (Dentaline styl).", "",
       "Odstavec o rezervaci ma KAZDY mail. Formular na ukazce:",
       "  1) Novy pacient / Stavajici pacient",
       "  2) Preferovany termin (od-do) + preferovany cas",
       "  3) Jmeno a prijmeni, telefon, e-mail, poznamka", "",
       "POZOR — r. 303 (drtondrova.cz), r. 370 (dentry.cz) a r. 371",
       "(clinic-plus.cz) web MAJI -> text na redesign. R. 352 (HI.Dentistry)",
       "ma jen facebookovou stranku -> vlastni uvod.", ""]

for i, e in enumerate(BATCH):
    subject, blocks = parts(i, e)
    txt.append("")
    txt.append("=" * 70)
    txt.append(f"{i + 1}. {e['nazev']}"
               + ("   [WEB MA - text na redesign]" if e["slug"] in HAS_WEB else ""))
    txt.append(f"   radek {e['radek']}")
    txt.append("=" * 70)
    txt.append("")
    if e["email"]:
        txt.append("KOMU ↓")
        txt.append(e["email"])
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

open("MAILY-301-450.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")

# ── kontroly ────────────────────────────────────────────────────────────
body = open("MAILY-301-450.txt", encoding="utf-8").read()
lines = body.split("\n")
starts = [k for k, ln in enumerate(lines) if re.match(r"^\d+\. \S", ln)]
bodies = ["\n".join(lines[k:(starts[n + 1] if n + 1 < len(starts) else len(lines))])
          for n, k in enumerate(starts)]

problems = []
if len(bodies) != len(BATCH):
    problems.append(f"rozdeleno {len(bodies)} mailu, ocekavano {len(BATCH)}")
for k, b in enumerate(bodies, start=1):
    if "PREDMET ↓" not in b:
        problems.append(f"mail {k}: chybi predmet")
    if "https://david-kral.github.io/salon-system/ordinace/" not in b:
        problems.append(f"mail {k}: chybi odkaz")
    if not re.search(r"rezerva|objedn", b, re.I):
        problems.append(f"mail {k}: chybi odstavec o rezervaci")
    if "fitego.cz" not in b:
        problems.append(f"mail {k}: chybi podpis")
for slug in ("Dentaline", "DomiDent"):
    if any(slug in b for b in bodies):
        problems.append(f"v textu mailu zbyl '{slug}'")
# nikomu s webem nesmi prijit "nemate web"
for c, b in zip(BATCH, bodies):
    if c["slug"] in HAS_WEB and re.search(r"nena[šs]el|nema[jí]?.{0,10}web|chyb[ií]", b):
        problems.append(f"{c['slug']}: text tvrdi, ze web nema")

print(f"OK — MAILY-301-450.md + .txt, {len(BATCH)} mailu")
print(f"   s predvyplnenym KOMU: {sum(1 for c in BATCH if c['email'])}")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
