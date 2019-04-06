import urllib.request
import urllib.error

# 增加重试下载功能

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

if __name__ == '__main__':
    html = download3('http://httpstat.us/500/')
    if html:
        print(html)
    # print(download3('http://httpstat.us/500').decode('utf-8'))
