"""Presune vsechny stranky ordinace/<slug>/ z ukazka-3 na ukazka-2.

Proc: ukazka-3 (tepla kremova) uzivateli nesedi, ukazka-1 (svetle modra
s fotkou pres celou obrazovku) byla vyrazena driv -> zustava ukazka-2.

NEMAZE nic v ukazka-3/. Slozka i jeji studia/*.json zustavaji nasazene,
protoze na ne miri UZ ROZESLANE odkazy `ukazka-3/?studio=<slug>`. Jen se
pro kazdy slug doplni protejsek v ukazka-2/studia/, aby generator stranek
mohl dat prednost ukazka-2.

Vlastni bohaty obsah (lfdent-olomouc ma ~4 kB sekci) v ukazka-3 zustava
netknuty — jen se pro stranku v ordinace/ nepouzije.

Spusteni:  python migrace-mimo-ukazka3.py
"""

import json
import os

PALETTE_2 = ["#34618F", "#7C4F8C", "#2E6F6B", "#8C4A52", "#3F5E8C", "#6B5B95",
             "#2F6E5A", "#8A5A3C", "#455F8A", "#7A4E6E", "#3C6B7D", "#5D5A8C"]

src_dir = os.path.join("ukazka-3", "studia")
dst_dir = os.path.join("ukazka-2", "studia")

slugs = sorted(f[:-5] for f in os.listdir(src_dir) if f.endswith(".json"))

created, existed = [], []
for i, slug in enumerate(slugs):
    dst = os.path.join(dst_dir, f"{slug}.json")
    src = json.load(open(os.path.join(src_dir, f"{slug}.json"), encoding="utf-8"))
    if os.path.exists(dst):
        existed.append(slug)
        continue
    # jmeno zachovame presne; barvu vezmeme z originalu, jinak z palety pro ukazka-2
    out = {"nazev": src.get("nazev") or src.get("name") or slug,
           "barva": src.get("barva") or src.get("color") or PALETTE_2[i % len(PALETTE_2)]}
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
        f.write("\n")
    created.append(slug)

# davka-195-242.json: prepsat sablonu, aby maily i prehled hlasily spravne
p = "davka-195-242.json"
if os.path.exists(p):
    batch = json.load(open(p, encoding="utf-8"))
    n = 0
    for k, e in enumerate(batch):
        if e["sablona"] != "ukazka-2":
            e["sablona"] = "ukazka-2"
            e["barva"] = PALETTE_2[k % len(PALETTE_2)]
            n += 1
    with open(p, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"davka-195-242.json: prepnuto {n} zaznamu na ukazka-2")

print(f"ukazka-2/studia: vytvoreno {len(created)}, uz existovalo {len(existed)}")
if created:
    print("  nove: " + ", ".join(created))
if existed:
    print("  preskoceno (uz melo ukazka-2): " + ", ".join(existed))
