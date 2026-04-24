import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

# 上传 viewer.html
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/viewer.html', 'r', encoding='utf-8') as f:
    viewer_content = f.read()

files = {'content': ('viewer.html', viewer_content, 'text/html')}

r = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/files/path/home/ppt/ppt-master/viewer.html',
    headers={'Authorization': f'Token {API_TOKEN}'},
    files=files,
    timeout=30
)
print(f"viewer.html 上传: {r.status_code}")
