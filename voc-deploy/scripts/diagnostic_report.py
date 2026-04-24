"""
PPT Master 部署问题诊断报告
============================

问题 1: WSGI 读取的 index.html 版本与 API 返回的不一致
- 网站返回: 21178 字节 (缺少 renderProjects())
- API 返回: 22960 字节 (正确的完整版本)
- 原因: PythonAnywhere 有静态文件配置，WSGI 未生效

问题 2: SVG 中文路径无法访问
- ASCII 路径: TacticalClothingReport/svg_final/slide_01_cover.svg → 404
- 中文路径: ppt169_战术服装_市场分析/svg_final/P01_封面.svg → 404
- 原因: WSGI 需要 URL 解码 (unquote)

问题 3: PythonAnywhere 静态文件配置拦截
- API 能正确读写文件
- WSGI 返回的文件与 API 不一致
- 说明 PythonAnywhere 的 Static files 配置优先于 WSGI

问题 4: WSGI 多次上传但未生效
- 多次 Reload 后问题依旧
- 可能需要清除 PythonAnywhere 的缓存

问题 5: SVG 文件路径编码问题
- 浏览器发送 URL 编码的中文
- WSGI 需要 decode URL 后再查找文件

问题 6: WSGI 未处理 SVG 的 Content-Type
- 旧版 WSGI 没有 SVG 的 MIME type

问题 7: 调试信息分散在多个临时文件
- 没有集中的问题追踪

问题 8: 服务器目录结构与预期不符
- API 显示 TacticalClothingReport 没有 svg_final/ 目录
- 该项目是 React 组件，不是标准 PPT 项目

问题 9: viewer.html 文件不存在
- /home/ppt/ppt-master/viewer.html → 404
- 只有 index.html 被部署

问题 10: WSGI 文件路径可能不正确
- /var/www/ppt_pythonanywhere_com_wsgi.py vs /home/ppt/ppt-master/WSGI.py
- 需要确认 WSGI 是否被正确加载

解决方案建议:
================

方案 A: 在 PythonAnywhere Web 界面禁用静态文件配置
1. 进入 Web 选项卡
2. 删除所有静态文件映射
3. Reload

方案 B: 上传 viewer.html 到服务器
- viewer.html 目前缺失

方案 C: 使用 PythonAnywhere Console 直接操作
- 在 Bash console 中运行 git clone
- 不依赖 WSGI 的文件服务

方案 D: 创建完整的测试 HTML 验证 WSGI 是否生效
"""

print(__doc__)
