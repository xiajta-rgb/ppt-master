import http.client
import ssl

context = ssl.create_default_context()
conn = http.client.HTTPSConnection('ppt.pythonanywhere.com', context=context)
conn.request('GET', '/', headers={'Accept-Encoding': 'identity'})

response = conn.getresponse()
body = response.read()

# 检查字节 20000-21000
print(f"总长度: {len(body)}")
print(f"字节 20000-20200 hex:")
print(body[20000:20200].hex())

# 检查是否看起来像 base64
print(f"\n字节 20000-20050: {body[20000:20050]}")

# 检查结尾
print(f"\n最后 50 字节 hex: {body[-50:].hex()}")

conn.close()
