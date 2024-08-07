import { FlatCompat } from '@eslint/eslintrc'
import js from '@eslint/js'
import path from 'path'
import { fileURLToPath } from 'url'
import { sveltePreprocess } from 'svelte-preprocess'
import typescript from 'typescript'
import eslintPluginSvelte from 'eslint-plugin-svelte'

// Mimic CommonJS variables -- not needed if using CommonJS
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const compat = new FlatCompat({
  baseDirectory: __dirname, // optional; default: process.cwd()
  resolvePluginsRelativeTo: __dirname, // optional
  recommendedConfig: js.configs.recommended, // optional unless you're using "eslint:recommended"
  allConfig: js.configs.all, // optional unless you're using "eslint:all"
})

export default [
  ...eslintPluginSvelte.configs['flat/recommended'],
  {
    rules: {
      // override/add rules settings here, such as:
      // 'svelte/rule-name': 'error'
    },
  },

  // Mimic environments
  ...compat.env({
    es2020: true,
    browser: true,
    node: true,
  }),

  // Translate an entire config
  ...compat.config({
    plugins: ['@typescript-eslint', 'prettier'],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      extraFileExtensions: ['.svelte'],
      project: './tsconfig.json',
      tsconfigRootDir: __dirname,
      allowImportingTsExtensions: true,
    },
    settings: {
      'svelte/preprocess': sveltePreprocess(),
      'svelte/typescript': () => typescript,
    },
    rules: {
      'prettier/prettier': 'error',
      '@typescript-eslint/explicit-module-boundary-types': 'warn',
      // Add any other custom rules here
    },
    globals: {
      localStorage: 'readonly',
      document: 'readonly',
      JSZip: 'readonly',
    },
  }),
]
