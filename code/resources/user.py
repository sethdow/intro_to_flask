import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
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
    
    def post(self):
        # Check if username already exists
        data = self.parser.parse_args()
        user = UserModel(**data)
        
        if UserModel.find_by_username(user.username):
            return {'message':'username already exists'}, 400

        user.save_to_db()
        return {'message':'user has been created, get logging'}, 201