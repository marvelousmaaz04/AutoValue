from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all_olx_car_listings.db'  # Replace with your database name
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
class olx_mumbai(db.Model):
    # Define your table structure here
    __tablename__ = 'olx_mumbai'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class olx_delhi(db.Model):
    # Define your table structure here
    __tablename__ = 'olx_delhi'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class olx_hyderabad(db.Model):
    # Define your table structure here
    __tablename__ = 'olx_hyderabad'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class olx_bangalore(db.Model):
    # Define your table structure here
    __tablename__ = 'olx_bangalore'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class olx_pune(db.Model):
    # Define your table structure here
    __tablename__ = 'olx_pune'

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
@app.route('/api/olx_mumbai', methods=['GET'])
def get_table1():
    # data = olx_mumbai.query.all()
    
    limit = request.args.get('limit', default=10, type=int)
    # company = request.args.get('company')
    model = request.args.get('model')

    query = olx_mumbai.query
    if model:
        query = query.filter(olx_mumbai.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/olx_delhi', methods=['GET'])
def get_table2():
    # data = olx_delhi.query.all()

    limit = request.args.get('limit', default=10, type=int)
    # company = request.args.get('company')
    model = request.args.get('model')

    query = olx_delhi.query
    if model:
        query = query.filter(olx_delhi.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/olx_hyderabad', methods=['GET'])
def get_table3():
    # data = olx_hyderabad.query.all()

    limit = request.args.get('limit', default=10, type=int)
    # company = request.args.get('company')
    model = request.args.get('model')

    query = olx_hyderabad.query
    if model:
        query = query.filter(olx_hyderabad.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/olx_bangalore', methods=['GET'])
def get_table4():
    # data = olx_bangalore.query.all()

    limit = request.args.get('limit', default=10, type=int)
    # company = request.args.get('company')
    model = request.args.get('model')

    query = olx_bangalore.query
    if model:
        query = query.filter(olx_bangalore.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

@app.route('/api/olx_pune', methods=['GET'])
def get_table5():
    # data = olx_pune.query.all()

    limit = request.args.get('limit', default=10, type=int)
    # company = request.args.get('company')
    model = request.args.get('model')

    query = olx_pune.query
    if model:
        query = query.filter(olx_pune.CarName.ilike(f"%{model}%"))

    car_listings = query.all()

    
    car_listings_dict = [model_to_dict(car) for car in car_listings]
    return jsonify(car_listings_dict)

# Repeat the above code for the remaining tables (Table3, Table4, Table5)

if __name__ == '__main__':
    app.run(debug=True,port=9000)
