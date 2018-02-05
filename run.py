from bs4 import BeautifulSoup
import requests
import collections


test_mode = 0


def agent():

    url = 'https://www.zoopla.co.uk/find-agents/london/?radius=40&page_size=100&pn=1'
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    data = collections.OrderedDict({'zoopla': []})

    def get_num(x):
        return int(''.join(ele for ele in x if ele.isdigit()))

    for div in soup.findAll('div', {'class': 'agents-results-item'}):
        title = div.find('a', itemprop='url')
        rent = div.find('strong', {'data-test': 'price-to-rent'})
        sale = div.find('strong', {'data-test': 'price-for-sale'})
        count = div.findAll('div', {'class': 'agents-stats-l'})

        if count:
            if test_mode:
                print(title.text)
            for can in count:

                x = can.text
                y = x.strip()
                if 'rent' in y:
                    if test_mode:
                        print('rent', get_num(y))
                    rent = get_num(y)
                else:
                    rent = None
                if 'sale' in y:
                    if test_mode:
                        print('sale', get_num(y))
                    sale = get_num(y)
                else:
                    sale = None

        data['zoopla'].append({'agent': title.text, 'sale': sale, 'rent': rent})

    if test_mode:
        print(data['zoopla'])

    print(len(data['zoopla']), 'agents processed')

agent()
