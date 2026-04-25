---
name: "ppt-dev-workflow"
description: "PPT development workflow with Vite hot reload. Use when setting up dev environment for PPT development."
---

# PPT Development Workflow

## Quick Start

### 1. Start Backend Server (Port 5001)
```bash
python .trae/skills/start-server/start_server.py
```

### 2. Start Vite Dev Server (Port 5373)
```bash
npm run dev
```

### 3. Access Viewer
- Frontend: http://localhost:5373/viewer.html
- Backend: http://localhost:5001/viewer.html

## Vite Configuration

**File**: `vite.config.js`
```javascript
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
    port: 5373,
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      },
      '/examples': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})
```

## Hot Module Replacement (HMR)

Vite provides **instant HMR** - changes to SVG, CSS, JS files update immediately in browser without full reload.

### Files Created
| File | Purpose |
|------|---------|
| `package.json` | Node project config |
| `vite.config.js` | Vite bundler config |
| `index.html` | Entry point (serves public/viewer.html) |

## Stopping Servers

```bash
# Stop Vite
Ctrl+C in terminal running npm run dev

# Stop backend
python .trae/skills/start-server/start_server.py stop
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr ":5373"

# Kill process
taskkill /PID <PID> /F
```

### Proxy Errors (ECONNREFUSED)
- Ensure backend is running on port 5001
- Restart both servers if proxy fails
