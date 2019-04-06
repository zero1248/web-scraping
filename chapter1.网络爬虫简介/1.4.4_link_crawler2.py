import re
from cpt1public import download
import urllib.parse

# 使用 urllib.parse 创建绝对路径

def link_crawler2(seed_url, link_regex):
    """Crawl from the given seed URL following links matched by link_regex
    """
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # filter for links matching our regular expression
        for link in get_links(html):
            if re.search(link_regex, link):
                """use search rather than match 
                """
                link = urllib.parse.urljoin(seed_url, link)
                crawl_queue.append(link)

def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

if __name__ == '__main__':
    link_crawler2('http://example.webscraping.com', '/(index|view)')