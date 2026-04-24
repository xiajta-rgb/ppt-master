import requests

r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"Content-Length header: {r.headers.get('Content-Length')}")
print(f"实际内容长度: {len(r.text)}")

# 检查是否截断
if r.text.endswith('img.alt = project.title'):
    print("\n[确认] 内容被截断在 img.alt = project.title")
