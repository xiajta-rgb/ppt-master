# Debug Session: viewer-route-not-found

Status: OPEN

## Symptom
访问 `http://localhost:5001/viewer.html` 返回 404 Not Found。

## Hypotheses
1. Flask 未注册 `/viewer.html` 路由。
2. 应用入口实际为根路径 `/`。
3. 启动脚本未启动 Vite 开发服务器。
4. 静态资源目录或前端入口路径配置不一致。

## Evidence
待收集。
