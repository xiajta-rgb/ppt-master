import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
INDEX_PATH = '/home/ppt/ppt-master/index.html'

# 读取本地最新的 index.html
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"准备上传 index.html，长度: {len(content)}")

# 上传
boundary = uuid.uuid4().hex
headers = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': f'multipart/form-data; boundary={boundary}'
}

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="content"; filename="index.html"\r\n'
    f'Content-Type: text/html\r\n\r\n'
    f'{content}\r\n'
    f'--{boundary}--\r\n'
)

url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{INDEX_PATH}'
print(f"上传到 {url}...")
resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=60)
print(f"上传状态: {resp.status_code}")
print(f"响应: {resp.text[:200] if resp.text else 'empty'}")

# 验证
print("\n验证上传...")
r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{INDEX_PATH}',
                 headers={'Authorization': f'Token {API_TOKEN}'})
if r.status_code == 200:
    print(f"API 返回长度: {len(r.text)}")
    if 'renderProjects()' in r.text:
        print("[OK] 上传成功，包含 renderProjects()")
    else:
        print("[X] 上传的文件缺少 renderProjects()")

# 测试网站
print("\n测试网站返回...")
r2 = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"网站返回长度: {len(r2.text)}")
if 'renderProjects()' in r2.text:
    print("[OK] 网站返回正确!")
else:
    print("[X] 网站仍然返回旧版本!")
