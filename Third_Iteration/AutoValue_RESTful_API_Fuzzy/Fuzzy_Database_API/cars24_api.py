from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,func,and_,text
from sqlalchemy.sql import text
from unidecode import unidecode
import string
from sqlalchemy.orm import aliased
import requests



def preprocess_query(query):
    # Remove punctuation
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    query = query.translate(translator)
    
    # Handle diacritics
    query = unidecode(query)
    
    return query


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all_cars24_car_listings_fuzzy.db'  # Replace with your database name
db = SQLAlchemy(app)


# Define data models as SQLAlchemy classes for each of the five tables
class cars24_mumbai_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_mumbai_fts'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_newdelhi_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_newdelhi_fts'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_hyderabad_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_hyderabad_fts'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_bangalore_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_bangalore_fts'

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingURL = db.Column(db.String())
    ImageURL = db.Column(db.String())

class cars24_pune_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'cars24_pune_fts'

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
@app.route('/api/cars24_any', methods=['GET'])
def get_all_tables():
    model = request.args.get('model')
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    params = {'limit': '100','model':model,'fuel-type':fuel_type,'location':location,'year':year,'kms-driven':kms_driven}
    print(params)

    mumbai_url = "http://127.0.0.1:9500/api/cars24_mumbai"
    response_mumbai = requests.get(mumbai_url, params=params)

    pune_url = "http://127.0.0.1:9500/api/cars24_pune"

    response_pune = requests.get(pune_url, params=params)

    hyderabad_url = "http://127.0.0.1:9500/api/cars24_hyderabad"
    response_hyderabad = requests.get(hyderabad_url, params=params)

    bangalore_url = "http://127.0.0.1:9500/api/cars24_bangalore"
    response_bangalore = requests.get(bangalore_url, params=params)

    newdelhi_url = "http://127.0.0.1:9500/api/cars24_newdelhi"
    response_newdelhi = requests.get(newdelhi_url, params=params)

    print()
    print()
    print()

    all_response = []
    for jsonobj in response_mumbai.json():
        all_response.append(jsonobj)
    for jsonobj in response_bangalore.json():
        all_response.append(jsonobj)
    for jsonobj in response_pune.json():
        all_response.append(jsonobj)
    for jsonobj in response_newdelhi.json():
        all_response.append(jsonobj)
    for jsonobj in response_hyderabad.json():
        all_response.append(jsonobj)
    
    print(all_response)
    car_listings_dict = [dict(car) for car in all_response]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)


    


# Define API endpoints to interact with each table
@app.route('/api/cars24_mumbai', methods=['GET'])
def get_table1():
    # data = cars24_mumbai.query.all()
    
    limit = request.args.get('limit', default=10, type=int)
    model = request.args.get('model')
    model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))

    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM cars24_mumbai_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = ""
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        query += ' OR '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])
        

        # Bind all the parameters to the query
        params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)
        print("*"*10)
        print()
        print()

    # Step 2: Filter by FuelType
    if fuel_type:
        if fuel_type == "any":
            query += '' # no filtering needed
            print("Step 2 Query:", query)

            # Bind all the parameters to the query

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        else:
            query += ' AND FuelType MATCH :fuel_type'
            print("Step 2 Query:", query)

            # Bind all the parameters to the query
            fuel_type_params = {'fuel_type': fuel_type}

            # Add the fuel_type parameters to the existing params dictionary
            params.update(fuel_type_params)
            print("Step 2 Params:", params)

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        print("*"*10)
        print()
        print()


    # Step 3: Filter by Location
    if location:
        if location == "any":
            query += '' # no filtering needed
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()
        else:

            query += ' AND Location MATCH :location'
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()


    # Step 4: Filter by Year
    if year:
        query += ' AND Year >= :year'
        print("Step 4 Query:", query)

        # Bind all the parameters to the query
        year_params = {'year': year}
        params.update(year_params)
        print("Step 4 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 4 Results:", results)
        print("*"*10)
        print()
        print()


    # Step 5: Filter by KilometersDriven
    if kms_driven:
        query += ' AND KilometersDriven >= :kms_driven'
        print("Step 5 Query:", query)

        # Bind all the parameters to the query
        kms_driven_params = {'kms_driven': kms_driven}
        params.update(kms_driven_params)
        print("Step 5 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 5 Results:", results)
        print("*"*10)
        print()
        print()

    car_listings = results

    
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)


@app.route('/api/cars24_newdelhi', methods=['GET'])
def get_table2():
    # data = cars24_delhi.query.all()

    limit = request.args.get('limit', default=10, type=int)
    model = request.args.get('model')
    model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))

    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM cars24_newdelhi_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = ""
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        query += ' OR '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])
        

        # Bind all the parameters to the query
        params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)

    # Step 2: Filter by FuelType
    if fuel_type:
        if fuel_type == "any":
            query += '' # no filtering needed
            print("Step 2 Query:", query)

            # Bind all the parameters to the query

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        else:
            query += ' AND FuelType MATCH :fuel_type'
            print("Step 2 Query:", query)

            # Bind all the parameters to the query
            fuel_type_params = {'fuel_type': fuel_type}

            # Add the fuel_type parameters to the existing params dictionary
            params.update(fuel_type_params)
            print("Step 2 Params:", params)

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        print("*"*10)
        print()
        print()

    # Step 3: Filter by Location
    if location:
        if location == "any":
            query += '' # no filtering needed
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()
        else:

            query += ' AND Location MATCH :location'
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()

    # Step 4: Filter by Year
    if year:
        query += ' AND Year >= :year'
        print("Step 4 Query:", query)

        # Bind all the parameters to the query
        year_params = {'year': year}
        params.update(year_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 4 Results:", results)

    # Step 5: Filter by KilometersDriven
    if kms_driven:
        query += ' AND KilometersDriven >= :kms_driven'
        print("Step 5 Query:", query)

        # Bind all the parameters to the query
        kms_driven_params = {'kms_driven': kms_driven}
        params.update(kms_driven_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 5 Results:", results)
    car_listings = results

    
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/cars24_hyderabad', methods=['GET'])
def get_table3():
    # data = cars24_hyderabad.query.all()

    limit = request.args.get('limit', default=10, type=int)
    model = request.args.get('model')
    model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))

    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM cars24_hyderabad_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = ""
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        query += ' OR '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])
        

        # Bind all the parameters to the query
        params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)

    # Step 2: Filter by FuelType
    if fuel_type:
        if fuel_type == "any":
            query += '' # no filtering needed
            print("Step 2 Query:", query)

            # Bind all the parameters to the query

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        else:
            query += ' AND FuelType MATCH :fuel_type'
            print("Step 2 Query:", query)

            # Bind all the parameters to the query
            fuel_type_params = {'fuel_type': fuel_type}

            # Add the fuel_type parameters to the existing params dictionary
            params.update(fuel_type_params)
            print("Step 2 Params:", params)

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        print("*"*10)
        print()
        print()

    # Step 3: Filter by Location
    if location:
        if location == "any":
            query += '' # no filtering needed
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()
        else:

            query += ' AND Location MATCH :location'
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()

    # Step 4: Filter by Year
    if year:
        query += ' AND Year >= :year'
        print("Step 4 Query:", query)

        # Bind all the parameters to the query
        year_params = {'year': year}
        params.update(year_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 4 Results:", results)

    # Step 5: Filter by KilometersDriven
    if kms_driven:
        query += ' AND KilometersDriven >= :kms_driven'
        print("Step 5 Query:", query)

        # Bind all the parameters to the query
        kms_driven_params = {'kms_driven': kms_driven}
        params.update(kms_driven_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 5 Results:", results)
    car_listings = results

    
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/cars24_bangalore', methods=['GET'])
def get_table4():
    # data = cars24_bangalore.query.all()

    limit = request.args.get('limit', default=10, type=int)
    model = request.args.get('model')
    model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))

    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM cars24_bangalore_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = ""
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        query += ' OR '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])
        

        # Bind all the parameters to the query
        params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)

    # Step 2: Filter by FuelType
    if fuel_type:
        if fuel_type == "any":
            query += '' # no filtering needed
            print("Step 2 Query:", query)

            # Bind all the parameters to the query

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        else:
            query += ' AND FuelType MATCH :fuel_type'
            print("Step 2 Query:", query)

            # Bind all the parameters to the query
            fuel_type_params = {'fuel_type': fuel_type}

            # Add the fuel_type parameters to the existing params dictionary
            params.update(fuel_type_params)
            print("Step 2 Params:", params)

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        print("*"*10)
        print()
        print()

    # Step 3: Filter by Location
    if location:
        if location == "any":
            query += '' # no filtering needed
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()
        else:

            query += ' AND Location MATCH :location'
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()

    # Step 4: Filter by Year
    if year:
        query += ' AND Year >= :year'
        print("Step 4 Query:", query)

        # Bind all the parameters to the query
        year_params = {'year': year}
        params.update(year_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 4 Results:", results)

    # Step 5: Filter by KilometersDriven
    if kms_driven:
        query += ' AND KilometersDriven >= :kms_driven'
        print("Step 5 Query:", query)

        # Bind all the parameters to the query
        kms_driven_params = {'kms_driven': kms_driven}
        params.update(kms_driven_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 5 Results:", results)
    car_listings = results

    
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/cars24_pune', methods=['GET'])
def get_table5():
    # data = cars24_pune.query.all()

    limit = request.args.get('limit', default=10, type=int)
    model = request.args.get('model')
    model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))

    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM cars24_pune_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = ""
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        query += ' OR '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])
        

        # Bind all the parameters to the query
        params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)

    # Step 2: Filter by FuelType
    if fuel_type:
        if fuel_type == "any":
            query += '' # no filtering needed
            print("Step 2 Query:", query)

            # Bind all the parameters to the query

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        else:
            query += ' AND FuelType MATCH :fuel_type'
            print("Step 2 Query:", query)

            # Bind all the parameters to the query
            fuel_type_params = {'fuel_type': fuel_type}

            # Add the fuel_type parameters to the existing params dictionary
            params.update(fuel_type_params)
            print("Step 2 Params:", params)

            results = db.session.execute(query, params).fetchall()
            print("Step 2 Results:", results)
        print("*"*10)
        print()
        print()

    # Step 3: Filter by Location
    if location:
        if location == "any":
            query += '' # no filtering needed
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()
        else:

            query += ' AND Location MATCH :location'
            print("Step 3 Query:", query)

            # Bind all the parameters to the query
            location_params = {'location': location}
            params.update(location_params)
            print("Step 3 Params:", params)
            results = db.session.execute(query, params).fetchall()
            print("Step 3 Results:", results)
            print("*"*10)
            print()
            print()

    # Step 4: Filter by Year
    if year:
        query += ' AND Year >= :year'
        print("Step 4 Query:", query)

        # Bind all the parameters to the query
        year_params = {'year': year}
        params.update(year_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 4 Results:", results)

    # Step 5: Filter by KilometersDriven
    if kms_driven:
        query += ' AND KilometersDriven >= :kms_driven'
        print("Step 5 Query:", query)

        # Bind all the parameters to the query
        kms_driven_params = {'kms_driven': kms_driven}
        params.update(kms_driven_params)
        results = db.session.execute(query, params).fetchall()
        print("Step 5 Results:", results)
    car_listings = results

    
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

# Repeat the above code for the remaining tables (Table3, Table4, Table5)

if __name__ == '__main__':
    app.run(debug=True,port=9500)
