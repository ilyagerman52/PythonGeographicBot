import requests
from bs4 import BeautifulSoup
import re


def get_cp():
    c = []
    cp = dict()
    for page in range(10):
        url = 'https://www.geonames.org/advanced-search.html?q=&featureClass=A&startRow=' + str(page * 50)
        r = requests.get(url)
        r = r.content.decode('utf-8')
        soup = BeautifulSoup(r, 'html.parser')
        for link in soup.find_all('tr'):
            blocks = link.find_all('td')
            try:
                if 'independent political entity' in blocks[3].text:  # here we could save dependent territories too,
                    # but some of them has no info about population
                    p_ = blocks[3].text.strip('independent political entitypopulation').replace(',', '').replace('\n',
                                                                                                                 '')
                    c_ = blocks[2].text.strip(', ')
                    if c_ != 'BL,FR' and c_ != 'MF,FR':
                        c.append(c_)
                        cp[c_] = p_
            except Exception:
                pass  # we are not in right place of table to parse

    return c, cp


def get_tpcC():
    t = []
    tp = dict()
    tc = dict()
    cC = dict()
    for page in range(30):
        url = 'https://www.geonames.org/advanced-search.html?q=&featureClass=P&startRow=' + str(page * 50)
        r = requests.get(url)
        r = r.content.decode('utf-8')
        soup = BeautifulSoup(r, 'html.parser')
        for link in soup.find_all('tr'):
            blocks = link.find_all('td')
            try:
                p_ = blocks[3].text.replace(',', '').replace('\n', '').split(' ')[-1]
                c_ = blocks[2].text.split(',')[0]
                t_ = blocks[1].text.split('\xa0')[0].split(',')[0]
                if len(re.findall(r'\b\d+\b', t_)) == 0 and \
                        len(re.findall(r'\w', t_[:1])) != 0 and \
                        len(re.findall(r'[a-z][A-Z]', t_)) == 0 and \
                        'Ukraine' not in c_:  # some territories are disputed, so it's easiest way to solve this
                    t.append(t_)
                    tp[t_] = p_
                    tc[t_] = c_
                    if 'capital of a political entity' in blocks[3].text:
                        cC[c_] = t_
            except Exception:
                pass
    return t, tp, tc, cC
