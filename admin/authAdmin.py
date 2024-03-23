#to create admin, check authority, login, assign roles to staff, manage tenant stores
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

# config_tenant = {
#     'host': DB_HOST,
#     'user': DB_USER,
#     'password': DB_PASSWORD,
#     'database': DB_TENANT_DATABASE
# }
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

class adminAuthMiddleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        # Check if it's a signup request
        if request.path == '/adminSignup' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                username = data.get('username')
                password = data.get('password')
                name = data.get('name')
                
                # Validate input data
                if not all([id, username, password, name]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Insert data into MySQL database
                try:
                    cursor.execute("INSERT INTO admin (id, username, password, name) VALUES (%s, %s, %s, %s)", (id, username, password, name))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
                
                # Return success response
                response = Response('Admin user added successfully', status=201)
                return response(environ, start_response)
                
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
        elif request.path == '/adminLogin' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                username = data.get('username')
                password = data.get('password')
                
                # Validate input data
                if not all([username, password]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("SELECT id, username, password, name FROM admin WHERE username = %s AND password = %s", (username, password))
                    user = cursor.fetchone()
                    if not user:
                        return jsonify({'error': 'Invalid username or password'}), 401
                    # Return success response
                    response = Response('Login successful', status=200)
                    return response(environ, start_response)
                
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
            
        elif request.path == "/adminLogout" and request.method == 'POST':
            # Check if the token cookie is present in the request
            if 'token' not in request.cookies:
                # If the token cookie is not present, return a response indicating the user is already logged out
                response = Response('User is already logged out', status=200)
                return response(environ, start_response)
            
            # Clear the token stored in the user's browser cookie
            response = Response('Logout successful', status=200)
            response.delete_cookie('token')
            return response(environ, start_response)
        
        # Pass other requests to the next middleware or application
        return self.app(environ, start_response)
    