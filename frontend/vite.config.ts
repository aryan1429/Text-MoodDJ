import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.js'
  },
  server: {
    port: 5173,
    host: true,
    // Reduce noise from extensions in console
    fs: {
      strict: false
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Reduce bundle analyzer noise
    rollupOptions: {
      external: [],
      output: {
        manualChunks: undefined
      }
    }
  },
  // Suppress some development warnings
  logLevel: 'info'
})
