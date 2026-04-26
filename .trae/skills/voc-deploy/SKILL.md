---
name: "ppt-master-deploy"
description: "Deploy PPT Master to PythonAnywhere with export functionality."
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
python ".trae\skills\voc-deploy\scripts\deploy.py"
```

部署脚本会自动完成：
1. Git Commit - 自动提交所有更改
2. Git Push - 推送到远程仓库
3. 上传 WSGI - 更新 WSGI 配置
4. Reload Webapp - 重载 Web 应用
5. 验证网站 - 确认部署成功

### Step 2: 验证
访问 https://ppt.pythonanywhere.com/ 确认网站正常运行

## 导出功能

### 前端使用
在 viewer.html 页面中，点击右上角的 PowerPoint 图标按钮即可导出当前项目为 PPTX 文件。

### API 端点
```
GET /api/export?project=项目名称
```

返回 PPTX 文件流（Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation）

## 已知问题与解决方案

### UTF-8 乱码问题
- **现象**: 中文字符显示为乱码，如 `ppt169_é¡¶çº§å¨è¯¢é£_å¿çæ²»çä¸­çä¾æ`
- **原因**: WSGI 响应头缺少 `charset=utf-8`
- **解决**: WSGI 中所有 Content-Type 都添加 `; charset=utf-8`

### git clone 导致超时
- **现象**: Reload 后网站返回 500 错误
- **原因**: WSGI 启动时执行 git clone 超时
- **解决**: 先通过其他方式（如 PythonAnywhere Console）执行 git clone，WSGI 只负责服务文件

### python-pptx 未安装
- **现象**: 导出 API 返回 `Import failed: pip failed`
- **原因**: python-pptx 库未安装
- **解决**: 在 PythonAnywhere Console 中执行 `pip install python-pptx --user`

## 项目状态

- ✅ WSGI 已配置 (charset=utf-8)
- ✅ 项目目录 `/home/ppt/ppt-master` 已存在
- ✅ 网站 https://ppt.pythonanywhere.com/ 正常运行
- ✅ 导出 API 已部署 (/api/export)
- ⚠️ python-pptx 需手动安装
