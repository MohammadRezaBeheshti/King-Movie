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

  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
  },
});
