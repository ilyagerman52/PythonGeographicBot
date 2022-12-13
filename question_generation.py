import random

c = ['Russia', 'China', 'Canada', 'USA']
cities = ['SPb', 'Toronto', 'Nankin', 'Boston']
C = ['Moskva', 'Beijing', 'Ottawa', 'Washington']
cC = {
    'Russia': 'Moskva',
    'China': 'Beijing',
    'Canada': 'Ottawa',
    'USA': 'Washington'
}


def generate_question(t='cC'):
    if t == 'cC':
        cid = random.randint(0, len(c) - 1)
        c_ = c[cid]
        C_ = cC[c_]
        return 'Назовите столицу ' + c_ + '.', C_
