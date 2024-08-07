import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  publicDir: 'public', // This tells Vite where to find public files
  build: {
    outDir: 'dist', // Specify the output directory
    rollupOptions: {
      input: 'public/index.html', // This specifies the entry point
    },
  },
})
