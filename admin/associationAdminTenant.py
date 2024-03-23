from sqlite3 import Cursor
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
DB_TENANT_DATABASE = os.getenv("DB_TENANT_DATABASE")

config_tenant = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_TENANT_DATABASE
}

# mydb = mysql.connector.connect(**config_tenant)
mydb = mysql.connector.connect(**config_tenant)
cursor = mydb.cursor()

#generate JWT key
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
cursor.execute("USE admin")

class Association:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.method == 'POST' and request.path == '/adminTenant':
            try:
                data = json.loads(request.data)
                admin_id = data.get('admin_id')
                tenant_id = data.get('tenant_id')
                # Validate input data
                if not all([admin_id, tenant_id]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                try:
                    cursor.execute("INSERT INTO admin_tenant (admin_id, tenant_id) VALUES (%s, %s)", (admin_id, tenant_id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    print("Association between admin and tenant inserted successfully")
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
                # Return success response
                response = Response('Association added successfully', status=201)
                return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)

        # Pass other requests to the next middleware or application
        return self.app(environ, start_response)
        

