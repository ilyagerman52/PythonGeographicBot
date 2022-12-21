import requests
from bs4 import BeautifulSoup
import re
from utils import translate
import sqlite3
import json


db_file = 'geonames.db'
db = sqlite3.connect(db_file)
cur = db.cursor()
cur.execute("""create table if not exists towns(
t text,
t_r text,
c text,
c_r text,
p integer
)""")
db.commit()

cur.execute("""create table if not exists countries(
c text,
c_r text,
Cap text,
Cap_r text,
a integer,
p integer,
flg picture,
brd picture
)""")
db.commit()

def get_towns():
    for page in range(7):
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
                    row = (str(t_), str(translate(t_)), c_, translate(c_), p_)
                    cur.execute('insert into towns values(?, ?, ?, ?, ?);', row)
                    db.commit()
            except Exception:
                pass
    print('parsed')
    return


def get_countries():
    url = 'https://www.geonames.org/countries/'
    r = requests.get(url)
    r = r.content.decode('utf-8')
    soup = BeautifulSoup(r, 'html.parser')
    for table in soup.find_all('tr'):
        blocks = table.find_all('td')
        if len(blocks) == 9:
            c = blocks[4].text
            C = blocks[5].text
            a = blocks[6].text
            p = blocks[7].text.replace(',', '')
            cont = blocks[8].text
            if C != '':
                try:
                    row = (c, translate(c), C, translate(C), a, p, 'flag', 'brd')
                    cur.execute('insert into countries values(?, ?, ?, ?, ?, ?, ?, ?);', row)
                    db.commit()
                except:
                    print(c, C, a, p)
    get_brd()
    print('parsed')
    return


def get_brd():
    link = 'https://raw.githubusercontent.com/daniinco/countries/main/images.json'
    r = requests.get(link).content.decode('utf-8')
    with open('images.json', 'w') as f:
        f.write(r)
    with open('images.json', 'r') as f:
        countries = json.load(f)
        countries = countries['countries']
        for row in countries:
            name = row['name']
            flag = row['flag']
            brd = row['shape']
            print(name, flag, brd)
            cur.execute(f'update countries set flg="{flag}", brd="{brd}" where c="{name}"')


# get_countries()
# get_towns()
# cur.execute('select * from towns')
# res = cur.fetchall()
# print(*res, sep='\n')