import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    // Default: your running `npm run dev` server. `npm run test:e2e` overrides this to a production build on :3100.
    baseUrl: process.env.CYPRESS_BASE_URL ?? "http://localhost:3000",
    defaultCommandTimeout: 15000,
    // First Pyodide load can be slow on a cold cache.
    pageLoadTimeout: 120000,
    video: false,
    screenshotOnRunFailure: true,
    retries: { runMode: 1, openMode: 0 },
  },
});
