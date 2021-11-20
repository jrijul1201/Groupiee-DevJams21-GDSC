from logging import DEBUG
from flask import Flask, render_template, flash, redirect, url_for, session,logging, request
from flask_pymongo import PyMongo
from werkzeug.local import F
from passlib.hash import sha256_crypt
from datetime import datetime

import secrets
import string

# Configuration
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://Wahhaj:3DS8ai8B7j7f989@cluster0.4eydy.mongodb.net/users_devjams21?retryWrites=true&w=majority"
mongo = PyMongo(app)

# The home page
@app.route('/')
def home():
    return render_template("home.html")

# TODO: Add flash messages
# The sign up page
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        full_name = request.form['name']
        password = sha256_crypt.hash(str(request.form['pwd'])) # hashing the password
        email = request.form['email']
        phone = request.form['phoneno']
        city = request.form['city']

        # Save profile pic file
        pfp = request.files['profile_image']
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(4))
        pfp_src = pfp.filename + username + res
        mongo.save_file(pfp_src, pfp)
        mongo.db.user_info.insert_one({'username': username, 'password': password,'email': email, 'phone': phone, 'city': city, 'date_of_join': datetime.now(), 'pfp_src': pfp_src})
        
        # Redirect user to login
        return redirect(url_for('login'))


    return render_template("signup.html")

#TODO: Add a check for whether user is logged in 
# The login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname')
        pwd_candidate = request.form.get('pwd')

        user_data = mongo.db.user_info.find_one({'username' : username})
        pwd = user_data.get('password')

        if sha256_crypt.verify(pwd_candidate, pwd):
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('index'))
        
        else:
            app.logger.info("Login failed")
            flash(message="Incorrect username or password", category='error')



    return render_template("login.html")

# The dashboard
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/profile/<username>')
def profile(username):
    return render_template("profile.html")

# Running the program
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug= True)