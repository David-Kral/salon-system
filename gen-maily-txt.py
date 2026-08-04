"""Vygeneruje MAILY-195-242.txt — cisty text pro kopirovani do mailu.

Rozdily proti .md verzi:
  * kazdy odstavec je JEDEN dlouhy radek (zadne rucni zlomy), takze po
    vlozeni do mailu netreba prerovnavat odstavce,
  * zadny markdown, zadne ```,
  * "Komu:" vypusteno (adresata si uzivatel vyplni v mailovem klientovi).

Texty 1-11 zustavaji obsahove NEZMENENE (uzivatel je uz prosel) — meni se
jen zalamovani. Od 12 dal se pridava odstavec o rezervacnim formulari.

Znalosti o formulari jsou overene naziva na ukazka-2:
  01 ZVOLTE SLUZBU (Konsultace, Implantace, Estetika, Rekonstrukce,
  Endodoncie, Dentalni hygiena) -> 02 ZVOLTE TERMIN -> 03 VASE UDAJE
  (jmeno, prijmeni, e-mail, telefon); sekce "Rezervovat termin online".

Spusteni:  python gen-maily-txt.py
"""

import json
import re

# pooly beru z .md generatoru, aby se texty 1-11 nemohly rozejit
import importlib.util

spec = importlib.util.spec_from_file_location("mailgen", "gen-maily-195-242.py")
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)  # znovu zapise .md (idempotentni)

unwrap = lambda s: re.sub(r"\s+", " ", s.replace("\n", " ")).strip()

MAN = mg.MAN
BATCH = mg.BATCH
HAS_WEB = mg.HAS_WEB

# Od 12. mailu dal: odstavec o rezervacnim formulari (rotujici varianty)
FORM = [
    "Součástí by nebyl jen web. Systém umí i rezervační formulář postavený přesně na to, co potřebujete — pacient si vybere zákrok, pak termín a nakonec vyplní jméno, telefon a e-mail. V ukázce si to můžete rovnou proklikat.",

    "K webu patří i online objednávání. Formulář se dá nastavit přesně podle vaší ordinace: vy určíte, jaké zákroky se dají vybrat, jaké termíny nabízet a které údaje od pacienta chcete. V ukázce je to funkční, zkuste to.",

    "Web by nebyl jen vizitka. Je v něm rezervační formulář — pacient projde třemi kroky (zákrok, termín, kontaktní údaje) a objedná se sám, bez telefonu. Nabídku zákroků i políčka si nadefinujete podle sebe.",

    "Kromě samotného webu bych přidal i rezervační formulář na míru. Vyberete si, jaké zákroky v něm budou, jak dlouhé termíny nabízet a co má pacient vyplnit. Cílem je, aby vám během ošetření nezvonil telefon.",

    "Součástí systému je i online objednání termínu. Pacient klikne na zákrok, zvolí čas a nechá kontakt — vy dostanete poptávku se všemi údaji, které potřebujete. Seznam zákroků i povinná pole se dají upravit podle vaší praxe.",

    "K webu bych rovnou udělal i rezervační formulář se specifikací přesně podle vás — jaké zákroky, jaké časy, jaké údaje od pacienta. V ukázce je nasazený, takže si vyzkoušíte, jak by to pacient viděl.",

    "Nešlo by jen o web, ale i o objednávkový formulář. Pacient si projde výběr zákroku, pak termínu a na konec zadá kontakt. Co přesně se nabízí a co musí vyplnit, určíte vy — přizpůsobí se to tomu, jak ordinujete.",

    "Web umí i online rezervaci. Postavil bych ji přesně na vaše potřeby: nabídku zákroků, dostupné termíny i rozsah údajů, které od pacienta chcete. V ukázce si formulář můžete projít celý.",
]

lines = []
lines.append("MAILY — ordinace bez webu (46 leadu, radky 195-242 Google Sheetu)")
lines.append("=" * 70)
lines.append("")
lines.append("Kazdy odstavec je jeden radek — po vlozeni do mailu se odstavce")
lines.append("nerozsypou a netreba nic prerovnavat.")
lines.append("")
lines.append("Adresata si vyplnte v mailovem klientovi; v tabulce u techto radku")
lines.append("zadne e-maily nejsou.")
lines.append("")
lines.append("Predmety jsou zamerne KRATKE a BEZ jmena adresata — na mobilu")
lines.append("se zobrazi jen ~40 znaku, takze dlouhe '— MUDr. Jmeno Prijmeni'")
lines.append("se utne a sezere misto pro to podstatne. Jmeno je v prvni casti")
lines.append("tela, ktera se zobrazuje v nahledu schranky.")
lines.append("")
lines.append("Texty 1-11 jsou obsahove stejne jako drive (uz jste je prosel).")
lines.append("Od 12. dal je navic odstavec o rezervacnim formulari.")
lines.append("")
lines.append("Rezervacni formular je na ukazce skutecne nasazeny (overeno naziva):")
lines.append("  01 ZVOLTE SLUZBU  ->  02 ZVOLTE TERMIN  ->  03 VASE UDAJE")
lines.append("  zakroky: Konsultace / Implantace / Estetika / Rekonstrukce /")
lines.append("           Endodoncie / Dentalni hygiena")
lines.append("  udaje:   jmeno, prijmeni, e-mail, telefon")
lines.append("")
lines.append("POZOR — r. 195 (MUDr. Andelin Mrozovsky) a r. 204 (Dentalni hygiena")
lines.append("Havirov) vlastni web MAJI, maji proto text na redesign.")
lines.append("")

for i, e in enumerate(BATCH):
    name = e["nazev"]
    url = MAN[e["slug"]]["url"]
    redesign = e["slug"] in HAS_WEB

    subject = mg.subject_for(i, name)
    if redesign:
        opener = mg.OPENERS_REDESIGN[list(HAS_WEB).index(e["slug"]) % len(mg.OPENERS_REDESIGN)]
        opener = opener.format(web=HAS_WEB[e["slug"]])
    else:
        opener = mg.OPENERS[(i * 3) % len(mg.OPENERS)]
    middle = mg.MIDDLES[(i * 5) % len(mg.MIDDLES)].format(name=name)
    attach = mg.ATTACH[(i * 7) % len(mg.ATTACH)]
    closer = mg.CLOSERS[(i * 11) % len(mg.CLOSERS)]

    lines.append("")
    lines.append("=" * 70)
    lines.append(f"{i + 1}. {name}"
                 + ("   [WEB MA - text na redesign]" if redesign else ""))
    lines.append(f"   radek {e['radek']}")
    lines.append("=" * 70)
    lines.append("")
    # predmet na vlastnim radku bez predpony — da se oznacit cely radek
    lines.append("PREDMET ↓")
    lines.append(subject)
    lines.append("")
    lines.append("Dobrý den,")
    lines.append("")
    lines.append(unwrap(opener))
    lines.append("")
    lines.append(unwrap(middle))
    lines.append("")
    lines.append(url)
    lines.append("")
    if i >= 11:  # od 12. mailu dal
        lines.append(unwrap(FORM[(i * 3) % len(FORM)]))
        lines.append("")
    lines.append(unwrap(attach))
    lines.append("")
    lines.append(unwrap(closer))
    lines.append("")
    lines.append("S pozdravem,")
    lines.append("David Král")
    lines.append("777 122 178")
    lines.append("fitego.cz")
    lines.append("")

open("MAILY-195-242.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")

# ── kontroly ────────────────────────────────────────────────────────────
txt = open("MAILY-195-242.txt", encoding="utf-8").read()
md = open("MAILY-195-242.md", encoding="utf-8").read()

norm = lambda s: re.sub(r"\s+", " ", s).strip()

# 1) texty 1-11 se obsahove nesmi zmenit proti .md
md_bodies = re.findall(r"```\nKomu:\n(.*?)\n```", md, re.S)

# rozdeleni .txt na maily: hlavickovy radek je "<cislo>. <jmeno>" na zacatku radku
all_lines = txt.split("\n")
starts = [k for k, ln in enumerate(all_lines) if re.match(r"^\d+\. \S", ln)]
txt_bodies = []
for n, k in enumerate(starts):
    end = starts[n + 1] if n + 1 < len(starts) else len(all_lines)
    txt_bodies.append("\n".join(all_lines[k:end]))

problems = []
if len(txt_bodies) != len(BATCH):
    problems.append(f"rozdeleno {len(txt_bodies)} mailu, ocekavano {len(BATCH)}")
for k in range(11):
    md_core = norm(md_bodies[k].split("Dobrý den,", 1)[1].split("S pozdravem")[0])
    txt_core = norm(txt_bodies[k].split("Dobrý den,", 1)[1].split("S pozdravem")[0])
    if md_core != txt_core:
        problems.append(f"mail {k+1} se obsahove lisi od .md verze")

# 2) od 12 dal musi byt zminka o formulari, do 11 nesmi
for k, body in enumerate(txt_bodies, start=1):
    has = bool(re.search(r"rezerva|objednáv|objednán", body, re.I))
    if k >= 12 and not has:
        problems.append(f"mail {k}: chybi odstavec o formulari")
    if k <= 11 and has:
        problems.append(f"mail {k}: zminka o formulari tam nema byt")

# 3) kazdy mail musi mit predmet, odkaz, prilohu i podpis
for k, body in enumerate(txt_bodies, start=1):
    if "PREDMET ↓" not in body:
        problems.append(f"mail {k}: chybi predmet")
    if "https://david-kral.github.io/salon-system/ordinace/" not in body:
        problems.append(f"mail {k}: chybi odkaz")
    if "příloz" not in body and "Přikládám" not in body and "příloh" not in body:
        problems.append(f"mail {k}: chybi zminka o priloze")
    if "fitego.cz" not in body:
        problems.append(f"mail {k}: chybi podpis")

print(f"OK — MAILY-195-242.txt, {len(BATCH)} mailu")
print(f"   s odstavcem o formulari: {sum(1 for k in range(len(BATCH)) if k >= 11)}")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
