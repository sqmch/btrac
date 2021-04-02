from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


def create_app():
    # creating an instance of the flask app
    app = Flask(__name__)

    # configure db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
