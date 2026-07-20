# Salon System — kontext pro AI agenta

Salon System je **rozcestnik** (dashboard) webu jednotlivych studii (zubari, salony,
barbershopy). Rozcestnik jen odkazuje kartami na weby; **kod projektu se do nej
nekopiruje** — kazdy web zije ve svem repu a ma svuj GitHub Pages web.

## Kdyz mas novy web z Lovable (dentista/salon/studio)

Lovable export = **TanStack Start** projekt (import `@lovable.dev/vite-tanstack-config`
ve `vite.config.ts`, slozka `.lovable/`). Kompletni postup (struktura, prebarveni,
prevod na klientsky staticky SPA, nasazeni na Pages) je v:

- **`skills/lovable-to-salon/SKILL.md`** — playbook.
- **`SABLONY.md`** — jak z Dentaline/Domident delat nova studia jednim prikazem.
- **`JAK-PRIDAT-PROJEKT.md`** — jak pridat kartu na rozcestnik.

## Zkratky

- Nove studio z existujici sablony:
  `node nova-studio.mjs <dentaline|domident> <nazev-studia>`
- Nove studio z libovolne Lovable slozky:
  `node skills/lovable-to-salon/scripts/new-studio.mjs --from <cesta> <nazev-studia>`

## Klicova fakta

- Barvy: `src/styles.css` -> `:root` (oklch). Meni se `--primary`, `--accent`, `--ring`.
- Texty: `src/routes/index.tsx`. SEO/title/font: `index.html` (po prevodu). Assety: `src/assets/` + `public/`.
- **POZOR:** novejsi Lovable sablona (TanStack Start SSR, Vite 8, nitro 3 beta) ma
  **rozbity staticky build** (`html file for SSR`). Scaffolder proto kazdou kopii
  **prevede na klientsky Vite SPA** (index.html + main.tsx, react-router, plain Vite).
  Vystup buildu je **`dist/`**. Nepokousej se to resit ladenim nitro/prerender.
- Base path z nazvu repa (workflow injektuje `BASE_PATH`).
- Lovable historie: NEprepisovat pushnute commity (force-push/rebase) — sync do Lovable.
