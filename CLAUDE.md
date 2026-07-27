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

## Personalizovane ukazky pro zubare (?studio=<slug>)

V korenu repa jsou tri **nasazene demo weby** (multi-tenant), na ktere se posilaji
osloveni zubari personalizovanym odkazem `?studio=<slug>` — ten jen prepise jmeno
ordinace + znackovou barvu z `studia/<slug>.json`, zbytek webu je stejny. Nejsou to
sablony pro `nova-studio.mjs` (ty jsou v `IdeaProjects/`, viz `SABLONY.md`) — tohle
jsou uz **zive weby na Pages**, kod se meni primo v teto slozce a pushne.

| Slozka      | Byvaly nazev (zachovan kvuli uz rozeslanym odkazum) | Co to je                          |
|-------------|------------------------------------------------------|-----------------------------------|
| `ukazka-1/` | `dentaline-web`                                       | Dentaline (React/Vite SPA)        |
| `ukazka-2/` | `domident-web`                                        | Domident (React/Vite SPA)         |
| `ukazka-3/` | `dentist/template`                                    | Univerzalni HTML sablona (`dentist/template/`) |

Nove odkazy pro zubare se posilaji **jen pres `ukazka-1/2/3`** (ne pres stare nazvy —
ty by v URL prozradily jmeno jine kliniky). Pridat noveho zubare = jeden JSON
`ukazka-N/studia/<slug>.json` = `{ "nazev": "...", "barva": "#hex" }`, viz
`ukazka-N/studia/README.md` v kazde slozce. `dentaline-web`, `domident-web` a
`dentist/template` zustavaji na Pages beze zmen jen kvuli starym odkazum — needituj
je dal, edituj rovnou `ukazka-1/2/3`.

**POZOR — base path je zapecenej v buildu.** `ukazka-1/` a `ukazka-2/` jsou *hotove
buildy* (React/Vite), takze maji absolutni cesty `/salon-system/<slozka>/` primo
v JS bundlech (`assets/*.js`): router basepath, `fetch` na `studia/<slug>.json`
i URL obrazku. Pri kopirovani/prejmenovani slozky **nestaci prepsat `index.html`** —
je nutne prepsat i vsechny vyskyty v `assets/*.js`, jinak SPA nenamatchuje routu
a stranka zustane prazdna. Kontrola:
`grep -ro "/salon-system/[a-z0-9/-]*" ukazka-N | sort -u` — vse musi ukazovat na
`ukazka-N`. (`ukazka-3/` je plain HTML s relativnimi cestami, tam problem neni.)

Pred rozeslanim odkazu vzdy over, ze se web opravdu prebrandoval — v titulku,
hlavicce i paticce ma byt jmeno ordinace a nikde nesmi zbyt `Dentaline`/`DomiDent`.

## Klicova fakta

- Barvy: `src/styles.css` -> `:root` (oklch). Meni se `--primary`, `--accent`, `--ring`.
- Texty: `src/routes/index.tsx`. SEO/title/font: `index.html` (po prevodu). Assety: `src/assets/` + `public/`.
- **POZOR:** novejsi Lovable sablona (TanStack Start SSR, Vite 8, nitro 3 beta) ma
  **rozbity staticky build** (`html file for SSR`). Scaffolder proto kazdou kopii
  **prevede na klientsky Vite SPA** (index.html + main.tsx, react-router, plain Vite).
  Vystup buildu je **`dist/`**. Nepokousej se to resit ladenim nitro/prerender.
- Base path z nazvu repa (workflow injektuje `BASE_PATH`).
- Lovable historie: NEprepisovat pushnute commity (force-push/rebase) — sync do Lovable.
