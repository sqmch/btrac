from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from basicconfig import config


# creating an instance of the flask app
app = Flask(__name__)
CORS(app, expose_headers="Authorization")

# configure db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config["SECRET_KEY"]
