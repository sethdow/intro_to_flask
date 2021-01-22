import sqlite3
import logging
from db import db

log = logging.getLogger('modelLogger')

class ItemModel(db.Model):
    def __init__(self, name, price):
        self.name = name
        self.price = price 

    def json(self):
        return {'name':self.name, 'price':self.price}
        
    @classmethod
    def retrieve(cls,name):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        item_query = "SELECT * FROM items where name = ?"
        result = cursor.execute(item_query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)
    
    def add_item(self):
      
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES (?, ?)"

        cursor.execute(insert_query,(self.name, self.price))
        connection.commit()
        connection.close()
        return self.json()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = "UPDATE items SET price = ? WHERE name = ?"
        try:
            cursor.execute(update_query,(self.price, self.name))
        except:
            return {'message':'an error occurred when adding the item'}, 500
        connection.commit()
        connection.close()