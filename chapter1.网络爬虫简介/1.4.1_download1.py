import urllib.request

# python3.x merges urllib and urllib2 in python2.x
# urllib of python3.x contains:
#    urllib.request
#    urllib.error
#    urllib.parse
#    urllib.robotparser

# 直接获取页面内容

def download1(url):
    # return urllib.request.urlopen(url).read()
    print(type(urllib.request.urlopen(url).read()) )
    return 0
    # return urllib.request.urlopen(url).read().decode('utf-8')
        # python3.x need ".decode('utf-8')"


if __name__ == '__main__':
    print(download1('http://www.meetup.com/'))


