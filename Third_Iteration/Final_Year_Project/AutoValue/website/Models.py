from . import db
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String()) 
    email = db.Column(db.String(),unique=True)
    password = db.Column(db.String())
    reset_token = db.Column(db.String(120), unique=True, nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    def generate_reset_token(self):
        # Generate a secure random token with 32 bytes
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiration = datetime.utcnow() + timedelta(minutes=1)
