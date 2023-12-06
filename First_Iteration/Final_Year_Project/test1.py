import pandas as pd
from flask import jsonify

all_cars = pd.read_csv("spinny_separated.csv")

# selected_company = request.form['company']

# # Filter models based on the selected company
# filtered_models = all_cars[all_cars['company'] == selected_company]['model'].tolist()
filtered_models = all_cars['model'].tolist()



print((filtered_models))