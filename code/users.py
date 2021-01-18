import sqlite3
from flask_restful import Resource, reqparse

class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        get_user_query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(get_user_query, (username,)) #queries must always take tuples as input
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        get_user_query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(get_user_query, (_id,)) #queries must always take tuples as input
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

class UserRegister(Resource):
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('username',
            required=True,
            help="A username is required",
            type=str
        )
        parser.add_argument('password',
            required=True,
            help="A password is required",
            type=str
        )

        # Check if username already exists
        data = parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {'message':'username already exists'}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        insert_query = "INSERT INTO users VALUES (null, ?,?)" #null for autoincrementing primary key
        
        cursor.execute(insert_query,(data['username'],data['password']))
        
        # Tear down
        connection.commit()
        connection.close()
        return {'message':'user has been created, get logging'}, 201