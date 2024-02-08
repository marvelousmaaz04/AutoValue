import pandas as pd

# List of file names
file_names = ['cars24_mumbai.csv', 'cars24_bangalore.csv', 'cars24_newdelhi.csv', 'cars24_hyderabad.csv', 'cars24_pune.csv']

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through each file and append its data to the combined_data DataFrame
for file_name in file_names:
    # Assuming the CSV files have a header. If not, you may need to adjust the header parameter.
    data = pd.read_csv(file_name)
    combined_data = combined_data._append(data, ignore_index=True)

# Save the combined data to a new CSV file
combined_data.to_csv('all_cars24_data.csv', index=False)

print("Files combined successfully. Output saved to 'all_cars24_data.csv'")
