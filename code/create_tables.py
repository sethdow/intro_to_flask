import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()


create_table = " CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username string, password string)"
cursor.execute(create_table)

drop_table = "DROP TABLE items"
cursor.execute(drop_table)

create_table = " CREATE TABLE IF NOT EXISTS items (name string, price real)"
cursor.execute(create_table)

add_test = "INSERT INTO items VALUES ('test',99.99)"
cursor.execute(add_test)
connection.commit()
connection.close()