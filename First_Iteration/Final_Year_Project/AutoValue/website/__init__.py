from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import hashlib
import os
from os import path

db = SQLAlchemy()
DB_NAME = "AutoValue.db"


def generate_secret_key(length=32):
    return secrets.token_hex(length // 2)

def hash_secret_key(secret_key):
    sha256 = hashlib.sha256()
    sha256.update(secret_key.encode('utf-8'))
    return sha256.hexdigest()


def create_app():
    app = Flask(__name__)
    secret_key = generate_secret_key()
    hashed_secret_key = hash_secret_key(secret_key)
    app.config["SECRET_KEY"] = hashed_secret_key

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .Views import views
    from .Authentication import auth

    print(os.getcwd())

    from .Car_Listings import spinny_routes # . is important since it signifies the current working directory because if we import create_app() in main the cwd will change
    from .Car_Listings import olx_routes
    from .Car_Listings import cars24_routes

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")

    app.register_blueprint(spinny_routes,url_prefix="/")
    app.register_blueprint(olx_routes,url_prefix="/")
    app.register_blueprint(cars24_routes,url_prefix="/")

    from .Models import User
    create_database(app)


    return app

def create_database(my_app):
    if not path.exists("website/"+DB_NAME):
        db.create_all(app=my_app)
        print("Database Created!")
