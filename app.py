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

#TODO: Verify Usersm
#TODO: Functional prototype instead of basic web app with mock data
#TODO: Make posts for each user


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

# Check if user is admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['username'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash('You must be admin to continue!', 'danger')
            return redirect(url_for('login'))
    return wrap

# Check if user is verified
def is_verified(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['verified'] == True:
            return f(*args, **kwargs)
        else:
            flash('You must be verified to continue!', 'danger')
            return redirect(url_for('verify_user'))
    return wrap

# The home page
@app.route('/')
def home():
    #return redirect(url_for('login'))
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

        if username in mongo.db.user_info.find({'username': username}):
            flash('Username is taken!', 'danger')
            app.logger.info('username taken')
            app.logger.info(mongo.db.user_info.find({'username': username}))
            return render_template('signup.html')

        if email in mongo.db.user_info.find({'email': email}):
            flash('Email is already in use for another account', 'danger')
            app.logger.info('email taken')
            return render_template('signup.html')

        # Save profile pic file
        pfp = request.files['profile_image']
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(4))
        pfp_src = username + res + pfp.filename
        mongo.save_file(pfp_src, pfp)
        mongo.db.user_info.insert_one({'username': username, 'password': password, 'full_name': full_name ,'email': email, 'phone': phone, 'city': city, 'date_of_join': datetime.now(), 'pfp_src': pfp_src, 'verified': False})
        
        # Redirect user to login
        return redirect(url_for('login'))


    return render_template("signup.html")


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
            session['verified'] = user_data.get('verified')
            return redirect(url_for('index'))
        
        else:
            app.logger.info("Login failed")
            flash(message="Incorrect username or password", category='error')



    return render_template("login.html")

# Link for users to submit verification details
@app.route('/verify_user', methods = ['GET', 'POST'])
def verify_user():
    if session.get('verified'):
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            username = session['username']
            user_data = mongo.db.user_info.find_one({'username': username})
            full_name = user_data.get('full_name')

            res1 = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(8))
            id_document = request.files.get('id_document')
            id_document_src = res1 + username + id_document.filename
            mongo.save_file(id_document_src, id_document)

            res2 = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(8))
            id_selfie = request.files.get('id_selfie')
            id_selfie_src = res2 + username + id_selfie.filename
            mongo.save_file(id_selfie_src, id_selfie)

            mongo.db.verification.insert_one({'username': username, 'full_name': full_name, 'id_document_src' :id_document_src, 'id_selfie_src': id_selfie_src})
            flash('Your account will be verified soon', 'success')
            return redirect(url_for('index'))

        return render_template('verify_user.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# For admins to verify users
@app.route('/admin_verify_users', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def admin_verify_users():
    users = mongo.db.verification.find()
    if request.method == 'POST':
        username = request.form.get('username')
        mongo.db.user_info.update_one({'username': username}, {'$set':{'verified': True}})
        mongo.db.verification.delete_one({'username': username})
    return render_template('admin_verify_users.html', users = users)

# Link to images
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/upload_files', methods = ['GET', 'POST'])
@is_admin
def upload_files():
    if request.method == 'POST':
        image = request.files['image']
        mongo.save_file(image.filename, image)
    return render_template('upload_image.html')

# The dashboard
@app.route('/index')
@is_logged_in
def index():
    username = session['username']
    user_data = mongo.db.user_info.find_one({'username': username})
    pfp_src = user_data.get('pfp_src')
    full_name = user_data.get('full_name')
    # Get names of places user plans to visit
    visiting_list = user_data.get('visiting')
    # Get data from those place
    visiting_destinations = []
    if visiting_list:
        for i in visiting_list:
            place_data = mongo.db.destinations.find_one({'name': i})
            visiting_destinations.append(place_data)
    return render_template("index.html", username = full_name, pfp_src = pfp_src, visiting_destinations = visiting_destinations)


# View profiles of other users
@app.route('/profile/<username>', methods = ['GET', 'POST'])
def profile(username):
    user_data = mongo.db.user_info.find_one_or_404({'username': username})
    full_name = user_data.get('full_name')
    phone = user_data.get('phone')
    email = user_data.get('email')
    city = user_data.get('city')
    pfp_src = user_data.get('pfp_src')
    # Get names of places user plans to visit
    visiting_list = user_data.get('visiting')
    # Get data from those place
    visiting_destinations = []
    if visiting_list:
        for i in visiting_list:
            place_data = mongo.db.destinations.find_one({'name': i})
            visiting_destinations.append(place_data)

    return render_template("profile.html", name = full_name, phone = phone, email = email, city = city, pfp_src = pfp_src, visiting_destinations = visiting_destinations)

@app.route('/destinations', methods = ['GET', 'POST'])
@is_verified
@is_logged_in
def destinations():
    destinations = mongo.db.destinations.find()
    if request.method == 'POST':
        app.logger.info(request.form['name'])
    return render_template('destinations.html', destinations = destinations)

@app.route('/add_user_to_destination', methods = ['POST'])
def add_user_to_destination():
    dest_name = request.form['name']
    username = session['username']
    mongo.db.destinations.update_one({'name': dest_name}, {'$addToSet': {'users': username}})
    mongo.db.user_info.update_one({'username': username}, {'$addToSet':{'visiting': dest_name}})
    flash('Added to Visiting', 'success')
    return redirect(url_for('index'))

#TODO: implement deleting users from destination
@app.route('/delete_user_from_destination', methods = ['POST'])
def delete_user_from_destination():
    dest_name = request.form['name']
    username = session['username']
    mongo.db.destinations.update_one({'name': dest_name}, {'$pull': {'users': username}})
    mongo.db.user_info.update_one({'username': username}, {'$pull':{'visiting': dest_name}})
    flash('Removed from Visiting', 'success')
    return redirect(url_for('index'))


@app.route('/add_destination', methods = ['GET', 'POST'])
@is_admin
def add_destination():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        #app.logger.info(description)

        image = request.files.get('image')
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(8))
        image_src = res + image.filename
        mongo.save_file(image_src, image)

        mongo.db.destinations.insert_one({'name': name, 'description': description, 'image_src': image_src})

    return render_template('add_destination.html')


@app.route('/search_destination', methods = ['GET', 'POST'])
@is_logged_in
@is_verified
def search_destination():
    if request.method == 'POST':
        # Create destination
        name = request.form.get('name')
        name_split = name.split(',')
        if name_split[0] == 'Unknown':
            name = name[8:]
        description = request.form.get('description')
        mongo.db.destinations.insert_one({'name': name, 'description': description})

        # Add user to destination
        username = session['username']
        mongo.db.destinations.update_one({'name': name}, {'$addToSet': {'users': username}})
        mongo.db.user_info.update_one({'username': username}, {'$addToSet':{'visiting': name}})
        flash('Added to Visiting', 'success')
        return redirect(url_for('index'))
        
    return render_template('search.html')

@app.route('/bookings')
@is_logged_in
@is_verified
def bookings():
    return render_template('bookings.html')


# Testing CKEditor
@app.route('/ckeditor', methods = ['GET', 'POST'])
def ckeditor():
    if request.method == 'POST':
        app.logger.info(request.form.get('description'))
    return render_template('CKEditorTest.html')


# Running the program
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug= True)