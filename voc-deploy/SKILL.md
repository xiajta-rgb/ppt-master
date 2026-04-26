---
name: "voc-deploy"
description: "Executes 4-step deployment pipeline: (1) build frontend with vite, (2) commit and push to git with timestamp, (3) deploy to PythonAnywhere cloud, (4) reload webapp. Invoke when user asks to deploy or run deployment pipeline."
---

# VOC Deploy Pipeline

**严格按以下步骤顺序执行**，除非该步骤已执行（构建和提交推送可根据 git status 判断是否需要跳过）。

## Pipeline Steps（严格顺序）

### Step 1/4: Build Frontend（构建前端）
```bash
cd frontend && npm run build
```
- 产物输出到 `frontend/dist`
- **判断是否需要执行**：检查 `frontend/dist` 是否存在且为最新（对比 `frontend/src` 修改时间）
- 如果 `frontend/dist` 已存在且比源码新，**可跳过**此步骤

### Step 2/4: Git Commit and Push（提交推送）
```bash
git add -A && git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')" && git push
```
- **判断是否需要执行**：检查 `git status` 是否有未提交更改
- 如果没有未提交更改，**可跳过**此步骤

### Step 3/4: Deploy to Cloud（云端部署）
执行 `.trae/skills/voc-deploy/scripts/deploy.py`（云端部署逻辑）

### Step 4/4: Reload Webapp（重载网站）
deploy.py 会自动触发重载

### Step 5: Verify（验证）
验证 `https://voc.pythonanywhere.com/` 返回 `text/html` 且包含 `<html>` 标签

## Quick Start

```bash
# 完整部署（构建 + 提交 + 云端部署）
cd .trae/skills/voc-deploy/scripts && python deploy.py

# 快速部署（仅云端部署，跳过构建和提交）
cd .trae/skills/voc-deploy/scripts && python deploy.py --quick
```

## Scripts Location

- `deploy.py` - **统一部署脚本**，支持 `--quick` 参数切换模式

## Usage

Invoke this skill when user asks to deploy the application.

**重要**：用户说"开始部署"时，必须严格按 Step 1 → 2 → 3 → 4 → 5 顺序执行，**不要跳过步骤**。只有当该步骤已经执行过时才能跳过（通过检查文件时间戳或 git status 判断）。

## 常见问题 / 踩坑记录

### 坑1：FRONTEND_DIST 路径错误

**现象**：部署后网站返回 404 或空白页

**原因**：后端 `main.py` 中 `FRONTEND_DIST` 指向了错误路径

```
# 错误写法 ❌ — backend/frontend/dist 不存在
BACKEND_DIR = Path(__file__).parent.parent          # backend/app/
FRONTEND_DIST = BACKEND_DIR / "frontend" / "dist"    # → backend/frontend/dist

# 正确写法 ✅ — vite 构建产物在项目根目录的 frontend/dist
PROJECT_ROOT = Path(__file__).parent.parent.parent    # 项目根目录/
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"    # → frontend/dist
```

**排查方法**：检查 `backend/app/main.py` 中 `FRONTEND_DIST` 变量的路径是否指向实际存在的 `dist` 目录。

### 坑2：根路由冲突导致返回 JSON 而非 HTML

**现象**：访问 `https://voc.pythonanywhere.com/` 返回 `{"message":"VOC API"}` 而非前端页面

**原因**：FastAPI 中 `@app.get("/")` 路由的优先级高于 `app.mount("/", StaticFiles...)`

```python
# 错误写法 ❌ — 这个路由会拦截所有 / 请求，StaticFiles 永远不会被命中
@app.get("/")
async def root():
    return {"message": "VOC API", "version": "1.0.0"}

app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")

# 正确做法 ✅ — 删除或移走 @app.get("/")，让 StaticFiles 处理 /
# API 根信息可以放到其他路径如 /api 或 /health
@app.get("/api")
async def api_root():
    return {"version": "1.0.0", "status": "running"}
```

**排查方法**：用 curl 或脚本请求 `/`，检查 Content-Type 是 `text/html` 还是 `application/json`。

## Important Notes

- All steps execute sequentially - each must complete before the next begins
- Step 1 generates production build in `frontend/dist`
- Step 2 commits with timestamp for clear deployment history
- Step 3 triggers PythonAnywhere deployment
- Step 4 reloads the webapp
- 如需跳过构建和提交快速部署，使用 `--quick` 参数
