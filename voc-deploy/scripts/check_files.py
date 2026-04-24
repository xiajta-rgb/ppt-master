import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
USERNAME = 'ppt'

# 检查文件是否存在
files_to_check = [
    '/home/ppt/ppt-master/skills/ppt-master/scripts/svg_to_pptx.py',
    '/home/ppt/ppt-master/skills/ppt-master/scripts/svg_to_pptx/__init__.py',
    '/home/ppt/ppt-master/skills/ppt-master/scripts/svg_to_pptx/pptx_cli.py',
]

for file_path in files_to_check:
    r = requests.get(
        f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{file_path}',
        headers={'Authorization': f'Token {API_TOKEN}'},
        timeout=30
    )
    print(f"{file_path}: {r.status_code}")
