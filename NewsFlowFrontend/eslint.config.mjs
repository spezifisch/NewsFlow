import eslintRecommended from '@eslint/js'
import tsParser from '@typescript-eslint/parser'
import tsPlugin from '@typescript-eslint/eslint-plugin'
import eslintPluginPrettier from 'eslint-plugin-prettier'
import eslintPluginSvelte from 'eslint-plugin-svelte'
import eslintPluginTypeScript from '@typescript-eslint/eslint-plugin'

const { configs: eslintRecommendedConfigs } = eslintRecommended

export default [
  eslintRecommendedConfigs.recommended,
  eslintPluginSvelte.configs.recommended,
  eslintPluginPrettier.configs.recommended,
  eslintPluginTypeScript.configs.recommended,
  {
    files: ['**/*.{js,ts,svelte}'],
    ignores: ['node_modules/**', 'public/**'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        extraFileExtensions: ['.svelte'],
        project: './tsconfig.json',
        allowImportingTsExtensions: true,
      },
      globals: {
        localStorage: 'readonly',
        document: 'readonly',
        JSZip: 'readonly',
      },
    },
    plugins: {
      svelte: eslintPluginSvelte,
      '@typescript-eslint': tsPlugin,
      prettier: eslintPluginPrettier,
    },
    rules: {
      'prettier/prettier': 'error',
      '@typescript-eslint/explicit-module-boundary-types': 'warn',
    },
  },
]
