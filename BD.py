import sqlite3

connect = sqlite3.connect('data.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    id INTEGER,
    Username TEXT,
    streak INTEGER
)""")
connect.commit()

def ADD_USER(message):

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [message.chat.id, 'guest', 0]
        cursor.execute("INSERT INTO login_id(id, Username, streak) VALUES(?, ?, ?);", user_id)
        connect.commit()

def Update_streak(given_id, t):
    if t == 0:
        cursor.execute('''UPDATE login_id
                        SET streak = ?
                        WHERE id = ?
                        ''', (0, given_id))
    else:
        for value in cursor.execute("SELECT * FROM login_id"):
            if value[0] == given_id:
                cursor.execute(f'''UPDATE login_id
                                        SET streak = ?
                                        WHERE id = ?
                                        ''', (1 + value[2], given_id))
    connect.commit()

def Update_Username(given_id, new):
    cursor.execute(f'''UPDATE login_id SET Username='{new}' WHERE id={given_id} ''')
    connect.commit()

def Get_Streak(given_id):
    for value in cursor.execute("SELECT * FROM login_id"):
        if value[0] == given_id:
            return value[2]

def Get_Username(given_id):
    for value in cursor.execute("SELECT * FROM login_id"):
        if value[0] == given_id:
            return value[1]

def Leader():
    answer = list()
    i = 0
    for value in cursor.execute("SELECT * FROM login_id ORDER BY streak DESC"):
        connect.commit()
        i += 1
        if i > 5:
            break
        answer.append(value)
    return answer
