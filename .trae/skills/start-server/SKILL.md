---
name: "start-server"
description: "Starts the PPT Master web server on port 5001. Invoke when user asks to start the frontend or server."
---

# Start PPT Master Server

启动 PPT Master 前端服务器（端口 5001）。

## 使用命令

```bash
python .trae/skills/start-server/start_server.py
```

## 启动步骤

1. 在项目根目录运行 `python .trae/skills/start-server/start_server.py`
2. 服务启动后访问：http://localhost:5001/viewer.html

## 功能特性

- 自动检测并终止占用端口 5001 的进程
- PID 文件管理（`.server_pid`）
- 服务器后台运行，启动脚本立即返回
- 启动成功/失败有明确提示

## 停止服务器

```bash
python .trae/skills/start-server/start_server.py stop
```

## 架构说明

- 使用 `WSGI_local.py` 处理跨目录路由（public/ 和 examples/）
- 中文路径自动正确编解码
- 使用 `subprocess.DEVNULL` 避免管道阻塞

## 注意事项

- 项目根目录：`c:\Users\xiajt\Documents\trae_projects\ppt-master`
- 端口 5001 用于避免与其他服务冲突
- 推荐直接用浏览器打开 http://localhost:5001/viewer.html
