import { defineConfig } from "vite";

export default defineConfig({
    base: "/static/dist/",
    build: {
        outDir: "static/dist/",
        emptyOutDir: true,
        rolldownOptions: {
            input: {
                base: "static/js/base.js",
                "auth-base": "static/js/auth/auth-base.js",
                "teach-index": "static/js/teach/index.js",
            },
            output: {
                entryFileNames: "[name].js",
                assetFileNames: "[name][extname]",
            },
        },
    },
});
