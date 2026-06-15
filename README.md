# Salon System — Multi-Site Management

Jeden codebase, nekonečně webů. Vyplň config.json a web je hotový.

---

## Struktura projektu

```
salon-system/
├── index.html                    ← Dashboard (přehled všech webů)
├── README.md                     ← Tento soubor
│
├── barbershop/
│   └── template/
│       ├── index.html            ← Šablona (načítá ./config.json)
│       ├── style.css             ← CSS barbershop stylu
│       └── assets/               ← Výchozí obrázky šablony
│
├── salon/
│   └── template/
│       ├── index.html            ← Šablona (načítá ./config.json)
│       ├── style.css             ← CSS salon stylu
│       └── assets/               ← Výchozí obrázky šablony
│
├── dentist/
│   └── template/
│       ├── index.html            ← Šablona (načítá ./config.json)
│       ├── style.css             ← CSS zubařského stylu
│       └── assets/               ← Výchozí SVG placeholdery
│
└── sites/
    ├── velvet-chrome/            ← Prémiový barbershop Praha
    │   └── config.json
    ├── barber-gold/              ← Barbershop Brno
    │   └── config.json
    ├── gabriela-cilova/          ← Vlasový salon Chrudim
    │   └── config.json
    └── studio-luna/              ← Vlasový salon Olomouc
        └── config.json
```

---

## Přidání nového webu za 5 minut

### Krok 1 — Vyber šablonu

| Chceš | Šablona |
|-------|---------|
| Barbershop (tmavý luxusní styl) | `barbershop` |
| Vlasový salon (světlý elegantní styl) | `salon` |
| Zubní studio (tmavý editoriální styl) | `dentist` |

### Krok 2 — Zkopíruj šablonu

```bash
# Barbershop:
cp -r barbershop/template/ sites/muj-novy-barbershop/

# Nebo salon:
cp -r salon/template/ sites/muj-novy-salon/

# Nebo zubař:
cp -r dentist/template/ sites/moje-nova-ordinace/
```

### Krok 3 — Vytvoř config.json

Zkopíruj existující konfiguraci a upravij: fdsaf dsa fsdaf

```bash
# Jako základ použij podobný existující web:
cp sites/velvet-chrome/config.json sites/ht-salon/config.json
```

Pak uprav `config.json` v textovém editoru. Viz sekci **Schéma config.json** níže.

### Krok 4 — Přidej vlastní obrázky (volitelné)

```bash
# Ulož klientovy fotky do:
sites/muj-novy-barbershop/assets/hero-interior.jpg
sites/muj-novy-barbershop/assets/about-chair.jpg
sites/muj-novy-barbershop/assets/barber-1.jpg
# atd.
```

Pokud obrázky nedodáš, web použije výchozí obrázky ze šablony.

### Krok 5 — Zaregistruj web v dashboardu

Otevři `index.html` a přidej řádek do pole `SITES`:

```js
const SITES = [
  { slug: 'velvet-chrome',       template: 'barbershop' },
  { slug: 'barber-gold',         template: 'barbershop' },
  { slug: 'gabriela-cilova',     template: 'salon'      },
  { slug: 'studio-luna',         template: 'salon'      },
  { slug: 'muj-novy-barbershop', template: 'barbershop' }, // ← přidej tuto řadu
  { slug: 'moje-nova-ordinace',  template: 'dentist'    }, // ← nebo zubařskou
];
```

### Krok 6 — Otevři náhled

Spusť lokální server (např. pomocí VS Code Live Server nebo Python):

```bash
# Python:
python -m http.server 8080

# Node:
npx serve .
```

Pak otevři: `http://localhost:8080/` (dashboard)

Web klienta: `http://localhost:8080/sites/muj-novy-barbershop/`

---

## Nasazení na GitHub Pages (jeden web)

Každý web v `sites/` je samostatný — stačí ho nasadit jako separátní repozitář:

```bash
# 1. Inicializuj nový git repozitář uvnitř složky webu
cd sites/muj-novy-barbershop/
git init
git add .
git commit -m "Initial site setup"

# 2. Vytvoř repozitář na GitHubu a pushni
git remote add origin https://github.com/UZIVATEL/muj-novy-barbershop.git
git push -u origin main

# 3. V nastavení repozitáře zapni GitHub Pages:
#    Settings → Pages → Source: Deploy from branch → main / (root)
```

Web bude živý na: `https://UZIVATEL.github.io/muj-novy-barbershop/`

> **Poznámka:** Šablony používají `fetch('./config.json')`, takže web vyžaduje HTTP server.
> GitHub Pages tuto podmínku splňuje automaticky. Pro lokální vývoj použij Live Server.

---

## Schéma config.json — Barbershop

```jsonc
{
  "template": "barbershop",     // Identifikátor šablony (informativní)

  "business": {
    "name": "BARBER·ROOM",      // Název firmy (tečka · se zobrazí jako accent)
    "tagline": "...",            // Krátký slogan
    "description": "...",       // Delší popis (meta description + hero)
    "city": "Praha",            // Město
    "established": "MMXXV"      // Rok vzniku (římskými číslicemi)
  },

  "colors": {
    "background": "#1a1815",    // Hlavní pozadí
    "foreground": "#f0ebe0",    // Barva textu
    "card": "#1e1c18",          // Pozadí karet
    "accent": "#37432f",        // Hlavní akcent (tlačítka, zvýraznění)
    "chrome": "#c8c2b5",        // Sekundární akcent (menu, ornament)
    "cream": "#f0ebe0",         // Světlá barva textu na tmavém pozadí
    "muted": "#868070",         // Tlumená barva textu
    "olive": "#4a5a38"          // Tmavší varianta akcentu (hover)
  },

  "contact": {
    "phone": "+420 777 123 456",
    "email": "info@barbershop.cz",
    "address": "Národní 28",
    "city": "110 00 Praha 1",
    "parking": "...",           // Volitelně: info o parkování
    "bookingUrl": "https://...",// Odkaz na rezervační systém
    "mapsLink": "https://...",  // Odkaz na Google Maps
    "mapEmbed": "https://..."   // Embed URL pro iframe mapy
  },

  "hours": [
    { "days": "Pondělí – Pátek", "hours": "09:00 — 20:00" },
    { "days": "Sobota",          "hours": "10:00 — 18:00" },
    { "days": "Neděle",          "hours": "Zavřeno", "closed": true }
  ],

  "social": {
    "instagram": "https://...", // Nebo "#" pro skrytí
    "facebook":  "https://..."
  },

  "nav": [
    { "label": "Domů",    "href": "#home"     },
    { "label": "Koncept", "href": "#about"    },
    { "label": "Služby",  "href": "#services" },
    { "label": "Lookbook","href": "#gallery"  },
    { "label": "Barbeři", "href": "#team"     },
    { "label": "Kontakt", "href": "#contact"  }
  ],

  "hero": {
    "ornament": "Praha · Estd. MMXXV",   // Malý text nad nadpisem
    "heading": "Nadpis\nna dva řádky.",   // \n = zalomení řádku
    "subheading": "Delší podnadpis...",
    "image": "./assets/hero-interior.jpg",
    "ctaLabel": "Rezervovat termín"
  },

  "stats": [
    { "value": "12+", "label": "Let řemesla" },
    { "value": "4",   "label": "Mistři barbeři" },
    { "value": "∞",   "label": "Pozornost detailu" }
  ],

  "ritual": {
    "heading": "Tři kroky k dokonalosti",
    "steps": [
      { "image": "./assets/gallery-1.jpg", "title": "Konzultace", "text": "..." },
      { "image": "./assets/gallery-6.jpg", "title": "Řemeslo",    "text": "..." },
      { "image": "./assets/gallery-3.jpg", "title": "Odchod",     "text": "..." }
    ]
  },

  "cta": {
    "heading": "Připraveni na svůj rituál?",
    "subheading": "..."
  },

  "services": [
    {
      "title": "The Classic Haircut",
      "desc": "Popis služby...",
      "duration": "45 min",
      "price": "890",           // Číslo bez měnové jednotky
      "currency": "Kč"
    }
  ],

  "about": {
    "heading": "Salón. Útočiště.\nPrivátní klubovna.",  // \n = zalomení
    "image": "./assets/about-chair.jpg",
    "paragraphs": ["Odstavec 1...", "Odstavec 2...", "Odstavec 3..."],
    "brands": [
      { "name": "Solingen",  "label": "Břitvy & nůžky"  },
      { "name": "Proraso",   "label": "Italská péče"    }
    ]
  },

  "teamHeading": "Mistři řemesla.",
  "team": [
    {
      "image": "./assets/barber-1.jpg",
      "name": "Tomáš Vlček",
      "role": "Senior Barber",
      "specialization": "Klasické střihy · Fade",
      "years": 9
    }
  ],

  "galleryHeading": "Atmosféra v obrazech.",
  "gallery": [
    { "image": "./assets/gallery-1.jpg", "alt": "Popis obrázku" }
  ],

  "contactHeading": "Zarezervujte si křeslo.",

  "footer": {
    "tagline": "Krátký popis do patičky...",
    "copyright": "Barber Room",   // Zobrazí se jako "© 2025 Barber Room"
    "established": "MMXXV"
  }
}
```

---

## Schéma config.json — Salon

```jsonc
{
  "template": "salon",

  "business": {
    "name": "Gabriela Cilová",
    "tagline": "Krátký slogan...",
    "description": "Delší popis...",
    "city": "Chrudim"
  },

  "colors": {
    "background": "#fdfbf7",    // Teplá bílá
    "foreground": "#262626",    // Tmavý text
    "primary": "#262626",       // Primární barva (tlačítka)
    "accent": "#a8a29e",        // Akcent (taupe/béžová)
    "sand": "#e7e2d8",          // Jemné pozadí sekcí
    "surface": "#f5f3ee",       // Povrch karet
    "muted": "#737373"          // Tlumená barva textu
  },

  "contact": {
    "phone": "+420 775 399 470",
    "email": "info@salon.cz",
    "address": "Rooseveltova 335",
    "city": "537 01 Chrudim",
    "mapsLink": "https://...",
    "mapEmbed": "https://..."
  },

  "hours": [
    { "days": "Pondělí – Pátek", "hours": "9:00 — 18:00" },
    { "days": "Sobota",          "hours": "9:00 — 14:00" },
    { "days": "Neděle",          "hours": "Zavřeno", "closed": true }
  ],

  "social": {
    "facebook":  "https://...",
    "instagram": "https://..."
  },

  "nav": [
    { "label": "Služby",   "href": "#services" },
    { "label": "O salonu", "href": "#about"    },
    { "label": "Kontakt",  "href": "#contact"  }
  ],

  "hero": {
    "heading": "Péče o vlasy, která dýchá přirozeností.",
    "subheading": "Popis...",
    "image": "./assets/hero-salon.jpg",
    "ctaLabel": "Ceník služeb"
  },

  "brands": ["Malibu C", "K18 Molecular", "Paul Mitchell", "Oway"],

  "servicesHeading": "Vybrané rituály",
  "services": [
    {
      "image": "./assets/service-cleanse.jpg",
      "tag": "Ozdravná kúra",           // Malý štítek nad názvem
      "title": "Malibu C Crystal Gel",
      "desc": "Popis služby...",
      "price": "od 1 200 Kč"            // Volný formát ceny
    }
  ],

  "about": {
    "label": "O salonu",                // Malý popis nad citátem
    "quote": "Citát majitelky/majitele...",
    "author": "Gabriela Cilová"
  },

  "contactHeading": "Najdete nás v Chrudimi",

  "footerLinks": [
    { "label": "Obchodní podmínky", "href": "#" },
    { "label": "Ochrana údajů",     "href": "#" }
  ],

  "footer": {
    "copyright": "Gabriela Cilová"
  }
}
```

---

## Schéma config.json — Zubař (dentist)

Tmavý editoriální „studio" styl (inspirováno MM zubní studio): full-bleed tmavý hero,
trust bar, číslované sekce **Filozofie · Služby · Ceník · FAQ · Kontakt**, B&W portrét,
accordiony, kontaktní formulář, tmavá patička. Design je monochromatický (černá/krémová) —
napříč ordinacemi vypadá identicky, liší se jen obsah.

V nadpisech: `*text*` = kurzívní serifový akcent, `\n` = zalomení řádku.

```jsonc
{
  "template": "dentist",

  "business": {
    "name": "MM zubní studio",
    "monogram": "MM",                 // 2 písmena do loga (jinak se odvodí z názvu)
    "tagline": "Precizní estetika.\nNekompromisní péče.",
    "description": "Meta popis pro SEO..."
  },

  "colors": {                          // monochromatická paleta (volitelné — má rozumné výchozí)
    "ink": "#0e0e0d", "paper": "#ffffff", "cream": "#f1ece3",
    "fg": "#15140f", "fgInv": "#f4f1ea", "muted": "#8c857a", "mutedInv": "#8f897e"
  },

  "contact": {
    "phone": "+420 777 000 000",
    "email": "studio@mmstudio.cz",
    "address": "Hronovická 2815",
    "city": "530 02 Pardubice",
    "region": "Pardubice · centrum"    // popisek u mapy
  },

  "hours": [ { "days": "Po – Čt", "hours": "08:00 — 17:00" } ],
  "social": { "instagram": "https://...", "facebook": "https://..." },
  "nav": [ { "label": "Studio", "href": "#about" } /* ... */ ],
  "cta": { "label": "Chci se objednat" },

  "hero": {
    "heading": "Precizní estetika.\nNekompromisní péče.",
    "ctaLabel": "Chci se objednat",
    "secondaryLabel": "Více o studiu",
    "image": "./assets/hero.svg"       // tmavá fotka interiéru (nahraď vlastní)
  },

  "trust": ["Skandinávský minimalismus", "Guided Biofilm Therapy", "..."],

  "philosophy": {                      // sekce 01
    "label": "Filozofie",
    "heading": "Změnili jsme strach ze zubaře *v relaxační* zážitek.",
    "paragraphs": ["Odstavec 1...", "Odstavec 2..."],
    "portrait": "./assets/portrait.svg",   // B&W portrét (auto grayscale)
    "caption": "MUDr. Michaela Hájková, MBA — zakladatelka",
    "stats": [ { "value": "12", "label": "Let praxe" } ]
  },

  "servicesLabel": "Služby",           // sekce 02 — accordion
  "servicesHeading": "Čtyři pilíře *naší* péče.",
  "servicesIntro": "Krátký text vpravo od nadpisu...",
  "services": [
    { "num": "01", "title": "Estetická stomatologie & fasety",
      "tag": "Premiérová proměna úsměvu", "detail": "Rozbalovací popis..." }
  ],

  "pricingLabel": "Ceník",             // sekce 03
  "pricingHeading": "Transparentní standard.",
  "pricingIntro": "Krátký text pod nadpisem...",
  "pricing": [ { "name": "Vstupní vyšetření & konzultace", "price": "1 800 Kč" } ],
  "pricingNote": "Poznámka pod ceníkem...",

  "faqLabel": "FAQ",                   // sekce 04 — accordion
  "faqHeading": "Pravidla studia.",
  "faq": [ { "q": "Berete nové pacienty?", "a": "Odpověď..." } ],

  "contactLabel": "Kontakt",           // sekce 05 — formulář + mapa + adresa
  "contactHeading": "Začněme *vaším* úsměvem.",

  "footerLinks": [ { "label": "Ochrana informací", "href": "#" } ],
  "footer": { "copyright": "MM zubní studio" }
}
```

> **Obrázky:** Dokud nedodáš fotky, šablona použije placeholdery `assets/hero.svg`
> (tmavý interiér) a `assets/portrait.svg` (B&W portrét). Stačí je přepsat reálnými
> soubory pod stejným názvem — layout zůstane identický.

> **Kontaktní formulář** otevře e-mailového klienta na `contact.email` (bez backendu).

---

r