from flask import Flask, render_template, flash, redirect, url_for, session,logging, request
from flask_pymongo import PyMongo
from werkzeug.local import F
from passlib.hash import sha256_crypt
from datetime import datetime

app = Flask(__name__)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug= True)