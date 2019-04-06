import itertools
from cpt1public import download

# ID 遍历爬虫，1 次下载失败则终止

def iteration_crawler1():
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' % page
        html = download(url)
        if html is None:
            break
        else:
            # success - can scrape the result
            pass

if __name__ == '__main__':
    iteration_crawler1()
