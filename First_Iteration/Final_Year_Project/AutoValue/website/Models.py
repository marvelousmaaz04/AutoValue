from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String()) 
    email = db.Column(db.String(),unique=True)
    password = db.Column(db.String())
