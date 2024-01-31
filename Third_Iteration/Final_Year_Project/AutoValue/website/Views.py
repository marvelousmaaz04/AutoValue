from flask import Blueprint, render_template,request,flash,jsonify,redirect
import requests # for sending api calls
import sqlite3
import pandas as pd
import json
import pickle
import numpy as np
from flask_login import login_required,current_user

views = Blueprint("views",__name__)

car_locations = ["Mumbai", "Pune", "Delhi","Hyderabad","Bangalore", 'Any']
cleaned_car_data = pd.read_csv("Cleaned_Car_Data_model.csv")


@views.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")


@views.route("/landing-page",methods=["GET","POST"])
@login_required
def landing_page():

    all_cars = pd.read_csv("combined_unique_entries.csv")

    all_cars_sorted = all_cars.sort_values(by='Company')

    # Extract unique values after sorting
    companies = sorted(all_cars_sorted['Company'].unique())
    all_cars_sorted['CarName'] = all_cars_sorted['CarName'].fillna('').astype(str)

    # Extract unique values after sorting
    models = (all_cars_sorted['CarName'].unique())
    fuel_types = sorted(cleaned_car_data["Fuel Type"].unique())
    fuel_types.append('Any')
    print(fuel_types)

    print(companies)
    print(models)
    api_url_spinny = "http://127.0.0.1:8000/api/spinny_any"
    api_url_olx = "http://127.0.0.1:9000/api/olx_any"
    api_url_cars24 = "http://127.0.0.1:9500/api/cars24_any"

    def landing_page_cars(params_1, params_2=None, params_3=None):
        all_response = []
        if params_1:
            response_spinny = requests.get(api_url_spinny, params=params_1)
            if response_spinny.status_code == 200:
                spinny_data = response_spinny.json()
                print("Received spinny response")
                for jsonobj in response_spinny.json():
                    all_response.append(jsonobj)
        if params_2:
            response_cars24 = requests.get(api_url_cars24, params=params_2)
            if response_cars24.status_code == 200:
                cars24_data = response_cars24.json()
                print("Received cars24 response")
            
                for jsonobj in response_cars24.json():
                    all_response.append(jsonobj)

        if params_3:
            response_olx = requests.get(api_url_olx, params=params_3)
            if response_olx.status_code == 200:
                olx_data = response_olx.json()
                print("Received olx response")
                for jsonobj in response_olx.json():
                    all_response.append(jsonobj)

        
        
        print(all_response)
        car_listings_dict = [dict(car) for car in all_response]
        print(car_listings_dict)
        car_listings_dict = [{key.lower(): value for key, value in dictionary.items()} for dictionary in car_listings_dict]
        print(car_listings_dict)
        print(jsonify(car_listings_dict))
        return car_listings_dict
        
    params_1 = {'limit': '2','company':'maruti','model':'suzuki','fuel-type':'any','kms-driven':'1000','year':'2010'}
    params_2 = {'limit': '2','company':'honda','model':'amaze','fuel-type':'any','kms-driven':'2000','year':'2010'}
    params_3 = {'limit': '2','company':'tata','model':'harrier','fuel-type':'any','kms-driven':'3000','year':'2010'}

    popular_car_listings_dict = landing_page_cars(params_1,params_2,None)

    params_1 = {'limit': '2','company':'maruti','fuel-type':'any','kms-driven':'1000','year':'2010'}
    

    spinny_featured_car_listings_dict = landing_page_cars(params_1,None,None)

    # params_2 = {'limit': '2','company':'honda','model':'amaze','fuel-type':'any','kms-driven':'2000','year':'2010'}
    params_2 = {'limit': '2','company':'honda','fuel-type':'any','kms-driven':'2000','year':'2010'}
    params_3 = {'limit': '2','company':'tata','model':'harrier','fuel-type':'any','kms-driven':'3000','year':'2010'}

    cars24_featured_car_listings_dict = landing_page_cars(None,params_2,None)
    

    return render_template('landing_page.html', companies=companies,locations=car_locations,fuel_types=fuel_types,popular_cars=popular_car_listings_dict,spinny_featured_cars=spinny_featured_car_listings_dict,cars24_featured_cars=cars24_featured_car_listings_dict)
    # return render_template("home.html",companies=car_companies,models=car_models,locations=car_locations)

# All Car Blog routes
@views.route("/home/car-blogs", methods=["GET","POST"])
def car_blogs():
    if request.method == "GET":
        response = requests.get("http://127.0.0.1:12000/blogs")
        # print(response.json())
        all_blogs = response.json()
        return render_template("car_blogs.html",all_blogs=all_blogs)
    elif request.method == "POST":
        keyword = request.form.get("search-input")
        # params = {'keyword':keyword}
        response = requests.get(f"http://127.0.0.1:12000/blogs/search?keyword={keyword}")
        print(response.json())
        all_blogs = response.json()
        return render_template("car_blogs.html",all_blogs=all_blogs)

# All Price Prediction routes

pipe = pickle.load(open('GRDBOOSTModel.pkl','rb'))

@views.route("/home/predict-price", methods=["GET"])
def price_prediction_page():
    company_names = sorted(cleaned_car_data["CompanyName"].unique())
    model_names = sorted(cleaned_car_data["ModelName"].unique())
    fuel_types = sorted(cleaned_car_data["Fuel Type"].unique())
    locations = sorted(cleaned_car_data["Location"].unique())
    return render_template("price_prediction.html", company_names=company_names, model_names=model_names, fuel_types=fuel_types, locations=locations)

@views.route("/home/get-car-models-prediction-page", methods=["POST"])
def get_car_models_for_prediction_page():
    cleaned_car_data = pd.read_csv("Cleaned_Car_Data_model.csv")

    data = json.loads(request.data)
    selected_company = data["company"]

    print(selected_company)
    # Filter models based on the selected company
    filtered_models = cleaned_car_data[cleaned_car_data['CompanyName'] == selected_company]['ModelName'].unique().tolist()
    # print(filtered_models)
    print((filtered_models))
    filtered_models = {"models":filtered_models}
    print((filtered_models))
    return jsonify(filtered_models)


@views.route("/home/get-price-prediction",methods=["POST"])
def get_car_price_prediction():
    company = request.form.get("company")
    model = request.form.get("model")
    kms_driven = request.form.get("kms-driven")
    fuel_type = request.form.get("fuel-type")
    year = int(request.form.get("year"))
    location = request.form.get("location")

    print(company, model, kms_driven, fuel_type, location)

    input = pd.DataFrame([[fuel_type, location, company, model, year, kms_driven]],columns=["Fuel Type", "Location", "CompanyName", "ModelName", "Year", "KilometersDriven"]) # the column should be the same as that of data used to train the model

    prediction = np.exp(pipe.predict(input)[0])
    prediction = int(prediction)
    print(prediction)

    return str(prediction)


# All Car Listing Routes

@views.route("/home/get-car-models",methods=["POST"])
def get_car_models():
    # combined_unique_entries.csv contains all models. it is made from cars24 data
    all_cars = pd.read_csv("combined_unique_entries.csv")

    data = json.loads(request.data)
    selected_company = data["company"]

    print(selected_company)
    # Filter models based on the selected company
    filtered_models = all_cars.loc[all_cars['Company'] == selected_company, 'CarName'].dropna().unique()
    filtered_models = filtered_models.tolist()
    print((filtered_models))
    filtered_models = {"models":filtered_models}
    print((filtered_models))
    return jsonify(filtered_models)


@views.route("/get-car-listings",methods=["POST"])
def get_car_listings():
    if request.method == "POST":
        car_company = request.form.get("select-company")
        car_model = request.form.get("select-model")
        car_kms_driven = request.form.get("kms-driven")
        car_location = request.form.get("select-location").strip().lower()
        car_fuel_type = request.form.get("select-fuel-type").strip().lower()
        car_year = request.form.get("year")

        print(car_company)
        print(car_model)
        print(car_kms_driven)
        print(car_location)
        print(type(car_location))
        print(car_fuel_type)
        print(car_year)

        
        api_url_spinny = ""
        api_url_olx = ""
        api_url_cars24 = ""

        if car_location == "mumbai":
            api_url_spinny = "http://127.0.0.1:8000/api/spinny_mumbai"
            api_url_olx = "http://127.0.0.1:9000/api/olx_mumbai"
            api_url_cars24 = "http://127.0.0.1:9500/api/cars24_mumbai"
            print("Request sent to Mumbai APIs")
        elif car_location == "delhi":
            api_url_spinny = "http://127.0.0.1:8000/api/spinny_delhi"
            api_url_olx = "http://127.0.0.1:9000/api/olx_delhi"
            api_url_cars24 = "http://127.0.0.1:9500/api/cars24_newdelhi"
            print("Request sent to Delhi APIs")
        elif car_location == "pune":
            api_url_spinny = "http://127.0.0.1:8000/api/spinny_pune"
            api_url_olx = "http://127.0.0.1:9000/api/olx_pune"
            api_url_cars24 = "http://127.0.0.1:9500/api/cars24_pune"
            print("Request sent to Pune APIs")
        elif car_location == "hyderabad":
            api_url_spinny = "http://127.0.0.1:8000/api/spinny_hyderabad"
            api_url_olx = "http://127.0.0.1:9000/api/olx_hyderabad"
            api_url_cars24 = "http://127.0.0.1:9500/api/cars24_hyderabad"
            print("Request sent to Hyderabad APIs")
        elif car_location == "bangalore":
            api_url_spinny = "http://127.0.0.1:8000/api/spinny_bangalore"
            api_url_olx = "http://127.0.0.1:9000/api/olx_bangalore"
            api_url_cars24 = "http://127.0.0.1:9500/api/cars24_bangalore"
            print("Request sent to Bangalore APIs")
        elif car_location == "any":
            api_url_spinny = "http://127.0.0.1:8000/api/spinny_any"
            api_url_olx = "http://127.0.0.1:9000/api/olx_any"
            api_url_cars24 = "http://127.0.0.1:9500/api/cars24_any"
        
        
        params = {'limit': '100','company':car_company,'model':car_model,'fuel-type':car_fuel_type,'location':car_location,'year':car_year,'kms-driven':car_kms_driven}

        response_spinny = requests.get(api_url_spinny, params=params)
        response_olx = requests.get(api_url_olx, params=params)
        response_cars24 = requests.get(api_url_cars24, params=params)

        all_car_listings = []

        spinny_data = ""
        olx_data = ""
        cars24_data = ""

        if response_spinny.status_code == 200:
            spinny_data = response_spinny.json()
            print("Received spinny response")
        
        
        if response_olx.status_code == 200:
            olx_data = response_olx.json()
            print("Received olx response")
        
        
        
        if response_cars24.status_code == 200:
            cars24_data = response_cars24.json()
            print("Received cars24 response")
            
        return render_template("car_listings.html",spinny_data=spinny_data,olx_data=olx_data,cars24_data=cars24_data)


        
