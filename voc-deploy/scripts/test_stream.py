import requests

# 使用 stream 模式获取完整响应
print("测试 stream 模式...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=60, stream=True)

print(f"状态: {r.status_code}")
print(f"headers: {dict(r.headers)}")

# 逐块读取
content = b''
for chunk in r.iter_content(chunk_size=4096):
    content += chunk
    print(f"已读取 {len(content)} 字节...")

text = content.decode('utf-8')
print(f"\n总长度: {len(text)}")
print(f"最后 200 字符:\n{text[-200:]}")

if 'renderProjects()' in text:
    print("\n[OK] 包含 renderProjects()")
else:
    print("\n[X] 不包含 renderProjects()")
