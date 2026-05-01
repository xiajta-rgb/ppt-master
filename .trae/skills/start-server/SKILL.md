---
name: "start-server"
description: "Starts both PPT Master backend (Flask on 5001) and Vite frontend (5373). Invoke when user asks to start, restart, or refresh the server."
---

# Start PPT Master Server

启动 PPT Master 双服务器架构（Flask 后端 + Vite 前端）。

## 启动命令

### 1. 后端服务器 (端口 5001)

使用 Flask 应用：
```bash
python app.py
```

或使用启动脚本：
```bash
python .trae/skills/start-server/start_server.py
```

### 2. 前端开发服务器 (端口 5373)

```bash
npm run dev
```

## 架构说明

| 服务 | 端口 | 用途 |
|------|------|------|
| Flask | 5001 | API 请求、SVG 文件服务 |
| Vite 前端 | 5373 | 热重载开发服务器、代理 |

## 新特性

- **Flask 框架**: 替换 wsgiref.simple_server，支持多线程
- **logging 模块**: 统一的日志输出到终端
- **Gunicorn 支持**: 可用于生产环境部署 (`gunicorn -w 4 -b localhost:5001 app:app`)

## 访问地址

- **前端主页：** http://localhost:5373/ （即 index.html，用于项目浏览）
- **后端 API：** http://localhost:5001/api/scan-projects
- **预览页面：** viewer.html

## 重启步骤

如果服务器无响应，按顺序执行：

1. **停止所有相关进程**
```bash
python .trae/skills/start-server/start_server.py stop
taskkill /F /IM node.exe
```

2. **重启后端**
```bash
python app.py
```

3. **重启前端**
```bash
npm run dev
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
netstat -ano | findstr :5001
netstat -ano | findstr :5373
```

## 注意事项

- 项目根目录：`c:\Users\xmls\Documents\trae_projects\ppt-master`
- Vite 代理配置：将 `/api` 和 `/examples` 请求转发到后端 5001
- 中文路径自动正确编解码
- 需要安装依赖: `pip install -r requirements.txt`
- WebSocket 实时同步功能因 Python 3.14 兼容性问题暂未启用