import { defineConfig } from "vite";

export default defineConfig({
    base: "/static/dist",
    build: {
        outDir: "static/dist",
        rolldownOptions: {
            input: {
                base: "static/js/base.js",
            },
            output: {
                entryFileNames: "[name].js",
                assetFileNames: "[name][extname]",
            },
        },
    },
});
