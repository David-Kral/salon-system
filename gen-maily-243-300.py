"""Vygeneruje MAILY-243-300.md a MAILY-243-300.txt pro davku 243-300.

Navazuje na gen-maily-195-242.py / gen-maily-txt.py — stejny ton, stejna
struktura, stejny podpis. Rozdily:

  * sablona je `ukazka-1` (Dentaline styl), ne ukazka-2/3,
  * odstavec o rezervacnim formulari ma KAZDY mail (u minule davky az od
    12. dal) a popisuje formular tak, jak skutecne vypada na ukazka-1:
    1) novy / stavajici pacient -> 2) preferovany termin (od-do + cas)
    -> 3) kontakt (jmeno a prijmeni, telefon, e-mail, poznamka),
  * r. 265 (DENT company) web MA -> text na redesign.

Jmeno se nikde neskloňuje — jen nominativ v uvozovkach.

Spusteni:  python gen-maily-243-300.py
"""

import json
import re

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
BATCH = json.load(open("davka-243-300.json", encoding="utf-8"))

# Kdo v tabulce web MA -> jiny uhel (redesign, ne "nemate web").
HAS_WEB = {
    "dent-company": ("dentcompany.cz",
                     "v hlavním menu jsou odkazy na blogové články místo služeb "
                     "a objednání"),
}

SUBJECTS = [
    "Návrh webu pro vaši ordinaci",
    "Ukázka webu na míru",
    "Web pro vaši ordinaci",
    "Připravil jsem návrh webu",
    "Vlastní web místo katalogového profilu",
    "Návrh webové stránky",
    "Jak by mohl vypadat váš web",
    "Ukázka webu zdarma",
    "Web, který si pacient najde",
    "Návrh prezentace ordinace",
    "Web pro vaši ordinaci — návrh zdarma",
    "Ukázka: moderní web ordinace",
    "Vlastní web místo katalogu",
    "Návrh webu — bez závazku",
    "Web ordinace: ukázka na míru",
    "Jak by vás pacient našel online",
]


def subject_for(i, name):
    base = SUBJECTS[i % len(SUBJECTS)]
    if not re.match(r"^(MUDr|MDDr|MVDr|PhDr|Dr)\.", name) and len(name) <= 15:
        if "—" not in base and len(base) + len(name) + 3 <= 45:
            return f"{base} — {name}"
    return base


OPENERS = [
    "hledal jsem na internetu vaši ordinaci a našel jsem jen záznamy v lékařských\n"
    "katalozích. Vlastní web, kde by se pacient dozvěděl něco o vás a o ordinaci\n"
    "samotné, jsem nikde nenašel.",

    "díval jsem se, jak vás na internetu najde nový pacient. Vyšly mi jen profily\n"
    "v katalozích lékařů — všechny vypadají jinak a ani jeden nepůsobí jako vaše\n"
    "vlastní vizitka.",

    "všiml jsem si, že vaše ordinace nemá vlastní webovou stránku. Dnes je přitom\n"
    "web většinou první místo, kam se pacient podívá ještě předtím, než vůbec\n"
    "zvedne telefon.",

    "prohlížel jsem si zubní ordinace v okolí a u té vaší jsem nenarazil na vlastní\n"
    "web — jen na katalogové zápisy, které o ordinaci samotné neřeknou téměř nic.",

    "zkoušel jsem si najít web vaší ordinace a skončil jsem jen na obecných\n"
    "profilech v katalozích. Chybí tam fotky, ceník i možnost se objednat.",

    "když si dnes někdo hledá zubaře, většinou skončí na webu ordinace. U vás jsem\n"
    "ale žádný nenašel — jen zápisy v katalozích lékařů.",

    "všiml jsem si, že o vaší ordinaci se dá na internetu dohledat jen to, co je\n"
    "v katalogových profilech. Vlastní web, který by ordinaci představil, chybí.",

    "díval jsem se po webu vaší ordinace a nenašel ho. To je škoda — katalogový\n"
    "zápis neukáže ani ordinaci, ani to, čím se od ostatních lišíte.",
]

OPENER_REDESIGN = (
    "našel jsem web vaší ordinace ({web}). Základ tam je, ale {problem} —\n"
    "pacient, který se chce objednat, se k tomu prokliká jen těžko."
)

MIDDLES = [
    "Připravil jsem proto ukázku, jak by mohl web vypadat. Není to obecná šablona —\n"
    "je pojmenovaná přímo na vaši ordinaci, v titulku i v hlavičce stojí\n"
    "„{name}“:",

    "Připravil jsem ukázku na míru. V hlavičce i v titulku stránky je\n"
    "„{name}“, takže si rovnou uvidíte, jak by web působil:",

    "Zkusil jsem načrtnout, jak by to mohlo vypadat. Ukázka nese jméno vaší\n"
    "ordinace — „{name}“ — takže to není neutrální demo:",

    "Udělal jsem návrh přímo pro vás. Stránka je pojmenovaná „{name}“,\n"
    "včetně titulku v prohlížeči:",

    "Připravil jsem konkrétní ukázku, ne obecnou prezentaci. Web je pojmenovaný\n"
    "na „{name}“ a má sekce, které u zubní ordinace čekám:",

    "Sestavil jsem návrh, jak by web mohl fungovat. V hlavičce je\n"
    "„{name}“, ať vidíte reálný dojem, ne prázdnou šablonu:",

    "Připravil jsem ukázku pojmenovanou na „{name}“ — s přehledem\n"
    "služeb, kontaktem i místem na ceník:",

    "Zpracoval jsem návrh na míru vaší ordinaci. Stránka je vedená pod jménem\n"
    "„{name}“:",
]

# Odstavec o rezervaci — popisuje formular, ktery je na ukazce nasazeny:
# 1) novy/stavajici pacient  2) termin od-do + preferovany cas
# 3) jmeno a prijmeni, telefon, e-mail, poznamka
FORM = [
    "Není to jen webovka. Součástí je i online objednání — pacient řekne, jestli\n"
    "je nový nebo stávající, vybere termín, který mu vyhovuje, a nechá kontakt.\n"
    "V ukázce si to můžete rovnou proklikat.",

    "Nešlo by o pouhou vizitku. Web má i rezervační formulář: tři kroky (nový nebo\n"
    "stávající pacient → preferovaný termín → jméno, telefon a e-mail) a objednávka\n"
    "vám přijde se vším, co potřebujete vědět.",

    "Kromě webu je v ukázce i objednávkový formulář. Pacient se objedná sám, bez\n"
    "telefonu — vy dostanete jméno, kontakt i preferovaný termín. Co má formulář\n"
    "obsahovat, se dá nastavit přesně podle vaší ordinace.",

    "Web by uměl i rezervace. Formulář provede pacienta třemi kroky a na konci vám\n"
    "pošle poptávku s termínem a kontaktem. Jednotlivé kroky i políčka se dají\n"
    "nastavit podle vás.",

    "Není to jen prezentace. Je v tom i online objednání, které vám ubere telefonáty\n"
    "během ošetření — pacient si vybere termín a nechá na sebe kontakt, vy se\n"
    "ozvete, až se to hodí.",

    "Součástí je i rezervační formulář na míru — vy určíte, jaké termíny nabízet\n"
    "a co má pacient vyplnit, klidně i výběr konkrétního zákroku. V ukázce je\n"
    "funkční, klidně si ho vyzkoušejte.",

    "Web by nebyl jen na koukání. Pacient se přes něj objedná: vybere, jestli je\n"
    "u vás poprvé, zvolí termín a vyplní kontakt. Poznámku může připsat taky,\n"
    "takže rovnou víte, o co jde.",

    "Kromě samotného webu bych přidal online objednávání. Tři jednoduché kroky pro\n"
    "pacienta, pro vás jedna poptávka se jménem, telefonem, e-mailem a termínem.\n"
    "Rozsah polí se dá upravit podle toho, jak ordinujete.",
]

ATTACH = [
    "V příloze posílám i screenshot úvodní obrazovky, ať se nemusíte nikam\n"
    "proklikávat.",
    "Do přílohy jsem přidal screenshot úvodní stránky pro rychlou představu.",
    "V příloze je snímek úvodní obrazovky, ať vidíte návrh i bez otevírání odkazu.",
    "Přikládám screenshot hlavní stránky — odkaz je pak na plnou verzi.",
    "V příloze najdete náhled úvodní obrazovky.",
    "Screenshot úvodní stránky přikládám do přílohy.",
]

CLOSERS = [
    "Je to ukázka zdarma a bez jakéhokoli závazku. Pokud by se vám líbila, rád\n"
    "proberu detaily i úpravy na míru.",

    "Nic za to nechci a nikam se tím nezavazujete. Kdyby vás to zaujalo, ozvěte se\n"
    "a domluvíme se na úpravách podle vašich představ.",

    "Ukázka je zdarma a bez závazku. Když vám padne do oka, doladíme texty, fotky\n"
    "i barvy podle vás.",

    "Berte to jako ukázku zdarma, žádný závazek v tom není. Pokud by to pro vás\n"
    "mělo smysl, rád na tom dál zapracuji.",

    "Je to zdarma a bez závazku — kdyby se vám návrh zamlouval, ozvěte se a\n"
    "probereme, co upravit.",

    "Za ukázku nic neplatíte a k ničemu se nezavazujete. Kdyby vás zajímalo\n"
    "pokračování, napište nebo zavolejte.",
]

SIGNATURE = ["S pozdravem,", "David Král", "777 122 178", "fitego.cz"]

unwrap = lambda s: re.sub(r"\s+", " ", s.replace("\n", " ")).strip()


def parts(i, e):
    """Vrati (predmet, uvod, stred, formular, priloha, zaver) pro i-ty mail."""
    name = e["nazev"]
    if e["slug"] in HAS_WEB:
        web, problem = HAS_WEB[e["slug"]]
        opener = OPENER_REDESIGN.format(web=web, problem=problem)
    else:
        opener = OPENERS[(i * 3) % len(OPENERS)]
    return (subject_for(i, name),
            opener,
            MIDDLES[(i * 5) % len(MIDDLES)].format(name=name),
            FORM[(i * 3) % len(FORM)],
            ATTACH[(i * 7) % len(ATTACH)],
            CLOSERS[(i * 11) % len(CLOSERS)])


# ── .md verze ───────────────────────────────────────────────────────────
md = []
md.append("# MAILY — dávka 243–300 (45 ordinací, šablona `ukazka-1`)")
md.append("")
md.append("Odpovídá řádkům 243–300 Google Sheetu. Vynecháno 13 řádků —")
md.append("buď nemají žádné jméno (nejde pojmenovat web ani mail), nebo to")
md.append("není zubní ordinace (oční, gynekologie, praktik, zubní laboratoř).")
md.append("Seznam vynechaných vypíše `python gen-davka-243-300.py`.")
md.append("")
md.append("**Šablona:** všech 45 ukázek běží na `ukazka-1` — tedy tom stylu,")
md.append("který se používal na Dentaline (světlý, s fotkou přes celou")
md.append("obrazovku a rezervačním formulářem).")
md.append("")
md.append("**Komu:** je záměrně prázdné — v tabulce u těchto řádků žádné")
md.append("e-maily nejsou.")
md.append("")
md.append("> **Pozor:** ř. 265 (DENT company) web **má** (dentcompany.cz),")
md.append("> takže má text psaný na redesign. U ostatních 44 jsem web nenašel,")
md.append("> ale před odesláním se to hodí přeťuknout.")
md.append("")
md.append("---")
md.append("")

for i, e in enumerate(BATCH):
    subject, opener, middle, form, attach, closer = parts(i, e)
    url = MAN[e["slug"]]["url"]
    md.append(f"## {i + 1}. {e['nazev']}")
    md.append("")
    md.append(f"*řádek {e['radek']} · šablona `{e['sablona']}`"
              + ("  · **web MÁ — text na redesign**" if e["slug"] in HAS_WEB else "") + "*")
    md.append("")
    md.append("```")
    md.append("Komu:")
    md.append(f"Předmět: {subject}")
    md.append("")
    md.append("Dobrý den,")
    md.append("")
    for block in (opener, middle):
        md.append(block)
        md.append("")
    md.append(url)
    md.append("")
    for block in (form, attach, closer):
        md.append(block)
        md.append("")
    md.extend(SIGNATURE)
    md.append("```")
    md.append("")

open("MAILY-243-300.md", "w", encoding="utf-8").write("\n".join(md) + "\n")

# ── .txt verze (kazdy odstavec jeden radek, nic k prerovnavani) ──────────
txt = []
txt.append("MAILY — ordinace bez webu (45 leadu, radky 243-300 Google Sheetu)")
txt.append("=" * 70)
txt.append("")
txt.append("Navazuje na MAILY-195-242.txt — stejny ton, stejna struktura.")
txt.append("")
txt.append("Kazdy odstavec je jeden radek — po vlozeni do mailu se odstavce")
txt.append("nerozsypou a netreba nic prerovnavat.")
txt.append("")
txt.append("Adresata si vyplnte v mailovem klientovi; v tabulce u techto radku")
txt.append("zadne e-maily nejsou.")
txt.append("")
txt.append("Predmety jsou zamerne KRATKE a BEZ jmena adresata — na mobilu")
txt.append("se zobrazi jen ~40 znaku. Jmeno je v prvni casti tela, ktera")
txt.append("se zobrazuje v nahledu schranky.")
txt.append("")
txt.append("SABLONA: vsech 45 ukazek bezi na ukazka-1 (Dentaline styl).")
txt.append("")
txt.append("Odstavec o rezervaci ma KAZDY mail. Formular je na ukazce")
txt.append("skutecne nasazeny (overeno v kodu):")
txt.append("  1) Novy pacient / Stavajici pacient")
txt.append("  2) Preferovany termin (od-do) + preferovany cas")
txt.append("  3) Jmeno a prijmeni, telefon, e-mail, poznamka")
txt.append("  sekce se jmenuje 'Objednejte se online'")
txt.append("")
txt.append("POZOR — r. 265 (DENT company) web MA (dentcompany.cz), ma proto")
txt.append("text na redesign.")
txt.append("")

for i, e in enumerate(BATCH):
    subject, opener, middle, form, attach, closer = parts(i, e)
    txt.append("")
    txt.append("=" * 70)
    txt.append(f"{i + 1}. {e['nazev']}"
               + ("   [WEB MA - text na redesign]" if e["slug"] in HAS_WEB else ""))
    txt.append(f"   radek {e['radek']}")
    txt.append("=" * 70)
    txt.append("")
    txt.append("PREDMET ↓")
    txt.append(subject)
    txt.append("")
    txt.append("Dobrý den,")
    txt.append("")
    txt.append(unwrap(opener))
    txt.append("")
    txt.append(unwrap(middle))
    txt.append("")
    txt.append(MAN[e["slug"]]["url"])
    txt.append("")
    for block in (form, attach, closer):
        txt.append(unwrap(block))
        txt.append("")
    txt.extend(SIGNATURE)
    txt.append("")

open("MAILY-243-300.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")

# ── kontroly ────────────────────────────────────────────────────────────
body = open("MAILY-243-300.txt", encoding="utf-8").read()
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
    if "říloz" not in b and "řikládám" not in b and "říloh" not in b:
        problems.append(f"mail {k}: chybi zminka o priloze")
    if "fitego.cz" not in b:
        problems.append(f"mail {k}: chybi podpis")
for slug in ("Dentaline", "DomiDent"):
    if any(slug in b for b in bodies):
        problems.append(f"v textu mailu zbyl '{slug}'")

combos = {((i % 16), ((i * 3) % 8), ((i * 5) % 8), ((i * 3) % 8), ((i * 7) % 6),
           ((i * 11) % 6)) for i in range(len(BATCH))}
print(f"OK — MAILY-243-300.md + .txt, {len(BATCH)} mailu")
print(f"   unikatnich kombinaci variant: {len(combos)}/{len(BATCH)}")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
