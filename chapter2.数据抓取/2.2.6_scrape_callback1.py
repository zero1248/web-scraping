import re
import lxml.html
from cpt2public import link_crawler
import html5lib

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code',
          'currency_name', 'phone','postal_code_format', 'postal_code_regex', 'languages', 'neighbours')

def scrape_callback(url, html):
    row = []
    if re.search('/view/', url):
        if re.search('/user/', url):
            return
        tree = lxml.html.fromstring(html)
        row = [tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content() for field in FIELDS]
        print(url, row)
    # return row


if __name__ == '__main__':
    # link_crawler('http://example.webscraping.com/', '/(index|view)', scrape_callback = scrape_callback)
    link_crawler('http://example.webscraping.com/places/default/view/Brazil-32', '/(index|view)',
                 scrape_callback = scrape_callback)












