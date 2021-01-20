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
    @classmethod
    def retrieve(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        item_query = "SELECT * FROM items where name = ?"
        result = cursor.execute(item_query, (name,))
        row = result.fetchone()
        connection.close()
        return row


    @jwt_required()
    def get(self, name):
        item = Item.retrieve(name)

        if item:
            item = {'item':{'name':item[0],'price':item[1]}}
            return item
        
        return {'message':'item did not exist'}, 404 # item not found

    @classmethod
    def add_item(cls, name):
        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES (?, ?)"
        new_item = name, data['price']
        cursor.execute(insert_query,new_item)
        connection.commit()
        connection.close()
        return {'name':name, 'price':data['price']}


    def post(self, name):
        # Check if it already exists
        item = Item.retrieve(name)
        
        if item:
            return {'message':'item already exists'}, 400

        try:
            added_item = Item.add_item(name)
        except:
            return {'message':'an error occurred when adding the item'}, 500

        return added_item, 201

    def put(self, name):
        # check if it is a new item
        item = Item.retrieve(name)
        
        if not item:
            try:
            added_item = Item.add_item(name)
            except:
                return {'message':'an error occurred when adding the item'}, 500
            return added_item, 201

        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = "UPDATE items SET price = ? WHERE name = ?"
        updated_item = data['price'], name
        cursor.execute(update_query,updated_item)
        connection.commit()
        connection.close()
        
        return {'message':'item has been updated'}, 200



    def delete(self, name):
        item = Item.retrieve(name)
        if not item:
            return {'message':'no item with that name exists'}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = "DELETE FROM items WHERE name = ?"
        cursor.execute(delete_query,(name,))
        connection.commit()
        connection.close()
        return {"message":'{} has been deleted'.format(name)}

class Item_list(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        all_query = "SELECT * FROM items"
        result = cursor.execute(all_query)
        items = result.fetchall()
        connection.close()
        return {"items":items}
