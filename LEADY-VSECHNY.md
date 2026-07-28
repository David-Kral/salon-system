# LEADY ZUBAŘI — všech 40 na jednom místě

Sjednocení všech dávek (dřív rozházené v `leady-zubari-*.txt`,
`maily-zubari-*.txt` a `e-maily-zubari.docx`). Texty mailů zůstávají
v původních souborech — **tady je seznam a nové odkazy.**

## Co se změnilo v odkazech

Dřív: `ukazka-N/?studio=<slug>` — jméno ordinace doplnil až JavaScript,
takže statický titulek stránky (a tím i náhled odkazu v mailu nebo na
WhatsAppu) hlásil `Dentaline` / `DomiDent`.

Teď má **každá ordinace vlastní stránku** se svým jménem už ve statickém
HTML (titulek, description, OG náhled) a bez `?studio=` v adrese:

```
https://david-kral.github.io/salon-system/ordinace/<slug>/
```

Staré odkazy `ukazka-N/?studio=<slug>` **fungují dál** — už rozeslané maily
se nerozbily. Pro nové oslovení používej ty nové.

Regenerace: `node patch-bundly.mjs && node gen-ordinace.mjs && python gen-leady.py`

## Přehled

| # | Ordinace | Šablona | E-mail | Odkaz |
|--:|----------|---------|--------|-------|
| 1 | Ordinace MUDr. René Štajner | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/stajner-dent/ |
| 2 | Bistrodent | Návrh 2 (prémiový) | ordinace@bistrodent.cz | https://david-kral.github.io/salon-system/ordinace/bistrodent/ |
| 3 | Zubní ordinace MUDr. Ladislava Vranová | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/vranova-dent/ |
| 4 | Dr.Dent Zlín | Návrh 2 (prémiový) | — | https://david-kral.github.io/salon-system/ordinace/drdent-zlin/ |
| 5 | Zubní ordinace MUDr. Iva Klimešová | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/klimesova-dent/ |
| 6 | MUDr. Michael Chmiel | Návrh 2 (prémiový) | — | https://david-kral.github.io/salon-system/ordinace/chmiel-dent/ |
| 7 | Zubní ambulance MUDr. Karla Odstrčilová | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/odstrcilova-dent/ |
| 8 | Zubní ordinace Ulman & Šíblová | Návrh 2 (prémiový) | — | https://david-kral.github.io/salon-system/ordinace/ulman-siblova-dent/ |
| 9 | Zubní lékař MUDr. Alexandra Reli | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/reli-dent/ |
| 10 | Dentista Zlín | Návrh 2 (prémiový) | — | https://david-kral.github.io/salon-system/ordinace/dentista-zlin/ |
| 11 | MUDr. Zdena Sýkorová | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/zdena-sykorova/ |
| 12 | Dentální hygiena Louny | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/hygiena-louny/ |
| 13 | MUDr. Lukáš Milič | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/lukas-milic/ |
| 14 | Zubní ordinace | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/zubni-ordinace/ |
| 15 | Zubní hygiena Děčín | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/hygiena-decin/ |
| 16 | Dentální hygiena Poděbrady | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/hygiena-podebrady/ |
| 17 | BHL dent | Návrh 1 | info@bhl-dent.cz | https://david-kral.github.io/salon-system/ordinace/bhl-dent/ |
| 18 | LIBENTO | Návrh 3 (rezervace) | recepce@libento.cz | https://david-kral.github.io/salon-system/ordinace/libento/ |
| 19 | Galaxy Dent | Návrh 2 (prémiový) | galaxydent.sro@gmail.com | https://david-kral.github.io/salon-system/ordinace/galaxy-dent/ |
| 20 | Krásný úsměv | Návrh 3 (rezervace) | info@vaskrasnyusmev.cz | https://david-kral.github.io/salon-system/ordinace/lfdent-olomouc/ |
| 21 | Centrum zubní medicíny | Návrh 3 (rezervace) | info@dentaldesign.cz | https://david-kral.github.io/salon-system/ordinace/centrum-zubni-mediciny/ |
| 22 | Stomatochirurgické centrum Olomouc | Návrh 1 | recepce@stomchircentrum.cz | https://david-kral.github.io/salon-system/ordinace/stomchir-olomouc/ |
| 23 | DENT — zubní klinika | Návrh 1 | info@kamenicekstoma.cz | https://david-kral.github.io/salon-system/ordinace/dent-klinika/ |
| 24 | Dental Sphere | Návrh 1 | recepce@dentalsphere.cz | https://david-kral.github.io/salon-system/ordinace/dental-sphere/ |
| 25 | MUDr. Jiří Procházka | Návrh 1 | mddr.prochazka@gmail.com | https://david-kral.github.io/salon-system/ordinace/jiri-prochazka/ |
| 26 | ART-MEDICA | Návrh 1 | objednani.artmedica@centrum.cz | https://david-kral.github.io/salon-system/ordinace/art-medica/ |
| 27 | ProEste - Dentální centrum | Návrh 1 | info@proeste.cz | https://david-kral.github.io/salon-system/ordinace/proeste-dent/ |
| 28 | MUDr. Jarmila Blažková | Návrh 3 (rezervace) | info@jtbdental.cz | https://david-kral.github.io/salon-system/ordinace/jtb-dent/ |
| 29 | Stomatologická ordinace Holice | Návrh 2 (prémiový) | recepce@stomaholice.cz | https://david-kral.github.io/salon-system/ordinace/holice-dent/ |
| 30 | Zubní ordinace Švec | Návrh 1 | ordinace@zubnisvec.cz | https://david-kral.github.io/salon-system/ordinace/svec-dent/ |
| 31 | JSmile stomatologie | Návrh 2 (prémiový) | jsmilestomatologie@gmail.com | https://david-kral.github.io/salon-system/ordinace/jsmile-dent/ |
| 32 | Perioimplants | Návrh 2 (prémiový) | recepce@collegiumdentalis.cz | https://david-kral.github.io/salon-system/ordinace/perioimplants/ |
| 33 | MUDr. Přemysl Janda | Návrh 3 (rezervace) | Premysl.Janda@seznam.cz | https://david-kral.github.io/salon-system/ordinace/janda-dent/ |
| 34 | ORTHOZLIN | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/orthozlin/ |
| 35 | WistDental | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/wistdental/ |
| 36 | Zubní ordinace MUDr. Beata Prucková | Návrh 1 | — | https://david-kral.github.io/salon-system/ordinace/pruckova-dent/ |
| 37 | MUDr. Jiří Grmela | Návrh 1 | jiri.grmela@seznam.cz | https://david-kral.github.io/salon-system/ordinace/grmela-dent/ |
| 38 | ZUBOSANA — MUDr. Miroslav Kuča | Návrh 2 (prémiový) | — | https://david-kral.github.io/salon-system/ordinace/kuca-dent/ |
| 39 | REGION BEST DENTAL — MUDr. Pavla Bradáčová | Návrh 2 (prémiový) | — | https://david-kral.github.io/salon-system/ordinace/bradacova-dent/ |
| 40 | Stomatologie Hanos | Návrh 3 (rezervace) | — | https://david-kral.github.io/salon-system/ordinace/hanos-dent/ |

**E-mail znám u 19 ze 40**, u zbylých 21 je potřeba dohledat.

## Detail

### 1. Ordinace MUDr. René Štajner

- **Web dnes:** stomatologiestajner.webmium.com
- **Problém:** Doména vrací 404 — web fakticky neexistuje.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/stajner-dent/
- _Pozn.: pro stejného zubaře existuje i slug `rene-stajner` (jiná šablona) — posílej jen jeden._

### 2. Bistrodent

- **Web dnes:** bistrodent.cz
- **Problém:** Holé HTML bez CSS stylů + zastaralé upozornění z dubna 2025.
- **E-mail:** ordinace@bistrodent.cz
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/bistrodent/

### 3. Zubní ordinace MUDr. Ladislava Vranová

- **Web dnes:** znamylekar.cz (profil)
- **Problém:** Nemá vlastní web, chybí rezervační kalendář i ceník.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/vranova-dent/
- _Pozn.: pro stejného zubaře existuje i slug `ladislava-vranova` (jiná šablona) — posílej jen jeden._

### 4. Dr.Dent Zlín

- **Web dnes:** drdentzlin.cz
- **Problém:** Výchozí nenastavená instalace WordPressu s „Hello world!“.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/drdent-zlin/

### 5. Zubní ordinace MUDr. Iva Klimešová

- **Web dnes:** olomouc-zubni.cz
- **Problém:** Doména nefunguje jako vlastní web, jen katalogový profil.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/klimesova-dent/

### 6. MUDr. Michael Chmiel

- **Web dnes:** katalog-stomatologu.cz
- **Problém:** Jen obecný katalogový profil; nepřijímá nové pacienty.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/chmiel-dent/

### 7. Zubní ambulance MUDr. Karla Odstrčilová

- **Web dnes:** katalog-stomatologu.cz
- **Problém:** Generický katalogový profil bez vlastní identity.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/odstrcilova-dent/

### 8. Zubní ordinace Ulman & Šíblová

- **Web dnes:** katalog-stomatologu.cz
- **Problém:** Generický profil; nepřijímají nové pacienty.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/ulman-siblova-dent/

### 9. Zubní lékař MUDr. Alexandra Reli

- **Web dnes:** stomatolog.cz/reli
- **Problém:** Statický XHTML z roku 2021, tabulkový layout.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/reli-dent/

### 10. Dentista Zlín

- **Web dnes:** dentistazlin.cz
- **Problém:** Opakující se navigace, chybí online rezervace.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/dentista-zlin/

### 11. MUDr. Zdena Sýkorová

- **Web dnes:** tylovka.cz
- **Problém:** Funkční, ale designově zastaralý a velmi strohý web.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/zdena-sykorova/

### 12. Dentální hygiena Louny

- **Web dnes:** hygiena-dentalni.cz
- **Problém:** Starší WordPress bez aktualizací.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/hygiena-louny/

### 13. MUDr. Lukáš Milič

- **Web dnes:** milic.cz
- **Problém:** Web vrací chybu 500.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/lukas-milic/

### 14. Zubní ordinace

- **Web dnes:** zubni-ordinace.eu
- **Problém:** Doména nedostupná.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/zubni-ordinace/

### 15. Zubní hygiena Děčín

- **Web dnes:** zubnihygienadecin.cz
- **Problém:** Doména neodpovídá.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/hygiena-decin/

### 16. Dentální hygiena Poděbrady

- **Web dnes:** hygienistkapdy.cz
- **Problém:** Doména neodpovídá.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/hygiena-podebrady/

### 17. BHL dent

- **Web dnes:** bhl-dent.cz
- **Problém:** Vizuálně uhlazené, ale texty hodně obecné a generické.
- **E-mail:** info@bhl-dent.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/bhl-dent/

### 18. LIBENTO

- **Web dnes:** libento.cz
- **Problém:** Nefunkční obrázkový slider na úvodní ploše.
- **E-mail:** recepce@libento.cz
- **Šablona:** Návrh 3 (rezervace) (`ukazka-3`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/libento/

### 19. Galaxy Dent

- **Web dnes:** (vlastní řešení)
- **Problém:** Chybí veřejně dostupný ceník.
- **E-mail:** galaxydent.sro@gmail.com
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/galaxy-dent/

### 20. Krásný úsměv

- **Web dnes:** vaskrasnyusmev.cz
- **Problém:** Úvodní stránka váží přes 3 MB — pomalé na mobilu.
- **E-mail:** info@vaskrasnyusmev.cz
- **Šablona:** Návrh 3 (rezervace) (`ukazka-3`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/lfdent-olomouc/

### 21. Centrum zubní medicíny

- **Web dnes:** dentaldesign.cz
- **Problém:** Přesměrovává na caiaclinic.cz, zubař je až podstránka.
- **E-mail:** info@dentaldesign.cz
- **Šablona:** Návrh 3 (rezervace) (`ukazka-3`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/centrum-zubni-mediciny/

### 22. Stomatochirurgické centrum Olomouc

- **Web dnes:** stomchircentrum.cz
- **Problém:** WordPress + Divi, těžký kód, pomalé načítání.
- **E-mail:** recepce@stomchircentrum.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/stomchir-olomouc/

### 23. DENT — zubní klinika

- **Web dnes:** kamenicekstoma.cz
- **Problém:** Postavené na Elementoru — těžký kód, horší SEO.
- **E-mail:** info@kamenicekstoma.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/dent-klinika/

### 24. Dental Sphere

- **Web dnes:** dentalsphere.cz
- **Problém:** Divi builder — těžký kód, dopad na rychlost a SEO.
- **E-mail:** recepce@dentalsphere.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/dental-sphere/

### 25. MUDr. Jiří Procházka

- **Web dnes:** (žádný)
- **Problém:** Nemá vlastní webovou prezentaci.
- **E-mail:** mddr.prochazka@gmail.com
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/jiri-prochazka/

### 26. ART-MEDICA

- **Web dnes:** (vlastní)
- **Problém:** Nepřijímá pacienty; projekty (Zubařská školka) zaslouží víc prostoru.
- **E-mail:** objednani.artmedica@centrum.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/art-medica/

### 27. ProEste - Dentální centrum

- **Web dnes:** proeste.cz
- **Problém:** Údaj o promoci lékaře až v roce 2026 může mást pacienty.
- **E-mail:** info@proeste.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/proeste-dent/

### 28. MUDr. Jarmila Blažková

- **Web dnes:** jtbdental.cz
- **Problém:** Dvě různé e-mailové adresy v kontaktní sekci.
- **E-mail:** info@jtbdental.cz
- **Šablona:** Návrh 3 (rezervace) (`ukazka-3`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/jtb-dent/

### 29. Stomatologická ordinace Holice

- **Web dnes:** stomaholice.cz
- **Problém:** Meta viewport blokuje přiblížení (user-scalable=0).
- **E-mail:** recepce@stomaholice.cz
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/holice-dent/

### 30. Zubní ordinace Švec

- **Web dnes:** zubnisvec.cz
- **Problém:** Info o nepřijímání pacientů splývá s textem; strohý Wix.
- **E-mail:** ordinace@zubnisvec.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/svec-dent/

### 31. JSmile stomatologie

- **Web dnes:** jsmile.cz
- **Problém:** Neutrální béžová paleta bez brandového akcentu.
- **E-mail:** jsmilestomatologie@gmail.com
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/jsmile-dent/

### 32. Perioimplants

- **Web dnes:** perioimplants.cz
- **Problém:** Načítá dvě verze jQuery současně — zbytečné zpomalení.
- **E-mail:** recepce@collegiumdentalis.cz
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/perioimplants/

### 33. MUDr. Přemysl Janda

- **Web dnes:** zubarjanda.cz
- **Problém:** Objednání jen obecným formulářem, žádný výběr termínu.
- **E-mail:** Premysl.Janda@seznam.cz
- **Šablona:** Návrh 3 (rezervace) (`ukazka-3`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/janda-dent/

### 34. ORTHOZLIN

- **Web dnes:** ortodonciezlin.cz
- **Problém:** Překlep v titulku („Ortodonice“) + žádný objednávkový formulář.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/orthozlin/

### 35. WistDental

- **Web dnes:** wistdental.cz
- **Problém:** Chybné kódování znaků — rozbitá diakritika.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/wistdental/

### 36. Zubní ordinace MUDr. Beata Prucková

- **Web dnes:** (žádný)
- **Problém:** Bez vlastního webu — jen katalogové profily.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/pruckova-dent/

### 37. MUDr. Jiří Grmela

- **Web dnes:** (žádný)
- **Problém:** Bez vlastního webu — jen katalogové profily.
- **E-mail:** jiri.grmela@seznam.cz
- **Šablona:** Návrh 1 (`ukazka-1`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/grmela-dent/

### 38. ZUBOSANA — MUDr. Miroslav Kuča

- **Web dnes:** (žádný)
- **Problém:** ZUBOSANA bez vlastního webu, chybí i online rezervace.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/kuca-dent/

### 39. REGION BEST DENTAL — MUDr. Pavla Bradáčová

- **Web dnes:** (žádný)
- **Problém:** Firma s vlastním jménem, ale bez vlastního webu.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 2 (prémiový) (`ukazka-2`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/bradacova-dent/

### 40. Stomatologie Hanos

- **Web dnes:** katalog-stomatologu.cz
- **Problém:** Jen strojově generovaný profil, bez fotek a ceníku.
- **E-mail:** _nedohledán_
- **Šablona:** Návrh 3 (rezervace) (`ukazka-3`)
- **Ukázka:** https://david-kral.github.io/salon-system/ordinace/hanos-dent/

---

## Nepoužité slugy

V `ordinace/` je 44 stránek, ale leadů je 40:

- `petr-seda`, `usmev-jana` — ukázková/dokumentační studia, ne skuteční leadi.
- `rene-stajner`, `ladislava-vranova` — druhá varianta šablony pro zubaře,
  kteří už v seznamu jsou (`stajner-dent`, `vranova-dent`).
