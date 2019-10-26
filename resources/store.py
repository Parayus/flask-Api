from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    
    def get(self,name):
        store  = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message':'store not found'},404 

    def post(self,name):
        store = StoreModel.find_by_name(name)
        
        if store:
            return {'message':'already present'},400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'messge':'internal server error'},500

        return store.json(),201


    def delete(self,name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {'message':'Store Deleted'}

class StoreList(Resource):
    
    def get(self):
        return {'store':[ store.json() for store in StoreModel.query.all()]}