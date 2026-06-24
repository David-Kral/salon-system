# Jak přidat nový projekt na rozcestník (Salon System)

Tento návod popisuje, jak vytvořit **nový samostatný projekt** ve vlastním GitHub repu,
nasadit ho na jeho **vlastní GitHub Pages** a pak ho jen **odkázat kartou** z rozcestníku
v repu `salon-system` — bez toho, aby se kód projektu kopíroval dovnitř `salon-system`.

```
salon-system/         ← rozcestník (dashboard) + pár demo webů
   index.html         ← tady přidáš jen KARTU s odkazem

muj-novy-projekt/     ← úplně samostatné repo
   ...                ← vlastní kód, vlastní GitHub Pages
   → běží na https://david-kral.github.io/muj-novy-projekt/
```

Rozcestník = jen rozcestník. Každý projekt žije ve svém repu a má svůj web. Karta na
rozcestníku na něj jen odkazuje.

---

## Krok 1 — Nasadit nový projekt na jeho vlastní GitHub Pages

Adresa webu bude vždy: `https://david-kral.github.io/<REPO>/` (kde `<REPO>` je název repa).

### A) Statický web (čisté HTML / CSS / JS)

1. Vytvoř repo `<REPO>` na GitHubu a nahraj soubory (`index.html` musí být v kořeni repa).
2. Repo → **Settings → Pages**.
3. **Source: Deploy from a branch** → branch `main` (nebo `master`), složka `/ (root)` → **Save**.
4. Za ~1 minutu web běží na `https://david-kral.github.io/<REPO>/`. Hotovo, žádný workflow netřeba.

### B) Vite / React projekt (jako papírnictví)

1. Vytvoř repo `<REPO>` a nahraj projekt.
2. Nastav správnou cestu, aby se assety načítaly z `/<REPO>/`:
   - ve `vite.config.ts`:
     ```ts
     export default defineConfig({
       base: "/<REPO>/",
       // ...zbytek beze změny
     });
     ```
   - **pokud používáš client-side router** (TanStack Router, React Router…), nastav i base routeru,
     jinak appka po nasazení ukáže vlastní „404 / Go home":
     ```ts
     const router = createRouter({
       routeTree,
       basepath: "/<REPO>",   // bez lomítka na konci
     });
     ```
3. Build skript v `package.json` nech jako `"build": "vite build"`.
   (Když máš v projektu nepoužité šablonové komponenty s chybami typů, **nedávej** tam
   `tsc --noEmit` — jinak build spadne. Buď je oprav, nebo vynech `tsc`.)
4. Přidej workflow `.github/workflows/deploy-pages.yml` (šablona je níže).
5. Repo → **Settings → Pages → Source: GitHub Actions**.
6. Pushni na `master` → záložka **Actions** ukáže běh → po zelené fajfce běží web na
   `https://david-kral.github.io/<REPO>/`.

**Šablona workflow pro samostatný Vite projekt** (`.github/workflows/deploy-pages.yml`):

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [master]      # nebo "main" — podle tvého repa
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
      - run: npm install
      - run: npm run build          # = vite build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

> Poznámka: pro samostatné repo je `base` rovno `/<REPO>/` (ne `/salon-system/...`).
> Proto je to jednodušší než to, co jsme řešili u papírnictví — to bylo výjimečně
> vnořené *uvnitř* `salon-system`, takže potřebovalo `/salon-system/stationery-haven/`.

---

## Krok 2 — Přidat kartu na rozcestník

V repu `salon-system` otevři `index.html` a najdi sekci **„Ostatní projekty"**:

```html
<div class="section-title">Ostatní projekty</div>
<div class="sites-grid">
  <div class="site-card"> ... papírnictví ... </div>

  <!-- SEM vlož novou kartu (před "add-card") -->

  <div class="add-card"> ... Přidat projekt ... </div>
</div>
```

Před blok `<div class="add-card">` vlož tuto kartu a vyplň `<...>`:

```html
<div class="site-card">
  <div class="site-card-header">
    <span class="template-badge badge-shop">TYP</span>
    <span class="site-slug">&lt;REPO&gt;</span>
  </div>
  <div class="site-card-body">
    <div class="site-name">Název projektu</div>
    <div class="site-city">Město / podtitulek</div>
    <div class="site-desc">Krátký popis, co to je.</div>
    <div class="site-meta">
      <span class="meta-pill">⚛️ Vite + React</span>
      <span class="meta-pill">🌐 GitHub Pages</span>
    </div>
  </div>
  <div class="site-card-footer">
    <button class="btn-open" onclick="window.open('https://david-kral.github.io/&lt;REPO&gt;/','_blank')">
      ↗ Otevřít web
    </button>
    <button class="btn-config" onclick="window.open('https://github.com/David-Kral/&lt;REPO&gt;','_blank')">
      GitHub
    </button>
  </div>
</div>
```

Dostupné barvy odznaku (`template-badge`): `badge-barbershop` (zelená), `badge-salon` (šedá),
`badge-dentist` (tyrkysová), `badge-shop` (zlatá).

Po **commitu `index.html`** se rozcestník sám přenasadí (workflow běží při každém pushi na
`master`) a nová karta se objeví. Tlačítko **Otevřít web** vede přímo na samostatný web projektu.

---

## Časté problémy (a čím to bylo)

| Příznak | Příčina | Oprava |
|---|---|---|
| Build v Actions spadne na chybách typů | `tsc --noEmit` kontroluje i nepoužité šablonové komponenty | build skript = `vite build` (vynech `tsc`), nebo komponenty oprav/smaž |
| Web se načte bíle / assety 404 | špatný `base` ve `vite.config.ts` | nastav `base: "/<REPO>/"` |
| Appka ukáže „404 / Go home" | `basepath` routeru nesedí s cestou nasazení | nastav `basepath: "/<REPO>"` |
| Web se neaktualizuje | Pages nemá zdroj GitHub Actions, nebo build neproběhl | Settings → Pages → Source = GitHub Actions; zkontroluj záložku Actions |

---

## Rychlý checklist pro nový projekt

1. [ ] Vytvořit repo `<REPO>` na GitHubu
2. [ ] (Vite) `base: "/<REPO>/"` + `basepath: "/<REPO>"` + workflow + Pages = GitHub Actions
       — / (statický) Settings → Pages → Deploy from branch
3. [ ] Ověřit, že běží `https://david-kral.github.io/<REPO>/`
4. [ ] Přidat kartu do `salon-system/index.html` (sekce „Ostatní projekty")
5. [ ] Commit → rozcestník se přenasadí → karta odkazuje na nový web
