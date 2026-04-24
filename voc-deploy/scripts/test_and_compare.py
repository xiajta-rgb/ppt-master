import requests

# 创建测试 HTML
test_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PPT Master Debug</title>
</head>
<body>
    <h1>PPT Master Debug Test</h1>
    <div id="projects"></div>
    <script>
        const projects = [
            {id: 'test1', title: '测试项目1'},
            {id: 'test2', title: '测试项目2'}
        ];
        document.getElementById('projects').innerHTML = '<p>Projects: ' + projects.length + '</p>';
        projects.forEach(function(p) {
            document.getElementById('projects').innerHTML += '<p>' + p.title + '</p>';
        });
    </script>
</body>
</html>
'''

# 上传到服务器
import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

# 上传到根目录作为测试
boundary = uuid.uuid4().hex
headers = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': f'multipart/form-data; boundary={boundary}'
}

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="content"; filename="test.html"\r\n'
    f'Content-Type: text/html\r\n\r\n'
    f'{test_html}\r\n'
    f'--{boundary}--\r\n'
)

url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path/home/ppt/ppt-master/test.html'
print(f"上传测试页面...")
resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=30)
print(f"上传状态: {resp.status_code}")

# 测试访问
print(f"\n测试访问 https://ppt.pythonanywhere.com/test.html")
r = requests.get('https://ppt.pythonanywhere.com/test.html', timeout=30)
print(f"状态: {r.status_code}")
print(f"内容: {r.text[:500]}")

# 检查本地和服务器 index.html 的 MD5
print("\n--- MD5 对比 ---")
import hashlib
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\index.html', 'rb') as f:
    local_md5 = hashlib.md5(f.read()).hexdigest()

with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\server_index_check.html', 'rb') as f:
    server_md5 = hashlib.md5(f.read()).hexdigest()

print(f"本地 index.html MD5: {local_md5}")
print(f"服务器 index.html MD5: {server_md5}")
print(f"是否相同: {local_md5 == server_md5}")
