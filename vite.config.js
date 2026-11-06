import { defineConfig } from "vite";

export default defineConfig({
    build: {
        outDir: "static/dist",
        emptyOutDir: true,
        rolldownOptions: {
            input: "assets/js/base.js",
        },
    },
});
