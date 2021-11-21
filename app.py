from logging import DEBUG
from flask import Flask, render_template, flash, redirect, url_for, session,logging, request
from flask_pymongo import PyMongo
from werkzeug.local import F
from passlib.hash import sha256_crypt
from datetime import datetime
from functools import wraps

import secrets
import string

# Configuration
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://Wahhaj:3DS8ai8B7j7f989@cluster0.4eydy.mongodb.net/users_devjams21?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You must login to continue!', 'danger')
            return redirect(url_for('login'))
    return wrap

# The home page
@app.route('/')
def home():
    return render_template("home.html")

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
        pfp_src = username + res + pfp.filename
        mongo.save_file(pfp_src, pfp)
        mongo.db.user_info.insert_one({'username': username, 'password': password, 'full_name': full_name ,'email': email, 'phone': phone, 'city': city, 'date_of_join': datetime.now(), 'pfp_src': pfp_src})
        
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
        if user_data:
            pwd = user_data.get('password')
        else:
            pwd = None

        if pwd and sha256_crypt.verify(pwd_candidate, pwd):
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('index'))
        
        else:
            app.logger.info("Login failed")
            flash(message="Incorrect username or password", category='error')



    return render_template("login.html")

# Link to images
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

# The dashboard
@app.route('/index')
@is_logged_in
def index():
    username = session['username']
    user_data = mongo.db.user_info.find_one({'username': username})
    pfp_src = user_data.get('pfp_src')
    full_name = user_data.get('full_name')
    return render_template("index.html", username = full_name, pfp_src = pfp_src)

# View profiles of other users
@app.route('/profile/<username>')
def profile(username):
    user_data = mongo.db.user_info.find_one({'username': username})
    full_name = user_data.get('full_name')
    phone = user_data.get('phone')
    email = user_data.get('email')
    city = user_data.get('city')
    pfp_src = user_data.get('pfp_src')
    return render_template("profile.html", name = full_name, phone = phone, email = email, city = city, pfp_src = pfp_src)

@app.route('/destinations', methods = ['GET', 'POST'])
@is_logged_in
def destinations():
    destinations = mongo.db.destinations.find()
    if request.method == 'POST':
        app.logger.info(request.form['name'])
    return render_template('destinations.html', destinations = destinations)


@app.route('/search_destination')
@is_logged_in
def search_destination():
    return render_template('search.html')

@app.route('/bookings')
@is_logged_in
def bookings():
    return render_template('bookings.html')


# Running the program
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug= True)