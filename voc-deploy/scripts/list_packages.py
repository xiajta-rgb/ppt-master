import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

print("获取已安装的包...")
r = requests.get(
    f'https://{HOST}/api/v0/user/{USERNAME}/packages/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    timeout=30
)
print(f"状态: {r.status_code}")
if r.status_code == 200:
    packages = r.json()
    for pkg in packages:
        print(f"  {pkg.get('package_name')}: {pkg.get('version')}")
