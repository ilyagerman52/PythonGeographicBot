import random

from utils import weather_in_city
from database_parser import *


def gen_wrong_answers(cat, true_ans):
    wrong_answers = set()
    count = 0
    while count != 3:
        new_ans = None
        conn = sqlite3.connect("geonames.db")
        cur = conn.cursor()
        if cat == 'c':
            cur.execute("""SELECT c_r
                        FROM countries
                        ORDER BY RANDOM()
                        LIMIT 1""")
            new_ans = cur.fetchone()[0]
        if cat == 'C':
            cur.execute("""SELECT Cap_r
                        FROM countries
                        ORDER BY RANDOM()
                        LIMIT 1""")
            new_ans = cur.fetchone()[0]
        elif cat == 't':
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
    conn = sqlite3.connect("geonames.db")
    cur = conn.cursor()
    if category == 'cC':  # country -> Capital
        cur.execute("""SELECT c_r, Cap_r
                        FROM countries
                        where not c_r = "None" and 
                        not Cap_r = "None"
                        ORDER BY RANDOM()
                        LIMIT 1""")
        c_r, C_r = cur.fetchone()
        return 'Назовите столицу ' + c_r + '.', C_r, gen_wrong_answers('C', C_r)
    elif category == 'wthr':  # weather -> town
        cur.execute("""SELECT t_r
                        FROM towns
                        where not t_r="None"
                        ORDER BY RANDOM()
                        LIMIT 1""")
        t_ = cur.fetchone()[0]
        you_weather = weather_in_city(t_)
        return 'Угадайте город. Температура: ' + str(you_weather['temp']) + ', а на небе: ' + str(
            you_weather['sky']), t_, gen_wrong_answers('t', t_)
    elif category == 'tc':  # town -> country
        cur.execute("""SELECT t_r, c_r
                        FROM towns
                        where not t_r="None" and
                        not c_r="None" 
                        ORDER BY RANDOM()
                        LIMIT 1""")
        t_r, c_r = cur.fetchone()
        return 'В какой стране находится город ' + t_r, c_r, gen_wrong_answers('c', c_r)
    elif category == "cd":  # country <- description
        cur.execute("""SELECT *
                        FROM ege_17
                        ORDER BY RANDOM()
                        LIMIT 1""")
        return *cur.fetchone(), []
    elif category == "rd":  # region <- description
        cur.execute("""SELECT *
                        FROM ege_18
                        ORDER BY RANDOM()
                        LIMIT 1""")
        return *cur.fetchone(), []
    elif category == "rnd":  # random question
        cat = random.choice(["cC", "wthr", "tc", "cd", "rd", "flg", "brd"])
        return generate_question(cat)
    elif category == "flg":
        cur.execute("""SELECT c_r, flg
                        FROM countries
                        where not flg="flag"
                        ORDER BY RANDOM()
                        LIMIT 1""")
        c_r, flg = cur.fetchone()
        return flg, c_r, gen_wrong_answers('c', c_r)
    elif category == "brd":
        cur.execute("""SELECT c_r, brd
                        FROM countries
                        where not brd="brd"
                        ORDER BY RANDOM()
                        LIMIT 1""")
        c_r, brd = cur.fetchone()
        return brd, c_r, gen_wrong_answers('c', c_r)
