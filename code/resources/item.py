from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from db import db

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
    parser.add_argument('store_id',
        type=int,
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
        
        item = ItemModel(name,**data)

        try:
            item.save_to_db()
        except Exception as e:
            log.warn('item {item.name} was not added to the database', e)
            return {'message':'The item was not able to be added to the database'}
        
        return item.json(), 201

    def put(self, name):
        # check if it is a new item
        item = ItemModel.retrieve(name)
        data = Item.parser.parse_args()
        # if no item add it
        if not item:
            item = ItemModel(name, **data)
        # if there is an item update the price
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        try:
            item.save_to_db()
        except:
            return {'message':'the item was not able to be added to the db'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.retrieve(name)
        if item:
            item.delete_from_db()
        return {"message":'{} has been deleted'.format(name)}

class Item_list(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
