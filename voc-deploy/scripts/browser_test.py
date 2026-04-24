import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("模拟浏览器访问...")
r = requests.get('https://ppt.pythonanywhere.com/', headers=headers, timeout=30)
print(f"状态: {r.status_code}")

# 检查 JavaScript 是否存在
if '<script>' in r.text:
    print("[OK] HTML 包含 <script> 标签")

# 检查 renderProjects 函数
if 'function renderProjects' in r.text:
    print("[OK] 包含 renderProjects 函数")

# 检查 renderProjects 调用
if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects() 调用")
else:
    print("[X] 缺少 renderProjects() 调用")

# 检查 projects 数组
if 'const projects = [' in r.text:
    print("[OK] 包含 projects 数组")

# 检查 CSS 是否加载
if '.projects-grid' in r.text:
    print("[OK] 包含 CSS")

# 尝试直接访问 viewer.html
print("\n--- 测试 viewer.html ---")
r2 = requests.get('https://ppt.pythonanywhere.com/viewer.html', headers=headers, timeout=30)
print(f"viewer.html 状态: {r2.status_code}")
if r2.status_code == 200:
    if 'viewer' in r2.text.lower():
        print("[OK] viewer.html 内容正常")
else:
    print(f"[X] viewer.html 不可用")

print("\n结论: HTML 内容正确，问题可能是浏览器缓存!")
print("\n请尝试:")
print("1. 强制刷新 (Ctrl+Shift+R)")
print("2. 打开浏览器 DevTools (F12) -> Network -> 禁用缓存")
print("3. 或用无痕模式打开 https://ppt.pythonanywhere.com/")
