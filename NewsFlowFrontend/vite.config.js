import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [
    svelte({
      preprocess: require('@sveltejs/vite-plugin-svelte').vitePreprocess(),
    }),
  ],
})
