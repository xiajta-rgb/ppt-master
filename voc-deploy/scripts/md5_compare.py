import requests
import hashlib

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'

print("重新获取服务器 index.html 并对比...")

# 通过网站获取 (WSGI 服务的版本)
r1 = requests.get('https://ppt.pythonanywhere.com/index.html', timeout=30)
website_md5 = hashlib.md5(r1.content).hexdigest()
print(f"网站返回 index.html MD5: {website_md5}")

# 通过 API 获取 (文件系统版本)
r2 = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html',
                  headers={'Authorization': f'Token {API_TOKEN}'})
api_md5 = hashlib.md5(r2.content).hexdigest()
print(f"API 返回 index.html MD5: {api_md5}")

# 本地
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\index.html', 'rb') as f:
    local_md5 = hashlib.md5(f.read()).hexdigest()
print(f"本地 index.html MD5: {local_md5}")

print(f"\n网站 vs API: {website_md5 == api_md5}")
print(f"网站 vs 本地: {website_md5 == local_md5}")
print(f"API vs 本地: {api_md5 == local_md5}")

# 保存所有版本
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\website_index.html', 'wb') as f:
    f.write(r1.content)
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\api_index.html', 'wb') as f:
    f.write(r2.content)

print("\n已保存所有版本到本地")
