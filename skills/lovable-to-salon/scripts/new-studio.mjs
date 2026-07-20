#!/usr/bin/env node
/**
 * new-studio.mjs — z Lovable / TanStack Start projektu udela novou kopii studia
 * a PREVEDE ji na cisty klientsky Vite SPA (spolehlivy staticky build -> GitHub Pages).
 *
 * Proc: novejsi Lovable sablona (TanStack Start = SSR, Vite 8, nitro 3 beta) ma
 * rozbity staticky build. Prevod na klientsky SPA (index.html + main.tsx,
 * @tanstack/react-router, plain Vite) to obchazi a builduje do dist/.
 *
 * Pouziti:
 *   node new-studio.mjs <sablona> <nazev-studia> [cilova-slozka]
 *   node new-studio.mjs --from <cesta-k-lovable-projektu> <nazev-studia> [cilova-slozka]
 */

import fs from "node:fs";
import path from "node:path";

const TEMPLATES = {
  dentaline: "C:\\Users\\david\\IdeaProjects\\dentaline-modern-sparkle",
  domident:  "C:\\Users\\david\\IdeaProjects\\domident-refined",
};
const DEFAULT_OUTPUT_DIR = process.cwd();
const SKIP = new Set([
  ".git", "node_modules", "dist", ".tanstack", ".output", ".nitro", ".vinxi",
  ".idea", ".qodo",
]);

function fail(msg) {
  console.error("\n[X] " + msg + "\n");
  console.error("Pouziti:");
  console.error("  node new-studio.mjs <sablona> <nazev-studia> [cilova-slozka]");
  console.error("  node new-studio.mjs --from <cesta> <nazev-studia> [cilova-slozka]");
  console.error("Sablony: " + Object.keys(TEMPLATES).join(", "));
  process.exit(1);
}

const argv = process.argv.slice(2);
let src, studioName, outArg;
if (argv[0] === "--from") {
  src = argv[1]; studioName = argv[2]; outArg = argv[3];
  if (!src) fail("Chybi cesta po --from.");
} else {
  const t = argv[0];
  if (!t) fail("Chybi sablona.");
  src = TEMPLATES[t];
  if (!src) fail("Neznama sablona '" + t + "'. Pouzij --from <cesta>.");
  studioName = argv[1]; outArg = argv[2];
}
if (!studioName) fail("Chybi nazev studia.");
if (!fs.existsSync(src)) fail("Zdroj nenalezen: " + src);

const slug = studioName.trim().toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, "");
if (!slug) fail("Neplatny nazev studia.");
const dest = path.join(outArg || DEFAULT_OUTPUT_DIR, slug);
if (fs.existsSync(dest)) fail("Cilova slozka uz existuje: " + dest);

fs.cpSync(src, dest, { recursive: true, filter: (s) => !SKIP.has(path.basename(s)) });
const rd = (p) => fs.readFileSync(path.join(dest, p), "utf8");
const wr = (p, c) => { fs.mkdirSync(path.dirname(path.join(dest, p)), { recursive: true }); fs.writeFileSync(path.join(dest, p), c); };
const rm = (p) => { const f = path.join(dest, p); if (fs.existsSync(f)) fs.rmSync(f, { recursive: true, force: true }); };

// SEO z puvodniho SSR __root.tsx
let title = slug, description = "", fontHref = "", faviconHref = "/favicon.ico";
try {
  const root = rd("src/routes/__root.tsx");
  const mTitle = root.match(/\{\s*title:\s*"([^"]+)"/); if (mTitle) title = mTitle[1];
  const mDesc = root.match(/name:\s*"description",\s*content:\s*"([^"]+)"/); if (mDesc) description = mDesc[1];
  const mFont = root.match(/href:\s*"(https:\/\/fonts\.googleapis\.com\/css2[^"]+)"/); if (mFont) fontHref = mFont[1];
  const mFav = root.match(/rel:\s*"icon",\s*href:\s*"([^"]+)"/); if (mFav) faviconHref = mFav[1];
} catch {}

const pkg = JSON.parse(rd("package.json"));
pkg.name = slug;
pkg.scripts = pkg.scripts || {};
pkg.scripts.dev = "vite"; pkg.scripts.build = "vite build"; pkg.scripts.preview = "vite preview";
for (const dep of ["@tanstack/react-start", "nitro", "@lovable.dev/vite-tanstack-config"]) {
  if (pkg.dependencies) delete pkg.dependencies[dep];
  if (pkg.devDependencies) delete pkg.devDependencies[dep];
}
wr("package.json", JSON.stringify(pkg, null, 2) + "\n");

wr("vite.config.ts", [
  'import { defineConfig } from "vite";',
  'import react from "@vitejs/plugin-react";',
  'import tailwindcss from "@tailwindcss/vite";',
  'import tsconfigPaths from "vite-tsconfig-paths";',
  'import { tanstackRouter } from "@tanstack/router-plugin/vite";',
  "",
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
  "<!doctype html>", '<html lang="cs">', "  <head>", ...headLines, "  </head>",
  "  <body>", '    <div id="root"></div>', '    <script type="module" src="/src/main.tsx"></script>',
  "  </body>", "</html>", "",
].join("\n"));

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

wr("src/routes/__root.tsx", `import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Outlet, Link, createRootRouteWithContext, useRouter } from "@tanstack/react-router";
import { useEffect } from "react";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-7xl font-bold text-foreground">404</h1>
        <h2 className="mt-4 text-xl font-semibold text-foreground">Stranka nenalezena</h2>
        <div className="mt-6">
          <Link to="/" className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">Zpet na domovskou stranku</Link>
        </div>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  const router = useRouter();
  useEffect(() => { console.error("Route error:", error); }, [error]);
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Stranka se nenacetla</h1>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <button onClick={() => { router.invalidate(); reset(); }} className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">Zkusit znovu</button>
          <a href="/" className="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent">Domu</a>
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

{
  let r = rd("src/router.tsx");
  if (!r.includes("basepath")) {
    r = r.replace("const router = createRouter({", [
      "const rawBase = import.meta.env.BASE_URL;",
      '  const basepath = rawBase === "/" ? undefined : rawBase.replace(/\\/$/, "");',
      "", "  const router = createRouter({", "    basepath,",
    ].join("\n"));
    wr("src/router.tsx", r);
  }
}

rm("src/server.ts");
rm("src/start.ts");

const D = "$";
wr(".github/workflows/deploy-pages.yml", [
  "name: Deploy to GitHub Pages", "",
  "on:", "  push:", "    branches: [main, master]", "  workflow_dispatch:", "",
  "permissions:", "  contents: read", "  pages: write", "  id-token: write", "",
  "concurrency:", "  group: pages", "  cancel-in-progress: true", "",
  "jobs:", "  build:", "    runs-on: ubuntu-latest", "    steps:",
  "      - uses: actions/checkout@v4",
  "      - uses: actions/setup-node@v4", "        with:", "          node-version: 22",
  "      - run: npm install",
  "      - name: Build (static SPA)", "        env:",
  '          BASE_PATH: /' + D + '{{ github.event.repository.name }}/',
  "        run: npm run build",
  "      - name: SPA fallback + .nojekyll", "        run: |",
  "          cp dist/index.html dist/404.html || true", "          touch dist/.nojekyll",
  "      - uses: actions/upload-pages-artifact@v3", "        with:", "          path: dist", "",
  "  deploy:", "    environment:", "      name: github-pages",
  '      url: ' + D + '{{ steps.deployment.outputs.page_url }}',
  "    runs-on: ubuntu-latest", "    needs: build", "    steps:",
  "      - id: deployment", "        uses: actions/deploy-pages@v4", "",
].join("\n"));

wr("PREBARVENI.md", [
  "# Prebarveni studia \"" + slug + "\" (klientsky SPA)", "",
  "Barvy: src/styles.css -> :root (oklch). Zmen --primary, --accent, --ring.",
  "Texty: src/routes/index.tsx. SEO/title/font: index.html (koren). Logo/fotky: src/assets/ + public/.",
  "", "Build: npm install && npm run build  (vystup: dist/)",
  "Nasazeni: GitHub repo -> Settings -> Pages -> GitHub Actions -> push.", "",
].join("\n"));

console.log("\n[OK] Nove studio (klientsky SPA): " + dest);
console.log("Dalsi: cd, npm install && npm run build (dist/), uprav styles.css + texty, push do repa.\n");
