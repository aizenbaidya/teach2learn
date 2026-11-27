import { defineConfig } from "vite";

export default defineConfig({
    build: {
        outDir: "static/dist/",
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
