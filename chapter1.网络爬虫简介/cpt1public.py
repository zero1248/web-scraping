import urllib.request
import urllib.error
import socket

def download1(url):
    return urllib.request.urlopen(url).read().decode('utf-8')

def download2(url):
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
    return html

def download3(url, num_retries = 5):
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download3(url, num_retries-1)
    return html

def download4(url, user_agent = 'wswp', num_retries = 5):
    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers = headers)
    try:
        html = urllib.request.urlopen(request, timeout = 5).read().decode('utf-8')
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download4(url, num_retries-1)
    except socket.timeout as e:
        print('Download error:', e)
        if num_retries > 0:
            return download4(url, num_retries-1)
    return html

def download5(url, user_agent = 'wswp', proxy = None, num_retries = 5, data = None):
    socket.setdefaulttimeout(5)
    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, data, headers=headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read().decode('utf-8')
        code = response.code
        # print(html.decode('utf-8'))  # print website content
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= e.code < 600:
                #recursively retry 5xx HTTP errors
                html = download5(url, user_agent, proxy, num_retries-1)
        else:
            code = None
    except socket.timeout as e:
        print('Download error:', e)
        if num_retries > 0:
            html = download5(url, user_agent, proxy, num_retries - 1)
    return html

# download4 加入了 请求超时处理，通过 urlopen(request, timeout = 5)，用 except 做故障处理。
# download5 加入了 请求超时处理，因为没有用到 URLopen(),而是用了 urllib.request.build_opener.open(request),
# 在 open 方法中使用了 timeout=socket._GLOBAL_DEFAULT_TIMEOUT 作为超时判断，
# 因此直接用 socket.setdefaulttimeout(5) 设置初值即可。

download = download5