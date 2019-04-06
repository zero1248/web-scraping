import re
import urllib.request
import urllib.error
from cpt1public import download


def scrape(html):
    # area = re.findall('<td class="w2p_fw">(.*?)</td>', html)[1]
    # print(html)
    area = re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html)[0]
    return area


if __name__ == '__main__':
    request = urllib.request.Request('http://example.webscraping.com/places/default/view/Brazil-32')
    response = urllib.request.urlopen(request, timeout = 5)
    html = response.read().decode('utf-8')
    # html = urllib.request.urlopen('http://example.webscraping.com/places/default/view/Brazil-32').read().decode('utf-8')
    print(scrape(html))

