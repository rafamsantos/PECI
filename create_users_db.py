import sqlite3

conn = sqlite3.connect('register_users.db')

cursor = conn.cursor()

create_table_query1 = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
'''

create_table_query2 = '''
CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT,
    expires_at TEXT
);
'''

create_table_query3 = '''
CREATE TABLE IF NOT EXISTS code (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code INTEGER,
    expires_at TEXT
);
'''

cursor.execute(create_table_query1)
cursor.execute(create_table_query2)
cursor.execute(create_table_query3)

conn.commit()
conn.close()
