"""Resets sqlite db for trvcker"""
from models import db

db.create_all()
