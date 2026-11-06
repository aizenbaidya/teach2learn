import { defineConfig } from "vite";

export default defineConfig({
    base: "static/dist/",
    build: {
        outDir: "static/dist/",
        emptyOutDir: true,
        rolldownOptions: {
            input: {
                base: "assets/js/base.js",
                homepage: "assets/js/homepage.js",
            },
            output: {
                entryFileNames: "[name].js",
                assetFileNames: "[name][extname]",
            },
        },
    },
});
