import urllib.request
import urllib.error
import socket

# 增加设置用户代理功能

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

if __name__ == '__main__':
    html = download4('http://example.webscraping.com/view/Brazil-3')
    if html:
        print(html)
