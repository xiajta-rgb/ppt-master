---
name: "ppt-master-deploy"
description: "Deploy PPT Master to PythonAnywhere: upload WSGI file and provide manual reload instructions."
---

# PPT Master Deploy

## 配置信息

| 配置项 | 值 |
|--------|-----|
| 用户名 | `ppt` |
| Webapp | `ppt.pythonanywhere.com` |
| 项目路径 | `/home/ppt/ppt-master` |
| API Token | `c061620aaca584d026e45dc2baede02bd46ae0de` |
| WSGI文件 | `/var/www/ppt_pythonanywhere_com_wsgi.py` |

## 部署步骤

### Step 1: 执行部署脚本
```bash
python "voc-deploy/scripts/deploy.py"
```

### Step 2: 手动重载 Webapp
由于 PythonAnywhere Reload API 返回 405 错误，需要手动重载：

1. 访问 https://www.pythonanywhere.com/
2. 登录后进入 **Web** 选项卡
3. 点击 **Reload** 按钮刷新 `ppt.pythonanywhere.com`

### Step 3: 验证
访问 https://ppt.pythonanywhere.com/ 确认网站正常运行

## 项目状态

- ✅ 项目已克隆到 `/home/ppt/ppt-master`
- ✅ WSGI 已配置服务该目录
- ⚠️ 需要手动 Reload 使配置生效

## 验证网站

**URL**: https://ppt.pythonanywhere.com/

## 故障排除

如果网站仍返回 500 错误：
1. 确认已在 PythonAnywhere Web 界面点击 Reload
2. 检查 `/home/ppt/ppt-master/index.html` 是否存在
3. 查看 PythonAnywhere 错误日志
