import logging
from db import db

log = logging.getLogger('modelLogger')

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    # tell this database what it's child is, each store has items from ItemModel
    # you want lazy loading because you don't want the self.items list to 
    # be a huge list that is just in memory all the time, it should only be
    # created when called, now items is a query builder instead of a list
    items = db.relationship('ItemModel', lazy='dynamic')
    
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items': [item.json() for item in self.items.all()]}
        
    @classmethod
    def retrieve(cls,name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.json()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()