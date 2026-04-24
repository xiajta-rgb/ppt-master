import requests

r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"内容长度: {len(r.text)}")

# 查找 projects 相关内容
if 'projects' in r.text:
    print("\n[OK] 包含 'projects'")
else:
    print("\n[X] 不包含 'projects'")

# 查找 render 函数
if 'renderProjects' in r.text:
    print("[OK] 包含 renderProjects")
else:
    print("[X] 不包含 renderProjects")

# 查找 examples 目录引用
if 'examples' in r.text:
    print("[OK] 包含 'examples'")
else:
    print("[X] 不包含 'examples'")

# 打印 body 部分
import re
body_match = re.search(r'<body[^>]*>(.*?)</body>', r.text, re.DOTALL)
if body_match:
    body = body_match.group(1)[:2000]
    print(f"\nBody 前 2000 字符:\n{body}")
