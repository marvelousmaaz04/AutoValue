import pandas as pd

# List of file names
file_names = ['all_spinny_data_model.csv', 'all_olx_data_model.csv', 'all_cars24_data_model.csv']

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through each file and append its data to the combined_data DataFrame
for file_name in file_names:
   
    data = pd.read_csv(file_name)
    combined_data = combined_data._append(data, ignore_index=True)

# Save the combined data to a new CSV file
combined_data.to_csv('all_car_listings_data_for_model.csv', index=False)

print("Files combined successfully. Output saved to 'all_car_listings_data_for_model.csv'")
