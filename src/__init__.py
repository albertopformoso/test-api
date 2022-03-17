from dotenv import load_dotenv, find_dotenv
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_cors import CORS
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, request, Response
# from flask_bcrypt import Bcrypt
# from flask_jwt import JWT, jwt_required

import json
import os
import requests
import datetime

app = Flask(__name__)

# .ENV FILE LOAD
try:
    load_dotenv(find_dotenv())
except Exception:
    raise RuntimeError("Failed to load .env file")

# CONFIGURATIONS
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# INITIALIZATION
api = Api(app)
mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
CORS(app)


# RESOURCES
class Users(Resource):

    # Get one user
    def get(self, user_name):

        if user_name:
            user = mongo.db.users.find_one({'user_name': ObjectId(user_name)})
            response = json_util.dumps(user)
            return Response(response, mimetype='application/json')
        else:
            res = {'response': 'Error 400 fail response'}
            res = json_util.dumps(res)
            return Response(res, mimetype='application/json')

        
    # Delete a user
    def delete(self, user_name):
        result = mongo.db.users.find_one({'user_name': user_name})

        if not result:
            res = {'response': 'Error 400 fail response'}
            res = json_util.dumps(res)
            return Response(res, mimetype='application/json')

        oid = result['_id']

        mongo.db.users.delete_one({'_id': ObjectId(oid)})
        res = {'resposne': f'200 User successfully deleted'}
        res = json_util.dumps(res)
        return Response(res, mimetype='application/json')
    
    # Update a user
    def patch(self, user_name):
        result = mongo.db.users.find_one({'user_name': user_name})

        if not result:
            res = {'response': 'Error 400 fail response'}
            res = json_util.dumps(res)
            return Response(res, mimetype='application/json')

        oid = result['_id']
        
        args = request.args
        user_name = args.get("user_name", None)
        role = args.get("role", None)
        age = args.get("age", None)
        
        if user_name and role and age:
            mongo.db.users.update_one({'_id': ObjectId(oid)}, {'$set': {
                'user_name': user_name,
                'role': role,
                'age': age
            }})
            
            response = {'response': f'200 User successfully updated'}
            return response
        response = {'response': f'Error 400 fail response'}


class AllUsers(Resource):
    
    def get(self):
        all_users = mongo.db.users.find()

        response = json_util.dumps(all_users)
        return Response(response[0], mimetype='application/json')

    # Create a user
    def post(self):

        args = request.args
        user_name = args.get("user_name", None)
        role = args.get("role", None)
        age = args.get("age", None)
        
        if user_name and role and age:
            id = mongo.db.users.insert_one(
                {
                    'user_name': user_name.capitalize(),
                    'role': role.capitalize(),
                    'age': int(age),
                }
            )

            return {
                'response': '200 User successfuly added',
                }
        else:
            return {'response': 'Error 400 fail response.'}


# DEFAULT
@app.route('/api/v1')
def index():
    return 'Welcome to Test API'

# RESOURCE URLs
api.add_resource(Users, '/api/v1/users/<string:user_name>')
api.add_resource(AllUsers, '/api/v1/users')