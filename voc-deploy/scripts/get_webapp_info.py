import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 获取完整 Web 应用信息
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/webapps/', headers=h)
if r.status_code == 200:
    for app in r.json():
        print("Web App 详情:")
        for key, value in app.items():
            print(f"  {key}: {value}")
