import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // This is the specific line you are likely missing:
    host: true,
    strictPort: true,
    port: 5173,
    // Add polling if you are on Windows/WSL to fix hot reload bugs
    watch: {
      usePolling: true,
    },
  },
});
