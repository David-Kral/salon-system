"""Vygeneruje LEADY-VSECHNY.md — sjednocený seznam všech 40 leadů.

Odkazy se berou z ordinace/manifest.json, takže nemůžou rozejít se
skutečně vygenerovanými stránkami.

Spuštění:  python gen-leady.py
"""

import json

man = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}

EMAIL = {
    "bhl-dent": "info@bhl-dent.cz",
    "libento": "recepce@libento.cz",
    "galaxy-dent": "galaxydent.sro@gmail.com",
    "lfdent-olomouc": "info@vaskrasnyusmev.cz",
    "centrum-zubni-mediciny": "info@dentaldesign.cz",
    "stomchir-olomouc": "recepce@stomchircentrum.cz",
    "dent-klinika": "info@kamenicekstoma.cz",
    "dental-sphere": "recepce@dentalsphere.cz",
    "jiri-prochazka": "mddr.prochazka@gmail.com",
    "art-medica": "objednani.artmedica@centrum.cz",
    "bistrodent": "ordinace@bistrodent.cz",
    "grmela-dent": "jiri.grmela@seznam.cz",
    "proeste-dent": "info@proeste.cz",
    "jtb-dent": "info@jtbdental.cz",
    "holice-dent": "recepce@stomaholice.cz",
    "svec-dent": "ordinace@zubnisvec.cz",
    "jsmile-dent": "jsmilestomatologie@gmail.com",
    "perioimplants": "recepce@collegiumdentalis.cz",
    "janda-dent": "Premysl.Janda@seznam.cz",
}

Q = "„"   # „
QE = "“"  # “

# (slug, web dnes, problem) — poradi = poradi oslovovani
LEADS = [
    ("stajner-dent", "stomatologiestajner.webmium.com", "Doména vrací 404 — web fakticky neexistuje."),
    ("bistrodent", "bistrodent.cz", "Holé HTML bez CSS stylů + zastaralé upozornění z dubna 2025."),
    ("vranova-dent", "znamylekar.cz (profil)", "Nemá vlastní web, chybí rezervační kalendář i ceník."),
    ("drdent-zlin", "drdentzlin.cz", "Výchozí nenastavená instalace WordPressu s " + Q + "Hello world!" + QE + "."),
    ("klimesova-dent", "olomouc-zubni.cz", "Doména nefunguje jako vlastní web, jen katalogový profil."),
    ("chmiel-dent", "katalog-stomatologu.cz", "Jen obecný katalogový profil; nepřijímá nové pacienty."),
    ("odstrcilova-dent", "katalog-stomatologu.cz", "Generický katalogový profil bez vlastní identity."),
    ("ulman-siblova-dent", "katalog-stomatologu.cz", "Generický profil; nepřijímají nové pacienty."),
    ("reli-dent", "stomatolog.cz/reli", "Statický XHTML z roku 2021, tabulkový layout."),
    ("dentista-zlin", "dentistazlin.cz", "Opakující se navigace, chybí online rezervace."),
    ("zdena-sykorova", "tylovka.cz", "Funkční, ale designově zastaralý a velmi strohý web."),
    ("hygiena-louny", "hygiena-dentalni.cz", "Starší WordPress bez aktualizací."),
    ("lukas-milic", "milic.cz", "Web vrací chybu 500."),
    ("zubni-ordinace", "zubni-ordinace.eu", "Doména nedostupná."),
    ("hygiena-decin", "zubnihygienadecin.cz", "Doména neodpovídá."),
    ("hygiena-podebrady", "hygienistkapdy.cz", "Doména neodpovídá."),
    ("bhl-dent", "bhl-dent.cz", "Vizuálně uhlazené, ale texty hodně obecné a generické."),
    ("libento", "libento.cz", "Nefunkční obrázkový slider na úvodní ploše."),
    ("galaxy-dent", "(vlastní řešení)", "Chybí veřejně dostupný ceník."),
    ("lfdent-olomouc", "vaskrasnyusmev.cz", "Úvodní stránka váží přes 3 MB — pomalé na mobilu."),
    ("centrum-zubni-mediciny", "dentaldesign.cz", "Přesměrovává na caiaclinic.cz, zubař je až podstránka."),
    ("stomchir-olomouc", "stomchircentrum.cz", "WordPress + Divi, těžký kód, pomalé načítání."),
    ("dent-klinika", "kamenicekstoma.cz", "Postavené na Elementoru — těžký kód, horší SEO."),
    ("dental-sphere", "dentalsphere.cz", "Divi builder — těžký kód, dopad na rychlost a SEO."),
    ("jiri-prochazka", "(žádný)", "Nemá vlastní webovou prezentaci."),
    ("art-medica", "(vlastní)", "Nepřijímá pacienty; projekty (Zubařská školka) zaslouží víc prostoru."),
    ("proeste-dent", "proeste.cz", "Údaj o promoci lékaře až v roce 2026 může mást pacienty."),
    ("jtb-dent", "jtbdental.cz", "Dvě různé e-mailové adresy v kontaktní sekci."),
    ("holice-dent", "stomaholice.cz", "Meta viewport blokuje přiblížení (user-scalable=0)."),
    ("svec-dent", "zubnisvec.cz", "Info o nepřijímání pacientů splývá s textem; strohý Wix."),
    ("jsmile-dent", "jsmile.cz", "Neutrální béžová paleta bez brandového akcentu."),
    ("perioimplants", "perioimplants.cz", "Načítá dvě verze jQuery současně — zbytečné zpomalení."),
    ("janda-dent", "zubarjanda.cz", "Objednání jen obecným formulářem, žádný výběr termínu."),
    ("orthozlin", "ortodonciezlin.cz", "Překlep v titulku (" + Q + "Ortodonice" + QE + ") + žádný objednávkový formulář."),
    ("wistdental", "wistdental.cz", "Chybné kódování znaků — rozbitá diakritika."),
    ("pruckova-dent", "(žádný)", "Bez vlastního webu — jen katalogové profily."),
    ("grmela-dent", "(žádný)", "Bez vlastního webu — jen katalogové profily."),
    ("kuca-dent", "(žádný)", "ZUBOSANA bez vlastního webu, chybí i online rezervace."),
    ("bradacova-dent", "(žádný)", "Firma s vlastním jménem, ale bez vlastního webu."),
    ("hanos-dent", "katalog-stomatologu.cz", "Jen strojově generovaný profil, bez fotek a ceníku."),
]

TPL = {
    "ukazka-1": "Návrh 1",
    "ukazka-2": "Návrh 2 (prémiový)",
    "ukazka-3": "Návrh 3 (rezervace)",
}
ALT = {"stajner-dent": "rene-stajner", "vranova-dent": "ladislava-vranova"}

o = []
o.append("# LEADY ZUBAŘI — všech 40 na jednom místě")
o.append("")
o.append("Sjednocení všech dávek (dřív rozházené v `leady-zubari-*.txt`,")
o.append("`maily-zubari-*.txt` a `e-maily-zubari.docx`). Texty mailů zůstávají")
o.append("v původních souborech — **tady je seznam a nové odkazy.**")
o.append("")
o.append("## Co se změnilo v odkazech")
o.append("")
o.append("Dřív: `ukazka-N/?studio=<slug>` — jméno ordinace doplnil až JavaScript,")
o.append("takže statický titulek stránky (a tím i náhled odkazu v mailu nebo na")
o.append("WhatsAppu) hlásil `Dentaline` / `DomiDent`.")
o.append("")
o.append("Teď má **každá ordinace vlastní stránku** se svým jménem už ve statickém")
o.append("HTML (titulek, description, OG náhled) a bez `?studio=` v adrese:")
o.append("")
o.append("```")
o.append("https://david-kral.github.io/salon-system/ordinace/<slug>/")
o.append("```")
o.append("")
o.append("Staré odkazy `ukazka-N/?studio=<slug>` **fungují dál** — už rozeslané maily")
o.append("se nerozbily. Pro nové oslovení používej ty nové.")
o.append("")
o.append("Regenerace: `node patch-bundly.mjs && node gen-ordinace.mjs && python gen-leady.py`")
o.append("")
o.append("## Přehled")
o.append("")
o.append("| # | Ordinace | Šablona | E-mail | Odkaz |")
o.append("|--:|----------|---------|--------|-------|")
for i, (slug, web, prob) in enumerate(LEADS, 1):
    e = man[slug]
    o.append(f"| {i} | {e['nazev']} | {TPL[e['sablona']]} | {EMAIL.get(slug, '—')} | {e['url']} |")

have = sum(1 for s, _, _ in LEADS if s in EMAIL)
o.append("")
o.append(f"**E-mail znám u {have} ze 40**, u zbylých {40 - have} je potřeba dohledat.")
o.append("")
o.append("## Detail")
o.append("")
for i, (slug, web, prob) in enumerate(LEADS, 1):
    e = man[slug]
    o.append(f"### {i}. {e['nazev']}")
    o.append("")
    o.append(f"- **Web dnes:** {web}")
    o.append(f"- **Problém:** {prob}")
    o.append(f"- **E-mail:** {EMAIL.get(slug, '_nedohledán_')}")
    o.append(f"- **Šablona:** {TPL[e['sablona']]} (`{e['sablona']}`)")
    o.append(f"- **Ukázka:** {e['url']}")
    if slug in ALT:
        o.append(f"- _Pozn.: pro stejného zubaře existuje i slug `{ALT[slug]}` (jiná šablona) — posílej jen jeden._")
    o.append("")

o.append("---")
o.append("")
o.append("## Nepoužité slugy")
o.append("")
o.append("V `ordinace/` je 44 stránek, ale leadů je 40:")
o.append("")
o.append("- `petr-seda`, `usmev-jana` — ukázková/dokumentační studia, ne skuteční leadi.")
o.append("- `rene-stajner`, `ladislava-vranova` — druhá varianta šablony pro zubaře,")
o.append("  kteří už v seznamu jsou (`stajner-dent`, `vranova-dent`).")

open("LEADY-VSECHNY.md", "w", encoding="utf-8").write("\n".join(o) + "\n")
print(f"OK — leadu: {len(LEADS)}, s e-mailem: {have}")
