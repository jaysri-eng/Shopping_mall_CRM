from flask import Flask, app, json, jsonify, make_response, request
import jwt
from werkzeug.wrappers import Request, Response, ResponseStream
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER_DATABASE = os.getenv("DB_USER_DATABASE")

# Create the configuration dictionary
config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_USER_DATABASE
}
mydb = mysql.connector.connect(**config)
# tenant_db = mysql.connector.connect(**config_tenant)
cursor = mydb.cursor()
# cursor_tenant = tenant_db.cursor()
#generate JWT key
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
cursor.execute("USE admin")

class Shop():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        # Check if it's a signup request
        if request.path == '/shopRegister' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                name = data.get('name')
                type = data.get('type')
                inventory_lvl = data.get('inventory_lvl')
                bank_account_no = data.get('bank_account_no')
                # Validate input data
                if not all([id, name, type, inventory_lvl, bank_account_no]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Insert data into MySQL database
                try:
                    cursor.execute("INSERT INTO shop (id, name, type, inventory_lvl, bank_account_no) VALUES (%s, %s, %s, %s, %s)", (id, name, type, inventory_lvl, bank_account_no))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
                
                # Return success response
                response = Response('Shop registered', status=201)
                return response(environ, start_response)
                
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
        elif request.path == '/updateShopInfo' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                name = data.get('name')
                type = data.get('type')
                inventory_lvl = data.get('inventory_lvl')
                bank_account_no = data.get('bank_account_no')
                # Validate input data
                if not all([id]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("UPDATE customer SET name = %s, type = %s, inventory_lvl = %s WHERE id = %s", (name, type, inventory_lvl, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Shop info updated', status=200)
                    return response(environ, start_response)
                
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
            
        elif request.path == "/deleteShop" and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                
                # Validate input data
                if not all([id, ]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("DELETE FROM customer WHERE id = %s", (id,))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Shop deleted', status=200)
                    return response(environ, start_response)
                
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
        
        elif request.path == "/updateTenant" and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                tenant_id = data.get('tenant_id')
                # Validate input data
                if not all([id, tenant_id]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("UPDATE shop SET tenant_id = %s WHERE id = %s", (tenant_id, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Owner updated', status=200)
                    return response(environ, start_response)
                
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
            
        # Pass other requests to the next middleware or application
        return self.app(environ, start_response)
    