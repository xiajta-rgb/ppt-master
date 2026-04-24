import requests

print("直接测试网站首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"长度: {len(r.text)}")

# 检查关键内容
content = r.text
if 'renderProjects()' in content:
    print("[OK] 包含 renderProjects() 调用")
else:
    print("[X] 不包含 renderProjects() 调用")

if 'Initial render' in content:
    print("[OK] 包含 Initial render")
else:
    print("[X] 不包含 Initial render")

# 打印最后 300 字符
print(f"\n最后 300 字符:\n{content[-300:]}")
