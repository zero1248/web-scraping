import re
from cpt1public import download

# 通过正则表达式从网站地图中的 <loc> 标签中提取出 URL

def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)


if __name__ == '__main__':
    crawl_sitemap('http://example.webscraping.com/sitemap.xml')