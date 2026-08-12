"""Vygeneruje MAILY-WEB.md a MAILY-WEB.txt — leady, ktere uz nejaky web maji.

Uvod ma tri podoby podle toho, co o nich tabulka vi:

  1. katalogovy profil / Facebook misto vlastniho webu -> rekne se to primo,
  2. vlastni web + pouzitelna slabina z analyzy -> hacek se cituje,
  3. vlastni web bez pouzitelne slabiny -> neutralni uvod na redesign
     (radeji nic netvrdit, nez tvrdit neco, co si adresat overi).

Za "pouzitelnou" se nepovazuje analyza, ktera mluvi o HTML/kodu/semantice
(to zubar na svem webu nevidi), je anglicky, nebo rika neco, co se do
oslovujiciho mailu nehodi (nepriji;ma nove pacienty, konci provoz).

Textove pooly se beru z gen-maily-243-300.py, aby ton sedel s ostatnimi
davkami.

Spusteni:  python gen-maily-web.py
"""

import importlib.util
import json
import re

spec = importlib.util.spec_from_file_location("mg243", "gen-maily-243-300.py")
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

MAN = {e["slug"]: e for e in json.load(open("ordinace/manifest.json", encoding="utf-8"))}
BATCH = json.load(open("davka-web.json", encoding="utf-8"))

TECH = re.compile(r"HTML|k[óo]d|s[ée]mantick|verb[oó]|DOM|\bdiv\b|Schema\.org|CSS|"
                  r"JavaScript|nested|structure|markup|atribut|WPBakery|Elementor|"
                  r"jQuery|Drupal|WordPress", re.I)
EN = re.compile(r"\b(the|is|and|which|weakness|website|page|content)\b")
NEVHODNE = re.compile(r"nep[řr]ij[íi]m|kon[čc][íi]\s+provoz|[úu]mrt[íi]|zem[řr]el|"
                      r"nebyl poskytnut|object Object|nelze prov[ée]st|"
                      r"pro anal[ýy]zu", re.I)
# zargon, kteremu zubar nerozumi, + retezce, kde je v tabulce utrzene slovo
# nebo preklep ("vodní hero" = utnute 'Úvodní', "generé")
JARGON = re.compile(r"\bhero\b|\bSEO\b|Slider Revolution|TweenMax|\bCTA\b|\bUX\b|"
                    r"viewport|Schema|\bgener[ée]\b|responzivit|\bvodn[íi]\s", re.I)

KATALOG_OPENERS = [
    "hledal jsem web vaší ordinace a našel jsem jen profil na {domena}. Ten vypadá\n"
    "u všech ordinací stejně a o té vaší toho moc neřekne.",

    "díval jsem se, jak vás na internetu najde nový pacient. Vyšel mi jen záznam\n"
    "na {domena} — žádný vlastní web, kde by se dozvěděl něco o vás a o ordinaci.",

    "vaši ordinaci jsem na internetu našel jen přes {domena}. Katalogový profil je\n"
    "lepší než nic, ale nemáte v něm ani fotky ordinace, ani možnost se objednat.",

    "když si dnes někdo hledá zubaře, většinou skončí na webu ordinace. U vás jsem\n"
    "narazil jen na profil na {domena} — vlastní web jsem nenašel.",
]

WEB_HACEK = [
    "prošel jsem si web vaší ordinace ({domena}). Funguje, ale všiml jsem si jedné\n"
    "věci: {hacek}",

    "díval jsem se na web vaší ordinace ({domena}). Základ tam je, ale zarazilo mě\n"
    "tohle: {hacek}",

    "koukal jsem na web vaší ordinace ({domena}) očima pacienta, který vás vidí\n"
    "poprvé. Jedna věc mi tam vadila: {hacek}",
]

WEB_NEUTRAL = [
    "našel jsem web vaší ordinace ({domena}). Funguje, ale vzhledem i chováním na\n"
    "mobilu už za dnešními weby ordinací zaostává — a to je první dojem, který\n"
    "o vás nový pacient udělá.",

    "prohlédl jsem si web vaší ordinace ({domena}). Obsah tam je, ale forma působí\n"
    "starším dojmem, než jakou péči podle všeho odvádíte.",

    "díval jsem se na web vaší ordinace ({domena}). Není na něm nic špatně, jen už\n"
    "vypadá jako z jiné doby — a pacient si dnes vybírá i podle toho.",
]


def hacek(e):
    """Slabina z tabulky prevedena na jednu vetu do mailu, nebo None."""
    a = " ".join(e.get("analyza", "").split())
    if len(a) < 30 or EN.search(a) or TECH.search(a) or NEVHODNE.search(a) or JARGON.search(a):
        return None
    veta = re.split(r"(?<=[.!?])\s", a)[0].strip()
    if len(veta) < 30 or len(veta) > 190:
        return None
    # cast analyz je v tabulce bez diakritiky — takovy text se do mailu dat neda
    if sum(c in "áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ" for c in veta) < len(veta) / 25:
        return None
    # "Hlavní slabinou webu je X" -> "X" (v mailu to jinak zni jako posudek)
    veta = re.sub(r"^Hlavn[íi]\s+slabin[ao]u?\s+(webu\s+|str[áa]nky\s+)?(je|jsou)\s+",
                  "", veta, flags=re.I)
    veta = veta[0].lower() + veta[1:]
    return veta if veta.endswith(".") else veta + "."


# Rucne psane uvody tam, kde zadna ze tri variant nesedi.
CUSTOM_OPENER = {
    726: "hledal jsem web vaší ordinace a zjistil jsem, že vlastní nemáte — jste\n"
         "podstránkou webu lékárny Alfa (alfafarm.cz). Pacient, který hledá zubaře,\n"
         "se k vám takhle dostane spíš náhodou.",
}


def parts(i, e):
    d = e["domena"]
    if e["radek"] in CUSTOM_OPENER:
        opener = CUSTOM_OPENER[e["radek"]]
    elif e["typ"] == "katalog":
        opener = KATALOG_OPENERS[i % len(KATALOG_OPENERS)].format(domena=d)
    else:
        h = hacek(e)
        if h:
            opener = WEB_HACEK[i % len(WEB_HACEK)].format(domena=d, hacek=h)
        else:
            opener = WEB_NEUTRAL[i % len(WEB_NEUTRAL)].format(domena=d)
    return mg.subject_for(i, e["nazev"]), [
        opener,
        mg.MIDDLES[(i * 5) % len(mg.MIDDLES)].format(name=e["nazev"]),
        "__URL__",
        mg.FORM[(i * 3) % len(mg.FORM)],
        mg.ATTACH[(i * 7) % len(mg.ATTACH)],
        mg.CLOSERS[(i * 11) % len(mg.CLOSERS)],
    ]


kat = sum(1 for e in BATCH if e["typ"] == "katalog")
sh = sum(1 for e in BATCH if e["typ"] != "katalog" and hacek(e))
mails = sum(1 for e in BATCH if e["email"])

md = [f"# MAILY — leady s webem ({len(BATCH)} ordinací, šablona `ukazka-1`)", "",
      "Na rozdíl od předchozích dávek tyhle ordinace **nějaký web mají**, takže",
      "text nemůže tvrdit „nemáte web“. Úvod má tři podoby:", "",
      f"- **{kat}× jen katalogový profil / Facebook** (znamylekar.cz, oteviracka.cz,",
      "  katalog-stomatologu.cz…) — v mailu je to řečeno přímo,",
      f"- **{sh}× vlastní web + konkrétní háček** ze sloupce s analýzou (jen tam,",
      "  kde je to něco, co adresát na svém webu opravdu uvidí),",
      f"- **{len(BATCH) - kat - sh}× vlastní web bez použitelného háčku** — neutrální",
      "  úvod na redesign, radši nic netvrdit než tvrdit něco ověřitelně mimo.", "",
      f"**Komu:** předvyplněno u **{mails}** ordinací, které mají e-mail v tabulce.", "",
      "U každého mailu je číslo řádku v tabulce.", "", "---", ""]

for i, e in enumerate(BATCH):
    subject, blocks = parts(i, e)
    url = MAN[e["slug"]]["url"]
    md.append(f"## {i + 1}. {e['nazev']}")
    md.append("")
    md.append(f"*řádek {e['radek']} · {e['domena']} · "
              + ("jen katalogový profil" if e["typ"] == "katalog" else "vlastní web") + "*")
    md.append("")
    md.append("```")
    md.append(f"Komu: {e['email']}")
    md.append(f"Předmět: {subject}")
    md.append("")
    md.append("Dobrý den,")
    md.append("")
    for block in blocks:
        md.append(url if block == "__URL__" else block)
        md.append("")
    md.extend(mg.SIGNATURE)
    md.append("```")
    md.append("")

open("MAILY-WEB.md", "w", encoding="utf-8").write("\n".join(md) + "\n")

txt = [f"MAILY — leady, ktere UZ WEB MAJI ({len(BATCH)} leadu)", "=" * 70, "",
       "Pozor: tyhle ordinace nejaky web maji, takze zadny mail netvrdi",
       "'nemate web'. Uvod ma tri podoby:",
       f"  {kat}x  jen katalogovy profil / Facebook -> rekne se to primo",
       f"  {sh}x  vlastni web + konkretni hacek z analyzy v tabulce",
       f"  {len(BATCH) - kat - sh}x  vlastni web bez pouzitelneho hacku -> neutralni uvod", "",
       f"KOMU je predvyplnene u {mails} ordinaci, ktere maji e-mail v tabulce.", "",
       "U kazdeho mailu je cislo radku v tabulce a domena, o ktere se v nem",
       "mluvi — pred odeslanim se hodi ji rychle otevrit a hacek preticknout.", "",
       "Kazdy odstavec je jeden radek — po vlozeni do mailu se nic nerozsype.", "",
       "SABLONA: vsechny ukazky bezi na ukazka-1 (Dentaline styl).", ""]

for i, e in enumerate(BATCH):
    subject, blocks = parts(i, e)
    txt.append("")
    txt.append("=" * 70)
    txt.append(f"{i + 1}. {e['nazev']}"
               + ("   [JEN KATALOGOVY PROFIL]" if e["typ"] == "katalog" else "   [MA WEB]"))
    txt.append(f"   radek {e['radek']} · {e['domena']}")
    txt.append("=" * 70)
    txt.append("")
    if e["email"]:
        txt.append("KOMU ↓")
        txt.append(e["email"])
        txt.append("")
    txt.append("PREDMET ↓")
    txt.append(subject)
    txt.append("")
    txt.append("Dobrý den,")
    txt.append("")
    for block in blocks:
        txt.append(MAN[e["slug"]]["url"] if block == "__URL__" else mg.unwrap(block))
        txt.append("")
    txt.extend(mg.SIGNATURE)
    txt.append("")

open("MAILY-WEB.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")

# ── kontroly ────────────────────────────────────────────────────────────
body = open("MAILY-WEB.txt", encoding="utf-8").read()
lines = body.split("\n")
starts = [k for k, ln in enumerate(lines) if re.match(r"^\d+\. \S", ln)]
bodies = ["\n".join(lines[k:(starts[n + 1] if n + 1 < len(starts) else len(lines))])
          for n, k in enumerate(starts)]

problems = []
if len(bodies) != len(BATCH):
    problems.append(f"rozdeleno {len(bodies)} mailu, ocekavano {len(BATCH)}")
for e, b in zip(BATCH, bodies):
    if "PREDMET ↓" not in b or "fitego.cz" not in b:
        problems.append(f"r.{e['radek']}: chybi predmet nebo podpis")
    if MAN[e["slug"]]["url"] not in b:
        problems.append(f"r.{e['radek']}: chybi odkaz")
    if not re.search(r"rezerva|objedn", b, re.I):
        problems.append(f"r.{e['radek']}: chybi odstavec o rezervaci")
    # nikdo z teto davky nesmi dostat "web jsem nenasel" o vlastnim webu
    if e["typ"] != "katalog" and e["radek"] not in CUSTOM_OPENER \
            and re.search(r"nena[šs]el jsem|nem[áa] vlastn[íi] web|web.{0,12}chyb[íi]",
                          b, re.I):
        problems.append(f"r.{e['radek']}: text tvrdi, ze web nema")
    if e["domena"] not in b:
        problems.append(f"r.{e['radek']}: chybi zminka domeny")

print(f"OK — MAILY-WEB.md + .txt, {len(BATCH)} mailu "
      f"({kat} katalog, {sh} s hackem, {len(BATCH)-kat-sh} neutralnich, {mails} s adresou)")
print("   problemy: " + ("; ".join(problems) if problems else "zadne"))
