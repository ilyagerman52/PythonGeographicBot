import translators
import re
from geopy import geocoders
import requests
import json

HELP_MESSAGE = '''
Бот был создан в качестве проекта по курсу DeepPython на направлении AMI HSE.
<em>Что умеет бот?</em>
Бот представляет собой квиз-викторину. Пользователям предлагается отвечать на вопросы, сгенерированные ботом.
<em>Категории вопросов:</em>

1) Назвать столицу страны или зависимой территории.

2) Угадать страну по городу в ней.

3) Угадать страну по описанию из ЕГЭ.

4) Угадать субъект РФ по описанию из ЕГЭ.

5) Назвать страну по флагу.

6) Угадать страну по очертаниям.

7) Угадать город по погоде.

8) Случайный вопрос.

Бот так же отслеживает стрики правильных ответов. 
Для каждого пользователя создаётся профиль, где можно посмотреть статистику. 
Также можно посмотреть TOP среди всех пользователей по стрикам.
Реализована возможность показать/скрыть варианты ответов.

<em>Команды:</em>
/start - Начать работу с ботом
/profile - узнать свои Name и Streak
/top - получить топ пользователей по стрикам
/change_username - изменить Name
'''

UNEXPEXTED = '''
Я тебя не понял. Справку можно вызвать командой /help
'''

token_accu = 'gBj1vV4C8jprBzXRFLHpyAriTn7nvO3G'


def translate(en_str):
    ru_str = translators.translate_text(en_str, 'yandex', 'auto', 'ru')
    if ru_str[:3] == 'г. ':
        ru_str = ru_str[3:]
    if len(re.findall(r"[а-яA-Я-'.’ ]", ru_str)) != len(ru_str):
        print('error')
        return None
    ru_str.replace('Город', '').strip()
    return ru_str


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

def good_name(string):
    return string.lower().replace('-', ' ').replace('`', ' ').replace('\'', ' ')
