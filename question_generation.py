import random

from utils import *
from database_parser import *


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
            new_ans = cur.fetchone()[0]
        if cat == 'C':
            conn = sqlite3.connect("geonames.db")
            cur = conn.cursor()
            cur.execute("""SELECT Cap_r
                        FROM countries
                        ORDER BY RANDOM()
                        LIMIT 1""")
            new_ans = cur.fetchone()[0]
        elif cat == 't':
            conn = sqlite3.connect("geonames.db")
            cur = conn.cursor()
            cur.execute("""SELECT t_r
                        FROM towns
                        ORDER BY RANDOM()
                        LIMIT 1""")
            new_ans = cur.fetchone()[0]
        if new_ans is not None and len(new_ans) > 2 and new_ans != true_ans and new_ans not in wrong_answers:
            wrong_answers.add(new_ans)
            count += 1
    return list(wrong_answers)


def generate_question(category):
    if category == 'cC':  # country -> Capital
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT c_r, Cap_r
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
        cat = random.choice(["cC", "wthr", "tc", "cd", "rd", "flg", "brd"])
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
    elif category == "brd":
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        cur.execute("""SELECT c_r, brd
                        FROM countries
                        ORDER BY RANDOM()
                        LIMIT 1""")
        temp = cur.fetchone()
        return temp[1], temp[0], gen_wrong_answers('c', temp[0])
