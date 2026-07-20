# Startovaci sablony: Dentaline & Domident

Jak z projektu **Dentaline** a **Domident** delat nova studia co nejrychleji,
prebarvit je a nasadit na GitHub Pages. Kazde studio se z master sablony vytvori
jednim prikazem a rovnou se **prevede na cisty klientsky Vite SPA**, ktery se
spolehlive vybuildi a nasadi.

## Dulezity kontext (proc converter)

Dentaline/Domident jsou z **novejsi Lovable sablony**: TanStack Start (**SSR**),
Vite 8, nitro 3.0 beta. Jejich **staticky build je v teto verzni kombinaci rozbity**
(`rolldownOptions.input should not be an html file when building for SSR`). Neni to
chyba configu - je to bug toho stacku.

Tvuj funkcni web `stationery-haven` (papirnictvi) je naopak **klientsky SPA**
(index.html + main.tsx, @tanstack/react-router, plain Vite) a na Pages jede.
Proto scaffolder kazdou kopii prevede do tohoto funkcniho stylu.

## Kde bydli sablony

| Sablona   | Cesta                                                  |
|-----------|--------------------------------------------------------|
| dentaline | `C:\Users\david\IdeaProjects\dentaline-modern-sparkle` |
| domident  | `C:\Users\david\IdeaProjects\domident-refined`         |

Barvy: `src/styles.css` -> blok `:root` (oklch). Texty: `src/routes/index.tsx`.

## Nove studio jednim prikazem

```bash
cd C:\Users\david\Downloads\salon-system
node nova-studio.mjs <sablona> <nazev-studia>
```

Priklady:

```bash
node nova-studio.mjs dentaline kr-dent
node nova-studio.mjs domident  usmev-brno
```

Nova slozka vznikne v `C:\Users\david\IdeaProjects\<nazev-studia>`.

## Co scaffolder v kopii udela (prevod na klientsky SPA)

1. Cista kopie (bez `.git`, `node_modules`, `dist`, `.idea`...), prejmenuje `package.json`.
2. Prepise `vite.config.ts` na **plain Vite** (react + tailwind + tsconfigPaths +
   tanstackRouter). Zadny lovable config, zadny nitro. `base` z `BASE_PATH` (CI).
3. Prida **`index.html`** (v koreni) + **`src/main.tsx`** (klientsky bootstrap).
   SEO (title, description, font) se prevezme z puvodniho `__root.tsx`.
4. Prepise `src/routes/__root.tsx` na klientskou verzi (bez SSR shellu / Scripts / head).
5. Smaze `src/server.ts` a `src/start.ts`, z `package.json` odebere
   `@tanstack/react-start`, `nitro`, `@lovable.dev/vite-tanstack-config`.
6. Do `src/router.tsx` doplni `basepath` (kvuli podslozce `/<repo>/`).
7. Prida `.github/workflows/deploy-pages.yml` + `PREBARVENI.md`.

**Vystup buildu je `dist/`** (overeno: `npm run build` -> `dist/index.html` + `dist/assets/`).

## Co pak upravit (5 minut)

1. **Barvy** - `src/styles.css`, blok `:root`. Staci `--primary`, `--accent`, `--ring`.
   U Domidentu je nahore "Logo-derived palette" (`--charcoal`, `--mist`, `--bone`,
   `--ivory`) - zmen tyhle 4. Barvy jsou v oklch; nejrychlejsi zmena = posledni cislo
   (odstin) u `--primary` a `--accent`.
2. **Texty** - `src/routes/index.tsx`.
3. **SEO / title / font** - `index.html` (v koreni).
4. **Logo a fotky** - `src/assets/` + `public/`.
5. Nahled: `npm install && npm run dev`. Build: `npm run build` (-> `dist/`).

## Nasazeni na GitHub Pages

1. Nahraj slozku studia do noveho GitHub repa (`<repo>` = nazev studia).
2. Repo -> **Settings -> Pages -> Source: GitHub Actions**.
3. Push na `main`/`master` -> workflow vybuildi a nasadi web na
   `https://david-kral.github.io/<repo>/`. Base path se dopocita z nazvu repa,
   takze **nic rucne neresis**.
4. (Volitelne) Pridej kartu na rozcestnik `salon-system/index.html` (viz `JAK-PRIDAT-PROJEKT.md`).

> **Vlastni domena:** kdyz studio pojede na vlastni domene (root), smaz ve workflow
> radek `BASE_PATH: ...` - base pak bude `/`.

## Gotcha: mazani stare kopie

Kdyz slozku maze Windows a je "in use" (bezi dev server / drzi ji editor), Remove-Item
selze a scaffolder pak hlasi "Cilova slozka uz existuje". Zavri dev server / editor,
nebo generuj pod jinym nazvem.

## Shrnuti workflow

```
master sablona (Dentaline/Domident, Lovable SSR)
        |  node nova-studio.mjs dentaline nove-studio
        v
nove-studio/  <- prevedeno na klientsky Vite SPA (index.html + main.tsx)
        |  npm run build -> dist/
        |  push do noveho GitHub repa (Pages = GitHub Actions)
        v
web na https://david-kral.github.io/nove-studio/
        |  (volitelne) karta na rozcestniku
        v
posles klientovi
```
