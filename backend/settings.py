from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# creating an instance of the flask app
app = Flask(__name__)
CORS(app)

# configure db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SECRET_KEY"
] = "\x80\xfbu\xa5U\xed4k\x98\x94m\x93\x14s:\xb6\x85\xce@/\xdc\xcb\xa3\xd1"
