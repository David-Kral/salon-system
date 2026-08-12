"""Studia pro leady, ktere UZ NEJAKY WEB MAJI (sloupec B vyplneny + rating).

Predchozi davky resily jen ordinace uplne bez webu. Tady jsou zbyle radky,
ktere web maji a tabulka je ohodnotila — vcetne analyzy slabiny a casto
i e-mailu. Deli se na dve skupiny:

  * "katalog"  — odkaz vede jen na katalogovy profil nebo Facebook
                 (katalog-stomatologu.cz, znamylekar.cz, zlatestranky.cz,
                 oteviracka.cz, firmy.cz, facebook.com) -> vlastni web
                 fakticky nemaji,
  * "web"      — vlastni domena -> mail se pise na redesign.

Vynechavaji se neordinace (gynekologie, veterina, lekarna, poliklinika…),
radky bez pouzitelneho jmena a ty, co uz ukazku maji.

Spusteni:
    python gen-davka-web.py --dry
    python gen-davka-web.py
"""

import csv
import json
import os
import re
import sys

from jmena import deacc, is_generic, normalize_name, slugify

TEMPLATE = "ukazka-1"
DRY = "--dry" in sys.argv

KATALOG = re.compile(
    r"katalog-stomatologu|znamylekar|zlatestranky|oteviracka|firmy\.cz|facebook\.com"
    r"|strakonak\.cz|najisto|edb\.cz|zivefirmy|detail\.cz|m\.facebook", re.I)

NOT_DENTIST = re.compile(
    r"gynekolog|veterin|l[ée]k[áa]rna|urolog|\bORL\b|alerg|rehabilitac|nemocnice"
    r"|poliklinik|v[ěe]deckotechnick|transfuz|o[čc]n[ií]|derma|ko[žz]n|neurolog"
    r"|pediatr|chirurg|interna|psychiatr|psycholog|ortoped|kardiolog|diabetolog"
    r"|plicn|imunolog|laborato[řr]|l[ée]ka[řr]sk[ýy]\s+d[ůu]m|zdravotn[ií]\s+st[řr]edisko"
    r"|moje\s+ambulance|euc\b|medicom|premium\s+clinic|dr\.?\s*max", re.I)

DENTAL_HINT = re.compile(r"zub|dent|stomat|ortodon|hygien|implant|smile|usmev|úsměv", re.I)

# Rucni opravy jmen (nazev firmy smichany se jmenem lekare apod.)
OVERRIDE = {
    20: ("Dr.Dent", "dr-dent"),
    25: ("MUDr. Světlana Ulman", "ulman-dent"),
    26: ("MUDr. František Cibulka", "cibulka-dent"),
    34: ("Stomatologická ordinace Holice", "stomaholice"),
    35: ("Zubní ordinace Švec", "svec-ordinace-dent"),
    40: ("Dentista Zlín", "dentista-zlin"),
    43: ("MDDr. Jan Lapiš", "lapis-dent"),
    49: ("MUDr. Pavel Vachulka", "vachulka-dent"),
    52: ("MUDr. Radoslav Lacina", "lacina-dent"),
    57: ("MDDr. Vít Pernička", "pernicka-dent"),
    639: ("PD Dent", "pd-dent"),
    643: ("MDDr. Tereza Perničková", "pernickova-dent"),
    653: ("MDDr. Zdeňka Filáková", "filakova-dent"),
    656: ("Daniela Raková, DiS.", "rakova-dent"),
    661: ("ORTOPEK — MUDr. Honzírková", "ortopek-dent"),
    663: ("Ordinace Gregora", "gregora-dent"),
    676: ("MUDr. Tereza Žáková", "zakova-dent"),
    688: ("Stomatologie Matas", "matas-dent"),
    710: ("Ordinace Velký", "velky-dent"),
    739: ("ia zuby", "ia-zuby"),
}

SKIP_ROWS = {
    21: "ordinace k 31.8.2026 konci provoz (podle analyzy)",
    65: "FN Olomouc — fakultni nemocnice, ne soukroma ordinace",
    71: "web oznamuje umrti lekare — neposilat",
    193: "AUCentrum — ordinace k pronajmu, ne ordinace",
    703: "MACE restaurant — restaurace, ne ordinace",
    724: "MUDr. Vidrasova — stejny web jako r. 42 (WistDental)",
    768: "MUDr. Stefkova — stejny web jako r. 767 (medivize.cz)",
}

PALETTE = ["#356FA3", "#0F6E77", "#2E7D6B", "#7A4E6E", "#8A5A3C", "#455F8A",
           "#2F6F8F", "#3C7A5E", "#6B5B95", "#A2694E", "#34618F", "#7C4F8C"]

rows = list(csv.reader(open("sheet2.csv", encoding="utf-8", newline="")))


def cells(r):
    """Vrati (web, rating, analyza, email). Nektere radky maji rating,
    technologie, barvy i analyzu naskladane v jedne bunce oddelene taby."""
    web = r[1].strip() if len(r) > 1 else ""
    raw_rating = r[2] if len(r) > 2 else ""
    email = ""
    for c in r[3:9]:
        m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", c)
        if m and len(c.strip()) < 60:  # delsi bunka = veta, ne adresa
            email = m.group(0)
            break
    if "\t" in raw_rating:
        parts = [p.strip() for p in raw_rating.split("\t")]
        rating = parts[0]
        anal = parts[3] if len(parts) > 3 else ""
    else:
        rating = raw_rating.strip()
        anal = r[5].strip() if len(r) > 5 else ""
    return web, rating, anal, email


existing_names, taken = {}, set()
for tpl in ("ukazka-1", "ukazka-2", "ukazka-3"):
    d = os.path.join(tpl, "studia")
    for fn in os.listdir(d):
        if fn.endswith(".json"):
            taken.add(fn[:-5])
            nazev = json.load(open(os.path.join(d, fn), encoding="utf-8")).get("nazev", "")
            existing_names[slugify(nazev)] = nazev

if not DRY and os.path.exists("davka-web.json"):
    for c in json.load(open("davka-web.json", encoding="utf-8")):
        p = os.path.join(c["sablona"], "studia", f"{c['slug']}.json")
        if os.path.exists(p):
            os.remove(p)
        taken.discard(c["slug"])
        existing_names.pop(slugify(c["nazev"]), None)

created, skipped = [], []
for n in range(1, len(rows) + 1):
    raw = rows[n - 1][0].strip()
    web, rating, anal, email = cells(rows[n - 1])
    if not raw or not web or not rating:
        continue
    if n in SKIP_ROWS:
        skipped.append((n, raw, SKIP_ROWS[n]))
        continue

    if n in OVERRIDE:
        name, slug = OVERRIDE[n]
    else:
        if NOT_DENTIST.search(raw) or (NOT_DENTIST.search(web) and not DENTAL_HINT.search(raw)):
            skipped.append((n, raw, "neni zubni ordinace"))
            continue
        name, surname = normalize_name(raw)
        if len(deacc(name).strip()) < 4 or is_generic(name):
            skipped.append((n, raw, "bez pouzitelneho jmena"))
            continue
        slug = slugify(surname) + "-dent" if surname else slugify(name)
        if not surname and "dent" not in slug:
            slug += "-dent"

    key = slugify(name)
    if key in existing_names:
        skipped.append((n, raw, f"ukazku uz ma ({existing_names[key]})"))
        continue

    b, k = slug, 2
    while slug in taken:
        slug = f"{b}-{k}"
        k += 1
    taken.add(slug)
    existing_names[key] = name

    # host bez query — jinak by utm_source=firmy.cz vypadal jako katalog
    domain = re.sub(r"^https?://(www\.)?", "", web).split("/")[0].split("?")[0]
    created.append({"radek": n, "slug": slug, "nazev": name, "puvodni": raw,
                    "sablona": TEMPLATE, "barva": PALETTE[len(created) % len(PALETTE)],
                    "web": web, "domena": domain, "email": email,
                    "rating": rating, "analyza": anal,
                    "typ": "katalog" if KATALOG.search(domain) else "web"})

if DRY:
    print(f"KANDIDATU: {len(created)}  (katalog: "
          f"{sum(1 for c in created if c['typ'] == 'katalog')}, "
          f"vlastni web: {sum(1 for c in created if c['typ'] == 'web')}, "
          f"s e-mailem: {sum(1 for c in created if c['email'])})")
    print(f"VYNECHANO: {len(skipped)}\n")
    for c in created:
        print(f"  {c['radek']:4} {c['typ']:8} {c['nazev'][:34]:36} {c['domena'][:34]:36} "
              f"{c['email'][:26]:28} {c['analyza'][:60]}")
    print("\n--- vynechano ---")
    for n, raw, why in skipped:
        print(f"  {n:4}  {raw[:52]:54} -> {why}")
    sys.exit(0)

for c in created:
    with open(os.path.join(TEMPLATE, "studia", f"{c['slug']}.json"), "w",
              encoding="utf-8") as f:
        json.dump({"nazev": c["nazev"], "barva": c["barva"]}, f, ensure_ascii=False)
        f.write("\n")

with open("davka-web.json", "w", encoding="utf-8") as f:
    json.dump(created, f, ensure_ascii=False, indent=2)
    f.write("\n")

with open("davka-web-vynechane.txt", "w", encoding="utf-8") as f:
    for n, raw, why in skipped:
        f.write(f"{n}\t{raw}\t{why}\n")

print(f"Vytvoreno {len(created)} studii ({sum(1 for c in created if c['typ']=='katalog')} "
      f"katalogovych, {sum(1 for c in created if c['typ']=='web')} s vlastnim webem), "
      f"vynechano {len(skipped)}")
