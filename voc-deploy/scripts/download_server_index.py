import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 下载服务器上的 index.html
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=headers)
if r.status_code == 200:
    content = r.text

    # 保存到文件
    with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\server_index_check.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"服务器 index.html 已保存，长度: {len(content)}")

    # 检查关键内容
    print("\n检查关键内容:")
    print(f"  renderProjects 函数: {'function renderProjects' in content}")
    print(f"  renderProjects() 调用: {'renderProjects()' in content}")
    print(f"  projects 数组: {'const projects = [' in content}")

    # 检查最后 200 个字符
    print(f"\n最后 200 字符:")
    print(content[-200:])
else:
    print(f"无法获取: {r.status_code}")
