# imports
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

#class
class Store(Resource):
    parser = reqparse.RequestParser()
    
#parse args
#get
    def get(self, name):
        store = StoreModel.retrieve(name)
        if store:
            return store.json()
        return {'message':'Store does not exist'}, 404

    def post(self, name):
        
        if StoreModel.retrieve(name):
            return {'message':'A store with this name already exists'}, 400

        store = StoreModel(name)

        
        store.save_to_db()
        
            # return {'message':'Store could not be addded to the database'}, 500
    
        return store.json()

    def delete(self,name):
        
        store = StoreModel.retrieve(name)
        
        if store is None:
            return {'message':'Store does not exist'}
        try:
            store.delete_from_db()
        except:
            return {'message':'store could not be deleted from db'}
        
        return {'message':'store was deleted successfully'}
#
class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}