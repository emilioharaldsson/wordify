from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from flask_pymongo import PyMongo
import collections
collections.Iterable = collections.abc.Iterable


# Initiate App
app = Flask(__name__)
# app.config['MONGO_URI'] = MainConfig['MONGO_URI']

# Enable CORS
CORS(app)

# Bcrypt 
bcrypt = Bcrypt(app)

# Set-up MongoDB
# mongoDB_client = PyMongo(app)
# db = mongoDB_client.db

from app import endpoints