import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";

const shared = fileURLToPath(new URL("../../ui_shared/src", import.meta.url));

export default defineConfig({
  plugins: [react()],
  base: "/",
  resolve: { alias: { "@ff": shared } },
  server: { fs: { allow: [fileURLToPath(new URL("../../..", import.meta.url))] } },
  build: { outDir: "dist", emptyOutDir: true },
});
