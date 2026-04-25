---
name: "ppt-debug-lessons"
description: "Debugs PPT page splitting issues. Invoke when PPT shows wrong page count or pages not loading."
---

# PPT Page Splitting Debug Lessons

## Common Issues and Solutions

### 1. API Returns Stale Data (Wrong Page Count)

**Symptom**: API `/api/scan-projects` returns fewer pages than actual SVG files in folder.

**Root Cause**: Server process cached old file scan results. New SVG files were created but server didn't rescan.

**Solution**:
```bash
# Restart the server to force file system rescan
python .trae/skills/start-server/start_server.py stop
python .trae/skills/start-server/start_server.py
```

**Prevention**: After adding new SVG files, always restart the server.

### 2. Static File 404 Due to URL Query String

**Symptom**: `net::ERR_ABORTED http://localhost:5001/js/collections.js?v=20250425`

**Root Cause**: `handle_static_file()` in WSGI_local.py didn't strip query string from path, so `js/collections.js?v=20250425` was treated as a literal path that doesn't exist.

**Solution**: Add query string stripping in WSGI_local.py:
```python
path_clean = path.lstrip('/').split('?')[0]
```

**Prevention**: Always strip query parameters when handling static file paths.

### 3. Static vs Dynamic Data Conflict

**Symptom**: PPT viewer ignores static `collections.js` and uses API data, showing wrong slides.

**Root Cause**: `loadDynamicCollections()` in viewer.html maps staticData but then overwrites `slides` with API's `p.slides`, losing proper titles and ordering.

**Solution**: Prioritize static slides configuration:
```javascript
slides: staticData?.slides?.length
    ? staticData.slides.filter(s => apiSlideFiles.has(s.file))
    : p.slides.map(s => ({...}))
```

**Prevention**: When both static config and API exist, prefer static config for content structure.

### 4. Browser Caching Issues

**Symptom**: Changes to files don't appear despite server restart.

**Solution**:
- Use Ctrl+Shift+R (hard refresh)
- Add version query strings: `?v=YYYYMMDD`
- Clear browser cache

### 5. Vite Dev Server Proxy Issues

**Symptom**: `net::ERR_ABORTED http://localhost:5373/api/scan-projects`

**Root Cause**: Backend server (port 5001) was stopped, or Vite proxy not configured correctly.

**Solution**:
```bash
# 1. Ensure backend is running
python .trae/skills/start-server/start_server.py

# 2. Ensure Vite proxy is configured in vite.config.js:
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
```

**Prevention**: Always start backend before frontend when doing development.

## Debug Checklist

1. **Verify SVG files exist**: Check file count in `svg_final/` folder
2. **Test API response**: `curl http://localhost:5001/api/scan-projects`
3. **Check static file serving**: `curl http://localhost:5001/js/collections.js`
4. **Restart server**: After any file system changes
5. **Hard refresh browser**: Ctrl+Shift+R

## Key Files Involved

| File | Purpose |
|------|---------|
| `WSGI_local.py` | Server routing and static file handling |
| `viewer.html` | PPT viewer, loads collections |
| `public/js/collections.js` | Static slide configuration |
| `config.py` | Project paths configuration |
