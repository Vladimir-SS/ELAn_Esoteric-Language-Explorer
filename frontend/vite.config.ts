import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  build: {
    assetsDir: 'static',
  },

  server: {
    proxy: {
      '/api': 'http://backend-fastapi:5000',
      '/static': 'http://backend-fastapi:5000',
    },
  },
})
