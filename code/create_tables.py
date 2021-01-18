import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()


create_table = " CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username string, password string)"

cursor.execute(create_table)
create_table = " CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name string, price float)"
cursor.execute(create_table)
connection.commit()
connection.close()