import { FlatCompat } from '@eslint/eslintrc'
import js from '@eslint/js'
import path from 'path'
import { fileURLToPath } from 'url'

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
  // Mimic ESLintRC-style extends
  ...compat.extends(
    'eslint:recommended',
    'plugin:svelte/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:prettier/recommended'
  ),

  // Mimic environments
  ...compat.env({
    es2020: true,
    browser: true,
    node: true,
  }),

  // Mimic plugins
  ...compat.plugins('svelte', '@typescript-eslint', 'prettier'),

  // Translate an entire config
  ...compat.config({
    plugins: ['svelte', '@typescript-eslint', 'prettier'],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      extraFileExtensions: ['.svelte'],
      project: './tsconfig.json',
      allowImportingTsExtensions: true,
    },
    rules: {
      'prettier/prettier': 'error',
      '@typescript-eslint/explicit-module-boundary-types': 'warn',
    },
    globals: {
      localStorage: 'readonly',
      document: 'readonly',
      JSZip: 'readonly',
    },
  }),
]
