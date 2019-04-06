import urllib.request
from bs4 import BeautifulSoup

def scrape(html):
    soup = BeautifulSoup(html, 'html5lib')
    # print(soup.body.tr)
    # print(soup)
    # print(soup.title)
    tr = soup.find(attrs={'id':'places_area__row'}) # locate the area row
    # 'class' is a special python attribute so instead 'class' is used
    td = tr.find(attrs = {'class':'w2p_fw'})  # locate the area tag
    # area = soup.find('tr')
    area = td.text  # locate the area tag

    # tbody = soup.find('tbody')  # locate the area tag
    # tr = tbody.find('tr')
    # area = tr.find(attrs = {'class':'w2p_fw'})

    # tr = soup.findAll('tr')[1] # locate the area tag
    # area = tr.find(attrs = {'class':'w2p_fw'})

    return area


if __name__ == '__main__':
    request = urllib.request.Request('http://example.webscraping.com/places/default/view/Brazil-32')
    response = urllib.request.urlopen(request, timeout = 5)
    html = response.read().decode('utf-8')
    # html = response.read().decode('utf-8')
    # print(html)
    print(scrape(html))

