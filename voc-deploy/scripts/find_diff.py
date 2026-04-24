import requests

# 读取两个文件
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\api_index.html', 'r', encoding='utf-8') as f:
    api_content = f.read()

with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\website_index.html', 'r', encoding='utf-8') as f:
    website_content = f.read()

print(f"API 版本长度: {len(api_content)}")
print(f"网站版本长度: {len(website_content)}")

# 找到差异位置
min_len = min(len(api_content), len(website_content))
diff_pos = -1
for i in range(min_len):
    if api_content[i] != website_content[i]:
        diff_pos = i
        break

if diff_pos == -1 and len(api_content) != len(website_content):
    diff_pos = min_len
    print(f"\n长度不同但前 {min_len} 字符相同")
else:
    print(f"\n第一个差异位置: {diff_pos}")

if diff_pos > 0:
    print(f"\n--- 差异位置附近 (API 版本) ---")
    start = max(0, diff_pos - 50)
    end = min(len(api_content), diff_pos + 100)
    print(api_content[start:end])

    print(f"\n--- 差异位置附近 (网站版本) ---")
    start = max(0, diff_pos - 50)
    end = min(len(website_content), diff_pos + 100)
    print(website_content[start:end])

# 搜索关键字符串
print("\n--- 检查 projects 数组 ---")
import re
api_match = re.search(r'const projects = \[', api_content)
web_match = re.search(r'const projects = \[', website_content)
print(f"API 中 projects 位置: {api_match.start() if api_match else 'NOT FOUND'}")
print(f"网站中 projects 位置: {web_match.start() if web_match else 'NOT FOUND'}")

# 检查 renderProjects
print(f"\nAPI 包含 'renderProjects()': {'renderProjects()' in api_content}")
print(f"网站包含 'renderProjects()': {'renderProjects()' in website_content}")

# 保存差异文件
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\diff_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"API 长度: {len(api_content)}\n")
    f.write(f"网站长度: {len(website_content)}\n")
    f.write(f"差异位置: {diff_pos}\n")
    if diff_pos > 0:
        start = max(0, diff_pos - 100)
        end = min(len(api_content), diff_pos + 100)
        f.write(f"\n--- API @ {diff_pos} ---\n")
        f.write(api_content[start:end])
        f.write(f"\n--- 网站 @ {diff_pos} ---\n")
        f.write(website_content[start:end])
print("\n差异已保存到 diff_output.txt")
