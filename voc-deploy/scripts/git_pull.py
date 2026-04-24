import requests
import json
import time

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

def create_console(command):
    print(f"创建 Console: {command[:50]}...")
    r = requests.post(
        f'https://{HOST}/api/v0/user/{USERNAME}/consoles/',
        headers={'Authorization': f'Token {API_TOKEN}'},
        json={'executable': '/bin/bash', 'arguments': f'-lc "{command}"'},
        timeout=30
    )
    if r.status_code == 201:
        result = r.json()
        console_id = result.get('id')
        print(f"Console ID: {console_id}")
        return console_id
    else:
        print(f"创建失败: {r.status_code} - {r.text[:200]}")
        return None

def get_console_output(console_id):
    r = requests.get(
        f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/',
        headers={'Authorization': f'Token {API_TOKEN}'},
        timeout=30
    )
    if r.status_code == 200:
        return r.json()
    return None

def main():
    print("="*50)
    print("PythonAnywhere Git Pull & Deploy")
    print("="*50)

    print("\n[Step 1] Git Pull...")
    console_id = create_console('cd /home/ppt/ppt-master && git pull')
    if not console_id:
        print("[X] Git pull failed")
        return

    print("等待 10 秒让命令执行...")
    time.sleep(10)

    output = get_console_output(console_id)
    if output:
        print(f"输出: {json.dumps(output, indent=2)[:500]}")

    print("\n[Step 2] 验证文件...")
    console_id2 = create_console('ls -la /home/ppt/ppt-master/viewer.html')
    if console_id2:
        time.sleep(5)
        output2 = get_console_output(console_id2)
        if output2:
            print(f"viewer.html: {json.dumps(output2, indent=2)[:500]}")

    print("\n" + "="*50)
    print("完成!")
    print("="*50)

if __name__ == '__main__':
    main()
