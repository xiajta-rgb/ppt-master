import http.client
import ssl

context = ssl.create_default_context()
conn = http.client.HTTPSConnection('ppt.pythonanywhere.com', context=context)
conn.request('GET', '/', headers={'Accept-Encoding': 'identity'})

response = conn.getresponse()
body = response.read()

print(f"Content-Length: {response.getheader('Content-Length')}")
print(f"实际读取: {len(body)}")

# 检查是否有 \r\n\r\n 分隔符
parts = body.split(b'\r\n\r\n', 1)
if len(parts) > 1:
    print(f"找到 HTTP body 分隔符")
    header_part = parts[0].decode('latin-1')
    print(f"头部:\n{header_part[-500:]}")
    body_only = parts[1]
    print(f"body 长度: {len(body_only)}")
else:
    print("未找到分隔符")

# 尝试 latin-1 解码
text_latin = body.decode('latin-1')
print(f"\nlatin-1 解码长度: {len(text_latin)}")

# 对比
text_utf8 = body.decode('utf-8', errors='replace')
print(f"utf-8 replace 解码长度: {len(text_utf8)}")

# 找差异位置
for i in range(min(len(body), 25000)):
    try:
        body[:i].decode('utf-8')
    except UnicodeDecodeError as e:
        print(f"\n第一个解码错误在位置 {i}: {e}")
        print(f"附近字节: {body[max(0,i-10):i+20]}")
        break

conn.close()
