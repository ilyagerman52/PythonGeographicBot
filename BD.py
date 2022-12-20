import sqlite3

connect = sqlite3.connect('data.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    id INTEGER,
    Username TEXT,
    streak INTEGER
)""")
connect.commit()

def add_user(chat_id):
    row = cursor.execute(f"SELECT id FROM login_id WHERE id = {chat_id}")
    row = row.fetchone()
    if row is None:
        row = [chat_id, 'guest', 0]
        cursor.execute("INSERT INTO login_id(id, username, streak) VALUES(?, ?, ?);", row)
        connect.commit()
    return row[1:]

def update_streak(user_id, value):
    streak = cursor.execute(f'select streak from login_id where id={user_id}')
    streak = int(streak.fetchone()[0])
    streak += value
    streak *= value
    cursor.execute(f'update login_id set streak = {streak} where id={user_id}')
    connect.commit()

def update_username(user_id, new):
    cursor.execute(f'UPDATE login_id SET username="{new}" WHERE id={user_id}')
    connect.commit()

def get_stats(user_id):
    info = cursor.execute(f'select username, streak from login_id where id={user_id}')
    info = info.fetchone()
    if info is None:
        return add_user(user_id)
    else:
        return info

def leader():
    leaders = cursor.execute("SELECT username, streak FROM login_id ORDER BY streak DESC LIMIT 5")
    leaders = leaders.fetchall()
    return leaders
