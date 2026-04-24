import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# Check viewer.html exists
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/viewer.html', headers=headers)
print('viewer.html Status:', r.status_code)

# Check index.html exists
r2 = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=headers)
print('index.html Status:', r2.status_code)
