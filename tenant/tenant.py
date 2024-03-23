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

# Create the configuration dictionary
config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_USER_DATABASE
}
mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()
#generate JWT key
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
cursor.execute("USE admin")

class TenantMiddleware:
    def __init__(self,app):
        self.app = app
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        # Check if it's a signup request
        if request.path == '/admin/addTenant' and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                name = data.get('name')
                phone = data.get('phone')
                stores = data.get('stores')
                
                # Validate input data
                if not all([id, name, phone, stores]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Insert data into MySQL database
                try:
                    cursor.execute("INSERT INTO tenant (id, name, phone, stores) VALUES (%s, %s, %s, %s)", (id, name, phone, stores))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                except Error as e:
                    response = Response(str(e), status=500)
                    return response(environ, start_response)
                
                # Return success response
                response = Response('Tenant added successfully', status=201)
                return response(environ, start_response)
                
            except json.JSONDecodeError:
                # JSON decoding error
                response = Response('Invalid JSON data', status=400)
                return response(environ, start_response)
        
        elif request.path == '/admin/tenants' and request.method == 'GET':
            try:
                # Query the tenant table to fetch all tenants
                cursor.execute("SELECT id, name, email, phone FROM tenant")
                tenants = cursor.fetchall()
                return jsonify(tenants), 200
            except Error as e:
                return jsonify({'error': str(e)}), 500 
            
        elif request.path == '/admin/tenants/<int:id>' and request.method == 'PUT':
            try:
                # Extract updated tenant data from request JSON
                data = request.json
                name = data.get('name')
                email = data.get('email')
                phone = data.get('phone')
                tenant_id = data.get('id')
                # Validate input data
                if not all([name, email, phone]):
                    return jsonify({'error': 'Missing required fields'}), 400

                # Update the tenant in the database
                cursor.execute("UPDATE tenant SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email, phone, tenant_id))
                mydb.commit()
                return jsonify({'message': 'Tenant updated successfully'}), 200
            except Error as e:
                return jsonify({'error': str(e)}), 500
        
        elif request.path == '/admin/tenants/<int:id>' and request.method == 'DELETE':
            try:
                data = request.get_json()
                id = data.get('id')
                # Delete the tenant from the database
                cursor.execute("DELETE FROM tenant WHERE id = %s", (id,))
                mydb.commit()
                return jsonify({'message': 'Tenant deleted successfully'}), 200
            except Error as e:
                return jsonify({'error': str(e)}), 500
        
        elif request.path == "/admin/updateOnwer" and request.method == 'POST':
            try:
                # Get JSON data from request
                data = json.loads(request.data)
                id = data.get('id')
                owner_of = data.get('owner_of')
                # Validate input data
                if not all([id, owner_of]):
                    response = Response('Missing required fields', status=400)
                    return response(environ, start_response)
                
                # Query the database to find the user
                try:
                    cursor.execute("UPDATE tenant SET owner_of = %s WHERE id = %s", (owner_of, id))
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    response = Response('Shops owned updated', status=200)
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