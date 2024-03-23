#import or add modules 
import requests 
from flask import Flask, jsonify, request, make_response, render_template
import jwt
from functools import wraps
import json
import os
from jwt.exceptions import DecodeError
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from dotenv import load_dotenv
from admin.authAdmin import adminAuthMiddleware
from tenant.tenant import TenantMiddleware
from admin.associationAdminTenant import Association
from customer.customerAuth import CustomerAuth
from customer.customer import Customer

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

# Create the configuration dictionary
config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_DATABASE
}

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

#initiate flask app and assign JWT toke for authentication
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

#function for authenticating the JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except DecodeError:
            return jsonify({'error': 'Authorization token is invalid'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

#mention the port number and assign app routes 
port = int(os.environ.get('PORT',5000))

@app.route("/homepage",methods=['GET'])
def homepage():
    return render_template('index.html')

# calling our middleware
app.wsgi_app = adminAuthMiddleware(app.wsgi_app)
@app.route("/adminSignup", methods=['POST'])
def adminSignup():
    data = request.get_json()
    id = data.get('id')
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    # Call your signup function from the middleware
    if adminAuthMiddleware(id, username, password, name):
        return jsonify({'message': 'Admin user added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add admin user'}), 500

@app.route("/adminLogin",methods=['POST'])
def adminLogin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if adminAuthMiddleware(username, password):
        return jsonify({'message': 'Admin logged in'}),201
    else:
        return jsonify({'error': 'Incorrect details entered'}), 500
    
@app.route("/adminLogout", methods=['POST'])
def adminLogout():
    if adminAuthMiddleware():
        return jsonify({'message': 'Admin logged in'}),201
    else:
        return jsonify({'error': 'Incorrect details entered'}), 500

# calling our middleware
app.wsgi_app = TenantMiddleware(app.wsgi_app)
@app.route("/admin/addTenant",methods=['POST'])
def addTenant():
    # Extract token from request headers
    token = request.cookies.get('token')
    # Validate token (e.g., check if it's present and valid)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    phone = data.get('phone')
    stores = data.get('stores')
    # Call your signup function from the middleware
    if TenantMiddleware(id, name, phone, stores):
        return jsonify({'message': 'Tenant added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add tenant'}), 500
    
# calling our middleware
app.wsgi_app = Association(app.wsgi_app)
@app.route("/adminTenant",methods=['POST'])
def createAssociation():
    data = request.get_json()
    admin_id = data.get('admin_id')
    tenant_id = data.get('tenant_id')
    # Call your signup function from the middleware
    if Association(id, admin_id, tenant_id):
        return jsonify({'message': 'Tenant added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add tenant'}), 500
    
# calling our middleware
app.wsgi_app = CustomerAuth(app.wsgi_app)
@app.route('/customerSignup',methods=['POST'])
def customerSignup():
    data = request.get_json()
    id = data.get('id')
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')

    # Call your signup function from the middleware
    if CustomerAuth(id, username, password, name):
        return jsonify({'message': 'Customer added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add customer'}), 500

@app.route('/customerLogin',methods=['POST'])
def customerLogin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Call your signup function from the middleware
    if CustomerAuth(username, password):
        return jsonify({'message': 'Customer logged in successfully'}), 201
    else:
        return jsonify({'error': 'Login failed'}), 500
    
app.wsgi_app = Customer(app.wsgi_app)
@app.route('/customerFeedback',methods=['POST'])
def customerFeedback():
    # Extract token from request headers
    token = request.cookies.get('customer_token')
    # Validate token (e.g., check if it's present and valid)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    data = request.get_json()
    id = data.get('id')
    feedback = data.get('feedback')
    # Call your signup function from the middleware
    if CustomerAuth(id, feedback):
        return jsonify({'message': 'feedback updated'}), 201
    else:
        return jsonify({'error': 'Feedback not updated'}), 500
    
@app.route('/customerRating',methods=['POST'])
def customerRating():
    # Extract token from request headers
    token = request.cookies.get('customer_token')
    # Validate token (e.g., check if it's present and valid)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    data = request.get_json()
    id = data.get('id')
    rating = data.get('rating')
    # Call your signup function from the middleware
    if CustomerAuth(id, rating):
        return jsonify({'message': 'feedback updated'}), 201
    else:
        return jsonify({'error': 'Feedback not updated'}), 500
    
@app.route('/customerComplaints',methods=['POST'])
def customerComplaints():
    # Extract token from request headers
    token = request.cookies.get('customer_token')
    # Validate token (e.g., check if it's present and valid)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    data = request.get_json()
    id = data.get('id')
    complaints = data.get('complaints')
    # Call your signup function from the middleware
    if CustomerAuth(id, complaints):
        return jsonify({'message': 'complaint updated'}), 201
    else:
        return jsonify({'error': 'complaint not updated'}), 500
    
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=port)