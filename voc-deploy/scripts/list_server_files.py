import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 列出 examples 目录
print("列出 /home/ppt/ppt-master/examples/ ...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/', headers=h)
if r.status_code == 200:
    data = r.json()
    for name, info in list(data.items())[:10]:
        print(f"  {name} ({info.get('type')})")
else:
    print(f"状态: {r.status_code}")

# 列出项目目录
print("\n列出 ppt169_战术服装_市场分析 目录...")
r2 = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/', headers=h)
if r2.status_code == 200:
    data = r2.json()
    for name, info in data.items():
        print(f"  {name} ({info.get('type')})")
else:
    print(f"状态: {r2.status_code}")
