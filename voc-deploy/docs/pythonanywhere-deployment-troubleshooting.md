# PythonAnywhere WSGI 部署问题排查总结

## 问题描述

在 PythonAnywhere 上部署静态 HTML 网站时，首页返回的内容被截断（22960 字节截断为 21178 字节），导致 JavaScript 无法正常执行，项目列表无法显示。

## 排查过程

### 1. 确认问题现象
- API 返回的 index.html 内容完整（22960 字符）
- 网站直接访问返回的内容被截断（21178 字符）
- 截断位置恰好在中文 em dash（—）字符处

### 2. 初步分析
- 检查 WSGI 配置：正确
- 检查文件路径：正确
- 检查 Reload：生效
- Content-Length header 显示 22960，但实际接收 21178

### 3. 深入排查
```python
# 用 http.client 直接获取原始响应
body = response.read()  # 读取 22960 字节
text = body.decode('utf-8')  # 解码后只有 21178
```

发现问题：Content-Length 设置的是**字符数**（22960），而不是**字节数**（24742）。

### 4. 根本原因
UTF-8 编码中，中文字符占 3 字节。例如：
- "PPT Master — AI" 中 "—" 是 `\xe2\x80\x94`（3 字节）
- 当 WSGI 设置 `Content-Length: 22960`（字符数）时
- 服务器按字节数传输，但只传输了 22960 字节
- 由于中文字符占 3 字节，实际解码后的字符数只有 21178

### 5. 解决方案
**不要设置 Content-Length header**，让服务器自动计算正确的字节数：

```python
# 错误做法
response_headers = [
    ('Content-Type', 'text/html; charset=utf-8'),
    ('Content-Length', str(len(content)))  # 这是字符数，不是字节数！
]

# 正确做法
response_headers = [
    ('Content-Type', 'text/html; charset=utf-8')
    # 不设置 Content-Length
]
```

### 6. 最佳实践：使用 Base64 内嵌内容

如果必须确保内容完整传输，可以使用 Base64 编码：

```python
import base64

INDEX_B64 = base64.b64encode(index_html.encode('utf-8')).decode('ascii')

def application(environ, start_response):
    content = base64.b64decode(INDEX_B64).decode('utf-8')
    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8')
    ]
    start_response(status, response_headers)
    return [content.encode('utf-8')]
```

## 关键教训

1. **WSGI 中 `len(content)` 是字符数，不是字节数**
2. **UTF-8 中文字符占 3 字节，字符数 ≠ 字节数**
3. **不确定时，不要手动设置 Content-Length**
4. **PythonAnywhere 的 Reload API：`POST /api/v0/user/{user}/webapps/{domain}/reload/`**

## 验证方法

```python
import http.client

conn = http.client.HTTPSConnection('your-domain.pythonanywhere.com')
conn.request('GET', '/', headers={'Accept-Encoding': 'identity'})
response = conn.getresponse()
body = response.read()
print(f"Content-Length: {response.getheader('Content-Length')}")
print(f"实际读取: {len(body)}")  # 如果不等，说明有问题
```

## 完整 WSGI 模板

```python
import os
import base64

PROJECT_DIR = '/home/user/project'
INDEX_B64 = """你的base64编码内容"""

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    # 处理 URL 编码路径
    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

    if path == '/' or path == '':
        content = base64.b64decode(INDEX_B64).decode('utf-8')
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
    else:
        static_file = os.path.join(PROJECT_DIR, path.lstrip('/'))
        if os.path.exists(static_file) and os.path.isfile(static_file):
            with open(static_file, 'r', encoding='utf-8') as f:
                content = f.read()
            status = '200 OK'
            if static_file.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif static_file.endswith('.css'):
                content_type = 'text/css; charset=utf-8'
            elif static_file.endswith('.js'):
                content_type = 'application/javascript; charset=utf-8'
            elif static_file.endswith('.svg'):
                content_type = 'image/svg+xml; charset=utf-8'
            else:
                content_type = 'text/plain; charset=utf-8'
        else:
            content = '<html><body><h1>404</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [('Content-Type', content_type)]
    start_response(status, response_headers)
    return [content.encode('utf-8')]
```
