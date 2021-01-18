from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    # this makes a parser for all routes within this resource
    # it can be accessed by any function in the class
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        item_query = "SELECT * FROM items where name = ?"
        result = cursor.execute(item_query, (name,))
        row = result.fetchone()
        connection.close()

        if result:
            item = {'item':{'name':row[0],'price':row[1]}}
            return item
        
        return {'message':'item did not exist'}, 404 # item not found


    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name']==name, items),None)
        #if it is a new item
        if not item:
            new_item = {
                'name':name,
                'price':data['price']
            }
            items.append(new_item)
            return {'message':'item has been created'}
        # if it already exists
        else:
            item.update()
            return {'message':'item has been updated'}, 200
        return {'message':'no item found'}, 400

    def post(self, name):
        # Check if it already exists
       
        
        if next(filter(lambda x: x['name']==name, items), None):
            return {'message':'Item already exists'}, 400

        
        data = Item.parser.parse_args()
        
        new_item = {
            "name":name,
            "price":data["price"]
        }
        items.append(new_item)
        return new_item, 201

    def delete(self, name):
        global items # this tells the function that the thing being assigned isn't local
        items = list(filter(lambda x:x['name'] != name, items))
        return {"message":'{} has been deleted'.format(name)}

class Item_list(Resource):
    def get(self):
        return {"items":items}
