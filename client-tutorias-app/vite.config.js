import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  // Agregamos la configuración de esbuild aquí
  esbuild: {
    // Elimina la función 'debugger' del código final
    drop: ['debugger'],
    // Elimina las llamadas a console.log, info, debug y trace,
    // pero MANTIENE console.warn y console.error para que puedas ver errores en producción.
    pure: ['console.log', 'console.info', 'console.debug', 'console.trace'],
  },
})
