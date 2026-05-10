#!/usr/bin/env python3
"""
测试 WSGI 安全漏洞
"""

import requests

BASE = "https://ppt.pythonanywhere.com"

print("=" * 60)
print("WSGI 安全漏洞测试")
print("=" * 60)

# 1. 路径遍历攻击
print("\n[1] 路径遍历攻击:")
traversal_paths = [
    '/../../../etc/passwd',
    '/..%2f..%2f..%2fetc/passwd',
    '/%2e%2e/%2e%2e/%2e%2e/etc/passwd',
    '/public/../../../etc/passwd',
    '/examples/../../etc/passwd',
]
for p in traversal_paths:
    r = requests.get(f"{BASE}{p}", timeout=10)
    safe = r.status_code == 404 or 'passwd' not in r.text.lower()
    print(f"    [{'SAFE' if safe else 'VULN'}] {p}: {r.status_code}")

# 2. 双重 URL 编码
print("\n[2] 双重 URL 编码:")
double_encode = [
    '/%252e%252e/%252e%252e/etc/passwd',
    '/examples/%252e%252e/%252e%252e/etc/passwd',
]
for p in double_encode:
    r = requests.get(f"{BASE}{p}", timeout=10)
    safe = r.status_code == 404 or 'passwd' not in r.text.lower()
    print(f"    [{'SAFE' if safe else 'VULN'}] {p}: {r.status_code}")

# 3. 敏感文件访问
print("\n[3] 敏感文件访问:")
sensitive_paths = [
    '/.env',
    '/.git/config',
    '/app.py',
    '/wsgi.py',
    '/requirements.txt',
]
for p in sensitive_paths:
    r = requests.get(f"{BASE}{p}", timeout=10)
    safe = r.status_code == 404
    print(f"    [{'SAFE' if safe else 'VULN'}] {p}: {r.status_code}")

# 4. 目录列表
print("\n[4] 目录列表:")
dir_paths = [
    '/examples/',
    '/public/',
    '/public/js/',
]
for p in dir_paths:
    r = requests.get(f"{BASE}{p}", timeout=10)
    safe = r.status_code == 404 or not ('<li>' in r.text or 'Index of' in r.text)
    print(f"    [{'SAFE' if safe else 'VULN'}] {p}: {r.status_code}")

# 5. check-changes 首次调用
print("\n[5] check-changes 首次调用:")
r = requests.get(f"{BASE}/api/check-changes", timeout=10)
data = r.json()
print(f"    changed={data.get('changed')}, files={len(data.get('files', []))}")
if data.get('changed'):
    print("    [BUG] 首次调用返回 changed=True，会误触发热重载通知")
else:
    print("    [OK] 首次调用返回 changed=False")

# 6. 缩略图路径测试
print("\n[6] 缩略图路径（相对 vs 绝对）:")
# 测试相对路径
r1 = requests.get(f"{BASE}/examples/ppt169_%E9%A1%B6%E7%BA%A7%E5%92%A8%E8%AF%A2%E9%A3%8E_%E9%87%8D%E5%BA%86%E5%B8%82%E5%8C%BA%E5%9F%9F%E6%8A%A5%E5%91%8A_ppt169_20251213/svg_final/P01_%E5%B0%81%E9%9D%A2.svg", timeout=10)
print(f"    绝对路径 /examples/...: {r1.status_code}")

# 测试不带前导 / 的路径（浏览器在 /viewer.html 时的解析）
# 当页面在 /viewer.html 时，相对路径 examples/... 会解析为 /examples/...
# 这是正确的，但如果页面在子目录下就会出错

# 7. save-svg 端点
print("\n[7] /api/save-svg 端点:")
r = requests.post(f"{BASE}/api/save-svg", json={}, timeout=10)
if r.status_code == 404:
    print("    [BUG] 端点不存在，编辑功能无法使用")
else:
    print(f"    [OK] 端点存在: {r.status_code}")
