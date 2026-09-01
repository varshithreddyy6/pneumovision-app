import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    allowedHosts: true,
    proxy: {
      "/health": "http://127.0.0.1:8000",
      "/v1": "http://127.0.0.1:8000",
      "/docs": "http://127.0.0.1:8000",
    },
  },
  preview: {
    host: "0.0.0.0",
    port: 5173,
  },
});
