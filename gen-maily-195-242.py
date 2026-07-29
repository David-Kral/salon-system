"""Vygeneruje MAILY-195-242.md — text + predmet pro kazdy lead z davky 195-242.

Kazdy mail se sklada z rotujicich variant (predmet / uvod / stred / priloha /
zaver), takze zadne dva nejsou stejne, ale drzi stejny ton.

Jmeno se nikde neskloňuje — pouziva se jen v nominativu (v predmetu za
pomlckou a v tele v uvozovkach). Diky tomu text funguje pro osoby
("MUDr. Ladislava Michnova") i pro firmy ("JaRo Dent") bez gramatickych chyb.

Spusteni:  python gen-maily-195-242.py
"""

import json

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
BATCH = json.load(open("davka-195-242.json", encoding="utf-8"))

# Overeno naziva: tihle dva vlastni web MAJI -> jiny uhel (redesign, ne "nemate web")
HAS_WEB = {
    "mrozovsky-dent": "ordinace-sumbark.webnode.cz",
    "dentalni-hygiena-havirov": "dentalni-hygiena-havirov.webnode.cz",
}

SUBJECTS = [
    "Návrh webu pro vaši ordinaci — {name}",
    "Ukázka webu na míru — {name}",
    "Web pro vaši ordinaci — {name}",
    "Připravil jsem návrh webu — {name}",
    "Vlastní web místo katalogového profilu — {name}",
    "Návrh webové stránky — {name}",
    "Jak by mohl vypadat váš web — {name}",
    "Ukázka zdarma: web pro vaši ordinaci — {name}",
    "Web, který si pacient najde — {name}",
    "Návrh prezentace ordinace — {name}",
]

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

OPENERS_REDESIGN = [
    "narazil jsem na web vaší ordinace ({web}). Funguje, ale je postavený\n"
    "na stavebnici Webnode a designem už dost zaostává za tím, co dnes pacient\n"
    "od zdravotnického webu čeká.",

    "našel jsem web vaší ordinace ({web}). Základ tam je, ale běží\n"
    "na šablonové stavebnici a vizuálně působí staromódně — na první dojem\n"
    "u nového pacienta je to zbytečná ztráta.",
]

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

SIGNATURE = "S pozdravem,\nDavid Král\n777 122 178\nfitego.cz"

out = []
out.append("# MAILY — dávka 195–242 (46 ordinací bez webu)")
out.append("")
out.append("Odpovídá řádkům 194–242 Google Sheetu. Vynecháno:")
out.append("")
out.append("- **ř. 194** — není ordinace, ale poznámka v tabulce")
out.append("  („Přesné maily a návrhy webu, přesně co napsat od řádku 190.“)")
out.append("- **ř. 207** („Odborný lékař stomatolog“) a **ř. 219** („Odborný lékař")
out.append("  stomatologie, ortodoncie“) — nemají v tabulce žádné jméno, takže")
out.append("  nejde pojmenovat ani web, ani mail.")
out.append("")
out.append("Zbývá **46 leadů**. Každý má vlastní stránku a vlastní text —")
out.append("předmět, úvod, střed, zmínka o příloze i závěr rotují, takže žádné")
out.append("dva maily nejsou stejné.")
out.append("")
out.append("**Komu:** je záměrně prázdné — adresy si dohledáváte sám. V tabulce")
out.append("u těchto řádků žádné nejsou.")
out.append("")
out.append("**Šablony:** použité jen `ukazka-2` (tmavá prémiová) a `ukazka-3`")
out.append("(teplá krémová s ceníkem a rezervací). `ukazka-1` (světle modrý styl")
out.append("s fotkou přes celou obrazovku) se záměrně nepoužívá.")
out.append("")
out.append("> **Pozor u dvou leadů:** ř. 195 (MUDr. Andělin Mrozovský) a ř. 204")
out.append("> (Dentální hygiena Havířov) vlastní web **mají** — ověřeno naživo.")
out.append("> Mají proto text psaný na redesign, ne na „nemáte web“. U ostatních")
out.append("> 44 jsem web nenašel, ale před odesláním se to hodí přeťuknout.")
out.append("")
out.append("---")
out.append("")

for i, e in enumerate(BATCH):
    name = e["nazev"]
    url = MAN[e["slug"]]["url"]
    redesign = e["slug"] in HAS_WEB

    subject = SUBJECTS[i % len(SUBJECTS)].format(name=name)
    if redesign:
        opener = OPENERS_REDESIGN[list(HAS_WEB).index(e["slug"]) % len(OPENERS_REDESIGN)]
        opener = opener.format(web=HAS_WEB[e["slug"]])
    else:
        opener = OPENERS[(i * 3) % len(OPENERS)]
    middle = MIDDLES[(i * 5) % len(MIDDLES)].format(name=name)
    attach = ATTACH[(i * 7) % len(ATTACH)]
    closer = CLOSERS[(i * 11) % len(CLOSERS)]

    out.append(f"## {i + 1}. {name}")
    out.append("")
    out.append(f"*řádek {e['radek']} · šablona `{e['sablona']}`"
               + ("  · **web MÁ — text na redesign**" if redesign else "") + "*")
    out.append("")
    out.append("```")
    out.append("Komu:")
    out.append(f"Předmět: {subject}")
    out.append("")
    out.append("Dobrý den,")
    out.append("")
    out.append(opener)
    out.append("")
    out.append(middle)
    out.append("")
    out.append(url)
    out.append("")
    out.append(attach)
    out.append("")
    out.append(closer)
    out.append("")
    out.append(SIGNATURE)
    out.append("```")
    out.append("")

open("MAILY-195-242.md", "w", encoding="utf-8").write("\n".join(out) + "\n")

# kontrola variability
combos = {((i % 10), ((i * 3) % 8), ((i * 5) % 8), ((i * 7) % 6), ((i * 11) % 6))
          for i in range(len(BATCH))}
print(f"OK — {len(BATCH)} mailu, unikatnich kombinaci variant: {len(combos)}/{len(BATCH)}")
print(f"     redesign varianta u: {', '.join(HAS_WEB)}")
