import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity 
from resources.user import UserRegister
from resources.item import Item, Item_list
from resources.store import Store, StoreList 
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'seth'
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# The function below allows authentication, it create route /auth
# which returns a JW token, which is then used when the next
# request is made, the request uses the token, extracts the
# id from the token 
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item_list, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
    