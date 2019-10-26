import sqlite3
from flask_jwt import JWT, jwt_required
from flask_restful import Resource,request,reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help = 'This field is necessary')
    parser.add_argument('store_id',type=int,required=True,help = 'This field is necessary')
    @jwt_required()
    def get(self,name):
        
        row = ItemModel.find_by_name(name)
        if row:
            return row.json()
        return {'message':"item doesnt exist"},404

    def post(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            return {'message':'Already Exists'},400 #bad request
        data = request.get_json()
        item = ItemModel(name,data['price'],data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message':'ERROR!!! OCCURED'},500 #internal server error
        return item.json(),201 # for created 

    def delete(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_from_db(item)

        return {'message':'Item name {} has been deleted'.format(name)} 

    def put(self,name):
        # data = request.get_json()
        
        data  = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

    
class ItemList(Resource):

    def get(self):
        return{'item':[item.json() for item in ItemModel.query.all()]} #list(map(lambda item:item.json(),ItemModel.query.all()))
