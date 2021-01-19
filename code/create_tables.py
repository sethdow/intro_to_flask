import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()


create_table = " CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username string, password string)"
cursor.execute(create_table)

# grab_stuff = "SELECT * FROM items"
# print(cursor.execute(grab_stuff).fetchall())

# drop_table = "DROP TABLE items"
# cursor.execute(drop_table)

create_table = " CREATE TABLE IF NOT EXISTS items (name string, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()