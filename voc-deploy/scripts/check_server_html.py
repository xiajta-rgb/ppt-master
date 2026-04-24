import requests
import json

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

print("检查服务器上的 index.html...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=headers)

if r.status_code == 200:
    content = r.text
    print(f"长度: {len(content)}")
    
    # 检查 projects 数组
    import re
    projects_match = re.search(r'const projects = \[([\s\S]*?)\];', content)
    if projects_match:
        print("\n[OK] 找到 projects 数组!")
        projects_str = projects_match.group(1)
        # 统计项目数量
        project_count = projects_str.count('{')
        print(f"项目数量: {project_count}")
        # 提取前几个标题
        titles = re.findall(r"title: '([^']+)'", projects_str)
        print(f"前5个项目: {titles[:5]}")
    else:
        print("\n[问题] 未找到 projects 数组!")
    
    # 检查 renderProjects 函数
    if 'function renderProjects' in content:
        print("\n[OK] 找到 renderProjects 函数!")
    else:
        print("\n[问题] 未找到 renderProjects 函数!")
    
    # 保存完整内容到本地文件对比
    with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\server_index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n已保存 server_index.html 到本地，请对比本地 index.html")
