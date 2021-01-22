from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import logging

log = logging.getLogger('tester.sub')

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
        item = ItemModel.retrieve(name)

        if item:
            return item.json()
        
        return {'message':'item did not exist'}, 404 # item not found

    def post(self, name):
        if ItemModel.retrieve(name):
            return {'message':'item already exists'}, 400

        # Check if it already exists
        data = Item.parser.parse_args()
        
        item = ItemModel(name,data['price'])

        try:
            item.add_item()
        except Exception as e:
            log.warn('item {item.name} was not added to the database', e)
            return {'message':'The item was not able to be added to the database'}
        
        return item.json(), 201

    def put(self, name):
        # check if it is a new item
        item = ItemModel.retrieve(name)
        
        if not item:
            try:
                item.add_item()
            except:
                return {'message':'the item was not able to be added to the db'}, 500
            return item.json(), 201
        else:
            data = Item.parser.parse_args()
            updated_item = ItemModel(name,data['price'])
            
            try:
                updated_item.update()
            except:
                return {'message':'the item was not able to be added to the db'}, 500
            
        
        return {'message':'item has been updated'}, 200

    def delete(self, name):
        item = ItemModel.retrieve(name)
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
