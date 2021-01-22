import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

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
        
        if UserModel.find_by_username(data['username']):
            return {'message':'username already exists'}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        insert_query = "INSERT INTO users VALUES (null, ?,?)" #null for autoincrementing primary key
        
        cursor.execute(insert_query,(data['username'],data['password']))
        
        # Tear down
        connection.commit()
        connection.close()
        return {'message':'user has been created, get logging'}, 201