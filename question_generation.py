import random
import requests
import json
from geopy import geocoders
from datetime import datetime

token_accu = 'gBj1vV4C8jprBzXRFLHpyAriTn7nvO3G'

c = ['Russia', 'China', 'Canada', 'USA']
cities = ['SPb', 'Toronto', 'Nankin', 'Boston']
C = ['Moscow', 'Beijing', 'Ottawa', 'Washington']
cC = {
    'Russia': 'Moscow',
    'China': 'Beijing',
    'Canada': 'Ottawa',
    'USA': 'Washington'
}


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


def generate_question(t):
    if t == 'cC':
        cid = random.randint(0, len(c) - 1)
        c_ = c[cid]
        C_ = cC[c_]
        return 'Назовите столицу ' + c_ + '.', C_
    if t == 'wthr':
    	cid = random.randint(0, len(C) - 1)
    	c_ = C[cid]
    	you_weather = weather_in_city(c_)
    	return 'Угадайте город. Температура: ' + str(you_weather['temp']) + ', а на небе: ' + str(you_weather['sky']), c_







