// 1. Importa 'globals' al inicio
import globals from 'globals'
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}'],
  },

  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
  },

  // 2. Agrega este nuevo objeto para definir los globales
  {
    languageOptions: {
      globals: {
        ...globals.browser, // Define los globales del navegador como 'console', 'window', etc.
        ...globals.node, // Opcional, pero recomendado si usas scripts de Node
      },
    },
  },

  // El resto de tu configuración
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  skipFormatting,
]
