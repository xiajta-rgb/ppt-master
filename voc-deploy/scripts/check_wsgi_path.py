import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 检查 /var/www/ 目录
print("检查 /var/www/ 目录...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/', headers=headers)
if r.status_code == 200:
    data = r.json()
    for name, info in data.items():
        print(f"  {name} ({info.get('type')})")
else:
    print(f"  状态: {r.status_code}")

# 检查工作目录配置
print("\n检查 Web 应用配置...")
r2 = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/webapps/', headers=headers)
print(f"Web 应用状态: {r2.status_code}")
if r2.status_code == 200:
    print(f"内容: {r2.json()}")
