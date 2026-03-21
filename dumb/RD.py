import sqlite3
import json
conn= sqlite3.connect('Cd.db')
cursor = conn.cursor()

def get_data() -> list:
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    return data

def get_one_data_per_month() -> list:
    cursor.execute('SELECT * FROM users AS u WHERE rowid IN (SELECT MAX(rowid) FROM users GROUP BY strftime("%Y-%m", date))ORDER BY date')
    data = cursor.fetchall()
    return data

def get_goal() -> dict:
    with open('goal.json', 'r') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    data = get_goal()
    print(data)