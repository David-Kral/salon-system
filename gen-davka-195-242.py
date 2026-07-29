"""Z radku 195-242 Google Sheetu vyrobi studia pro ukazka-2 / ukazka-3.

Radek 194 je poznamka, ne ordinace.
Radky 207 a 219 ("Odborny lekar stomatolog", "Odborny lekar stomatologie,
ortodoncie") neobsahuji zadne jmeno — web pojmenovany takhle nema smysl,
takze jsou vynechane.

Vsech 48 radku ma v tabulce POUZE jmeno + rating 7. Zadny web, zadny
e-mail, zadne mesto.

ukazka-1 se zamerne NEPOUZIVA (svetle modry styl s fotkou pres celou
obrazovku) — pouzivame jen ukazka-2 (tmava premiova) a ukazka-3 (tepla
kremova s cenikem a rezervaci).

Spusteni:  python gen-davka-195-242.py
"""

import csv
import json
import os
import re
import unicodedata

ROWS = (195, 242)
SKIP = {194, 207, 219}  # poznamka + dva radky bez jmena

# Rucni opravy tam, kde heuristika na registrovy tvar nestaci
# radek: (zobrazovane jmeno, slug)
OVERRIDE = {
    203: ("MUDr. Vladimír Komár", "komar-dent"),
    206: ("Ta Denta", "ta-denta"),
    214: ("Zubní praxe MŽ", "mz-dent"),
    218: ("Slavík Dental", "slavik-dental"),
    220: ("MUDr. Vladimíra Novotná — ortodoncie", "novotna-ortodoncie"),
    221: ("Běla Kutalová — Dental", "kutalova-dent"),
    228: ("Praxident DK", "praxident-dk"),
    230: ("Tradent Stom", "tradent-stom"),
    235: ("Parosan Medical", "parosan-medical"),
    237: ("JaRo Dent", "jaro-dent"),
    238: ("Gem Dent", "gem-dent"),
    240: ("MUDr. Helena Lošťáková", "lostakova-dent"),
}

TITLES = {"mudr": "MUDr.", "mddr": "MDDr.", "mvdr": "MVDr.", "phdr": "PhDr.", "dis": "Dis."}
LEGAL = r",?\s*\b(s\.?\s?r\.?\s?o\.?|sro\.?|a\.?s\.?)\b\.?"
TAIL_JUNK = [
    r"\s*[-–—]\s*soukrom[áa]\s+ambulance$", r",?\s*zubn[ií]\s+l[ée]ka[řr]k?a?$",
    r",\s*ordinace\s+praktick[éeh]+o?\s+zubn[ií]ho\s+l[ée]ka[řr]e$",
]
LEAD_GENERIC = [r"^zubn[ií]\s+l[ée]ka[řr]k?a?\b", r"^zubn[ií]\s+ordinace\b", r"^ordinace\b"]
GENERIC_TOK = {"zubni", "lekar", "lekarka", "ordinace", "ambulance", "dentalni",
               "hygiena", "stomatolog", "praxe", "praktickeho", "zubniho", "lekare"}


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def normalize_name(raw):
    s = re.sub(LEGAL, "", raw.strip(), flags=re.I).strip(" ,.")
    for pat in TAIL_JUNK:
        s = re.sub(pat, "", s, flags=re.I).strip(" ,")
    s = re.sub(r"\b(MUDr|MDDr|MVDr|PhDr)\.(?=\S)", r"\1. ", s, flags=re.I)

    toks = [t for t in re.split(r"\s+", s) if t]
    title, title_idx, kept = None, None, []
    for i, t in enumerate(toks):
        if deacc(t).lower().strip(".,") in TITLES:
            if title is None:
                title, title_idx = TITLES[deacc(t).lower().strip(".,")], i
            continue
        kept.append(t)

    if title is None:
        out = s
        for pat in LEAD_GENERIC:
            out = re.sub(pat, "", out, flags=re.I).strip(" ,")
        return (out or s).strip(" ,."), None

    name_toks = [t for t in kept if deacc(t).lower().strip(".,") not in GENERIC_TOK]
    name_toks = [t for t in name_toks if re.search(r"[A-Za-zÁ-Žá-ž]", t)]
    if not name_toks:
        return s.strip(" ,."), None

    # titul na konci => tabulka ma "Prijmeni Jmeno" -> obratit
    if title_idx is not None and title_idx >= len(toks) - 2 and len(name_toks) >= 2:
        name_toks = [name_toks[1], name_toks[0]] + name_toks[2:]

    name_toks = name_toks[:2]
    surname = name_toks[-1] if len(name_toks) >= 2 else name_toks[0]
    return f"{title} " + " ".join(name_toks), surname


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", deacc(s).lower())).strip("-")


PALETTE_2 = ["#34618F", "#7C4F8C", "#2E6F6B", "#8C4A52", "#3F5E8C", "#6B5B95",
             "#2F6E5A", "#8A5A3C", "#455F8A", "#7A4E6E", "#3C6B7D", "#5D5A8C"]
PALETTE_3 = ["#B07D48", "#A2694E", "#8F7A46", "#9C6B52", "#7E8552", "#A8794F",
             "#8B6F4E", "#B08050", "#96704A", "#A67C55", "#7F6B4A", "#AD8455"]

rows = list(csv.reader(open("sheet2.csv", encoding="utf-8", newline="")))

if os.path.exists("davka-195-242.json"):
    for c in json.load(open("davka-195-242.json", encoding="utf-8")):
        p = os.path.join(c["sablona"], "studia", f"{c['slug']}.json")
        if os.path.exists(p):
            os.remove(p)

taken = set()
for tpl in ("ukazka-1", "ukazka-2", "ukazka-3"):
    d = os.path.join(tpl, "studia")
    if os.path.isdir(d):
        taken |= {f[:-5] for f in os.listdir(d) if f.endswith(".json")}

created, skipped = [], []
i2 = i3 = 0
for n in range(ROWS[0], ROWS[1] + 1):
    raw = rows[n - 1][0].strip()
    if n in SKIP or not raw:
        skipped.append({"radek": n, "puvodni": raw, "duvod": "bez identifikovatelneho jmena"})
        continue

    if n in OVERRIDE:
        name, slug = OVERRIDE[n]
    else:
        name, surname = normalize_name(raw)
        slug = slugify(surname) + "-dent" if surname else slugify(name)
        if not surname and "dent" not in slug:
            slug += "-dent"

    b, k = slug, 2
    while slug in taken:
        slug = f"{b.replace('-dent', '')}-{k}-dent" if b.endswith("-dent") else f"{b}-{k}"
        k += 1
    taken.add(slug)

    tpl = "ukazka-2" if len(created) % 2 == 0 else "ukazka-3"
    if tpl == "ukazka-2":
        color = PALETTE_2[i2 % len(PALETTE_2)]; i2 += 1
    else:
        color = PALETTE_3[i3 % len(PALETTE_3)]; i3 += 1

    with open(os.path.join(tpl, "studia", f"{slug}.json"), "w", encoding="utf-8") as f:
        json.dump({"nazev": name, "barva": color}, f, ensure_ascii=False)
        f.write("\n")
    created.append({"radek": n, "slug": slug, "nazev": name, "puvodni": raw,
                    "sablona": tpl, "barva": color})

with open("davka-195-242.json", "w", encoding="utf-8") as f:
    json.dump(created, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Vytvoreno {len(created)} studii "
      f"({sum(1 for c in created if c['sablona']=='ukazka-2')}x ukazka-2, "
      f"{sum(1 for c in created if c['sablona']=='ukazka-3')}x ukazka-3)")
print(f"Vynechano {len(skipped)}: " + "; ".join(f"r.{s['radek']} {s['puvodni']}" for s in skipped))
print()
for c in created:
    print(f"  {c['radek']}  {c['sablona']}  {c['slug']:22} {c['nazev']}")
