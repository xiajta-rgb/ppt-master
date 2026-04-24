import requests

# 通过 API 获取
api_h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}
api_r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=api_h)
api_content = api_r.text

# 通过网站获取
site_r = requests.get('https://ppt.pythonanywhere.com/')
site_content = site_r.text

print(f"API 返回长度: {len(api_content)}")
print(f"网站返回长度: {len(site_content)}")

# 逐字节对比
diffs = 0
for i in range(min(len(api_content), len(site_content))):
    if api_content[i] != site_content[i]:
        diffs += 1
        if diffs <= 5:
            print(f"差异 {diffs} at pos {i}: API '{repr(api_content[i])}' vs Site '{repr(site_content[i])}'")

print(f"\n总差异数: {diffs}")
