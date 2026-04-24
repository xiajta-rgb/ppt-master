---
name: "start-server"
description: "Starts the PPT Master web server on port 5001. Invoke when user asks to start the frontend or server."
---

# Start PPT Master Server

启动 PPT Master 前端服务器（端口 5001）。

## 使用命令

```bash
python -c "from wsgiref.simple_server import make_server; from WSGI_local import application; srv = make_server('localhost', 5001, application); srv.serve_forever()"
```

## 启动步骤

1. 在项目根目录运行上述命令
2. 服务启动后访问：http://localhost:5001

## 注意事项

- 项目根目录：`c:\Users\xiajt\Documents\trae_projects\ppt-master`
- 使用 `WSGI_local.py` 替代简单的 http.server，支持本地 PPT 导出功能
- 端口 5001 用于避免与其他服务冲突
