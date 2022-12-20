import random
import requests
import json
from geopy import geocoders
import sqlite3
from datetime import datetime

from database_parser import *

token_accu = 'gBj1vV4C8jprBzXRFLHpyAriTn7nvO3G'


def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude


def code_location(latitude: str, longitude: str, token_accu: str):
    url_location_key = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' \
                       f'{token_accu}&q={latitude},{longitude}&language=ru'
    resp_loc = requests.get(url_location_key, headers={"APIKey": token_accu})
    json_data = json.loads(resp_loc.text)
    code = json_data['Key']
    return code


def get_weather(code_loc: str, token_accu: str):
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{code_loc}?' \
                  f'apikey={token_accu}&language=ru&metric=True'
    response = requests.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    dict_weather = dict()
    dict_weather['link'] = json_data[0]['MobileLink']
    weather = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
    return weather


def weather_in_city(city):
    latitude, longitude = geo_pos(city)
    code_loc = code_location(latitude, longitude, token_accu)
    you_weather = get_weather(code_loc, token_accu)
    return you_weather


def gen_wrong_answers(cat, true_ans):
    wrong_answers = set()
    count = 0
    while count != 3:
        new_ans = None
        if cat == 'c':
            conn = sqlite3.connect("geonames.db")
            cur = conn.cursor()
            cur.execute("""SELECT c_r
                                        FROM countries
                                        ORDER BY RANDOM()
                                        LIMIT 1""")
            temp = cur.fetchone()
            new_ans = random.choice(temp[0])
        if cat == 'C':
            conn = sqlite3.connect("geonames.db")
            cur = conn.cursor()
            cur.execute("""SELECT C_r
                                        FROM countries
                                        ORDER BY RANDOM()
                                        LIMIT 1""")
            temp = cur.fetchone()
            new_ans = random.choice(temp[0])
        elif cat == 't':
            conn = sqlite3.connect("geonames.db")
            cur = conn.cursor()
            cur.execute("""SELECT t_r
                                        FROM towns
                                        ORDER BY RANDOM()
                                        LIMIT 1""")
            temp = cur.fetchone()
            new_ans = random.choice(temp[0])
        if len(new_ans) > 2 and new_ans != true_ans and new_ans not in wrong_answers:
            wrong_answers.add(new_ans)
            count += 1
    return list(wrong_answers)


def generate_question(category, ans_hidden=True):
    if category == 'cC':  # country -> Capital
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT c_r, C_r
                    FROM countries
                    ORDER BY RANDOM()
                    LIMIT 1""")
        temp = cur.fetchone()
        return 'Назовите столицу ' + temp[0] + '.', temp[1], gen_wrong_answers('C', temp[1])
    elif category == 'wthr':  # weather -> town
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT t_r
                            FROM towns
                            ORDER BY RANDOM()
                            LIMIT 1""")
        temp = cur.fetchone()
        t_ = temp[0]
        you_weather = weather_in_city(t_)
        return 'Угадайте город. Температура: ' + str(you_weather['temp']) + ', а на небе: ' + str(
            you_weather['sky']), t_, gen_wrong_answers('t', t_)
    elif category == 'tc':  # town -> country
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT t_r, c_r
                            FROM towns
                            ORDER BY RANDOM()
                            LIMIT 1""")
        temp = cur.fetchone()
        return 'В какой стране находится город ' + temp[0], temp[1], gen_wrong_answers('c', temp[1])
    elif category == "cd":  # country <- description
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT *
            FROM ege_17
            ORDER BY RANDOM()
            LIMIT 1""")
        return *cur.fetchone(), []
    elif category == "rd":  # region <- description
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT *
                    FROM ege_18
                    ORDER BY RANDOM()
                    LIMIT 1""")
        return *cur.fetchone(), []
    elif category == "rnd":  # random question
        cat = random.choice(["cC", "wthr", "tc", "cd", "rd", "flg", "shp"])
        return generate_question(cat)
    elif category == "flg":
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT c_r, flg
                                    FROM countries
                                    ORDER BY RANDOM()
                                    LIMIT 1""")
        temp = cur.fetchone()
        return temp[1], temp[0], gen_wrong_answers('c', temp[0])
    elif category == "shp":
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT c_r, brd
                                            FROM countries
                                            ORDER BY RANDOM()
                                            LIMIT 1""")
        temp = cur.fetchone()
        return temp[1], temp[0], gen_wrong_answers('c', temp[0])
