from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///all_blogs.db"

CORS(app) 
db = SQLAlchemy(app)


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
   
    last_10_blogs = car_blogs_dict[-19:-9]

    return jsonify({"all_blogs": car_blogs_dict, "last_10_blogs": last_10_blogs})

@app.route("/blogs/search", methods=["GET"])
def search_blogs():
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
   
    last_10_blogs = car_blogs_dict[-19:-9]

    keyword = request.args.get("keyword")
    
    if not keyword:
        return jsonify({"message": "Please provide a 'keyword' parameter"}), 400
    
    # the above code is for featured blogs

    all_searched_blogs = []

    table_names = ["rushlane_blogs","autocar_india_blogs", "indian_autos_blogs", "autox_blogs"]

    for table_name in table_names:
        query = f"SELECT * FROM {table_name} WHERE title LIKE '%{keyword}%' OR description LIKE '%{keyword}%' LIMIT 100"
        searched_blogs = execute_query(query)
        
        if searched_blogs:
            all_searched_blogs.extend(searched_blogs)
    
    car_blogs_dict = [dict(blog) for blog in all_searched_blogs]
    # print(car_blogs_dict)
    car_blogs_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_blogs_dict]
    print(car_blogs_dict)
   
    print(last_10_blogs)
    return jsonify({"all_blogs": car_blogs_dict, "last_10_blogs": last_10_blogs})


if __name__ == "__main__":
    app.run(debug=True,port=12000)
