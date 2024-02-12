from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
# from whooshalchemy import IndexService,Searcher,whoosh
from unidecode import unidecode
import string
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all_spinny_car_listings_fuzzy.db'  # Replace with your database name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True


def preprocess_query(query):
    # Remove punctuation
    print("Before processing", query)
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    query = query.translate(translator)
    
    # Handle diacritics
    query = unidecode(query)
    # query= query.split(" ")
    # query = query[0:2]
    # processed_query = '-'.join(query)
    
    processed_query = (query)
    print("After processing", processed_query)
    
    return processed_query
    


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
class spinny_mumbai_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'spinny_mumbai_fts'
    __searchable__ = ['CarName']

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingUrl = db.Column(db.String())
    ImageUrl = db.Column(db.String())

class spinny_delhi_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'spinny_delhi_fts'
    __searchable__ = ['CarName']

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingUrl = db.Column(db.String())
    ImageUrl = db.Column(db.String())

class spinny_hyderabad_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'spinny_hyderabad_fts'
    __searchable__ = ['CarName']

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingUrl = db.Column(db.String())
    ImageUrl = db.Column(db.String())

class spinny_bangalore_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'spinny_bangalore_fts'
    __searchable__ = ['CarName']

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingUrl = db.Column(db.String())
    ImageUrl = db.Column(db.String())

class spinny_pune_fts(db.Model):
    # Define your table structure here
    __tablename__ = 'spinny_pune_fts'
    __searchable__ = ['CarName']

    ListingID = db.Column(db.Integer, primary_key=True)
    CarName = db.Column(db.String())
    Price = db.Column(db.Float)
    Year = db.Column(db.Integer)
    KilometersDriven = db.Column(db.Integer)
    FuelType = db.Column(db.String())
    Location = db.Column(db.String())
    ListingUrl = db.Column(db.String())
    ImageUrl = db.Column(db.String())

# Define API endpoints to interact with each table
@app.route('/api/spinny_any', methods=['GET'])
def get_all_tables():
    limit = request.args.get('limit')
    company = request.args.get('company')
    model = request.args.get('model')
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    params = {'limit': limit,'company':company,'model':model,'fuel-type':fuel_type,'location':location,'year':year,'kms-driven':kms_driven}
    print(params)

    mumbai_url = "http://127.0.0.1:8000/api/spinny_mumbai"
    response_mumbai = requests.get(mumbai_url, params=params)

    pune_url = "http://127.0.0.1:8000/api/spinny_pune"

    response_pune = requests.get(pune_url, params=params)

    hyderabad_url = "http://127.0.0.1:8000/api/spinny_hyderabad"
    response_hyderabad = requests.get(hyderabad_url, params=params)

    bangalore_url = "http://127.0.0.1:8000/api/spinny_bangalore"
    response_bangalore = requests.get(bangalore_url, params=params)

    delhi_url = "http://127.0.0.1:8000/api/spinny_delhi"
    response_delhi = requests.get(delhi_url, params=params)
    print(response_mumbai.json())

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
    for jsonobj in response_delhi.json():
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
@app.route('/api/spinny_mumbai', methods=['GET'])
def get_table1():
    # data = spinny_mumbai.query.all()
    
    limit = request.args.get('limit', default=10, type=int)
    company = request.args.get('company')
    model = request.args.get('model')
    if model:
        model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    print(model)
    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM spinny_mumbai_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = {}
    

    # Step 0 match company
    if company:
        search_terms = company.split(" ")
        # query += ' AND '.join(['CarName MATCH :company_term{}'.format(i) for i in range(len(search_terms))])
        company_query = 'CarName MATCH :company_term '
        # Bind all the parameters to the query
        # company_params = {'company_term{}'.format(i): term for i, term in enumerate(search_terms)}
        company_params = {'company_term': ' '.join(search_terms)}
        params.update(company_params)
        query += company_query
        print("Step 0 Query:", query)
        print("Step 0 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 0 Results:", results)
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        print(search_terms)
        model_query = 'AND ' +' AND '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])

        # Bind all the parameters to the query
        model_params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        params.update(model_params)
        query += model_query
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)
        print("*" * 10)
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
    #     else:

    #         query += ' AND Location MATCH :location'
    #         print("Step 3 Query:", query)

    #         # Bind all the parameters to the query
    #         location_params = {'location': location}
    #         params.update(location_params)
    #         print("Step 3 Params:", params)
    #         results = db.session.execute(query, params).fetchall()
    #         print("Step 3 Results:", results)
    #         print("*"*10)
    #         print()
    #         print()
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
    

    # Apply LIMIT to the query based on the 'limit' parameter
    query += ' LIMIT :limit'

    # Add the 'limit' parameter to the params dictionary
    limit_param = {'limit': limit}
    params.update(limit_param)

    # Execute the final query
    results = db.session.execute(query, params).fetchall()
    print("Final Query:", query)
    print("Final Params:", params)
    print("Final Results:", results)
    # car_listings_dict = [model_to_dict(car) for car in car_listings]
    # return jsonify(car_listings_dict)
    car_listings = results
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/spinny_delhi', methods=['GET'])
def get_table2():
    # data = spinny_delhi.query.all()

    limit = request.args.get('limit', default=10, type=int)
    company = request.args.get('company')
    model = request.args.get('model')
    if model:
        model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    print(model)
    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM spinny_delhi_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = {}

    # Step 0 match company
    if company:
        search_terms = company.split(" ")
        # query += ' AND '.join(['CarName MATCH :company_term{}'.format(i) for i in range(len(search_terms))])
        company_query = 'CarName MATCH :company_term '
        # Bind all the parameters to the query
        # company_params = {'company_term{}'.format(i): term for i, term in enumerate(search_terms)}
        company_params = {'company_term': ' '.join(search_terms)}
        params.update(company_params)
        query += company_query
        print("Step 0 Query:", query)
        print("Step 0 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 0 Results:", results)
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        model_query = 'AND ' +' AND '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])

        # Bind all the parameters to the query
        model_params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        params.update(model_params)
        query += model_query
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)
        print("*" * 10)
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
        # else:

        #     query += ' AND Location MATCH :location'
        #     print("Step 3 Query:", query)

        #     # Bind all the parameters to the query
        #     location_params = {'location': location}
        #     params.update(location_params)
        #     print("Step 3 Params:", params)
        #     results = db.session.execute(query, params).fetchall()
        #     print("Step 3 Results:", results)
        #     print("*"*10)
        #     print()
        #     print()

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

    query += ' LIMIT :limit'

    # Add the 'limit' parameter to the params dictionary
    limit_param = {'limit': limit}
    params.update(limit_param)

    # Execute the final query
    results = db.session.execute(query, params).fetchall()
    print("Final Query:", query)
    print("Final Params:", params)
    print("Final Results:", results)
    car_listings = results

    
    # car_listings_dict = [model_to_dict(car) for car in car_listings]
    # return jsonify(car_listings_dict)
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/spinny_hyderabad', methods=['GET'])
def get_table3():
    # data = spinny_delhi.query.all()

    limit = request.args.get('limit', default=10, type=int)
    company = request.args.get('company')
    model = request.args.get('model')
    if model:
        model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    print(model)
    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM spinny_hyderabad_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = {}
    # Step 0 match company
    if company:
        search_terms = company.split(" ")
        # query += ' AND '.join(['CarName MATCH :company_term{}'.format(i) for i in range(len(search_terms))])
        company_query = 'CarName MATCH :company_term '
        # Bind all the parameters to the query
        # company_params = {'company_term{}'.format(i): term for i, term in enumerate(search_terms)}
        company_params = {'company_term': ' '.join(search_terms)}
        params.update(company_params)
        query += company_query
        print("Step 0 Query:", query)
        print("Step 0 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 0 Results:", results)
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        model_query = 'AND ' +' AND '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])

        # Bind all the parameters to the query
        model_params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        params.update(model_params)
        query += model_query
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)
        print("*" * 10)
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
        # else:

        #     query += ' AND Location MATCH :location'
        #     print("Step 3 Query:", query)

        #     # Bind all the parameters to the query
        #     location_params = {'location': location}
        #     params.update(location_params)
        #     print("Step 3 Params:", params)
        #     results = db.session.execute(query, params).fetchall()
        #     print("Step 3 Results:", results)
        #     print("*"*10)
        #     print()
        #     print()

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
    
    query += ' LIMIT :limit'

    # Add the 'limit' parameter to the params dictionary
    limit_param = {'limit': limit}
    params.update(limit_param)

    # Execute the final query
    results = db.session.execute(query, params).fetchall()
    print("Final Query:", query)
    print("Final Params:", params)
    print("Final Results:", results)
    car_listings = results

    
    # car_listings_dict = [model_to_dict(car) for car in car_listings]
    # return jsonify(car_listings_dict)
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/spinny_bangalore', methods=['GET'])
def get_table4():
    # data = spinny_bangalore.query.all()

    limit = request.args.get('limit', default=10, type=int)
    company = request.args.get('company')
    model = request.args.get('model')
    if model:
        model = preprocess_query(model)
   
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    print(model)
    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM spinny_bangalore_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = {}
    # Step 0 match company
    if company:
        search_terms = company.split(" ")
        # query += ' AND '.join(['CarName MATCH :company_term{}'.format(i) for i in range(len(search_terms))])
        company_query = 'CarName MATCH :company_term '
        # Bind all the parameters to the query
        # company_params = {'company_term{}'.format(i): term for i, term in enumerate(search_terms)}
        company_params = {'company_term': ' '.join(search_terms)}
        params.update(company_params)
        query += company_query
        print("Step 0 Query:", query)
        print("Step 0 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 0 Results:", results)
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        model_query = 'AND ' +' AND '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])

        # Bind all the parameters to the query
        model_params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        params.update(model_params)
        query += model_query
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)
        print("*" * 10)
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
        # else:

        #     query += ' AND Location MATCH :location'
        #     print("Step 3 Query:", query)

        #     # Bind all the parameters to the query
        #     location_params = {'location': location}
        #     params.update(location_params)
        #     print("Step 3 Params:", params)
        #     results = db.session.execute(query, params).fetchall()
        #     print("Step 3 Results:", results)
        #     print("*"*10)
        #     print()
        #     print()

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

    query += ' LIMIT :limit'

    # Add the 'limit' parameter to the params dictionary
    limit_param = {'limit': limit}
    params.update(limit_param)

    # Execute the final query
    results = db.session.execute(query, params).fetchall()
    print("Final Query:", query)
    print("Final Params:", params)
    print("Final Results:", results)
    car_listings = results

    
    # car_listings_dict = [model_to_dict(car) for car in car_listings]
    # return jsonify(car_listings_dict)
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)

@app.route('/api/spinny_pune', methods=['GET'])
def get_table5():
    # data = spinny_pune.query.all()

    limit = request.args.get('limit', default=10, type=int)
    company = request.args.get('company')
    model = request.args.get('model')
    if model:
        model = preprocess_query(model)
    fuel_type = request.args.get('fuel-type')
    location = request.args.get('location')
    year = int(request.args.get('year'))
    kms_driven = float(request.args.get('kms-driven'))
    print(model)
    print(fuel_type, location, year, kms_driven)
    query = 'SELECT * FROM spinny_pune_fts WHERE '  # Placeholder condition that is always true
    results = ""
    params = {}
    # Step 0 match company
    if company:
        search_terms = company.split(" ")
        # query += ' AND '.join(['CarName MATCH :company_term{}'.format(i) for i in range(len(search_terms))])
        company_query = 'CarName MATCH :company_term '
        # Bind all the parameters to the query
        # company_params = {'company_term{}'.format(i): term for i, term in enumerate(search_terms)}
        company_params = {'company_term': ' '.join(search_terms)}
        params.update(company_params)
        query += company_query
        print("Step 0 Query:", query)
        print("Step 0 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 0 Results:", results)
    # Step 1: Match CarName
    if model:
        search_terms = model.split(" ")
        model_query = 'AND ' +' AND '.join(['CarName MATCH :term{}'.format(i) for i in range(len(search_terms))])

        # Bind all the parameters to the query
        model_params = {'term{}'.format(i): search_terms[i] for i in range(len(search_terms))}
        params.update(model_params)
        query += model_query
        print("Step 1 Query:", query)
        print("Step 1 Params:", params)
        results = db.session.execute(query, params).fetchall()
        print("Step 1 Results:", results)
        print("*" * 10)
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
        # else:

        #     query += ' AND Location MATCH :location'
        #     print("Step 3 Query:", query)

        #     # Bind all the parameters to the query
        #     location_params = {'location': location}
        #     params.update(location_params)
        #     print("Step 3 Params:", params)
        #     results = db.session.execute(query, params).fetchall()
        #     print("Step 3 Results:", results)
        #     print("*"*10)
        #     print()
        #     print()
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
    
    query += ' LIMIT :limit'

    # Add the 'limit' parameter to the params dictionary
    limit_param = {'limit': limit}
    params.update(limit_param)

    # Execute the final query
    results = db.session.execute(query, params).fetchall()
    print("Final Query:", query)
    print("Final Params:", params)
    print("Final Results:", results)
    car_listings = results

    
    # car_listings_dict = [model_to_dict(car) for car in car_listings]
    # return jsonify(car_listings_dict)
    car_listings_dict = [dict(car) for car in car_listings]
    print(car_listings_dict)
    car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
    print(car_listings_dict)
    return jsonify(car_listings_dict)



if __name__ == '__main__':
    app.run(debug=True,port=8000)
