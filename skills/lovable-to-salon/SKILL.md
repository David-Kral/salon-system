---
name: lovable-to-salon
description: >
  Convert a Lovable / TanStack Start website export into a Salon System studio
  template — recolor/rebrand it, convert it to a client-side static SPA, and deploy
  to GitHub Pages. Use whenever the user works with a new Lovable web export
  (a dentist / salon / barber / studio marketing site), mentions "Lovable",
  "@lovable.dev/vite-tanstack-config", "TanStack Start", wants to turn such a
  project into a reusable startovaci sablona / template, recolor or rebrand a
  studio, copy it into the Salon System rozcestnik, or deploy it to GitHub Pages.
  Czech triggers: "novy web z Lovable", "prebarvit studio", "udelat sablonu",
  "nasadit na GitHub Pages", "pridat do Salon Systemu".
---

# Lovable web -> Salon System studio (klientsky SPA na GitHub Pages)

Jak vzit **novy web z Lovable** a rychle z nej udelat prebarvitelnou sablonu studia,
ktera se **staticky nasadi na GitHub Pages** a da se odkazat z rozcestniku `salon-system`.

## 1. Jak Lovable web poznas

Lovable export = **TanStack Start** projekt (React 19, Vite, Tailwind v4, shadcn/ui).
Pozna se podle: `@lovable.dev/vite-tanstack-config` ve `vite.config.ts`,
slozky `.lovable/`, `AGENTS.md` s blokem `<!-- LOVABLE:BEGIN -->`.

`src/`: `routes/` (`__root.tsx`, `index.tsx`), `components/ui/` (shadcn), `hooks/`,
`lib/`, `assets/`, `styles.css`, `router.tsx`, a u SSR sablony i `server.ts`/`start.ts`.
Typicky **jednostrankovy marketingovy web** (jen route `/`).

### Kde co bydli
| Menis | Kde |
|---|---|
| Barvy / branding | `src/styles.css`, blok `:root` (oklch) |
| Texty, sekce, sluzby, cenik | `src/routes/index.tsx` |
| Logo a fotky | `src/assets/`, `public/` |
| SEO / title / meta | SSR: `src/routes/__root.tsx` head(); klientsky SPA: `index.html` |

## 2. Prebarveni

Barvy jsou CSS promenne v `src/styles.css` -> `:root`. Staci zmenit `--primary`,
`--accent`, `--ring` (+ `--background`/`--foreground`). Nekdy je nahore odvozena
paleta (napr. Domident: `--charcoal`, `--mist`, `--bone`, `--ivory`) - pak staci tyhle.
Barvy jsou `oklch(svetlost chroma odstin)`; nejrychlejsi zmena identity = posledni
cislo (odstin) u `--primary` a `--accent`.

## 3. DULEZITE: staticky build novejsi SSR sablony je ROZBITY

Novejsi Lovable sablona (`.lovable/project.json` -> `tanstack_start_ts_current`) je
**TanStack Start SSR + Vite 8 + nitro 3.0 beta**. Jeji staticky build (`nitro:
{ preset: "static" }` + prerender) v teto verzni kombinaci **padne**:

```
rolldownOptions.input should not be an html file when building for SSR.
Please specify a dedicated SSR entry.
```

Neni to chyba configu - je to bug stacku. NEsnaz se to resit ladenim prerender/nitro
options; misto toho **preved projekt na klientsky Vite SPA** (viz nize). To je presne
struktura, kterou ma funkcni `stationery-haven` a ktera na Pages jede.

## 4. Prevod na klientsky Vite SPA (spolehlivy staticky build)

Cil = z SSR projektu udelat plain client SPA (jako stationery-haven). Kroky:

1. **package.json**: build skript = `vite build`. Odeber deps
   `@tanstack/react-start`, `nitro`, `@lovable.dev/vite-tanstack-config`.
2. **vite.config.ts** -> plain Vite (bez lovable/nitro):
   ```ts
   import { defineConfig } from "vite";
   import react from "@vitejs/plugin-react";
   import tailwindcss from "@tailwindcss/vite";
   import tsconfigPaths from "vite-tsconfig-paths";
   import { tanstackRouter } from "@tanstack/router-plugin/vite";
   const base = process.env.BASE_PATH || "/";
   export default defineConfig({
     base,
     plugins: [tsconfigPaths(), tailwindcss(),
       tanstackRouter({ target: "react", autoCodeSplitting: true }), react()],
   });
   ```
3. **index.html** (v koreni) - klientsky entry; SEO preber z puvodniho `__root.tsx`:
   ```html
   <!doctype html>
   <html lang="cs"><head>
     <meta charset="UTF-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
     <title>...z __root head...</title>
     <meta name="description" content="..." />
     <link rel="icon" href="/favicon.ico" />
     <!-- font link z __root -->
   </head><body>
     <div id="root"></div>
     <script type="module" src="/src/main.tsx"></script>
   </body></html>
   ```
4. **src/main.tsx** - bootstrap: `ReactDOM.createRoot(#root).render(<RouterProvider router={getRouter()} />)`, importuje `./styles.css`.
5. **src/routes/__root.tsx** -> klientska verze: BEZ `shellComponent`, `HeadContent`,
   `Scripts`, `head()`. Jen `QueryClientProvider` + `<Outlet/>` (+ NotFound/Error komponenty).
6. **src/router.tsx** -> pridej `basepath` z `import.meta.env.BASE_URL` (kvuli `/<repo>/`).
7. Smaz `src/server.ts`, `src/start.ts`.

Build: `npm run build` -> vystup **`dist/`** (`dist/index.html` + `dist/assets/`).

> Tohle vsechno dela automaticky scaffolder `scripts/new-studio.mjs`:
> `node new-studio.mjs --from <cesta-k-lovable-projektu> <nazev-studia>`

## 5. GitHub Pages workflow

`.github/workflows/deploy-pages.yml` (sablona: `scripts/deploy-pages.yml`) buildi do
`dist/`, prida 404.html fallback + .nojekyll, nasadi na Pages. `BASE_PATH` se v CI
dopocita z nazvu repa. Nasazeni: repo -> Settings -> Pages -> Source: GitHub Actions ->
push -> `https://<user>.github.io/<repo>/`. Vlastni domena: smaz radek `BASE_PATH`.

## 6. Zarazeni do Salon Systemu

`salon-system` je **jen rozcestnik** - kod se do nej NEkopiruje. Pridej jen kartu s
odkazem do `salon-system/index.html` (viz `JAK-PRIDAT-PROJEKT.md`). NEkopiruj projekt
do `salon-system/sites/` (tam jsou zkompilovane weby, nedaji se prebarvovat).

## 7. Gotchas

- **Lovable git historie:** neprepisuj pushnute commity (force-push/rebase) - sync do Lovable.
- **Staticky build SSR sablony padne** na `html file for SSR` -> preved na klientsky SPA (bod 4).
- **Windows "in use":** kdyz nejde smazat stara kopie (bezi dev server/editor), generuj pod jinym nazvem.
- **Bily web / 404 assety:** spatny `base` -> ma byt `/<repo>/` (nebo `/` u domeny).
