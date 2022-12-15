import random
import requests
import json
from geopy import geocoders
from datetime import datetime

from database_parser import *

t, tp, tc, cC, c = get_tpcC()


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
    print(json_data)
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
            new_ans = random.choice(c)
        if cat == 'C':
            new_ans = random.choice(list(cC.values()))
        elif cat == 't':
            new_ans = random.choice(t)
        if new_ans != true_ans and new_ans not in wrong_answers:
            wrong_answers.add(new_ans)
            count += 1
    return list(wrong_answers)

def generate_question(category, ans_hidden=True):
    if category == 'cC': # country -> Capital
        cid = random.randint(0, len(cC.keys()) - 1)
        c_ = c[cid]
        C_ = cC[c_]
        return 'Назовите столицу ' + c_ + '.', C_, gen_wrong_answers('C', C_)
    elif category == 'wthr': # weather -> town
        tid = random.randint(0, len(t) - 1)
        t_ = t[tid]
        you_weather = weather_in_city(t_)
        return 'Угадайте город. Температура: ' + str(you_weather['temp']) + ', а на небе: ' + str(you_weather['sky']), t_, gen_wrong_answers('t', t_)
    elif category == 'tc': # town -> country
        tid = random.randint(0, len(t) - 1)
        t_ = t[tid]
        c_ = tc[t_]
        return 'В какой стране находится город ' + t_, c_, gen_wrong_answers('c', c_)
    elif category == "cd": # country <- description
        with open("cd.json") as f:
            questions = json.load(f)
        cid = random.randint(0, len(questions["questions"]) - 1)
        return questions["questions"][cid]["question"], questions["questions"][cid]["answer"], []
    elif category == "rd": # region <- description
        with open("rd.json") as f:
            questions = json.load(f)
        cid = random.randint(0, len(questions["questions"]) - 1)
        return questions["questions"][cid]["question"], questions["questions"][cid]["answer"], []
    elif category == "rnd": #random question
        cat = random.choice(["cC", "wthr", "tc", "cd", "rd"])
        return generate_question(cat)








