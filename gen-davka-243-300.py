"""Z radku 243-300 Google Sheetu vyrobi studia na sablone ukazka-1.

Navazuje na davku 195-242 (gen-davka-195-242.py). Rozdil: tahle davka
pouziva VYHRADNE `ukazka-1` (Dentaline styl) — tak si to vyzadal zadavatel.

Vsech 58 radku ma v tabulce POUZE jmeno + rating 7 (vyjimky: r. 243 a 265
maji web). Vynechane radky viz SKIP nize.

Spusteni:  python gen-davka-243-300.py
"""

import csv
import json
import os

ROWS = (243, 300)
TEMPLATE = "ukazka-1"

# Radky, ze kterych nejde udelat lead: bud nemaji zadne jmeno (nelze
# pojmenovat web ani mail), nebo to vubec neni zubni ordinace.
SKIP = {
    243: "ocni ordinace (facebook ocni.sedlackova.prostejov), ne zubar",
    245: "Stomatologicka Laborator — laborator bez jmena, neprijima pacienty",
    257: "Prakticky zubni lekar — zadne jmeno",
    269: "Soukroma zubni ordinace — zadne jmeno",
    270: "GynPro Blansko — gynekologie, ne zubar",
    284: "Ordinace PL - stomatologa — zadne jmeno",
    286: "Prakticky lekar pro dospele — praktik, ne zubar",
    288: "Prakticke zubni lekarstvi — zadne jmeno",
    289: "Zubni laborator — laborator, pacienty neobjednava",
    290: "Samostatna ordinace PL stomatologa — zadne jmeno",
    292: "Tabor, poliklinika — zadne jmeno ordinace",
    294: "Ordinace praktickeho zubniho lekare — zadne jmeno",
    296: "Stomatologicka ambulance — zadne jmeno",
}

# Zobrazovane jmeno + slug tam, kde heuristika nestaci (firmy, genitiv,
# dvojite nazvy). Zbytek se odvodi automaticky.
OVERRIDE = {
    244: ("Ludmila Holá", "hola-dent"),
    246: ("MUDr. Michaela Skácelová", "skacelova-dent"),
    248: ("Medico Dent", "medico-dent"),
    249: ("MUDr. Miluše Dvořáčková", "dvorackova-dent"),
    250: ("Zuzana Hlaváčková", "hlavackova-dent"),
    251: ("Luxury Dent", "luxury-dent"),
    252: ("Dentální hygiena Anirda", "anirda-dent"),
    253: ("MUDr. Marie Kuchaříková", "kucharikova-dent"),
    254: ("MUDr. Kinclová", "kinclova-dent"),
    # r. 255 neni samostatna ordinace, ale klinika Dentalstyl s.r.o.
    # (dentalstyl.cz) — MUDr. Dufkova je tam vedouci lekarka. Web tedy
    # nese jmeno kliniky, ne jednoho lekare.
    255: ("Dentalstyl", "dufkova-dent"),
    256: ("MDDr. Sylvie Konečná", "konecna-dent"),
    258: ("MDDr. Jana Bušová", "busova-dent"),
    259: ("MUDr. Pavel Čarvaš", "carvas-dent"),
    260: ("MDDr. Jiří Potůček", "potucek-dent"),
    261: ("MUDr. Lucie Nečasová", "necasova-dent"),
    262: ("MDDr. Dagmar Potůčková", "potuckova-dent"),
    263: ("MUDr. Petra Havlová", "havlova-dent"),
    264: ("HELIOS DENT", "helios-dent"),
    265: ("DENT company", "dent-company"),
    266: ("MUDr. Bohdana Ševčíková", "sevcikova-dent"),
    267: ("MUDr. Martina Řehořková", "rehorkova-dent"),
    268: ("MUDr. Jarmila Kupková", "kupkova-dent"),
    271: ("MUDr. Vlasta Slabá", "slaba-vlasta-dent"),
    272: ("MUDr. Jana Hlasivcová", "hlasivcova-dent"),
    273: ("MUDr. Josef Duraj", "duraj-dent"),
    274: ("Dentave", "dentave"),
    275: ("MUDr. Eva Horáková", "horakova-dent"),
    276: ("MUDr. Magda Slabá", "slaba-magda-dent"),
    277: ("MUDr. Eva Housková", "houskova-dent"),
    278: ("MUDr. Anna Haraštová", "harastova-dent"),
    279: ("MUDr. Miroslav Šimák", "simak-dent"),
    280: ("MUDr. Petr Kolář", "kolar-dent"),
    281: ("MUDr. Jana Berková", "berkova-dent"),
    282: ("MUDr. Josef Voborník", "vobornik-dent"),
    283: ("MUDr. Šárka Švarcová", "svarcova-dent"),
    285: ("MUDr. Alena Kottová", "kottova-dent"),
    287: ("MUDr. Jitka Šimková", "simkova-dent"),
    291: ("DentTabo", "denttabo"),
    293: ("MUDr. Renata Vutjanoková", "vutjanokova-dent"),
    295: ("MarivaDent", "marivadent"),
    297: ("MUDr. Zuzana Kropíková", "kropikova-dent"),
    298: ("Dr. Landa", "landa-dent"),
    299: ("MUDr. Karel Šmíd", "smid-dent"),
    300: ("Stomamed", "stomamed"),
    247: ("MUDr. Vladimír Drahoš", "drahos-dent"),
}

# Paleta pro ukazka-1 (svetly styl s fotkou) — sytejsi tony, ktere na
# svetlem pozadi drzi kontrast.
PALETTE = ["#356FA3", "#0F6E77", "#2E7D6B", "#7A4E6E", "#8A5A3C", "#455F8A",
           "#2F6F8F", "#3C7A5E", "#6B5B95", "#A2694E", "#34618F", "#7C4F8C"]

# Kdyz uz ordinace ma svou znackovou barvu, drzime se ji misto palety.
COLOR = {255: "#EE8B1E"}  # Dentalstyl — oranzova z jejich loga

rows = list(csv.reader(open("sheet2.csv", encoding="utf-8", newline="")))

# Idempotence: smaz studia z predchoziho behu teto davky
if os.path.exists("davka-243-300.json"):
    for c in json.load(open("davka-243-300.json", encoding="utf-8")):
        p = os.path.join(c["sablona"], "studia", f"{c['slug']}.json")
        if os.path.exists(p):
            os.remove(p)

taken = set()
for tpl in ("ukazka-1", "ukazka-2", "ukazka-3"):
    d = os.path.join(tpl, "studia")
    if os.path.isdir(d):
        taken |= {f[:-5] for f in os.listdir(d) if f.endswith(".json")}

created, skipped = [], []
for n in range(ROWS[0], ROWS[1] + 1):
    raw = rows[n - 1][0].strip()
    if n in SKIP or not raw:
        skipped.append({"radek": n, "puvodni": raw, "duvod": SKIP.get(n, "prazdny radek")})
        continue
    if n not in OVERRIDE:
        raise SystemExit(f"radek {n} ({raw!r}) nema OVERRIDE — doplnit rucne")

    name, slug = OVERRIDE[n]
    b, k = slug, 2
    while slug in taken:
        slug = f"{b}-{k}"
        k += 1
    taken.add(slug)

    color = COLOR.get(n, PALETTE[len(created) % len(PALETTE)])
    with open(os.path.join(TEMPLATE, "studia", f"{slug}.json"), "w", encoding="utf-8") as f:
        json.dump({"nazev": name, "barva": color}, f, ensure_ascii=False)
        f.write("\n")
    created.append({"radek": n, "slug": slug, "nazev": name, "puvodni": raw,
                    "sablona": TEMPLATE, "barva": color})

with open("davka-243-300.json", "w", encoding="utf-8") as f:
    json.dump(created, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Vytvoreno {len(created)} studii na {TEMPLATE}")
print(f"Vynechano {len(skipped)}:")
for s in skipped:
    print(f"  r.{s['radek']}  {s['puvodni']}  -> {s['duvod']}")
print()
for c in created:
    print(f"  {c['radek']}  {c['slug']:22} {c['nazev']}")
