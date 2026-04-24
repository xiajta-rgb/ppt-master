import subprocess
import requests

# 用 curl 测试
result = subprocess.run(
    ['curl', '-s', '-H', 'Accept-Encoding: identity', 'https://ppt.pythonanywhere.com/'],
    capture_output=True,
    text=True,
    timeout=30
)

text = result.stdout
print(f"curl 长度: {len(text)}")
print(f"最后 300 字符:\n{text[-300:]}")

if 'renderProjects()' in text:
    print("\n[OK] 包含 renderProjects()")
else:
    print("\n[X] 不包含 renderProjects()")

# 检查 Content-Length
result2 = subprocess.run(
    ['curl', '-sI', 'https://ppt.pythonanywhere.com/'],
    capture_output=True,
    text=True,
    timeout=30
)
print(f"\n响应头:\n{result2.stdout}")
