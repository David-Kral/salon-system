"""Davka B: 51 ordinaci se znamymi e-maily -> vlastni stranka na ukazka-1.

Na vyslovnou zadost se pouziva ukazka-1 (Dentaline) — svetle modra
s fotkou pres celou obrazovku.

Krome vytvoreni studii tento skript take:
  * hlasi duplicitni e-maily (nekolik ordinaci ma stejnou adresu),
  * hlasi kolize s uz existujicimi leady z predchozich davek,
  * hlasi podezrele adresy (napr. preklep v domene).

Spusteni:  python gen-davka-b.py
"""

import json
import os
import re
import unicodedata

SRC = "vstup-davka-b.txt"

# Rucni slugy tam, kde nazev sam nestaci nebo se opakuje na vic adresach
OVERRIDE_SLUG = {
    "Zubní praxe MŽ s.r.o. (Denisova, Jeseník)": "mz-jesenik",
    "Zubní praxe MŽ s.r.o. (Žulová)": "mz-zulova",
    "Břeňovi a Makris, s.r.o. (Březinova)": "brenovi-makris-brezinova",
    "Břeňovi a Makris, s.r.o. (Mikulášská)": "brenovi-makris-mikulasska",
    "NIKLdent s.r.o. (Oskava)": "nikldent-oskava",
    "NIKLdent s.r.o. (Libina)": "nikldent-libina",
    "EMIDENTAL s.r.o. (Šumperk, Pod Vodárnou)": "emidental-sumperk",
    "EMIDENTAL s.r.o. (Nový Malín)": "emidental-novy-malin",
    "MUDr. P. Slavíková-zubní praxe s.r.o.": "slavikova-praxe-dent",
    "MDDr. Lucie Václavková, DiS s.r.o.": "vaclavkova-dent",
    "MDDr. Zdeněk Jureček, DIS.": "jurecek-dent",
    "MDDr. Lenka Zdvyhalová Tvrdá": "zdvyhalova-tvrda-dent",
    "MUDr. Staněk Dent s.r.o.": "stanek-dent",
    "M - Smile s.r.o.": "m-smile",
    "denti belli s.r.o.": "denti-belli",
    "Jiří Szostek s.r.o.": "szostek-dent",
    "MUDr. Ivana Grygarová s.r.o.": "grygarova-dent",
    "MUDr. Milena Čamková s.r.o.": "camkova-dent",
    "MDDr. Vladimír Leškovský s.r.o.": "leskovsky-dent",
    # posledni slovo nazvu by dalo nicnerikajici slug (dent / dental / ms ...)
    "Dostal dent s.r.o.": "dostal-dent",
    "KRAUSOVÁ Dental s.r.o.": "krausova-dental",
    "SOFRONIESKI MS s.r.o.": "sofronieski-dent",
    "SV dent Šumperk s.r.o.": "sv-dent-sumperk",
    "DENTAL STUDIO H20 s.r.o.": "dental-studio-h20",
    "Aludentia s.r.o.": "aludentia",
    "JOSENIKA s.r.o.": "josenika-dent",
    "ECHTDENT s.r.o.": "echtdent",
    "SANODENT s.r.o.": "sanodent",
}

# Zobrazovane jmeno: pryc pravni forma a upresneni adresy v zavorce
LEGAL = r",?\s*\b(s\.?\s?r\.?\s?o\.?|sro\.?|a\.?s\.?)\b\.?"


def display_name(raw):
    s = re.sub(r"\s*\([^)]*\)\s*$", "", raw).strip()
    s = re.sub(LEGAL, "", s, flags=re.I).strip(" ,.")
    return s.strip(" -–")


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def auto_slug(name):
    s = deacc(name).lower()
    s = re.sub(r"\b(mudr|mddr|mvdr|phdr|dis)\b\.?", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    toks = [t for t in s.split() if len(t) > 1]
    base = toks[-1] if toks else "ordinace"
    return base if "dent" in base else base + "-dent"


PALETTE_1 = ["#2F6F8F", "#3C7A5E", "#8A5A3C", "#6B5B95", "#2E7D6B", "#8C4A52",
             "#455F8A", "#7C4F8C", "#3C6B7D", "#A2694E", "#4A7C59", "#7A4E6E"]

# E-mail je vzdy na konci radku; jmeno je vsechno pred nim. Nedelime na
# kazde pomlcce — nazev ji muze obsahovat ("M - Smile s.r.o.").
LINE = re.compile(r"^(?P<name>.*?)\s*[–—-]\s*(?P<email>[^\s@]+@[^\s@]+\.[^\s@]+)\s*$")

rows = []
for ln in open(SRC, encoding="utf-8"):
    ln = ln.strip()
    if not ln:
        continue
    m = LINE.match(ln)
    if not m:
        raise SystemExit(f"nerozparsovano: {ln!r}")
    name = m.group("name").strip()
    if len(name) < 3:
        raise SystemExit(f"podezrele kratke jmeno {name!r} z radku {ln!r}")
    rows.append((name, m.group("email").strip()))

# uklid po predchozim behu, aby po zmene slugu nezustaly osirele studia
if os.path.exists("davka-b.json"):
    for c in json.load(open("davka-b.json", encoding="utf-8")):
        p = os.path.join(c["sablona"], "studia", f"{c['slug']}.json")
        if os.path.exists(p):
            os.remove(p)

# slugy uz obsazene
taken = set()
existing_names = {}
for tpl in ("ukazka-1", "ukazka-2", "ukazka-3"):
    d = os.path.join(tpl, "studia")
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if f.endswith(".json"):
            taken.add(f[:-5])
            try:
                nm = json.load(open(os.path.join(d, f), encoding="utf-8")).get("nazev", "")
                existing_names.setdefault(deacc(nm).lower().strip(), f[:-5])
            except Exception:
                pass

created, collisions = [], []
for i, (raw, email) in enumerate(rows):
    name = display_name(raw)
    slug = OVERRIDE_SLUG.get(raw) or auto_slug(name)

    key = deacc(name).lower().strip()
    if key in existing_names:
        collisions.append((raw, existing_names[key]))

    b, k = slug, 2
    while slug in taken:
        slug = f"{b}-{k}"
        k += 1
    taken.add(slug)

    path = os.path.join("ukazka-1", "studia", f"{slug}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"nazev": name, "barva": PALETTE_1[i % len(PALETTE_1)]}, f, ensure_ascii=False)
        f.write("\n")
    created.append({"poradi": i + 1, "slug": slug, "nazev": name,
                    "puvodni": raw, "email": email, "sablona": "ukazka-1"})

with open("davka-b.json", "w", encoding="utf-8") as f:
    json.dump(created, f, ensure_ascii=False, indent=2)
    f.write("\n")

# ── hlaseni ────────────────────────────────────────────────────────────
print(f"Vytvoreno {len(created)} studii na ukazka-1\n")

from collections import Counter
dupes = {e: n for e, n in Counter(c["email"].lower() for c in created).items() if n > 1}
if dupes:
    print("DUPLICITNI E-MAILY (neposilat dvakrat na stejnou adresu):")
    for em, n in dupes.items():
        who = [c["nazev"] + (" " + re.search(r"\(([^)]*)\)", c["puvodni"]).group(1)
                             if re.search(r"\(([^)]*)\)", c["puvodni"]) else "")
               for c in created if c["email"].lower() == em]
        print(f"  {em}  ({n}x): {'; '.join(who)}")
    print()

if collisions:
    print("KOLIZE s uz existujicim leadem z predchozi davky:")
    for raw, slug in collisions:
        print(f"  {raw}  -> uz ma stranku jako '{slug}'")
    print()

SUSPECT = [r"cebtrum\.cz", r"^\d+x\d+@"]
sus = [c for c in created if any(re.search(p, c["email"], re.I) for p in SUSPECT)]
if sus:
    print("PODEZRELE ADRESY (zkontroluj pred odeslanim):")
    for c in sus:
        print(f"  {c['nazev']}: {c['email']}")
