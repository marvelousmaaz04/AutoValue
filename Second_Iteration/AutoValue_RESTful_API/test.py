from fuzzywuzzy import fuzz

# Example car names with slight variations
car_names = [
    "Maruti Suzuki S-Cross Zeta",
    "Maruti Suzuki S-Cross",
    "Maruti S Cross"
]

# Define a reference car name (you can choose any from the list)
reference_car_name = "Maruti Suzuki S-Cross Zeta"

# Set a threshold for similarity
threshold = 70  # You can adjust this based on your requirements

# Use fuzzy matching to find similar car names
similar_car_names = [name for name in car_names if fuzz.ratio(reference_car_name, name) >= threshold]

# Print the results
print("Reference Car Name:", reference_car_name)
print("Similar Car Names:", similar_car_names)
