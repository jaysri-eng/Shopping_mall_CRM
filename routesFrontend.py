#for frontend pages
from flask import render_template, send_from_directory
from main import app


@app.route("/homepage",methods=['GET'])
def homepage():
    return render_template('templates/index.html')

@app.route("/adminLoginPage",methods=['GET'])
def adminLoginPage():
    return render_template('login/adminLogin.html')

@app.route("/tenantLoginPage",methods=['GET'])
def tenantLoginPage():
    return render_template('login/tenantLogin.html')

@app.route("/customerLoginPage",methods=['GET'])
def customerLoginPage():
    return render_template('login/customerLogin.html')

@app.route("/shopLoginPage",methods=['GET'])
def shopLoginpage():
    return render_template('login/shopLogin.html')

@app.route("/adminSignupPage",methods=['GET'])
def adminSignupPage():
    return render_template('signup/adminSignup.html')

@app.route("/tenantSignupPage",methods=['GET'])
def tenantSignupPage():
    return render_template('signup/tenantSignup.html')

@app.route("/customerSignupPage",methods=['GET'])
def customerSignupPage():
    return render_template('signup/customerSignup.html')

@app.route("/shopSignupPage",methods=['GET'])
def shopSignupPage():
    return render_template('signup/shopSignup.html')

@app.route("/adminForgotPasswordPage",methods=['GET'])
def adminForgotPasswordPage():
    return render_template('forgotPassword/adminForgotPassword.html')

@app.route("/customerForgotPasswordPage",methods=['GET'])
def customerForgotPasswordPage():
    return render_template('forgotPassword/customerForgotPassword.html')

@app.route("/tenantForgotPasswordPage",methods=['GET'])
def tenantForgotPasswordPage():
    return render_template('forgotPassword/tenantForgotPassword.html')

@app.route("/shopForgotPasswordPage",methods=['GET'])
def shopForgotPasswordPage():
    return render_template('forgotPassword/shopForgotPassword.html')
##end for rendering pages

# Serve the 'admin.html' file from the 'homepages' directory
# @app.route('/homepages/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('homepages', filename)