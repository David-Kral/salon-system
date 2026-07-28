#!/usr/bin/env node
/**
 * Vygeneruje pro KAŽDÉ studio vlastní stránku `ordinace/<slug>/index.html`.
 *
 * Proč: dosud se posílal odkaz `ukazka-N/?studio=<slug>`. Jméno ordinace
 * doplnil až JavaScript, takže:
 *   - statický <title> v HTML zůstával "Dentaline" / "DomiDent",
 *   - náhled odkazu (WhatsApp, Messenger, mailoví klienti) i první
 *     vykreslení karty ukazovaly cizí jméno kliniky,
 *   - chyběly OG tagy úplně.
 *
 * Tento skript vytvoří pro každé studio samostatnou stránku, která má
 * jméno ordinace už ve statickém HTML (title, description, OG, Twitter)
 * a slug předává přes `window.__STUDIO__` — žádný `?studio=` v URL.
 *
 * Těžké assety (JS bundle, CSS, fotky) se NEkopírují: stránky odkazují
 * absolutně do `ukazka-N/assets/`, takže 40 ordinací nezvětší repo.
 *
 * Staré odkazy `ukazka-N/?studio=<slug>` fungují dál (viz patch-bundly.mjs,
 * který nechává `?studio=` jako fallback).
 *
 * Spuštění:  node gen-ordinace.mjs
 */

import fs from "node:fs";
import path from "node:path";

const ROOT = import.meta.dirname;
const BASE = "/salon-system";
const OUT_DIR = path.join(ROOT, "ordinace");

/** Když stejný slug existuje ve víc šablonách, tady je rozhodnuto, která
 *  se použije — musí odpovídat šabloně, se kterou už byl lead oslovený. */
const OVERRIDE = {
  bistrodent: "ukazka-2", // mail šel na domident-web
  "lfdent-olomouc": "ukazka-3", // mail šel na dentist/template
  "petr-seda": "ukazka-3",
  "usmev-jana": "ukazka-3",
};

const esc = (s) =>
  String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

/** Přípona "— zubní ordinace" se přidá jen tehdy, když už jméno samo
 *  neříká, že jde o zubaře (jinak vznikne "Zubní ordinace X — zubní ordinace"). */
function smartTitle(name) {
  return /zub|stomatolog|dent/i.test(name) ? name : `${name} — zubní ordinace`;
}

/** Z původního index.html vytáhne odkazy na fonty/CSS/JS, ať se generátor
 *  nerozbije, když se změní hash v názvu buildu. */
function readShell(tpl) {
  const html = fs.readFileSync(path.join(ROOT, tpl, "index.html"), "utf8");
  const fonts = [...html.matchAll(/<link[^>]+fonts\.(googleapis|gstatic)[^>]*>/g)].map((m) => m[0]);
  const preconnect = [...html.matchAll(/<link rel="preconnect"[^>]*>/g)].map((m) => m[0]);
  const js = html.match(/<script type="module"[^>]*src="([^"]+)"[^>]*>/);
  const css = html.match(/<link rel="stylesheet"[^>]*href="([^"]+\.css)"[^>]*>/);
  if (!js || !css) throw new Error(`${tpl}: nenašel jsem <script>/<link rel=stylesheet> v index.html`);
  return {
    fontLinks: [...new Set([...preconnect, ...fonts])].join("\n  "),
    jsSrc: js[1],
    cssHref: css[1],
  };
}

/** Najde reprezentativní obrázek pro OG náhled. */
function findOgImage(tpl) {
  const dir = path.join(ROOT, tpl, "assets");
  if (!fs.existsSync(dir)) return null;
  const files = fs.readdirSync(dir);
  const hero =
    files.find((f) => /^hero.*\.(jpg|jpeg|png|webp)$/i.test(f)) ||
    files.find((f) => /\.(jpg|jpeg|png|webp)$/i.test(f));
  return hero ? `${BASE}/${tpl}/assets/${hero}` : null;
}

/** React SPA (ukazka-1, ukazka-2): tenká vlastní schránka nad společnými assety. */
function pageForReact(tpl, slug, studio, shell, ogImage) {
  const name = studio.nazev || studio.name || slug;
  const title = smartTitle(name);
  const desc =
    studio.description ||
    `${name} — moderní zubní péče, přehledný ceník a objednání termínu online.`;
  const url = `${BASE}/ordinace/${slug}/`;
  return `<!doctype html>
<html lang="cs">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="${esc(name)}" />
  <meta property="og:title" content="${esc(title)}" />
  <meta property="og:description" content="${esc(desc)}" />
  <meta property="og:url" content="${esc(url)}" />${
    ogImage ? `\n  <meta property="og:image" content="${esc(ogImage)}" />` : ""
  }
  <meta name="twitter:card" content="${ogImage ? "summary_large_image" : "summary"}" />
  <meta name="twitter:title" content="${esc(title)}" />
  <meta name="twitter:description" content="${esc(desc)}" />
  <link rel="icon" href="${BASE}/${tpl}/favicon.ico" />
  ${shell.fontLinks}
  <script>window.__STUDIO__=${JSON.stringify(slug)};window.__TENANT_BASE__=${JSON.stringify(
    `${BASE}/${tpl}/`
  )};</script>
  <script type="module" crossorigin src="${shell.jsSrc}"></script>
  <link rel="stylesheet" crossorigin href="${shell.cssHref}">
</head>
<body>
  <div id="root"></div>
</body>
</html>
`;
}

/** ukazka-3 je plain HTML s relativními cestami — kopii přepíšeme na
 *  absolutní cesty do společné složky a doplníme statické meta tagy. */
function pageForPlain(tpl, slug, studio, ogImage) {
  let html = fs.readFileSync(path.join(ROOT, tpl, "index.html"), "utf8");
  const name = studio.nazev || studio.name || slug;
  const title = smartTitle(name);
  const desc =
    studio.description ||
    `${name} — moderní zubní péče, přehledný ceník a objednání termínu online.`;
  const url = `${BASE}/ordinace/${slug}/`;

  // relativní "./x" -> absolutní do společné složky šablony
  const before = (html.match(/(["'])\.\//g) || []).length;
  html = html.replace(/(["'])\.\//g, `$1${BASE}/${tpl}/`);
  const after = (html.match(/(["'])\.\//g) || []).length;
  if (after !== 0) throw new Error(`${slug}: zůstaly relativní cesty (${after})`);
  if (before === 0) throw new Error(`${slug}: nenašel jsem žádnou relativní cestu k přepsání`);

  // slug natvrdo do stránky (JS ho pak vezme z window.__STUDIO__)
  html = html.replace(
    /<head>/,
    `<head>\n  <script>window.__STUDIO__=${JSON.stringify(slug)};</script>`
  );

  // statický title + description místo "Loading…"
  html = html.replace(
    /<title id="page-title">[^<]*<\/title>/,
    `<title id="page-title">${esc(title)}</title>`
  );
  html = html.replace(
    /<meta name="description" id="meta-desc" content="[^"]*">/,
    `<meta name="description" id="meta-desc" content="${esc(desc)}">`
  );

  // OG / Twitter tagy
  const og = [
    `<meta property="og:type" content="website" />`,
    `<meta property="og:site_name" content="${esc(name)}" />`,
    `<meta property="og:title" content="${esc(title)}" />`,
    `<meta property="og:description" content="${esc(desc)}" />`,
    `<meta property="og:url" content="${esc(url)}" />`,
    ogImage ? `<meta property="og:image" content="${esc(ogImage)}" />` : null,
    `<meta name="twitter:card" content="${ogImage ? "summary_large_image" : "summary"}" />`,
    `<meta name="twitter:title" content="${esc(title)}" />`,
    `<meta name="twitter:description" content="${esc(desc)}" />`,
  ]
    .filter(Boolean)
    .join("\n  ");
  html = html.replace(/<\/head>/, `  ${og}\n</head>`);

  return html;
}

// ── sesbírat studia ze všech šablon ────────────────────────────────────
const templates = ["ukazka-1", "ukazka-2", "ukazka-3"];
const found = new Map(); // slug -> [tpl, ...]

for (const tpl of templates) {
  const dir = path.join(ROOT, tpl, "studia");
  if (!fs.existsSync(dir)) continue;
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith(".json")) continue;
    const slug = f.replace(/\.json$/, "");
    if (!found.has(slug)) found.set(slug, []);
    found.get(slug).push(tpl);
  }
}

const shells = Object.fromEntries(
  templates.map((t) => [t, t === "ukazka-3" ? null : readShell(t)])
);
const ogImages = Object.fromEntries(templates.map((t) => [t, findOgImage(t)]));

fs.rmSync(OUT_DIR, { recursive: true, force: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

const manifest = [];
const dupes = [];

for (const [slug, tpls] of [...found].sort(([a], [b]) => a.localeCompare(b))) {
  let tpl = tpls[0];
  if (tpls.length > 1) {
    tpl = OVERRIDE[slug] && tpls.includes(OVERRIDE[slug]) ? OVERRIDE[slug] : tpls[0];
    dupes.push(`${slug}: ${tpls.join(", ")} -> ${tpl}`);
  }

  const studio = JSON.parse(
    fs.readFileSync(path.join(ROOT, tpl, "studia", `${slug}.json`), "utf8")
  );
  const html =
    tpl === "ukazka-3"
      ? pageForPlain(tpl, slug, studio, ogImages[tpl])
      : pageForReact(tpl, slug, studio, shells[tpl], ogImages[tpl]);

  fs.mkdirSync(path.join(OUT_DIR, slug), { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, slug, "index.html"), html, "utf8");

  manifest.push({
    slug,
    nazev: studio.nazev || studio.name || slug,
    sablona: tpl,
    url: `https://david-kral.github.io${BASE}/ordinace/${slug}/`,
  });
}

fs.writeFileSync(
  path.join(OUT_DIR, "manifest.json"),
  JSON.stringify(manifest, null, 2) + "\n",
  "utf8"
);

console.log(`Vygenerováno ${manifest.length} stránek do ordinace/`);
if (dupes.length) {
  console.log(`\nSlug ve víc šablonách (vybrána jedna):`);
  for (const d of dupes) console.log("  " + d);
}
