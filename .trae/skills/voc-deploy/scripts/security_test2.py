#!/usr/bin/env python3
"""
测试 WSGI 安全漏洞（带错误处理）
"""

import requests

BASE = "https://ppt.pythonanywhere.com"

def safe_get(url, **kwargs):
    try:
        return requests.get(url, timeout=10, **kwargs)
    except Exception as e:
        return None

def safe_post(url, **kwargs):
    try:
        return requests.post(url, timeout=10, **kwargs)
    except Exception as e:
        return None

print("=" * 60)
print("WSGI 安全漏洞测试")
print("=" * 60)

# 1. 路径遍历攻击
print("\n[1] 路径遍历攻击:")
traversal_paths = [
    '/../../../etc/passwd',
    '/public/../../../etc/passwd',
    '/examples/../../etc/passwd',
]
for p in traversal_paths:
    r = safe_get(f"{BASE}{p}")
    if r is None:
        print(f"    [WARN] {p}: 请求异常（可能WSGI崩溃）")
    else:
        safe = r.status_code == 404 or 'passwd' not in r.text.lower()
        print(f"    [{'SAFE' if safe else 'VULN'}] {p}: {r.status_code}")

# 2. 敏感文件访问
print("\n[2] 敏感文件访问:")
sensitive_paths = [
    '/.env',
    '/.git/config',
    '/app.py',
    '/wsgi.py',
]
for p in sensitive_paths:
    r = safe_get(f"{BASE}{p}")
    if r is None:
        print(f"    [VULN/CRASH] {p}: WSGI 崩溃！路径未做安全检查")
    else:
        safe = r.status_code == 404
        print(f"    [{'SAFE' if safe else 'VULN'}] {p}: {r.status_code}")

# 3. check-changes 首次调用
print("\n[3] check-changes 首次调用:")
r = safe_get(f"{BASE}/api/check-changes")
if r and r.status_code == 200:
    data = r.json()
    print(f"    changed={data.get('changed')}, files={len(data.get('files', []))}")
    if data.get('changed'):
        print("    [BUG] 首次调用返回 changed=True，会误触发热重载通知")
    else:
        print("    [OK] 首次调用返回 changed=False")
else:
    print(f"    [FAIL] status={r.status_code if r else 'error'}")

# 4. save-svg 端点
print("\n[4] /api/save-svg 端点:")
r = safe_post(f"{BASE}/api/save-svg", json={})
if r is None:
    print("    [BUG] WSGI 崩溃！")
elif r.status_code == 404:
    print("    [BUG] 端点不存在，编辑功能无法保存")
else:
    print(f"    [OK] 端点存在: {r.status_code}")

# 5. 缩略图路径测试
print("\n[5] 缩略图路径:")
r = safe_get(f"{BASE}/examples/ppt169_%E9%A1%B6%E7%BA%A7%E5%92%A8%E8%AF%A2%E9%A3%8E_%E9%87%8D%E5%BA%86%E5%B8%82%E5%8C%BA%E5%9F%9F%E6%8A%A5%E5%91%8A_ppt169_20251213/svg_final/P01_%E5%B0%81%E9%9D%A2.svg")
print(f"    绝对路径: {r.status_code if r else 'error'}")

# 6. viewer.html 中的 index.html 链接
print("\n[6] viewer.html -> index.html 链接:")
r = safe_get(f"{BASE}/index.html")
if r and r.status_code == 200:
    print(f"    [OK] /index.html 可访问 ({len(r.content)} bytes)")
else:
    print(f"    [BUG] /index.html 不可访问: {r.status_code if r else 'error'}")

# 7. WSGI 日志文件访问
print("\n[7] WSGI 日志文件:")
r = safe_get(f"{BASE}/wsgi_export.log")
if r and r.status_code == 200:
    print(f"    [VULN] 日志文件可访问！({len(r.content)} bytes)")
else:
    print(f"    [SAFE] 不可访问: {r.status_code if r else 'error'}")

# 8. Python 源文件访问
print("\n[8] Python 源文件:")
py_files = [
    '/app.py',
    '/public/app.py',
]
for p in py_files:
    r = safe_get(f"{BASE}{p}")
    if r and r.status_code == 200:
        print(f"    [VULN] {p}: 可访问")
    else:
        print(f"    [SAFE] {p}: 不可访问")
