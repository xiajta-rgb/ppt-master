import http.client
import ssl

context = ssl.create_default_context()
conn = http.client.HTTPSConnection('ppt.pythonanywhere.com', context=context)
conn.request('GET', '/', headers={'Accept-Encoding': 'identity'})

response = conn.getresponse()
print(f"状态: {response.status}")
print(f"Content-Length: {response.getheader('Content-Length')}")
print(f"Content-Type: {response.getheader('Content-Type')}")

body = response.read()
print(f"实际读取长度: {len(body)}")

# 尝试解码
try:
    text = body.decode('utf-8')
    print(f"解码后长度: {len(text)}")
    if 'renderProjects()' in text:
        print("[OK] 包含 renderProjects()")
    else:
        print("[X] 不包含 renderProjects()")
except Exception as e:
    print(f"解码错误: {e}")

conn.close()
