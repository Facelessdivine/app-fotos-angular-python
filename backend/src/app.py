
from flask import Flask, request, Response

from flask_pymongo import pymongo
import hashlib  
import os  

from dotenv import load_dotenv

from flask.json import jsonify

from bson import json_util

from bson.objectid import ObjectId

import dbconfig as db

from flask_cors import CORS, cross_origin

load_dotenv()  


salt = os.getenv('SALT').encode()


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)  

cors = CORS(app, resources={r"*": {"origins": "http://localhost:4200"}})
db1 = db.c_users.users  




@app.route('/users/<id>', methods=['GET'])
def get_user(id):  
    
    user = db1.find_one({'_id': ObjectId(id)})
    
    response = json_util.dumps(user)
    
    return Response(response, mimetype='application/json')



@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):  
    
    db1.delete_one({'username': username})
    
    response = jsonify({'message': 'User: ' + username +
                       ' was deleted successfully'})
    return response  



@app.route('/users/<id>', methods=['PUT'])
def update_user(id):  
    
    username = request.json['username']
    
    user = db1.find_one({'_id': ObjectId(id)})
    
    if user != None:  
        if username:  
            
            
            usernameold = user['username']
            db1.update_one({'_id': ObjectId(id)}, {'$set': {
                'username': username}})  
            
            response = jsonify(
                {'message': 'User: ' + usernameold + ' was updated successfully to ' + username})
            return response  
    else:
        
        return {'alert': 'Username do not match with any username account'}



@app.route('/users', methods=['GET'])
def get_users():
    
    users = db1.find()
    
    response = json_util.dumps(users)
    
    return Response(response, mimetype='application/json')



@app.route('/signup', methods=['POST'])
def create_user():
    username = request.json['username']
    name = request.json['nombre']
    direccion = request.json['direccion']
    ape1 = request.json['ape1']
    ape2 = request.json['ape2']
    tel = request.json['tel']
    user = db1.find_one({'username': username})
    password = request.json['password'].encode()
    if user == None:  
        if username and password:  
            hashed_password = hashlib.pbkdf2_hmac(
                'sha512', password, salt, 100000).hex()
            id = db1.insert_one(
                {'username': username, 'password': hashed_password, 'nombre': name, 'direccion': direccion, 'Apellido_paterno':ape1, 'Apellido_materno':ape2,'Telefono':tel}
            )  
            response = {
                
                'id': str(id),
                'username': username,  
                'password': hashed_password  
            }
            return response  
        else:
            return not_found()  
    else:
        
        return {'alert': 'Username is already taken, try to login or choose another one'}



@app.route('/signin', methods=['POST'])
def login():
    
    username = request.json['username']
    
    user = db1.find_one({'username': username})
    
    password = request.json['password'].encode()
    
    hashed_password = hashlib.pbkdf2_hmac(
        'sha512', password, salt, 100000).hex()

    if user != None and hashed_password == user['password']:
        return {'message': 'Login Success',
                'response': 'welcome ' + username}  
    else:
        return {'message': 'Login failed',
                'response': 'invalid username or pasword'}  



@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found',
        'status': 404
    })  
    
    response.status_code = 404
    return response  


if __name__ == "__main__":
    app.run(load_dotenv=True)  
