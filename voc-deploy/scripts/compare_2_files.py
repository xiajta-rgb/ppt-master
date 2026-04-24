print("对比两个文件...")

with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\server_index.html', 'r', encoding='utf-8') as f1, \
     open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\website_returned.html', 'r', encoding='utf-8') as f2:
    c1 = f1.read()
    c2 = f2.read()
    
print(f"服务器文件长度: {len(c1)}")
print(f"网站返回长度: {len(c2)}")

import re
# 对比 projects 数组部分
p1 = re.search(r'const projects = \[([\s\S]*?)\];', c1).group(1)
p2 = re.search(r'const projects = \[([\s\S]*?)\];', c2).group(1)

print(f"\nprojects 数组是否相同: {p1.strip() == p2.strip()}")

# 检查 renderProjects 函数
r1 = 'renderProjects' in c1
r2 = 'renderProjects' in c2
print(f"都有 renderProjects 函数: {r1 and r2}")

# 检查项目标题
import json
print("\n--- 请按以下步骤排查问题 ---")
print("1. 强制刷新浏览器 (Ctrl + Shift + R / Cmd + Shift + R)")
print("2. 或者打开浏览器 DevTools (F12) -> Application -> Clear storage -> Clear site data")
print("3. 或者用无痕/隐私模式访问 https://ppt.pythonanywhere.com/")
print("\n如果还是看不到项目，请按 F12 打开浏览器控制台，看看有没有 JavaScript 错误，然后把错误信息发给我")
