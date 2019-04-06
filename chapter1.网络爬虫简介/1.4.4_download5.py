import urllib.request
import urllib.error
import socket

# 支持代理、超时重试

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
            return download5(url, num_retries-1)
    return html

if __name__ == '__main__':
    # html = download5('http://example.webscraping.com/view')
    html = download5('http://example.webscraping.com/view/Brazil-3')
    if html:
        print(html)