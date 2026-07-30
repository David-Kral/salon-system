"""Vygeneruje MAILY-DAVKA-B.txt — 51 ordinaci, sablona ukazka-1, s e-maily.

Format stejny jako MAILY-195-242.txt: kazdy odstavec je jeden radek, takze
po vlozeni do mailu netreba prerovnavat odstavce.

Ctyri adresy se v seznamu opakuji (dve pobocky, jeden mail). U nich jde
JEDEN mail, ktery zmiňuje obe pobocky a odkazuje na obe stranky; druhy
vyskyt je oznaceny jako pokryty, aby se neposilalo dvakrat.

Popis formulare je overeny naziva na ukazka-1:
  1) Novy pacient / Stavajici pacient
  2) preferovany termin (od-do) + cast dne (Rano / Poledne / Odpoledne)
  3) Jmeno a prijmeni, Telefon, E-mail, Poznamka (volitelne)
  -> "Odeslat zadost";  sekce "Objednejte se online"

Spusteni:  python gen-maily-davka-b.py
"""

import json
import re
from collections import Counter, defaultdict

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
B = json.load(open("davka-b.json", encoding="utf-8"))

unwrap = lambda s: re.sub(r"\s+", " ", s).strip()

# ── kolize a podezrele adresy (hlasi gen-davka-b.py) ───────────────────
OVERLAP = {  # slug v davce B -> slug v predchozi davce
    "kolcavova-dent-2": "kolcavova-dent",
    "mz-jesenik": "mz-dent",
    "mz-zulova": "mz-dent",
}
SUSPECT = {
    "mkolc@cebtrum.cz": "domena 'cebtrum.cz' vypada jako preklep — nejspis 'centrum.cz'",
    "222x222@seznam.cz": "adresa vypada nestandardne, over ze je spravna",
}

email_count = Counter(c["email"].lower() for c in B)
first_of_email = {}
for c in B:
    first_of_email.setdefault(c["email"].lower(), c["slug"])

# pobocky sdilejici mail
branches = defaultdict(list)
for c in B:
    branches[c["email"].lower()].append(c)


def branch_label(c):
    m = re.search(r"\(([^)]*)\)", c["puvodni"])
    return m.group(1) if m else None


SUBJECTS = [
    "Návrh webu pro vaši ordinaci — {name}",
    "Ukázka webu na míru — {name}",
    "Web pro vaši ordinaci — {name}",
    "Připravil jsem návrh webu — {name}",
    "Vlastní web s online objednáním — {name}",
    "Návrh webové stránky — {name}",
    "Jak by mohl vypadat váš web — {name}",
    "Ukázka zdarma: web pro vaši ordinaci — {name}",
    "Web, na kterém se pacient objedná sám — {name}",
    "Návrh prezentace ordinace — {name}",
    "Web + online objednávání — {name}",
]

OPENERS = [
    "hledal jsem na internetu vaši ordinaci a našel jsem hlavně záznamy v katalozích lékařů. Vlastní web, kde by se pacient dozvěděl něco o vás a o ordinaci samotné, mi chyběl.",
    "díval jsem se, jak vás na internetu najde nový pacient. Vyšly mi jen profily v katalozích — každý vypadá jinak a ani jeden nepůsobí jako vaše vlastní vizitka.",
    "všiml jsem si, že vaše ordinace nemá vlastní webovou stránku. Dnes je přitom web většinou první místo, kam se pacient podívá ještě předtím, než zvedne telefon.",
    "prohlížel jsem si zubní ordinace v okolí a u té vaší jsem nenarazil na vlastní web — jen na katalogové zápisy, které o ordinaci samotné neřeknou téměř nic.",
    "zkoušel jsem si najít web vaší ordinace a skončil jsem na obecných profilech v katalozích. Chybí tam fotky, ceník i možnost se objednat.",
    "když si dnes někdo hledá zubaře, většinou skončí na webu ordinace. U vás jsem ale žádný nenašel — jen zápisy v katalozích lékařů.",
    "o vaší ordinaci se dá na internetu dohledat jen to, co je v katalogových profilech. Vlastní web, který by ji představil, chybí.",
    "díval jsem se po webu vaší ordinace a nenašel ho. To je škoda — katalogový zápis neukáže ani ordinaci, ani to, čím se od ostatních lišíte.",
]

MIDDLES = [
    "Připravil jsem proto ukázku, jak by web mohl vypadat. Není to obecná šablona — je pojmenovaná přímo na vaši ordinaci, v titulku i v hlavičce stojí „{name}“:",
    "Připravil jsem ukázku na míru. V hlavičce i v titulku stránky je „{name}“, takže hned uvidíte, jak by web působil:",
    "Zkusil jsem načrtnout, jak by to mohlo vypadat. Ukázka nese jméno vaší ordinace — „{name}“ — takže to není neutrální demo:",
    "Udělal jsem návrh přímo pro vás. Stránka je pojmenovaná „{name}“, včetně titulku v prohlížeči:",
    "Připravil jsem konkrétní ukázku, ne obecnou prezentaci. Web je pojmenovaný na „{name}“ a má sekce, které u zubní ordinace čekám — péči, ceník, ordinační hodiny:",
    "Sestavil jsem návrh, jak by web mohl fungovat. V hlavičce je „{name}“, ať vidíte reálný dojem, ne prázdnou šablonu:",
    "Připravil jsem ukázku pojmenovanou na „{name}“ — s přehledem péče, ceníkem, ordinačními hodinami i kontaktem:",
    "Zpracoval jsem návrh na míru vaší ordinaci. Stránka je vedená pod jménem „{name}“:",
]

# formular na ukazka-1: typ pacienta -> termin + cast dne -> kontakt + poznamka
FORM = [
    "Není to jen vizitka. Je v tom i objednávkový formulář: pacient řekne, jestli je nový nebo stávající, vybere preferovaný termín a část dne (ráno, poledne, odpoledne) a nechá jméno, telefon, e-mail a případnou poznámku. Vám přijde žádost se všemi údaji pohromadě.",
    "Součástí je i online objednávání. Pacient projde třemi kroky — nový nebo stávající pacient, preferovaný termín a část dne, pak kontaktní údaje s poznámkou. Co přesně se ptáte a jaké termíny nabízíte, se dá nastavit podle vaší ordinace.",
    "K webu patří formulář na objednání, postavený přesně na to, co potřebujete. Pacient vybere, zda je nový či stávající, zvolí termín a část dne a vyplní jméno, telefon a e-mail. Rozsah polí i nabídku si nadefinujete sám.",
    "Web umí i online objednání termínu. Pacient si zvolí, jestli přichází poprvé, kdy mu to vyhovuje (včetně ráno / poledne / odpoledne) a nechá kontakt s poznámkou — cílem je, aby vám během ošetření nezvonil telefon.",
    "Kromě webu bych přidal i objednávkový formulář se specifikací podle vás: jaké údaje od pacienta chcete, jaké termíny nabízet a jak rozlišit nového a stávajícího pacienta. V ukázce je funkční, můžete si ho projít.",
    "Je v tom i rezervační formulář. Pacient uvede, zda je nový nebo stávající, vybere si termín a denní dobu a doplní jméno, telefon, e-mail a poznámku. Vy dostanete hotovou žádost, ne jen prozvonění.",
    "Součástí systému je i online objednávka. Nastavíme ji přesně na vaši praxi — které zákroky a termíny nabízet, co má pacient povinně vyplnit. V ukázce si celý průchod vyzkoušíte tak, jak ho uvidí pacient.",
    "Web není jen prezentace — obsahuje objednávkový formulář, kde pacient vybere typ návštěvy, preferovaný termín a část dne a nechá na sebe kontakt. Políčka i nabídku termínů upravíme podle toho, jak ordinujete.",
]

ATTACH = [
    "V příloze posílám i screenshot úvodní obrazovky, ať se nemusíte nikam proklikávat.",
    "Do přílohy jsem přidal screenshot úvodní stránky pro rychlou představu.",
    "V příloze je snímek úvodní obrazovky, ať vidíte návrh i bez otevírání odkazu.",
    "Přikládám screenshot hlavní stránky — odkaz je pak na plnou verzi.",
    "V příloze najdete náhled úvodní obrazovky.",
    "Screenshot úvodní stránky přikládám do přílohy.",
]

CLOSERS = [
    "Je to ukázka zdarma a bez jakéhokoli závazku. Pokud by se vám líbila, rád proberu detaily i úpravy na míru.",
    "Nic za to nechci a nikam se tím nezavazujete. Kdyby vás to zaujalo, ozvěte se a domluvíme se na úpravách podle vašich představ.",
    "Ukázka je zdarma a bez závazku. Když vám padne do oka, doladíme texty, fotky i barvy podle vás.",
    "Berte to jako ukázku zdarma, žádný závazek v tom není. Pokud by to pro vás mělo smysl, rád na tom dál zapracuji.",
    "Je to zdarma a bez závazku — kdyby se vám návrh zamlouval, ozvěte se a probereme, co upravit.",
    "Za ukázku nic neplatíte a k ničemu se nezavazujete. Kdyby vás zajímalo pokračování, napište nebo zavolejte.",
]

L = []
L.append("MAILY — DAVKA B (51 ordinaci, sablona ukazka-1 / Dentaline)")
L.append("=" * 70)
L.append("")
L.append("Kazdy odstavec je jeden radek — po vlozeni do mailu se odstavce")
L.append("nerozsypou a netreba nic prerovnavat.")
L.append("")
L.append("E-maily jsou vyplnene podle tvého seznamu.")
L.append("")
L.append("Objednavkovy formular je na ukazce skutecne nasazeny (overeno naziva):")
L.append("  1) Novy pacient / Stavajici pacient")
L.append("  2) preferovany termin (od-do) + cast dne: Rano / Poledne / Odpoledne")
L.append("  3) Jmeno a prijmeni, Telefon, E-mail, Poznamka (volitelne)")
L.append("  -> tlacitko 'Odeslat zadost', sekce 'Objednejte se online'")
L.append("")

dup_emails = {e: n for e, n in email_count.items() if n > 1}
if dup_emails:
    L.append("-" * 70)
    L.append("POZOR — CTYRI ADRESY SE OPAKUJI (dve pobocky, jeden mail).")
    L.append("Mail jde jen u prvni z nich a zminuje obe pobocky vcetne obou")
    L.append("odkazu. Druhy vyskyt je oznaceny 'POKRYTO' — neposilej ho.")
    L.append("-" * 70)
    L.append("")

if OVERLAP:
    L.append("-" * 70)
    L.append("POZOR — TRI ORDINACE UZ JSOU V PREDCHOZI DAVCE (MAILY-195-242.txt):")
    for slug, old in OVERLAP.items():
        c = next(x for x in B if x["slug"] == slug)
        lbl = branch_label(c)
        L.append(f"  {c['nazev']}{' (' + lbl + ')' if lbl else ''} — tam jako '{old}'")
    L.append("Posli jim jen JEDEN mail. Tato davka je novejsi (ma e-mail i")
    L.append("pozadovanou sablonu), takze doporucuju poslat tuhle verzi a v")
    L.append("MAILY-195-242.txt je preskocit.")
    L.append("-" * 70)
    L.append("")

if SUSPECT:
    L.append("-" * 70)
    L.append("POZOR — PODEZRELE ADRESY, over pred odeslanim:")
    for em, why in SUSPECT.items():
        who = next((x["nazev"] for x in B if x["email"].lower() == em.lower()), "?")
        L.append(f"  {who}: {em}")
        L.append(f"    {why}")
    L.append("-" * 70)
    L.append("")

for i, c in enumerate(B):
    name = c["nazev"]
    url = MAN[c["slug"]]["url"]
    em = c["email"]
    eml = em.lower()
    is_dup_second = email_count[eml] > 1 and first_of_email[eml] != c["slug"]

    L.append("")
    L.append("=" * 70)
    head = f"{i + 1}. {name}"
    lbl = branch_label(c)
    if lbl:
        head += f"  ({lbl})"
    L.append(head)
    if is_dup_second:
        prim = next(x for x in B if x["slug"] == first_of_email[eml])
        pidx = B.index(prim) + 1
        L.append(f"   POKRYTO v mailu c. {pidx} (stejny e-mail) — NEPOSILAT")
    if c["slug"] in OVERLAP:
        L.append(f"   POZOR: uz je v MAILY-195-242.txt jako '{OVERLAP[c['slug']]}'")
    L.append(f"   {url}")
    L.append("=" * 70)
    L.append("")

    if is_dup_second:
        L.append("(Tato pobocka je zminena v mailu vyse, ktery jde na stejnou adresu.)")
        L.append("")
        continue

    L.append(f"Komu: {em}")
    if eml in SUSPECT:
        L.append(f"      !! {SUSPECT[eml]}")
    L.append(f"Predmet: {SUBJECTS[i % len(SUBJECTS)].format(name=name)}")
    L.append("")
    L.append("Dobrý den,")
    L.append("")
    L.append(unwrap(OPENERS[(i * 3) % len(OPENERS)]))
    L.append("")
    L.append(unwrap(MIDDLES[(i * 5) % len(MIDDLES)].format(name=name)))
    L.append("")
    L.append(url)
    L.append("")

    # pobocky na stejnem mailu -> zminit obe a dat oba odkazy
    sibs = [x for x in branches[eml] if x["slug"] != c["slug"]]
    if sibs:
        labels = [branch_label(x) or x["nazev"] for x in sibs]
        mine = branch_label(c)
        L.append(unwrap(
            f"Vím, že máte víc pracovišť, tak jsem ukázku připravil pro "
            f"{'obě' if len(sibs) == 1 else 'všechna'}. Odkaz výše je pobočka "
            f"{mine if mine else 'první'} — a tady "
            f"{'je' if len(sibs) == 1 else 'jsou'} {', '.join(labels)}:"))
        L.append("")
        for x in sibs:
            L.append(MAN[x["slug"]]["url"])
        L.append("")

    L.append(unwrap(FORM[(i * 3) % len(FORM)]))
    L.append("")
    L.append(unwrap(ATTACH[(i * 7) % len(ATTACH)]))
    L.append("")
    L.append(unwrap(CLOSERS[(i * 11) % len(CLOSERS)]))
    L.append("")
    L.append("S pozdravem,")
    L.append("David Král")
    L.append("777 122 178")
    L.append("fitego.cz")
    L.append("")

open("MAILY-DAVKA-B.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")

# ── kontroly ───────────────────────────────────────────────────────────
txt = open("MAILY-DAVKA-B.txt", encoding="utf-8").read()
all_lines = txt.split("\n")
starts = [k for k, ln in enumerate(all_lines) if re.match(r"^\d+\. \S", ln)]
bodies = []
for n, k in enumerate(starts):
    end = starts[n + 1] if n + 1 < len(starts) else len(all_lines)
    bodies.append("\n".join(all_lines[k:end]))

problems = []
if len(bodies) != len(B):
    problems.append(f"rozdeleno {len(bodies)} bloku, ocekavano {len(B)}")

sendable = 0
for k, body in enumerate(bodies, start=1):
    if "NEPOSILAT" in body:
        continue
    sendable += 1
    for need, label in [("Komu:", "adresat"), ("Predmet:", "predmet"),
                        ("/ordinace/", "odkaz"), ("fitego.cz", "podpis")]:
        if need not in body:
            problems.append(f"mail {k}: chybi {label}")
    if not re.search(r"objednáv|objednán|rezervačn|formulář", body, re.I):
        problems.append(f"mail {k}: chybi odstavec o formulari")
    if not re.search(r"příloz|Přikládám|příloh", body):
        problems.append(f"mail {k}: chybi zminka o priloze")

# kazda stranka z davky B musi existovat
for c in B:
    if c["slug"] not in MAN:
        problems.append(f"{c['slug']}: chybi stranka")

print(f"OK — MAILY-DAVKA-B.txt")
print(f"   bloku: {len(bodies)} | k odeslani: {sendable} | pokryto jinym mailem: {len(bodies)-sendable}")
print(f"   unikatnich predmetu: {len(set(re.findall(r'Predmet: (.+)', txt)))}")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
