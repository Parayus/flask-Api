from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required


from security import authenticate,identify
from resources.user import UserRegister
from resources.item import ItemList,Item  # import things which u want sqlAlchemy to see
from resources.store import Store,StoreList
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # can be used for oracle mysql and sqlite without changing code
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False # to stop the track of every change made in sql beacuse sql alchemy has its own tracker
app.secret_key = 'pmpm'
api = Api(app)

@app.before_first_request
def creat_tables():
    db.create_all()
jwt = JWT(app,authenticate,identify) #/auth




api.add_resource(Item,'/item/<string:name>')              
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ =='__main__':
    from db import db
    db.init_app(app) #flask app circular import our item will import db
    app.run(port=5001,debug=True)
