from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///all_blogs.db"

CORS(app) 
db = SQLAlchemy(app)

class autocar_india_blogs(db.Model):
    # this sequence should be according to the table
    Blog_ID = db.Column(db.Integer,primary_key=True)
    Blog_Website = db.Column(db.String())
    Title = db.Column(db.String())
    Description = db.Column(db.String())
    Published_Date = db.Column(db.String())
    Image_URL = db.Column(db.String())
    Blog_URL = db.Column(db.String())

class rushlane_blogs(db.Model):
    Blog_ID = db.Column(db.Integer,primary_key=True)
    Blog_Website = db.Column(db.String())
    Title = db.Column(db.String())
    Description = db.Column(db.String())
    Published_Date = db.Column(db.String())
    Image_URL = db.Column(db.String())
    Blog_URL = db.Column(db.String())

class indian_autos_blogs(db.Model):
    Blog_ID = db.Column(db.Integer,primary_key=True)
    Blog_Website = db.Column(db.String())
    Title = db.Column(db.String())
    Description = db.Column(db.String())
    Published_Date = db.Column(db.String())
    Image_URL = db.Column(db.String())
    Blog_URL = db.Column(db.String())

class autox_blogs(db.Model):
    Blog_ID = db.Column(db.Integer,primary_key=True)
    Blog_Website = db.Column(db.String())
    Title = db.Column(db.String())
    Description = db.Column(db.String())
    Published_Date = db.Column(db.String())
    Image_URL = db.Column(db.String())
    Blog_URL = db.Column(db.String())


def execute_query(query, params=(), fetch_one=False):
    # if we use SQLAlchemy directly then params should have key-value pairs
    result = None
    if fetch_one:
        result = db.session.execute(query,params).fetchone()
    else:
        result = db.session.execute(query,params).fetchall()

    return result

@app.route("/blogs", methods=["GET"])
def get_all_blogs():
    all_blogs = []
    
    table_names = ["rushlane_blogs","autocar_india_blogs", "indian_autos_blogs", "autox_blogs"]

    for table_name in table_names:
        query = f"SELECT * FROM {table_name} LIMIT 20"
        blogs = execute_query(query)
        
        if blogs:
            all_blogs.extend(blogs)
    # print(all_blogs)

    car_blogs_dict = [dict(blog) for blog in all_blogs]
    print(car_blogs_dict)
    car_blogs_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_blogs_dict]
    print(car_blogs_dict)
    # return jsonify({"blogs": all_blogs})
    # print(car_blogs_dict)
    # return jsonify(car_blogs_dict)
    last_10_blogs = car_blogs_dict[-19:-9]

    return jsonify({"all_blogs": car_blogs_dict, "last_10_blogs": last_10_blogs})

@app.route("/blogs/search", methods=["GET"])
def search_blogs():
    keyword = request.args.get("keyword")
    
    if not keyword:
        return jsonify({"message": "Please provide a 'keyword' parameter"}), 400

    all_searched_blogs = []

    table_names = ["rushlane_blogs","autocar_india_blogs", "indian_autos_blogs", "autox_blogs"]

    for table_name in table_names:
        query = f"SELECT * FROM {table_name} WHERE title LIKE '%{keyword}%' OR description LIKE '%{keyword}%' LIMIT 10"
        searched_blogs = execute_query(query)
        
        if searched_blogs:
            all_searched_blogs.extend(searched_blogs)
    
    car_blogs_dict = [dict(blog) for blog in all_searched_blogs]
    # print(car_blogs_dict)
    car_blogs_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_blogs_dict]
    # print(car_blogs_dict)
    
    # return jsonify({"blogs": all_blogs})
    return jsonify(car_blogs_dict)


if __name__ == "__main__":
    app.run(debug=True,port=12000)
