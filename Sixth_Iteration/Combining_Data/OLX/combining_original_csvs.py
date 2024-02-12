import pandas as pd

# List of file names
file_names = ['corrected_data/olx_mumbai_corrected.csv', 'olx_bangalore.csv', 'olx_delhi.csv', 'corrected_data/olx_hyderabad_corrected.csv', 'olx_pune.csv']

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through each file and append its data to the combined_data DataFrame
for file_name in file_names:
    # Assuming the CSV files have a header. If not, you may need to adjust the header parameter.
    data = pd.read_csv(file_name)
    combined_data = combined_data._append(data, ignore_index=True)

# Save the combined data to a new CSV file
combined_data.drop(columns=["Unnamed: 0"], inplace=True)
combined_data.to_csv('all_olx_data_model.csv', index=False)

print("Files combined successfully. Output saved to 'all_olx_data_model.csv'")
