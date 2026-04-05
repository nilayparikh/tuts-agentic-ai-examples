import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      "/api": "http://localhost:3100",
      "/health": "http://localhost:3100",
    },
  },
});
