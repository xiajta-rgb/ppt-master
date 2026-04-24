import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'

# PythonAnywhere reload API
url = 'https://www.pythonanywhere.com/api/v0/user/ppt/webapps/ppt.pythonanywhere.com/reload/'

headers = {'Authorization': f'Token {API_TOKEN}'}

print("尝试 API Reload...")
resp = requests.post(url, headers=headers, timeout=60)
print(f"状态码: {resp.status_code}")
print(f"响应: {resp.text}")
