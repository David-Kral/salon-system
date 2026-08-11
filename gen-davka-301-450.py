"""Z radku 301-450 Google Sheetu vyrobi studia na sablone ukazka-1.

Navazuje na gen-davka-243-300.py — stejny princip, stejna sablona.

POZOR: radky 414-447 jsou v tabulce DUPLICITA radku 380-413 (stejna jmena
ve stejnem poradi, jen poradi 410/411 je prohozene). Jsou proto vynechane,
jinak by stejna ordinace dostala dva ruzne weby a dva maily.

Spusteni:  python gen-davka-301-450.py
"""

import csv
import json
import os

ROWS = (301, 450)
TEMPLATE = "ukazka-1"

SKIP = {
    335: "Stomatolog Ceske Budejovice — zadne jmeno",
    338: "MUDr. Vodickova — lekarka site klinik EUC, vlastni web neresi",
    341: "Poliklinika Prazska — zadne jmeno ordinace",
    345: "Matice Skolske 1786/17 — adresa, ne nazev",
    348: "Стоматология — zadne jmeno",
    365: "Stomatologicka protetika — zadne jmeno",
    382: "Soukroma zubni ordinace Usti nad Labem — zadne jmeno",
    391: "KERA-DENS — zubni laborator, pacienty neobjednava",
    398: "Stomatologicka laborator — laborator bez jmena",
    405: "Ord. praktickeho lekare stomatologa — zadne jmeno",
    406: "Ord. praktickeho lekare stomatologa — zadne jmeno",
    408: "Ortodoncie, zubni laborator — zadne jmeno",
    409: "MUDr. Michalek — neurologie, ne zubar",
    411: "Zubni Peml — duplicita r. 395 (MUDr. Ladislav Peml)",
    412: "Ord. praktickeho lekare pro dospele — zadne jmeno",
}
# radky 414-447 = duplicita 380-413
SKIP.update({n: f"duplicita radku {n - 34}" for n in range(414, 448)})

# E-maily, ktere v tabulce u techto radku jsou (jinde chybi).
EMAILS = {
    303: "info@drtondrova.cz",
    352: "info@hi-dentistry.cz",
    370: "info@dentry.cz",
    371: "info@clinic-plus.cz",
}

OVERRIDE = {
    301: ("MUDr. Miroslav Valha", "valha-dent"),
    302: ("Endivia dent", "endivia-dent"),
    303: ("MDDr. Andrea Tondrová", "tondrova-dent"),
    304: ("MDDr. Miroslav Bísek", "bisek-dent"),
    305: ("UB Dent", "ub-dent"),
    306: ("MUDr. Mirek Musil", "musil-dent"),
    307: ("MUDr. Zdeněk Tesař", "tesar-dent"),
    308: ("MUDr. Radmila Trávníčková", "travnickova-dent"),
    309: ("MDDr. Petra Kováříková", "kovarikova-dent"),
    310: ("MUDr. Michaela Kotyzová", "kotyzova-dent"),
    311: ("ELZET DENTAL", "elzet-dental"),
    312: ("MUDr. Lenka Kuriálová", "kurialova-dent"),
    313: ("Miloslava Truszyková", "truszykova-dent"),
    314: ("MUDr. Ludmila Krátká", "kratka-ludmila-dent"),
    315: ("MUDr. Radmila Jáchymová", "jachymova-dent"),
    316: ("MDDr. Radovana Plochová", "plochova-dent"),
    317: ("MUDr. Marie Mácová", "macova-dent"),
    318: ("MUDr. Olga Krejcarová", "krejcarova-dent"),
    319: ("MUDr. Hana Panochová", "panochova-dent"),
    320: ("MUDr. Zuzana Vystrčilová", "vystrcilova-dent"),
    321: ("MUDr. Miroslav Červený", "cerveny-dent"),
    322: ("MUDr. Milada Kubušová", "kubusova-dent"),
    323: ("MUDr. Iva Michalová a MUDr. Pavla Herrmannová", "michalova-herrmannova-dent"),
    324: ("MUDr. Petr Kulovaný", "kulovany-dent"),
    325: ("MUDr. Ján Bočkay", "bockay-dent"),
    326: ("MUDr. Ivana Škodová", "skodova-dent"),
    327: ("Kulvadent", "kulvadent"),
    328: ("MUDr. Václav Rezek", "rezek-dent"),
    329: ("MUDr. Petra Pragerová", "pragerova-dent"),
    330: ("MUDr. Tomáš Bulan", "bulan-dent"),
    331: ("MUDr. Blanka Jakubcová-Sýkorová", "jakubcova-sykorova-dent"),
    332: ("MUDr. Štěpánka Nádravská", "nadravska-dent"),
    333: ("MUDr. Ladislav Dolanský", "dolansky-dent"),
    334: ("MUDr. Eva Vurmová", "vurmova-dent"),
    336: ("Dětská zubní společnost", "detska-zubni-spolecnost"),
    337: ("MUDr. Soňa Hüttnerová", "huttnerova-dent"),
    339: ("MUDr. Libor Zdařil", "zdaril-dent"),
    340: ("MUDr. Petr Jindra, Ph.D.", "jindra-dent"),
    342: ("MUDr. Stanislav Ryčovský", "rycovsky-dent"),
    343: ("MUDr. Anatolij Micaj", "micaj-dent"),
    344: ("MUDr. Petr Peška", "peska-dent"),
    346: ("MUDr. Olga Stecherová", "stecherova-dent"),
    347: ("MUDr. Josef Dvořák", "dvorak-dent"),
    349: ("MUDr. Daniela Frommová", "frommova-dent"),
    350: ("MUDr. Terézie Marešová", "maresova-dent"),
    351: ("MUDr. Jana Vališová", "valisova-dent"),
    352: ("HI.Dentistry", "hi-dentistry"),
    353: ("Majada", "majada-dent"),
    354: ("MUDr. Marcela Potyšová", "potysova-dent"),
    355: ("MUDr. Pavla Ježková", "jezkova-dent"),
    356: ("MUDr. Zdena Sádlová", "sadlova-dent"),
    357: ("MUDr. Hana Kučerová", "kucerova-dent"),
    358: ("MUDr. Hana Voldřichová", "voldrichova-dent"),
    359: ("MUDr. Jana Česánková", "cesankova-dent"),
    360: ("MUDr. Olga Kabátová", "kabatova-dent"),
    361: ("Daniela Šindlerová", "sindlerova-dent"),
    362: ("Dentio Strakonice", "dentio-strakonice"),
    363: ("MUDr. Karel Karas", "karas-dent"),
    364: ("MUDr. Marie Thöndlová", "thondlova-dent"),
    366: ("MUDr. Jana Vlachová", "vlachova-dent"),
    367: ("MUDr. Jitka Hradecká", "hradecka-dent"),
    368: ("MUDr. Dana Tušková", "tuskova-dent"),
    369: ("MUDr. Jaroslav Mareš", "mares-dent"),
    370: ("Dentry", "dentry"),
    371: ("CLINIC+", "clinic-plus"),
    372: ("MDDr. Pavel Fidler", "fidler-dent"),
    373: ("MUDr. Vladimíra Strnadová", "strnadova-dent"),
    374: ("MUDr. Ivana Otavová", "otavova-dent"),
    375: ("Stomat", "stomat-dent"),
    376: ("MUDr. Helena Šprinclová", "sprinclova-dent"),
    377: ("MUDr. Aleš Leger", "leger-dent"),
    378: ("MUDr. Karel Votava", "votava-dent"),
    379: ("MUDr. Martin Theimer", "theimer-dent"),
    380: ("3Mdent", "3mdent"),
    381: ("MUDr. Jana Dvořáková", "dvorakova-dent"),
    383: ("MUDr. Jan Münster", "munster-dent"),
    384: ("MUDr. Alexandra Cermanová", "cermanova-dent"),
    385: ("BlackDental", "blackdental"),
    386: ("MUDr. Aleš Zýka", "zyka-dent"),
    387: ("Zubní ordinace Kačírek", "kacirek-dent"),
    388: ("MUDr. Bohumila Domorádová", "domoradova-dent"),
    389: ("Dentcom", "dentcom"),
    390: ("MUDr. Milan Čabrádek", "cabradek-dent"),
    392: ("MUDr. Jiřina Sedláčková", "sedlackova-jirina-dent"),
    393: ("MUDr. Helena Szabóová", "szaboova-dent"),
    394: ("MUDr. Blanka Nalosová", "nalosova-dent"),
    395: ("MUDr. Ladislav Peml", "peml-dent"),
    396: ("MUDr. Alena Klapková", "klapkova-dent"),
    397: ("MUDr. Olga Jizerová", "jizerova-dent"),
    399: ("MUDr. Iva Kačírková", "kacirkova-dent"),
    400: ("MUDr. Ivan Fryček", "frycek-dent"),
    401: ("MUDr. Marie Klančíková", "klancikova-dent"),
    402: ("Studio Dent", "studio-dent"),
    403: ("Dentis", "dentis"),
    404: ("ULDENTA", "uldenta"),
    407: ("MUDr. Alena Havránková", "havrankova-dent"),
    410: ("MUDr. Radka Charouzdová", "charouzdova-dent"),
    413: ("MUDr. Jan Nebáznivý", "nebaznivy-dent"),
    448: ("MUDr. Jana Šolcová", "solcova-dent"),
    449: ("MUDr. Monika Budínová", "budinova-dent"),
    450: ("Zubní centrum Kronusová", "kronusova-dent"),
}

PALETTE = ["#356FA3", "#0F6E77", "#2E7D6B", "#7A4E6E", "#8A5A3C", "#455F8A",
           "#2F6F8F", "#3C7A5E", "#6B5B95", "#A2694E", "#34618F", "#7C4F8C"]

rows = list(csv.reader(open("sheet2.csv", encoding="utf-8", newline="")))

if os.path.exists("davka-301-450.json"):
    for c in json.load(open("davka-301-450.json", encoding="utf-8")):
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

    color = PALETTE[len(created) % len(PALETTE)]
    with open(os.path.join(TEMPLATE, "studia", f"{slug}.json"), "w", encoding="utf-8") as f:
        json.dump({"nazev": name, "barva": color}, f, ensure_ascii=False)
        f.write("\n")
    created.append({"radek": n, "slug": slug, "nazev": name, "puvodni": raw,
                    "sablona": TEMPLATE, "barva": color,
                    "email": EMAILS.get(n, ""), "web": (rows[n - 1][1].strip()
                                                        if len(rows[n - 1]) > 1 else "")})

with open("davka-301-450.json", "w", encoding="utf-8") as f:
    json.dump(created, f, ensure_ascii=False, indent=2)
    f.write("\n")

dupl = sum(1 for s in skipped if s["duvod"].startswith("duplicita"))
print(f"Vytvoreno {len(created)} studii na {TEMPLATE}")
print(f"Vynechano {len(skipped)} ({dupl} z toho duplicitni radky 414-447):")
for s in skipped:
    if not s["duvod"].startswith("duplicita"):
        print(f"  r.{s['radek']}  {s['puvodni']}  -> {s['duvod']}")
print(f"  r.414-447  -> duplicita radku 380-413 (34 radku)")
print(f"S e-mailem v tabulce: {sum(1 for c in created if c['email'])}")
