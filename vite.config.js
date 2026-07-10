import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],

  build: {
    outDir: "static/build",
    emptyOutDir: true,
    manifest: true,

    rollupOptions: {
      input: {
        app: "frontend/js/app.js",
      },
    },
  },
});
