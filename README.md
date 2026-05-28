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

### Krok 2 — Zkopíruj šablonu

```bash
# Barbershop:
cp -r barbershop/template/ sites/muj-novy-barbershop/

# Nebo salon:
cp -r salon/template/ sites/muj-novy-salon/
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

## Tipy

**Obrázky:** Doporučená velikost pro hero je 1200×1500px (poměr 4:5). Pro galerii 800×800px.

**Barvy:** Lze zadat v libovolném CSS formátu: `#hex`, `rgb()`, `oklch()` atd.

**Mapa embed:** Google Maps embed URL získáš na `maps.google.com` → sdílet → vložit mapu → zkopíruj src z iframe.  
OpenStreetMap embed: `https://www.openstreetmap.org/export/embed.html?bbox=LON1,LAT1,LON2,LAT2&layer=mapnik&marker=LAT,LON`

**Rezervace:** Doporučené systémy: [Reservio](https://reservio.com), [Bookio](https://bookio.cz), [Fresha](https://fresha.com).

**Vlastní font:** Přidej do `<head>` v šabloně `<link>` tag z Google Fonts a uprav CSS proměnnou `--font-display` nebo `--font-serif`.

---

## Jak funguje technicky

1. Prohlížeč načte `index.html` ze šablony  
2. JavaScript provede `fetch('./config.json')`  
3. Z konfigurace aplikuje barvy jako CSS proměnné (`document.documentElement.style.setProperty(...)`)  
4. Naplní všechny sekce obsahem z JSON (název, texty, obrázky, ceník, tým, mapa...)  
5. Spustí IntersectionObserver pro scroll reveal animace  

Výsledek: **jeden HTML soubor = nekonečně různých webů** — stačí vyměnit config.json.
