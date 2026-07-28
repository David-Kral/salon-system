#!/usr/bin/env node
/**
 * Upraví hotové buildy ukazka-1/ukazka-2 (a ukazka-3/index.html) tak, aby
 * fungovaly i na vlastní adrese `ordinace/<slug>/`:
 *
 *   1) basepath routeru se přestane brát ze zapečeného `/salon-system/ukazka-N/`
 *      a odvodí se z `location.pathname`. Bez toho router na jiné cestě
 *      nenamatchuje routu a stránka zůstane prázdná (viz varování v CLAUDE.md).
 *
 *   2) slug studia se přednostně bere z `window.__STUDIO__` (vloží ho
 *      generovaná stránka), `?studio=` v URL zůstává jako fallback —
 *      takže UŽ ROZESLANÉ odkazy `ukazka-N/?studio=<slug>` fungují dál.
 *
 * Cesty k assetům a k `studia/<slug>.json` zůstávají absolutní do
 * `ukazka-N/`, takže se nic nekopíruje.
 *
 * Skript je idempotentní — opakované spuštění nic nerozbije.
 *
 * Spuštění:  node patch-bundly.mjs
 */

import fs from "node:fs";
import path from "node:path";

const ROOT = import.meta.dirname;
let changed = 0;
let already = 0;

const DYNAMIC_BASEPATH = "location.pathname.replace(/index\\.html?$/,``).replace(/\\/$/,``)";

function patchReactBundle(tpl) {
  const dir = path.join(ROOT, tpl, "assets");
  const file = fs
    .readdirSync(dir)
    .find((f) => /^index-.*\.js$/.test(f) && fs.readFileSync(path.join(dir, f), "utf8").includes("basepath:"));
  if (!file) throw new Error(`${tpl}: nenašel jsem bundle s basepath:`);
  const p = path.join(dir, file);
  let js = fs.readFileSync(p, "utf8");
  const orig = js;

  // 1) dynamický basepath
  const bakedBasepath = "basepath:`/salon-system/" + tpl + "/`.replace(/\\/$/,``)";
  if (js.includes(bakedBasepath)) {
    js = js.replace(bakedBasepath, "basepath:" + DYNAMIC_BASEPATH);
  } else if (!js.includes("basepath:" + DYNAMIC_BASEPATH)) {
    throw new Error(`${tpl}/${file}: nenašel jsem zapečený basepath ani hotový patch`);
  }

  // 2) slug z window.__STUDIO__, ?studio= jako fallback
  const bakedSlug = "let e=new URLSearchParams(location.search).get(`studio`);if(!e)return ma;";
  const patchedSlug =
    "let e=window.__STUDIO__||new URLSearchParams(location.search).get(`studio`);if(!e)return ma;";
  if (js.includes(bakedSlug)) {
    js = js.replace(bakedSlug, patchedSlug);
  } else if (!js.includes(patchedSlug)) {
    throw new Error(`${tpl}/${file}: nenašel jsem čtení ?studio= ani hotový patch`);
  }

  if (js !== orig) {
    fs.writeFileSync(p, js, "utf8");
    console.log(`  patch: ${tpl}/assets/${file}`);
    changed++;
  } else {
    console.log(`  už opravené: ${tpl}/assets/${file}`);
    already++;
  }
}

function patchPlainTemplate(tpl) {
  const p = path.join(ROOT, tpl, "index.html");
  let html = fs.readFileSync(p, "utf8");
  const orig = html;

  const baked = "const slug = new URLSearchParams(location.search).get('studio');";
  const patched =
    "const slug = window.__STUDIO__ || new URLSearchParams(location.search).get('studio');";
  if (html.includes(baked)) {
    html = html.replace(baked, patched);
  } else if (!html.includes(patched)) {
    throw new Error(`${tpl}/index.html: nenašel jsem čtení ?studio= ani hotový patch`);
  }

  if (html !== orig) {
    fs.writeFileSync(p, html, "utf8");
    console.log(`  patch: ${tpl}/index.html`);
    changed++;
  } else {
    console.log(`  už opravené: ${tpl}/index.html`);
    already++;
  }
}

/**
 * ukazka-3 bere cesty k obrázkům z `config.json` a `studia/*.json` a strká je
 * do `src`. Relativní "./assets/..." se pak vyhodnotí proti ADRESE STRÁNKY,
 * takže na `ordinace/<slug>/` skončí jako 404. Přepíšeme je na absolutní —
 * funguje to pak i na původní adrese `ukazka-3/`.
 */
function patchPlainAssetPaths(tpl) {
  const files = [
    path.join(ROOT, tpl, "config.json"),
    ...fs
      .readdirSync(path.join(ROOT, tpl, "studia"))
      .filter((f) => f.endsWith(".json"))
      .map((f) => path.join(ROOT, tpl, "studia", f)),
  ].filter((p) => fs.existsSync(p));

  for (const p of files) {
    const orig = fs.readFileSync(p, "utf8");
    const next = orig.replaceAll('"./assets/', `"/salon-system/${tpl}/assets/`);
    if (next !== orig) {
      JSON.parse(next); // pojistka, ať nerozbijeme JSON
      fs.writeFileSync(p, next, "utf8");
      console.log(`  patch: ${path.relative(ROOT, p)}`);
      changed++;
    }
  }
}

console.log("Patchuju šablony:");
patchReactBundle("ukazka-1");
patchReactBundle("ukazka-2");
patchPlainTemplate("ukazka-3");
patchPlainAssetPaths("ukazka-3");
console.log(`\nHotovo — změněno ${changed}, už bylo opravené ${already}.`);
