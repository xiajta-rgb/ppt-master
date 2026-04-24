import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 列出 svg_final 目录
print("列出 svg_final 目录...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/', headers=h)
if r.status_code == 200:
    data = r.json()
    for name, info in data.items():
        print(f"  {name}")
else:
    print(f"状态: {r.status_code}")
    print(r.text)
