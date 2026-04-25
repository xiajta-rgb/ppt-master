---
name: "start-server"
description: "Starts both PPT Master backend (5001) and Vite frontend (5373). Invoke when user asks to start, restart, or refresh the server."
---

# Start PPT Master Server

启动 PPT Master 双服务器架构（后端 API + 前端开发服务器）。

## 启动命令

### 1. 后端服务器 (端口 5001)

```bash
python -c "from wsgiref.simple_server import make_server; from WSGI_local import application; srv = make_server('localhost', 5001, application); srv.serve_forever()"
```

或使用启动脚本：
```bash
python .trae/skills/start-server/start_server.py
```

### 2. 前端开发服务器 (端口 5373)

```bash
npx vite --port 5373
```

## 架构说明

| 服务 | 端口 | 用途 |
|------|------|------|
| 后端 WSGI | 5001 | API 请求、SVG 文件服务 |
| Vite 前端 | 5373 | 热重载开发服务器、代理 |

## 访问地址

- 前端：http://localhost:5373/viewer.html
- 后端 API：http://localhost:5001/api/scan-projects

## 重启步骤

如果服务器无响应，按顺序执行：

1. **停止所有相关进程**
```bash
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*5001*" -or $_.CommandLine -like "*WSGI*" } | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
```

2. **重启后端**
```bash
python -c "from wsgiref.simple_server import make_server; from WSGI_local import application; srv = make_server('localhost', 5001, application); srv.serve_forever()"
```

3. **重启前端**
```bash
npx vite --port 5373
```

## 常见问题

### ERR_ABORTED 错误
- 通常是浏览器快速切换导致请求取消
- 尝试刷新页面
- 如果持续出现，重启服务器

### API 超时
- 后端服务器可能卡住
- 执行重启步骤

### 端口占用
```bash
# Windows 查找占用端口的进程
netstat -ano | findstr :5001
netstat -ano | findstr :5373
```

## 注意事项

- 项目根目录：`c:\Users\xiajt\Documents\trae_projects\ppt-master`
- Vite 代理配置：将 `/api` 和 `/examples` 请求转发到后端 5001
- 中文路径自动正确编解码
