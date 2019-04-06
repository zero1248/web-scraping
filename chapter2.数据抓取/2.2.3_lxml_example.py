import urllib.request
import lxml.html

def scrape(html):
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    area = td.text_content()
    return area

if __name__ == '__main__':
    html = urllib.request.urlopen('http://example.webscraping.com/places/default/view/Brazil-32',
                                  timeout=5).read().decode('utf-8')
    # print(html)
    print(scrape(html))