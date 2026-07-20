#!/usr/bin/env node
/**
 * nova-studio.mjs — vytvori nove studio ze startovaci sablony (Dentaline / Domident)
 * a PREVEDE ho na cisty klientsky Vite SPA (jako funkcni stationery-haven),
 * ktery se spolehlive vybuildi a nasadi na GitHub Pages.
 *
 * Proc: Dentaline/Domident jsou z novejsi Lovable sablony (TanStack Start = SSR,
 * Vite 8, nitro 3 beta) a jejich staticky build je v teto verzni kombinaci rozbity.
 * Prevod na klientsky SPA (index.html + main.tsx, react-router, plain Vite) to obchazi.
 *
 * Pouziti:
 *   node nova-studio.mjs <sablona> <nazev-studia> [cilova-slozka]
 * Priklady:
 *   node nova-studio.mjs dentaline kr-dent
 *   node nova-studio.mjs domident  usmev-brno
 */

import fs from "node:fs";
import path from "node:path";

const TEMPLATES = {
  dentaline: "C:\\Users\\david\\IdeaProjects\\dentaline-modern-sparkle",
  domident:  "C:\\Users\\david\\IdeaProjects\\domident-refined",
};
const DEFAULT_OUTPUT_DIR = "C:\\Users\\david\\IdeaProjects";
const SKIP = new Set([
  ".git", "node_modules", "dist", ".tanstack", ".output", ".nitro", ".vinxi",
  ".idea", ".qodo",
]);

function fail(msg) {
  console.error("\n[X] " + msg + "\n");
  console.error("Pouziti: node nova-studio.mjs <sablona> <nazev-studia> [cilova-slozka]");
  console.error("Dostupne sablony: " + Object.keys(TEMPLATES).join(", "));
  process.exit(1);
}

const [, , templateName, studioName, outArg] = process.argv;
if (!templateName || !studioName) fail("Chybi argument.");
const src = TEMPLATES[templateName];
if (!src) fail("Neznama sablona '" + templateName + "'.");
if (!fs.existsSync(src)) fail("Sablona '" + templateName + "' nenalezena: " + src);

const slug = studioName.trim().toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, "");
if (!slug) fail("Neplatny nazev studia.");

const dest = path.join(outArg || DEFAULT_OUTPUT_DIR, slug);
if (fs.existsSync(dest)) fail("Cilova slozka uz existuje: " + dest);

// 1) cista kopie
fs.cpSync(src, dest, { recursive: true, filter: (s) => !SKIP.has(path.basename(s)) });

const rd = (p) => fs.readFileSync(path.join(dest, p), "utf8");
const wr = (p, c) => { fs.mkdirSync(path.dirname(path.join(dest, p)), { recursive: true }); fs.writeFileSync(path.join(dest, p), c); };
const rm = (p) => { const f = path.join(dest, p); if (fs.existsSync(f)) fs.rmSync(f, { recursive: true, force: true }); };

// 2) vytahnout SEO/head z puvodniho SSR __root.tsx (title, description, font, favicon)
let title = slug, description = "", fontHref = "", faviconHref = "/favicon.ico";
try {
  const root = rd("src/routes/__root.tsx");
  const mTitle = root.match(/\{\s*title:\s*"([^"]+)"/);
  if (mTitle) title = mTitle[1];
  const mDesc = root.match(/name:\s*"description",\s*content:\s*"([^"]+)"/);
  if (mDesc) description = mDesc[1];
  const mFont = root.match(/href:\s*"(https:\/\/fonts\.googleapis\.com\/css2[^"]+)"/);
  if (mFont) fontHref = mFont[1];
  const mFav = root.match(/rel:\s*"icon",\s*href:\s*"([^"]+)"/);
  if (mFav) faviconHref = mFav[1];
} catch {}

// 3) package.json -> prejmenovat, build = vite build, odebrat SSR/nitro/lovable deps
const pkg = JSON.parse(rd("package.json"));
pkg.name = slug;
pkg.scripts = pkg.scripts || {};
pkg.scripts.dev = "vite";
pkg.scripts.build = "vite build";
pkg.scripts.preview = "vite preview";
for (const dep of ["@tanstack/react-start", "nitro"]) {
  if (pkg.dependencies) delete pkg.dependencies[dep];
  if (pkg.devDependencies) delete pkg.devDependencies[dep];
}
if (pkg.devDependencies) delete pkg.devDependencies["@lovable.dev/vite-tanstack-config"];
if (pkg.dependencies) delete pkg.dependencies["@lovable.dev/vite-tanstack-config"];
wr("package.json", JSON.stringify(pkg, null, 2) + "\n");

// 4) plain Vite config (bez lovable/nitro); base injektuje CI
wr("vite.config.ts", [
  'import { defineConfig } from "vite";',
  'import react from "@vitejs/plugin-react";',
  'import tailwindcss from "@tailwindcss/vite";',
  'import tsconfigPaths from "vite-tsconfig-paths";',
  'import { tanstackRouter } from "@tanstack/router-plugin/vite";',
  "",
  '// BASE_PATH injektuje GitHub Actions (= /<nazev-repa>/). Lokalne "/".',
  'const base = process.env.BASE_PATH || "/";',
  "",
  "export default defineConfig({",
  "  base,",
  "  plugins: [",
  "    tsconfigPaths(),",
  "    tailwindcss(),",
  '    tanstackRouter({ target: "react", autoCodeSplitting: true }),',
  "    react(),",
  "  ],",
  "});",
  "",
].join("\n"));

// 5) index.html (klientsky entry) s prevzatym SEO
const headLines = [
  '    <meta charset="UTF-8" />',
  '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />',
  '    <title>' + title + "</title>",
];
if (description) headLines.push('    <meta name="description" content="' + description.replace(/"/g, "&quot;") + '" />');
headLines.push('    <link rel="icon" href="' + faviconHref + '" />');
if (fontHref) {
  headLines.push('    <link rel="preconnect" href="https://fonts.googleapis.com" />');
  headLines.push('    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />');
  headLines.push('    <link href="' + fontHref + '" rel="stylesheet" />');
}
wr("index.html", [
  "<!doctype html>",
  '<html lang="cs">',
  "  <head>",
  ...headLines,
  "  </head>",
  "  <body>",
  '    <div id="root"></div>',
  '    <script type="module" src="/src/main.tsx"></script>',
  "  </body>",
  "</html>",
  "",
].join("\n"));

// 6) src/main.tsx (klientsky bootstrap)
wr("src/main.tsx", `import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "@tanstack/react-router";
import { getRouter } from "./router";
import "./styles.css";

const router = getRouter();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
`);

// 7) src/routes/__root.tsx -> klientska verze (bez SSR shellu, Scripts, head)
wr("src/routes/__root.tsx", `import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
} from "@tanstack/react-router";
import { useEffect } from "react";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-7xl font-bold text-foreground">404</h1>
        <h2 className="mt-4 text-xl font-semibold text-foreground">Stranka nenalezena</h2>
        <div className="mt-6">
          <Link to="/" className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">
            Zpet na domovskou stranku
          </Link>
        </div>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  const router = useRouter();
  useEffect(() => {
    console.error("Route error:", error);
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Stranka se nenacetla</h1>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <button onClick={() => { router.invalidate(); reset(); }} className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">
            Zkusit znovu
          </button>
          <a href="/" className="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent">
            Domu
          </a>
        </div>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  );
}
`);

// 8) router.tsx -> doplnit basepath z BASE_URL (kvuli podslozce /<repo>/)
{
  let r = rd("src/router.tsx");
  if (!r.includes("basepath")) {
    r = r.replace("const router = createRouter({", [
      "const rawBase = import.meta.env.BASE_URL;",
      '  const basepath = rawBase === "/" ? undefined : rawBase.replace(/\\/$/, "");',
      "",
      "  const router = createRouter({",
      "    basepath,",
    ].join("\n"));
    wr("src/router.tsx", r);
  }
}

// 9) odstranit SSR-only soubory
rm("src/server.ts");
rm("src/start.ts");

// 10) GitHub Actions workflow (build -> dist/ -> Pages)
const D = "$";
wr(".github/workflows/deploy-pages.yml", [
  "name: Deploy to GitHub Pages",
  "",
  "on:",
  "  push:",
  "    branches: [main, master]",
  "  workflow_dispatch:",
  "",
  "permissions:",
  "  contents: read",
  "  pages: write",
  "  id-token: write",
  "",
  "concurrency:",
  "  group: pages",
  "  cancel-in-progress: true",
  "",
  "jobs:",
  "  build:",
  "    runs-on: ubuntu-latest",
  "    steps:",
  "      - uses: actions/checkout@v4",
  "      - uses: actions/setup-node@v4",
  "        with:",
  "          node-version: 22",
  "      - run: npm install",
  "      - name: Build (static SPA)",
  "        env:",
  '          BASE_PATH: /' + D + '{{ github.event.repository.name }}/',
  "        run: npm run build",
  "      - name: SPA fallback + .nojekyll",
  "        run: |",
  "          cp dist/index.html dist/404.html || true",
  "          touch dist/.nojekyll",
  "      - uses: actions/upload-pages-artifact@v3",
  "        with:",
  "          path: dist",
  "",
  "  deploy:",
  "    environment:",
  "      name: github-pages",
  '      url: ' + D + '{{ steps.deployment.outputs.page_url }}',
  "    runs-on: ubuntu-latest",
  "    needs: build",
  "    steps:",
  "      - id: deployment",
  "        uses: actions/deploy-pages@v4",
  "",
].join("\n"));

// 11) PREBARVENI.md
const domidentNote = templateName === "domident"
  ? "\n> Domident ma nahore \"Logo-derived palette\" (--charcoal, --mist, --bone, --ivory). Zmen tyhle 4.\n"
  : "";
wr("PREBARVENI.md", [
  "# Prebarveni studia \"" + slug + "\" (sablona: " + templateName + ", klientsky SPA)",
  "",
  "Barvy: src/styles.css -> blok :root (oklch). Zmen --primary, --accent, --ring.",
  domidentNote,
  "Texty: src/routes/index.tsx. SEO/title/font: index.html (v koreni).",
  "Logo/fotky: src/assets/ + public/.",
  "",
  "Nahled:  npm install && npm run dev",
  "Build:   npm run build   (vystup: dist/)",
  "",
  "Nasazeni: nahraj do GitHub repa -> Settings -> Pages -> Source: GitHub Actions",
  "-> push -> web na https://<user>.github.io/<repo>/ (base z nazvu repa automaticky).",
  "",
].join("\n"));

console.log("\n[OK] Nove studio (klientsky SPA) ze sablony '" + templateName + "':");
console.log("   " + dest);
console.log("   Prevedeno na plain Vite SPA (index.html + main.tsx, bez SSR/nitro).\n");
console.log("Dalsi kroky:");
console.log("   1) cd " + dest);
console.log("   2) npm install  &&  npm run build   (vystup: dist/)");
console.log("   3) uprav barvy (src/styles.css) a texty (src/routes/index.tsx)");
console.log("   4) push do noveho GitHub repa, Settings -> Pages -> 'GitHub Actions'\n");
