import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

drop_table = "DROP TABLE items"
cursor.execute(drop_table)

create_table = " CREATE TABLE IF NOT EXISTS users (id int, username string, password string)"

cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES (?,?,?)"

user = 1, "seth", "asdf"
cursor.execute(insert_query, user)

users = [
    (2, "galen", "asdf"),
    (3, "mickey", "asdf")
]
cursor.executemany(insert_query,users)

select_query = " SELECT * FROM users"
cursor.execute(select_query) # this retrieves a list, each row is a tuple in a list

username = "seth"
get_user_query = "SELECT * FROM users WHERE username = '{}'".format(username)
u_example = cursor.execute(get_user_query)
print(next(u_example))

connection.commit()
connection.close()