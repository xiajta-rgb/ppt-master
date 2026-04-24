import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# Check current WSGI
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
print(f"WSGI status: {r.status_code}")
if r.status_code == 200:
    content = r.text
    print(f"Length: {len(content)}")
    print("\n--- First 300 chars ---")
    print(content[:300])
    print("\n--- Last 200 chars ---")
    print(content[-200:])

    if 'git pull' in content:
        print("\n[OK] WSGI has git pull")
    elif 'git clone' in content:
        print("\n[OK] WSGI has git clone")
    else:
        print("\n[X] WSGI does NOT have git commands - using OLD WSGI!")
