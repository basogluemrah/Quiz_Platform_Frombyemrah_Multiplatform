import { defineConfig } from 'vite'
export default defineConfig({
  root: '.',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    // The local JSON generator in admin.html is deliberately excluded from public builds.
  },
  server: {
    port: 3000,
    open: true
  }
})
