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

### Vlastni stranka pro kazdou ordinaci: `ordinace/<slug>/`

Odkazy `ukazka-N/?studio=<slug>` mely vadu: jmeno ordinace doplnil az JavaScript,
takze staticky `<title>` (a tim i **nahled odkazu** v mailu/WhatsAppu) hlasil
`Dentaline` / `DomiDent`, a OG tagy chybely uplne.

Proto ma dnes kazda ordinace vlastni stranku `ordinace/<slug>/` — jmeno je uz
ve statickem HTML (title, description, og:*), v URL neni zadny `?studio=`:

```
https://david-kral.github.io/salon-system/ordinace/<slug>/
```

Generuje se z `ukazka-*/studia/*.json`, **nic se nekopiruje** — stranky odkazuji
absolutne do `ukazka-N/assets/`, takze 44 ordinaci = 360 kB.

```bash
node patch-bundly.mjs && node gen-ordinace.mjs && python gen-leady.py
```

- `patch-bundly.mjs` — idempotentne opravi hotove buildy: basepath routeru se bere
  z `location.pathname` (jinak router na jine ceste nenamatchuje routu a stranka
  je prazdna) a slug se cte z `window.__STUDIO__`, `?studio=` zustava fallback.
  Taky prepise relativni `"./assets/` v `ukazka-3/config.json` a `studia/*.json`
  na absolutni — jinak se vyhodnoti proti adrese stranky a obrazky jsou 404.
- `gen-ordinace.mjs` — vygeneruje `ordinace/<slug>/index.html` + `manifest.json`.
- `gen-leady.py` — z manifestu poskláda `LEADY-VSECHNY.md` (seznam vsech 40 leadu).

**Stare odkazy `ukazka-N/?studio=<slug>` funguji dal** — uz rozeslane maily se
nerozbily. Pro nove oslovovani pouzivej `ordinace/<slug>/`.

Kdyz pridas nove studio: pridej JSON do `ukazka-N/studia/` a pust ty tri prikazy.
Nova slozka v korenu repa se **musi** pridat do `cp -r` seznamu ve
`.github/workflows/deploy-pages.yml`, jinak ji Pages nepublikuji (404).

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


# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
