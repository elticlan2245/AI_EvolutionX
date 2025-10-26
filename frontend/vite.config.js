import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Escuchar en todas las interfaces
    port: 3000,
    strictPort: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '192.168.50.123',
      'iaevolutionxm.asuscomm.com',
      '.asuscomm.com' // Permite todos los subdominios
    ],
    hmr: {
      host: 'localhost'
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 3000
  }
})
