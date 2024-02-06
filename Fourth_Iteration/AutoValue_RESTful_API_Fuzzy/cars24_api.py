from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,func,and_,text
import re
from nltk import word_tokenize, WordNetLemmatizer

def normalize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    normalized = []
    for word in tokens:
        word = lemmatizer.lemmatize(word) 
        normalized.append(word)
    return " ".join(normalized)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all_cars24_car_listings.db'  # Replace with your database name
db = SQLAlchemy(app)

def model_to_dict(model_instance):
    """
    Convert an SQLAlchemy model instance to a Python dictionary.
    """
    result = {}
    for key, value in model_instance.__dict__.items():
        if not key.startswith("_"):
            result[key] = value
    return result

# Define data models as SQLAlchemy classes for each of the five tables
class cars24_mumbai(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_mumbai'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_newdelhi(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_newdelhi'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_hyderabad(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_hyderabad'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_bangalore(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_bangalore'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_pune(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_pune'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

# Define API endpoints to interact with each table
@app.route('/api/cars24_mumbai', methods=['GET'])
def get_table1():
    # data = cars24_mumbai.query.all()
    
    limit = request.args.get('limit', default=10, type=int)
    # company = request.args.get('company')
    model = request.args.get('model')

    normalized_text = normalize(model)
    print(normalized_text)
    query = cars24_mumbai.query
    model = re.sub('[^a-zA-Z0-9]+', ' ', model)
    print(model)
    if model:
        # Split the input model string into individual words
        model_words = model.split()
        print(model_words)
        if any(word.lower() == "suzuki" for word in model_words):
            # Filter based on the last word in the model string
            query = query.filter(cars24_mumbai.CarName.ilike(f"%{model_words[-1]}%"))
        else:
            # Ensure that there are at least two words in the model string
            query = query.filter(cars24_mumbai.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/cars24_newdelhi', methods=['GET'])
def get_table2():
    # data = cars24_delhi.query.all()

    limit = request.args.get('limit', default=10, type=int)
    
    model = request.args.get('model')

    query = cars24_newdelhi.query
    if model:
        query = query.filter(cars24_newdelhi.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/cars24_hyderabad', methods=['GET'])
def get_table3():
    # data = cars24_hyderabad.query.all()

    limit = request.args.get('limit', default=10, type=int)
    
    model = request.args.get('model')

    query = cars24_hyderabad.query
    if model:
        query = query.filter(cars24_hyderabad.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/cars24_bangalore', methods=['GET'])
def get_table4():
    # data = cars24_bangalore.query.all()

    limit = request.args.get('limit', default=10, type=int)
    
    model = request.args.get('model')

    query = cars24_bangalore.query
    if model:
        query = query.filter(cars24_bangalore.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/cars24_pune', methods=['GET'])
def get_table5():
    # data = cars24_pune.query.all()

    limit = request.args.get('limit', default=10, type=int)
    
    model = request.args.get('model')

    query = cars24_pune.query
    if model:
        query = query.filter(cars24_pune.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

# Repeat the above code for the remaining tables (Table3, Table4, Table5)

if __name__ == '__main__':
    app.run(debug=True,port=9500)
