import sqlite3
import json
# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('Cd.db')

# Create a cursor object
cursor = conn.cursor()

def create_data():
    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            wage FLOAT DEFAULT 0,
            currentLs FLOAT DEFAULT 0,
            currentCs FLOAT DEFAULT 0,
            debt FLOAT DEFAULT 0,
            date DATE DEFAULT (CURRENT_DATE)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def remove_data():
    # Connect to the database
    conn = sqlite3.connect('Cd.db')
    cursor = conn.cursor()

    # Delete all data from the table
    cursor.execute( """
    DELETE FROM users 
    WHERE rowid IN (
        SELECT rowid FROM users 
        ORDER BY rowid DESC 
        LIMIT 2
    )
""")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def Put_data(wage: float=0, currentLs: float=0, currentCs: float=0, debt: float=0):
    # Connect to the database
    conn = sqlite3.connect('Cd.db')
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO users (wage, currentLs, currentCs, debt)
        VALUES (?, ?, ?, ?)
    ''', (wage, currentLs, currentCs, debt))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def update_data(wage: float=None, currentLs: float=None, currentCs: float=None, debt: float=None):
    # Connect to the database
    conn = sqlite3.connect('Cd.db')
    cursor = conn.cursor()

    # Get the latest entry
    cursor.execute('SELECT * FROM users ORDER BY rowid DESC LIMIT 1')
    latest_entry = cursor.fetchone()

    if latest_entry is None:
        # If there are no entries, insert a new one
        Put_data(wage or 0, currentLs or 0, currentCs or 0, debt or 0)
    else:
        # Update the latest entry with new values if provided
        new_wage = wage if wage is not None else latest_entry[0]
        new_currentLs = currentLs if currentLs is not None else latest_entry[1]
        new_currentCs = currentCs if currentCs is not None else latest_entry[2]
        new_debt = debt if debt is not None else latest_entry[3]

        cursor.execute('''
            INSERT INTO users (wage, currentLs, currentCs, debt)
            VALUES (?, ?, ?, ?)
        ''', (new_wage, new_currentLs, new_currentCs, new_debt))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def init_data(LSgoal: float=0, CSgoal: float=0,Life_saving_rate: float=0.25, consumption_rate: float=0.50, debt_payment_rate: float=0.10):
    data = {
        "LSgoal": LSgoal,
        "CSgoal": CSgoal,
        "Life_saving_rate": Life_saving_rate,
        "consumption_rate": consumption_rate,
        "debt_payment_rate": debt_payment_rate
    }
    with open('goal.json', 'w') as f:
        json.dump(data, f)

def change_goal(LSgoal: float=None, CSgoal: float=None, Life_saving_rate: float=None, consumption_rate: float=None, debt_payment_rate: float=None):
    with open('goal.json', 'r') as f:
        data = json.load(f)
    if LSgoal is not None:
        data['LSgoal'] = LSgoal
    if CSgoal is not None:
        data['CSgoal'] = CSgoal
    if Life_saving_rate is not None:
        data['Life_saving_rate'] = Life_saving_rate
    if consumption_rate is not None:
        data['consumption_rate'] = consumption_rate
    if debt_payment_rate is not None:
        data['debt_payment_rate'] = debt_payment_rate

    with open('goal.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    # init_data()
    # with open('goal.json', 'r') as f:
    #     data = json.load(f)
    # print(data)
    # change_goal(LSgoal=100)
    # with open('goal.json', 'r') as f:
    #     data = json.load(f)
    # print(data)
    # change_goal(CSgoal=200)
    # with open('goal.json', 'r') as f:
    #     data = json.load(f)
    # print(data)
    remove_data()
    cursor.execute('SELECT * FROM users')
    data= cursor.fetchall()
    print(data)