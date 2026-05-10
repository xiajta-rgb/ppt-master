#!/usr/bin/env python3
"""
测试完整的访问流程
"""

import requests
from urllib.parse import urljoin

BASE_URL = "https://ppt.pythonanywhere.com"

print("=" * 60)
print("测试完整访问流程")
print("=" * 60)

# 1. 测试重定向
print("\n1. 测试 /viewer.html 重定向:")
try:
    r = requests.get(urljoin(BASE_URL, "/viewer.html"), allow_redirects=False, timeout=10)
    print(f"   Status: {r.status_code}")
    if r.status_code in [301, 302]:
        print(f"   Location: {r.headers.get('Location', 'N/A')}")
    else:
        # 检查内容是否有 JavaScript 重定向
        if "window.location.replace" in r.text:
            print(f"   JavaScript redirect to: public/viewer.html")
        else:
            print(f"   Content length: {len(r.text)}")
except Exception as e:
    print(f"   ERROR: {e}")

# 2. 测试 API
print("\n2. 测试 /api/scan-projects:")
try:
    r = requests.get(urljoin(BASE_URL, "/api/scan-projects"), timeout=10)
    if r.status_code == 200:
        data = r.json()
        projects = data.get('projects', [])
        print(f"   OK - {len(projects)} projects found")
        if projects:
            print(f"   First project: {projects[0]['id']}")
            print(f"   Slides: {len(projects[0]['slides'])}")
    else:
        print(f"   FAIL - Status: {r.status_code}")
except Exception as e:
    print(f"   ERROR: {e}")

# 3. 测试 SVG 文件访问
print("\n3. 测试 SVG 文件访问:")
try:
    svg_path = "/examples/ppt169_战术服装_市场分析/svg_final/P01_封面.svg"
    r = requests.get(urljoin(BASE_URL, svg_path), timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Content-Type: {r.headers.get('Content-Type', 'N/A')}")
    print(f"   Content-Length: {len(r.content)}")
    if r.status_code == 200:
        print(f"   OK - SVG file accessible")
    else:
        print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   ERROR: {e}")

# 4. 测试 projects-data
print("\n4. 测试 /api/projects-data:")
try:
    r = requests.get(urljoin(BASE_URL, "/api/projects-data"), timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"   OK - {len(data)} projects data")
    else:
        print(f"   FAIL - Status: {r.status_code}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 60)
