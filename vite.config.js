import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: 'public',
  publicDir: resolve(__dirname, 'public'),
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true
  },
  server: {
    host: true,
    port: 5373,
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        timeout: 30000,
        configure: (proxy) => {
          proxy.on('error', (err, req, res) => {
            console.error('[Proxy Error]', err.message)
          })
        }
      },
      '/examples': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        timeout: 30000,
        configure: (proxy) => {
          proxy.on('error', (err, req, res) => {
            console.error('[Proxy Error]', err.message)
          })
        }
      }
    }
  }
})