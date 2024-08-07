module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:svelte/recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    extraFileExtensions: ['.svelte'],
    project: './tsconfig.json',
    allowImportingTsExtensions: true,
  },
  plugins: ['svelte', '@typescript-eslint', 'prettier'],
  overrides: [
    {
      files: ['*.svelte'],
      parser: 'svelte-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser',
      },
    },
  ],
  rules: {
    'prettier/prettier': 'error',
  },

  globals: {
    localStorage: 'readonly',
    document: 'readonly',
    JSZip: 'readonly',
  },
  settings: {
    'svelte3/typescript': () => require('typescript'),
  },
}
