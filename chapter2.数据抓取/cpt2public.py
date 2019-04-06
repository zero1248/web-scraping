import urllib.error
import urllib.request
import re
import urllib.parse
import urllib.robotparser
from datetime import datetime
import queue
import socket
import time


def link_crawler(seed_url, link_regex = None, delay = 1, max_depth = -1, max_urls = -1,
                 headers = None, user_agent = 'wswp', proxy = None, num_retries = 5, scrape_callback = None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = queue.deque([seed_url])
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop() # remove the last element of queue
        depth = seen[url]
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy = proxy, num_retries = num_retries)    # 根据 url 下载页面
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])

            if depth != max_depth:
                # can still crawl further
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(link for link in get_links(html) if re.search(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:', url)
        print()

class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        # print('domain:', domain)
        last_accessed = self.domains.get(domain)
        # print('dealy, last_accessed:', self.delay, last_accessed)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            # print('sleep_secs:', sleep_secs)
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
            # update the last accessed time
        self.domains[domain] = datetime.now()

# a little different from download5()
def download(url, headers, proxy = None, num_retries = 5, data = None):
    socket.setdefaulttimeout(5)
    print('Downloading:', url)
    request = urllib.request.Request(url, data, headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read().decode('utf-8')
        code = response.code
        # print(html)  # print website content
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            print("HTTP error", code)
            if num_retries > 0 and 500 <= code < 600:
                #recursively retry 5xx HTTP errors
                print('Re-downloading:')
                html = download(url, headers, proxy, num_retries-1, data)
                # return download(url, user_agent, proxy, num_retries-1)
            elif num_retries > 0 and code == 429:
                # print('except1')
                # print('Sleep start--------------')
                time.sleep(1)
                # print('Sleep end--------------')
                print('HTTP error 429 Re-downloading:')
                html = download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    except socket.timeout as e:
        print('Timeout error:', e)
        # print('Sleep start--------------')
        time.sleep(1)
        # print('Sleep end--------------')
        print('Timeout Re-downloading:')
        if num_retries > 0:
            html = download(url, headers, proxy, num_retries-1, data = None)
    return html

def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urllib.parse.urldefrag(link) # remove hash to avoid duplicates 把url #后的部分赋给变量 _
    return urllib.parse.urljoin(seed_url, link) # 连接 url 协议域名部分和虚拟目录部分

def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc

def get_links(html):
    """Return a list of links from html
    """
    if html:
        # a regular expression to extract all links from the webpage
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        # list of all links from the webpage
        return webpage_regex.findall(html)
    else:
        return ""

def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp



if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/index', '/(index|view)',
             delay=0, num_retries=1, max_depth=2, user_agent='GoodCrawler')
    # link_crawler('http://example.webscraping.com', '/(index|view)',
    #          delay=0, num_retries=1, max_depth=1, user_agent='BadCrawler')




