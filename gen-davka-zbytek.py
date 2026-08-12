"""Dogeneruje studia pro VSECHNY zbyle leady: sloupec B (web) prazdny,
rating 7, radek jeste nebyl v zadne predchozi davce.

Proti predchozim davkam (243-300, 301-450) se jmena neprepisuji rucne po
jednom — je jich pres tristo. Pouziva se heuristika prevzata z
gen-davka-195-242.py (obraceni "Prijmeni Jmeno MUDr." -> "MUDr. Jmeno
Prijmeni", odriznuti "s.r.o.", generickych predpon apod.) a rucne se
opravuje jen to, co heuristika nezvladne (OVERRIDE).

Vynechavaji se radky bez identifikovatelneho jmena (GENERIC_ONLY),
laboratore a neordinace (NOT_DENTIST) a jmena, ktera uz nekde ukazku maji
(kontrola proti vsem ukazka-*/studia/*.json — at nikomu neprijdou dva
maily se dvema ruznymi weby).

Spusteni:
    python gen-davka-zbytek.py --dry   # jen vypis, nic nezapisuje
    python gen-davka-zbytek.py         # vytvori studia + davka-zbytek.json
"""

import csv
import json
import os
import re
import sys
import unicodedata

TEMPLATE = "ukazka-1"
PREV = ("davka-195-242.json", "davka-243-300.json", "davka-301-450.json")
DRY = "--dry" in sys.argv

# ── normalizace jmena (prevzato z gen-davka-195-242.py) ─────────────────
TITLES = {"mudr": "MUDr.", "mddr": "MDDr.", "mvdr": "MVDr.", "phdr": "PhDr.", "dis": "Dis."}
LEGAL = r",?\s*\b(s\.?\s?r\.?\s?o\.?|sro\.?|spol\.?|a\.?s\.?)\b\.?"
TAIL_JUNK = [
    r"\s*[-–—]\s*soukrom[áa]\s+ambulance$", r",?\s*zubn[ií]\s+l[ée]ka[řr]k?a?$",
    r",\s*ordinace\s+praktick[éeh]+o?\s+zubn[ií]ho\s+l[ée]ka[řr]e$",
    r"\s*[-–—]\s*ortodontist[ak]$", r",?\s*prakti[cčk][^,]*$",
]
LEAD_GENERIC = [r"^zubn[ií]\s+l[ée]ka[řr]k?a?\b", r"^zubn[ií]\s+ordinace\b",
                r"^ordinace\b", r"^stomatologick[áa]\s+ordinace\b",
                r"^zubn[ií]\s+ambulance\b"]
GENERIC_TOK = {"zubni", "lekar", "lekarka", "ordinace", "ambulance", "dentalni",
               "hygiena", "stomatolog", "stomatologicka", "praxe", "praktickeho",
               "zubniho", "lekare", "mudr", "mddr"}


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


# Krestni jmena — tabulka mixuje "Jmeno Prijmeni" i "Prijmeni Jmeno",
# takze samotna pozice titulu na poradi nestaci.
FIRST = set("""jiri jan josef petr michal martin pavel tomas miroslav zdenek vaclav
karel ladislav frantisek roman radek adam david lukas marek milan vladimir stanislav
antonin alois robert richard igor ivan ales bohumil oldrich rudolf libor daniel filip
jakub ondrej vojtech simon dominik patrik lubos kamil vlastimil jaroslav ivo bendito
joseph michael vladislav mirko roland anatolij jindrich otakar bretislav
jana marie eva hana anna vera alena lenka petra lucie katerina zuzana jitka ivana
helena dagmar miroslava blanka olga vlasta yvetta miriam irena milena daniela andrea
bozena ludmila marta monika michaela sarka simona radka renata iveta sona tereza
barbora klara veronika denisa nikola adela karolina pavla nadezda zdenka dana iva
jarmila bohumila emilie julie karin libuse miluse terezie stepanka vladimira zdena
katarina kvetoslava kvetuse regina rita alzbeta magda beata jaroslava maketa marketa
oldriska lamis taťana tatana natalie""".split())

# Slova, ze kterych nevznikne jmeno ordinace (obecne oznaceni + mesta).
GENERIC_NAME_TOK = GENERIC_TOK | set("""zubar zubarka technik klinika centrum stredisko
pohotovost sluzba privatni soukromy soukroma esteticka parodontologie ortodoncie
protetika implantologie a v pro pri komora dum lekarsky odborny odbor prakticka
ambulance olomouc zlin brno praha ostrava plzen liberec pardubice hradec budejovice
usti most teplice cheb karlovy vary jihlava kladno melnik decin louny podebrady
klatovy tabor strakonice blansko havirov karvina frydek opava prerov prostejov
sumperk vsetin kromeriz uherske hradiste breclav hodonin znojmo trebic""".split())


def is_generic(name):
    toks = [deacc(t).lower().strip(".,-") for t in re.split(r"[\s,\-–—]+", name) if t]
    toks = [t for t in toks if t]
    return bool(toks) and all(t in GENERIC_NAME_TOK for t in toks)


def order_name(toks):
    """Rozhodne poradi 'Jmeno Prijmeni' u dvouslovneho jmena."""
    if len(toks) != 2:
        return toks
    a, b = deacc(toks[0]).lower().strip(".,"), deacc(toks[1]).lower().strip(".,")
    if a in FIRST:
        return toks
    if b in FIRST:
        return [toks[1], toks[0]]
    if a.endswith("ova") and not b.endswith("ova"):
        return [toks[1], toks[0]]
    return toks


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

    name_toks = name_toks[:2]
    # poradi urcuje seznam krestnich jmen; teprve kdyz nerozhodne, rozhoduje
    # pozice titulu (titul na konci => tabulka ma "Prijmeni Jmeno")
    before = list(name_toks)
    name_toks = order_name(name_toks)
    if name_toks == before and title_idx is not None \
            and title_idx >= len(toks) - 2 and len(name_toks) >= 2:
        name_toks = [name_toks[1], name_toks[0]]
    # velka pismena v celem jmene (SONA HUTTNEROVA) -> Titulkovy tvar
    name_toks = [t.capitalize() if t.isupper() and len(t) > 3 else t for t in name_toks]
    surname = name_toks[-1] if len(name_toks) >= 2 else name_toks[0]
    return f"{title} " + " ".join(name_toks), surname


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", deacc(s).lower())).strip("-")


# ── co se nikdy neposila ────────────────────────────────────────────────
# radek, ze ktereho nezbude jmeno (jen obecne oznaceni sluzby/mista)
GENERIC_ONLY = re.compile(
    r"^(zubn[ií]\s+(l[ée]ka[řr]k?a?|ordinace|ambulance|st[řr]edisko|centrum|hygiena|"
    r"laborato[řr]|prax[eě]|p[ée][čc]e|pohotovost)|"
    r"stomatolog(ie|icka?\s+\w+)?|stomatolog|ordinace\b.*|ord\.\s*.*|"
    r"prakti[cčk]\w*\s+.*|samostatn[áa]\s+.*|soukrom[áa]\s+.*|"
    r"d[ěe]tsk[áa]\s+(zubn[ií]|stomatolog\w*)|poliklinika\b.*|"
    r"zdravotn[ií]\s+st[řr]edisko.*|nemocnice\b.*|l[ée]ka[řr]sk[ýy]\s+d[ůu]m.*|"
    r"[^a-zA-Zá-žÁ-Ž]*|.*\d{2,}.*)$", re.I)

NOT_DENTIST = re.compile(
    r"laborato[řr]|neurolog|gynekolog|o[čc]n[ií]|kožn|derma|prakti[cčk]\w*\s+l[ée]ka[řr]"
    r"|pediatr|d[ěe]tsk[ýy]\s+l[ée]ka[řr]|chirurg|interna|rehabilitac|l[ée]k[áa]rna"
    r"|veterin|psychiatr|psycholog|o[čc]n[ií]\s|ORL\b|urolog|ortoped", re.I)

# Rucni opravy tam, kde heuristika selze (nazev firmy smichany se jmenem
# lekare, dva lekari v jednom radku, preklep v tabulce). Podle vypisu --dry.
OVERRIDE = {
    104: ("DI DENT", "di-dent"),
    105: ("MUDr. Michal Hečko", "hecko-dent"),
    153: ("MUDr. Pavlína Adamková", "adamkova-dent"),
    456: ("MUDr. Petr Nový", "novy-dent"),
    457: ("MUDr. Robert Houba, Ph.D.", "houba-dent"),
    460: ("MDDr. Michael Vajskebr", "vajskebr-dent"),
    498: ("MUDr. Michal Slavotínek a MUDr. Marta Slavotínková", "slavotinek-dent"),
    563: ("Dentální hygiena a bělení — Petr Köck", "kock-dent"),
    598: ("Dentální hygiena Děčín — Daniela Kubátová", "kubatova-dent"),
    607: ("MUDr. Romana Červová-Hájková", "cervova-hajkova-dent"),
    616: ("MUDr. Markéta Skolilová", "skolilova-dent"),  # v tabulce preklep "Maketa"
    619: ("Dental Poděbrady", "dental-podebrady"),
    623: ("MUDr. Pavel Raba", "raba-dent"),
    633: ("MUDr. Eva Nesměráková", "nesmerakova-dent"),
}

# Radky, ktere heuristika propusti, ale posilat se nemaji: obecne oznaceni
# sluzby, zubni technici/laboratore (pacienty neobjednavaji), komora, blog.
SKIP_ROWS = {
    69: "Zubni ordinace Olomouc — jen obor + mesto",
    74: "dentalni hygiena olomouc — jen obor + mesto",
    75: "Zubar Olomouc — jen obor + mesto",
    97: "Zubar v Olomouci — jen obor + mesto",
    99: "Zubni technik — bez jmena, navic technik",
    118: "Esteticka Stomatologie — bez jmena",
    125: "Stomatologicka ordinace — bez jmena",
    126: "Stomatologie a parodontologie — bez jmena",
    130: "Oblastni Stomatologicka Komora Zlin — komora, ne ordinace",
    136: "Privatni stomatologicka ordinace — bez jmena",
    137: "Soukromy zubni lekar — bez jmena",
    140: "Privatni zubni technik — bez jmena, navic technik",
    143: "Privatni zubni lekarka — bez jmena",
    149: "Privatni stomatolog — bez jmena",
    152: "LDK-lekarsky dum Koterova — budova, ne ordinace",
    155: "Z denicku dentalni hygienistky — blog",
    158: "Privatni stomatologicka praxe — bez jmena",
    160: "Zubni technik Staskova — technik, pacienty neobjednava",
    179: "Odbor. lekar ortodoncie a stomatologie — bez jmena",
    479: "Privatni zubni ordinace — bez jmena",
    512: "Privatni zubni praxe — bez jmena",
    519: "Privatni stomatologicka ambulance — bez jmena",
    533: "Spolecna praxe lekaru - Orofacialni centrum — bez jmena",
    540: "Ing. Rudolf Fejtek — Ing., ne zubni lekar",
    546: "Ambulance zubniho lekare — bez jmena",
    627: "Zubni pohotovost Melnik — pohotovost, ne ordinace",
    628: "Zubni klinika — bez jmena",
}

PALETTE = ["#356FA3", "#0F6E77", "#2E7D6B", "#7A4E6E", "#8A5A3C", "#455F8A",
           "#2F6F8F", "#3C7A5E", "#6B5B95", "#A2694E", "#34618F", "#7C4F8C"]

rows = list(csv.reader(open("sheet2.csv", encoding="utf-8", newline="")))

# Rozsahy 195-450 uz byly protriedene v predchozich davkach — vcetne radku,
# ktere se tam zamerne vynechaly (duplicity, laboratore, radky bez jmena).
# Kdyby se bral jen seznam vytvorenych, vratily by se sem prave ty vynechane.
done_rows = set(range(195, 451))
for f in PREV:
    if os.path.exists(f):
        done_rows |= {c["radek"] for c in json.load(open(f, encoding="utf-8"))}

# jmena, ktera uz nekde ukazku maji (aby nikomu neprisly dva maily)
existing_names, taken = {}, set()
for tpl in ("ukazka-1", "ukazka-2", "ukazka-3"):
    d = os.path.join(tpl, "studia")
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.endswith(".json"):
            continue
        taken.add(fn[:-5])
        nazev = json.load(open(os.path.join(d, fn), encoding="utf-8")).get("nazev", "")
        existing_names[slugify(nazev)] = nazev

if not DRY and os.path.exists("davka-zbytek.json"):
    for c in json.load(open("davka-zbytek.json", encoding="utf-8")):
        p = os.path.join(c["sablona"], "studia", f"{c['slug']}.json")
        if os.path.exists(p):
            os.remove(p)
        taken.discard(c["slug"])
        existing_names.pop(slugify(c["nazev"]), None)

created, skipped = [], []
for n in range(1, len(rows) + 1):
    r = rows[n - 1]
    raw = r[0].strip()
    web = r[1].strip() if len(r) > 1 else ""
    rating = r[2].strip() if len(r) > 2 else ""
    if not raw or web or rating != "7" or n in done_rows:
        continue
    if n in SKIP_ROWS:
        skipped.append((n, raw, SKIP_ROWS[n]))
        continue

    if n in OVERRIDE:
        name, slug = OVERRIDE[n]
    else:
        if GENERIC_ONLY.match(raw):
            skipped.append((n, raw, "bez identifikovatelneho jmena"))
            continue
        if NOT_DENTIST.search(raw):
            skipped.append((n, raw, "neni zubni ordinace / laborator"))
            continue
        name, surname = normalize_name(raw)
        if len(deacc(name).strip()) < 4 or not re.search(r"[A-Za-zÁ-Žá-ž]{3}", name):
            skipped.append((n, raw, "z nazvu nezbylo pouzitelne jmeno"))
            continue
        if is_generic(name):
            skipped.append((n, raw, "zbylo jen obecne oznaceni / mesto"))
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

    created.append({"radek": n, "slug": slug, "nazev": name, "puvodni": raw,
                    "sablona": TEMPLATE,
                    "barva": PALETTE[len(created) % len(PALETTE)]})

if DRY:
    print(f"KANDIDATU: {len(created)}   VYNECHANO: {len(skipped)}\n")
    print("--- vytvorilo by se ---")
    for c in created:
        print(f"  {c['radek']:4}  {c['slug']:26} {c['nazev']:42} <- {c['puvodni']}")
    print("\n--- vynechano ---")
    for n, raw, why in skipped:
        print(f"  {n:4}  {raw[:52]:54} -> {why}")
    sys.exit(0)

for c in created:
    with open(os.path.join(TEMPLATE, "studia", f"{c['slug']}.json"), "w",
              encoding="utf-8") as f:
        json.dump({"nazev": c["nazev"], "barva": c["barva"]}, f, ensure_ascii=False)
        f.write("\n")

with open("davka-zbytek.json", "w", encoding="utf-8") as f:
    json.dump(created, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Vytvoreno {len(created)} studii na {TEMPLATE}, vynechano {len(skipped)}")
with open("davka-zbytek-vynechane.txt", "w", encoding="utf-8") as f:
    for n, raw, why in skipped:
        f.write(f"{n}\t{raw}\t{why}\n")
print("Vynechane radky: davka-zbytek-vynechane.txt")
