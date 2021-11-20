from flask import Flask, render_template, flash, redirect, url_for, session,logging, request
from flask_pymongo import PyMongo
from werkzeug.local import F
from passlib.hash import sha256_crypt
from datetime import datetime

# Configuration
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://Wahhaj:3DS8ai8B7j7f989@cluster0.4eydy.mongodb.net/users_devjams21?retryWrites=true&w=majority"
mongo = PyMongo(app)

# The home page
@app.route('/')
def home():
    return render_template("home.html")

# The sign up page
@app.route('/register')
def register():
    return render_template("signup.html")

# The login page
@app.route('/login')
def login():
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