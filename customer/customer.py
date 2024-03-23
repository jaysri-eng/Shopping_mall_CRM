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

class Customer():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        # Check if it's a signup request
        # if request.path == '/customerRegister' and request.method == 'POST':
        #     try:
        #         # Get JSON data from request
        #         data = json.loads(request.data)
        #         id = data.get('id')
        #         username = data.get('username')
        #         password = data.get('password')
        #         # Validate input data
        #         if not all([id, username, password]):
        #             response = Response('Missing required fields', status=400)
        #             return response(environ, start_response)
                
        #         # Insert data into MySQL database
        #         try:
        #             cursor.execute("INSERT INTO customer (id, username, password) VALUES (%s, %s, %s)", (id, username, password))
        #             mydb.commit()
        #             cursor.close()
        #             mydb.close()
        #         except Error as e:
        #             response = Response(str(e), status=500)
        #             return response(environ, start_response)
                
        #         # Return success response
        #         response = Response('Customer added successfully', status=201)
        #         return response(environ, start_response)
                
        #     except json.JSONDecodeError:
        #         # JSON decoding error
        #         response = Response('Invalid JSON data', status=400)
        #         return response(environ, start_response)
            
        if request.path == '/customerFeedback' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                feedback = data.get('feedback')
                
                # Validate input data
                if not all([id, feedback]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Insert data into MySQL database
                try:
                    cursor.execute("UPDATE customer set feedback = %s WHERE id = %s", (feedback, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
                
                # Return success response
                response = Response('Feedback updated', status=201)
                return response(environ, start_response)
                
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
        elif request.path == '/customerRating' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                rating = data.get('rating')
                
                # Validate input data
                if not all([id, rating]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("UPDATE customer SET rating = %s WHERE id = %s", (rating, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Rating updated', status=200)
                    return response(environ, start_response)
                
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
            
        elif request.path == "/customerComplaints" and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                complaints = data.get('complaints')
                
                # Validate input data
                if not all([id, rating]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("UPDATE customer SET complaints = %s WHERE id = %s", (complaints, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Complaint updated', status=200)
                    return response(environ, start_response)
                
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
            
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
        
        elif request.path == "/shoppedFrom" and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                shopped_from = data.get('shopped_from')
                
                # Validate input data
                if not all([id, shopped_from]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("UPDATE customer SET shopped_from = %s WHERE id = %s", (shopped_from, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Complaint updated', status=200)
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
    