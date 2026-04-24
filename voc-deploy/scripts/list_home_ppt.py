import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 列出 /home/ppt/ 目录
print("列出 /home/ppt/ 目录...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/', headers=h)
if r.status_code == 200:
    data = r.json()
    for name, info in data.items():
        print(f"  {name} ({info.get('type')})")
else:
    print(f"状态: {r.status_code}")
