import urllib.request
import urllib.error

# 增加捕获异常类型功能

def download2(url):
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
    return html

if __name__ == '__main__':
    html = download2('http://www.meetup.com/')
    if html:
        print(html)