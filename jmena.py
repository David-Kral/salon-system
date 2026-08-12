"""Prevod nazvu z tabulky na jmeno ordinace + slug.

Vytazeno z gen-davka-zbytek.py, aby to mohly pouzivat i dalsi davky.
"""

import re
import unicodedata

TITLES = {"mudr": "MUDr.", "mddr": "MDDr.", "mvdr": "MVDr.", "phdr": "PhDr.", "dis": "Dis."}
LEGAL = r",?\s*\b(s\.?\s?r\.?\s?o\.?|sro\.?|spol\.?|a\.?s\.?)\b\.?"
TAIL_JUNK = [
    r"\s*[-–—]\s*soukrom[áa]\s+ambulance$", r",?\s*zubn[ií]\s+l[ée]ka[řr]k?a?$",
    r",\s*ordinace\s+praktick[éeh]+o?\s+zubn[ií]ho\s+l[ée]ka[řr]e$",
    r"\s*[-–—]\s*ortodontist[ak]$", r",?\s*prakti[cčk][^,]*$",
    r"\s*[-–—]\s*nep[řr]ij[íi]m[áa]me\s+nov[ée].*$", r"\s*\|.*$",
]
LEAD_GENERIC = [r"^zubn[ií]\s+l[ée]ka[řr]k?a?\b", r"^zubn[ií]\s+ordinace\b",
                r"^ordinace\b", r"^stomatologick[áa]\s+ordinace\b",
                r"^zubn[ií]\s+ambulance\b"]
GENERIC_TOK = {"zubni", "lekar", "lekarka", "ordinace", "ambulance", "dentalni",
               "hygiena", "stomatolog", "stomatologicka", "praxe", "praktickeho",
               "zubniho", "lekare", "mudr", "mddr"}

FIRST = set("""jiri jan josef petr michal martin pavel tomas miroslav zdenek vaclav
karel ladislav frantisek roman radek adam david lukas marek milan vladimir stanislav
antonin alois robert richard igor ivan ales bohumil oldrich rudolf libor daniel filip
jakub ondrej vojtech simon dominik patrik lubos kamil vlastimil jaroslav ivo bendito
joseph michael vladislav mirko roland anatolij jindrich otakar bretislav premysl vit
jana marie eva hana anna vera alena lenka petra lucie katerina zuzana jitka ivana
helena dagmar miroslava blanka olga vlasta yvetta miriam irena milena daniela andrea
bozena ludmila marta monika michaela sarka simona radka renata iveta sona tereza
barbora klara veronika denisa nikola adela karolina pavla nadezda zdenka dana iva
jarmila bohumila emilie julie karin libuse miluse terezie stepanka vladimira zdena
katarina kvetoslava kvetuse regina rita alzbeta magda beata jaroslava marketa lydie
oldriska lamis tatana natalie svetlana milada dominika sylva kamila""".split())

GENERIC_NAME_TOK = GENERIC_TOK | set("""zubar zubarka technik klinika centrum stredisko
pohotovost sluzba privatni soukromy soukroma esteticka parodontologie ortodoncie
protetika implantologie a v pro pri komora dum lekarsky odborny odbor prakticka
ambulance olomouc zlin brno praha ostrava plzen liberec pardubice hradec budejovice
usti most teplice cheb karlovy vary jihlava kladno melnik decin louny podebrady
klatovy tabor strakonice blansko havirov karvina frydek opava prerov prostejov
sumperk vsetin kromeriz uherske hradiste breclav hodonin znojmo trebic""".split())


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", deacc(s).lower())).strip("-")


def is_generic(name):
    toks = [deacc(t).lower().strip(".,-") for t in re.split(r"[\s,\-–—]+", name) if t]
    return bool(toks) and all(t in GENERIC_NAME_TOK for t in toks)


def order_name(toks):
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
    name_toks = [t.capitalize() if t.isupper() and len(t) > 3 else t for t in name_toks]
    before = list(name_toks)
    name_toks = order_name(name_toks)
    if name_toks == before and title_idx is not None \
            and title_idx >= len(toks) - 2 and len(name_toks) >= 2:
        name_toks = [name_toks[1], name_toks[0]]

    surname = name_toks[-1] if len(name_toks) >= 2 else name_toks[0]
    return f"{title} " + " ".join(name_toks), surname
