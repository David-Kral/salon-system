import { defineConfig } from "@lovable.dev/vite-tanstack-config";

const base = process.env.BASE_PATH || "/";

export default defineConfig({
    vite: { base },
    tanstackStart: {
        prerender: { enabled: true, crawlLinks: true },
    },
    nitro: { preset: "static" },
});