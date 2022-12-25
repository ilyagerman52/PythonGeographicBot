import sqlite3

connect = sqlite3.connect('database_preparition/profiles.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    id INTEGER,
    Username TEXT,
    streak INTEGER,
    max_streak INTEGER,
    total_answers INTEGER,
    correct_answers INTEGER,
    accuracy text,
    rating float
)""")
connect.commit()

def add_user(chat_id):
    row = cursor.execute(f"SELECT id FROM login_id WHERE id = {chat_id}")
    row = row.fetchone()
    if row is None:
        row = [chat_id, 'guest', 0, 0, 0, 0, 0, 0]
        cursor.execute("INSERT INTO login_id(id, username, streak, max_streak, total_answers, correct_answers, accuracy, rating) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", row)
        connect.commit()
    return row[1:]

def update_stats(user_id, value):
    data = cursor.execute(f'select streak, max_streak, total_answers, correct_answers from login_id where id={user_id}')
    data = data.fetchone()
    streak = (int(data[0]) + value) * value
    max_streak = max(int(data[1]), streak)
    total_answers = int(data[2]) + 1
    correct_answer = int(data[3]) + value
    accuracy = int(10000 * correct_answer / total_answers)
    accuracy = str(accuracy // 100) + '.' + str(accuracy % 100)
    rating = (correct_answer + 100) / (70 + total_answers)
    cursor.execute(f'update login_id set streak = {streak},'
                   f'max_streak = {max_streak},'
                   f'total_answers = {total_answers},'
                   f'correct_answers = {correct_answer},'
                   f'accuracy = {accuracy},'
                   f'rating = {rating} '
                   f'where id={user_id}')
    connect.commit()

def update_username(user_id, new):
    new = new.replace('\n', ' ').replace('\t', ' ')
    cursor.execute(f'UPDATE login_id SET username="{new}" WHERE id={user_id}')
    connect.commit()

def get_stats(user_id):
    info = cursor.execute(f'select username, streak, max_streak, total_answers, correct_answers, accuracy, rating from login_id where id={user_id}')
    info = info.fetchone()
    if info is None:
        return add_user(user_id)
    else:
        return info

def leader(t='correct_answers'): # тут надо сделать рейтинг, но для этого надо написать нормальную функцию рейтинга
    leaders = cursor.execute(f"SELECT username, streak, max_streak, total_answers, correct_answers, accuracy, rating FROM login_id ORDER BY {t} DESC LIMIT 5")
    leaders = leaders.fetchall()
    return leaders
