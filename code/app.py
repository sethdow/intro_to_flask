from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity 
from users import UserRegister
from item import Item, Item_list

app = Flask(__name__)
app.secret_key = 'seth'
api = Api(app)


# The function below allows authentication, it create route /auth
# which returns a JW token, which is then used when the next
# request is made, the request uses the token, extracts the
# id from the token 
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item_list, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)