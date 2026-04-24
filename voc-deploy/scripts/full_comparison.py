import requests
from requests.structures import CaseInsensitiveDict

# 完整的原始响应
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30, headers={'Accept-Encoding': 'identity'})

print(f"状态: {r.status_code}")
print(f"编码: {r.encoding}")
print(f"Content-Type: {r.headers.get('Content-Type')}")

# 保存完整内容
with open('site_homepage.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print(f"\n保存到 site_homepage.html，长度: {len(r.text)}")

# 对比 API
api_r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html',
                     headers={'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'})
with open('api_homepage.html', 'w', encoding='utf-8') as f:
    f.write(api_r.text)
print(f"API 保存到 api_homepage.html，长度: {len(api_r.text)}")
